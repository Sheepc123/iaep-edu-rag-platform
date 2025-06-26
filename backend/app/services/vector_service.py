"""
向量数据库服务
"""
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    import numpy as np
    VECTOR_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"向量数据库依赖未安装: {e}")
    VECTOR_DEPENDENCIES_AVAILABLE = False

from app.core.vector_config import get_vector_config, ensure_chroma_directory


class VectorService:
    """向量数据库服务"""
    
    def __init__(self):
        self.config = get_vector_config()
        self.client = None
        self.collection = None
        self.embedding_model = None
        self._initialized = False
        
        if VECTOR_DEPENDENCIES_AVAILABLE:
            self._initialize()
    
    def _initialize(self):
        """初始化向量数据库"""
        try:
            # 确保数据目录存在
            persist_dir = ensure_chroma_directory()
            
            # 初始化Chroma客户端
            self.client = chromadb.PersistentClient(
                path=persist_dir,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # 获取或创建集合
            try:
                self.collection = self.client.get_collection(
                    name=self.config.CHROMA_COLLECTION_NAME
                )
                logger.info(f"加载现有向量集合: {self.config.CHROMA_COLLECTION_NAME}")
            except Exception:
                self.collection = self.client.create_collection(
                    name=self.config.CHROMA_COLLECTION_NAME,
                    metadata={"description": "教师知识库文档向量"}
                )
                logger.info(f"创建新向量集合: {self.config.CHROMA_COLLECTION_NAME}")
            
            # 初始化嵌入模型
            self.embedding_model = SentenceTransformer(self.config.EMBEDDING_MODEL)
            logger.info(f"加载嵌入模型: {self.config.EMBEDDING_MODEL}")
            
            self._initialized = True
            logger.info("向量数据库初始化成功")
            
        except Exception as e:
            logger.error(f"向量数据库初始化失败: {e}")
            self._initialized = False
    
    def is_available(self) -> bool:
        """检查向量服务是否可用"""
        return VECTOR_DEPENDENCIES_AVAILABLE and self._initialized
    
    def add_document(self, doc_id: int, title: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """添加文档到向量数据库"""
        if not self.is_available():
            logger.warning("向量服务不可用，跳过文档向量化")
            return False
        
        try:
            # 分块处理长文本
            chunks = self._split_text(content)
            
            # 为每个块生成向量
            embeddings = []
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []
            
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                # 生成嵌入向量
                embedding = self.embedding_model.encode(chunk).tolist()
                embeddings.append(embedding)
                
                # 生成唯一ID
                chunk_id = f"doc_{doc_id}_chunk_{i}"
                chunk_ids.append(chunk_id)
                chunk_texts.append(chunk)
                
                # 元数据
                chunk_metadata = {
                    "doc_id": doc_id,
                    "title": title,
                    "chunk_index": i,
                    "chunk_count": len(chunks),
                    **(metadata or {})
                }
                chunk_metadatas.append(chunk_metadata)
            
            if not embeddings:
                logger.warning(f"文档 {doc_id} 没有有效内容，跳过向量化")
                return False
            
            # 添加到向量数据库
            self.collection.add(
                embeddings=embeddings,
                documents=chunk_texts,
                metadatas=chunk_metadatas,
                ids=chunk_ids
            )
            
            logger.info(f"文档 {doc_id} 向量化完成，生成 {len(embeddings)} 个向量块")
            return True
            
        except Exception as e:
            logger.error(f"文档向量化失败: {e}")
            return False
    
    def search_similar(self, query: str, top_k: int = None, filter_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """语义搜索"""
        if not self.is_available():
            logger.warning("向量服务不可用，返回空结果")
            return []
        
        try:
            top_k = top_k or self.config.VECTOR_SEARCH_TOP_K
            
            # 生成查询向量
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # 构建查询参数
            query_params = {
                "query_embeddings": [query_embedding],
                "n_results": top_k
            }
            
            # 添加元数据过滤
            if filter_metadata:
                query_params["where"] = filter_metadata
            
            # 执行搜索
            results = self.collection.query(**query_params)
            
            # 格式化结果
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    result = {
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i],
                        "similarity": 1 - results["distances"][0][i]  # 转换为相似度
                    }
                    
                    # 过滤低相似度结果
                    if result["similarity"] >= self.config.SIMILARITY_THRESHOLD:
                        formatted_results.append(result)
            
            logger.info(f"语义搜索完成，查询: '{query}'，返回 {len(formatted_results)} 个结果")
            return formatted_results
            
        except Exception as e:
            logger.error(f"语义搜索失败: {e}")
            return []
    
    def delete_document(self, doc_id: int) -> bool:
        """删除文档的所有向量"""
        if not self.is_available():
            return False
        
        try:
            # 查找该文档的所有向量块
            results = self.collection.get(
                where={"doc_id": doc_id}
            )
            
            if results["ids"]:
                # 删除所有相关向量
                self.collection.delete(ids=results["ids"])
                logger.info(f"删除文档 {doc_id} 的 {len(results['ids'])} 个向量块")
                return True
            else:
                logger.info(f"文档 {doc_id} 没有找到向量数据")
                return True
                
        except Exception as e:
            logger.error(f"删除文档向量失败: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """获取向量集合统计信息"""
        if not self.is_available():
            return {"available": False}
        
        try:
            count = self.collection.count()
            return {
                "available": True,
                "total_vectors": count,
                "collection_name": self.config.CHROMA_COLLECTION_NAME,
                "embedding_model": self.config.EMBEDDING_MODEL,
                "embedding_dimension": self.config.EMBEDDING_DIMENSION
            }
        except Exception as e:
            logger.error(f"获取向量统计失败: {e}")
            return {"available": False, "error": str(e)}
    
    def _split_text(self, text: str) -> List[str]:
        """分割文本为块"""
        if not text:
            return []
        
        chunk_size = self.config.CHUNK_SIZE
        chunk_overlap = self.config.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # 尝试在句号或换行符处分割
            if end < len(text):
                last_period = chunk.rfind('。')
                last_newline = chunk.rfind('\n')
                split_point = max(last_period, last_newline)
                
                if split_point > chunk_size * 0.5:  # 确保块不会太小
                    chunk = chunk[:split_point + 1]
                    end = start + split_point + 1
            
            chunks.append(chunk.strip())
            start = end - chunk_overlap
            
            if start >= len(text):
                break
        
        return [chunk for chunk in chunks if chunk.strip()]


# 全局向量服务实例
vector_service = VectorService()


def get_vector_service() -> VectorService:
    """获取向量服务实例"""
    return vector_service

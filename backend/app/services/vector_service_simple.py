"""
简化的向量数据库服务（不依赖sentence-transformers）
"""
import os
import uuid
import hashlib
from typing import List, Dict, Any, Optional
from loguru import logger

try:
    import chromadb
    from chromadb.config import Settings
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    import jieba
    VECTOR_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"向量数据库依赖未安装: {e}")
    VECTOR_DEPENDENCIES_AVAILABLE = False

from app.core.vector_config import get_vector_config, ensure_chroma_directory


class SimpleVectorService:
    """简化的向量数据库服务"""
    
    def __init__(self):
        self.config = get_vector_config()
        self.client = None
        self.collection = None
        self.tfidf_vectorizer = None
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
                    name=self.config.CHROMA_COLLECTION_NAME + "_simple"
                )
                logger.info(f"加载现有向量集合: {self.config.CHROMA_COLLECTION_NAME}_simple")
            except Exception:
                self.collection = self.client.create_collection(
                    name=self.config.CHROMA_COLLECTION_NAME + "_simple",
                    metadata={"description": "教师知识库文档向量(简化版)"}
                )
                logger.info(f"创建新向量集合: {self.config.CHROMA_COLLECTION_NAME}_simple")
            
            # 初始化TF-IDF向量化器
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=384,  # 限制特征数量
                stop_words=None,   # 不使用停用词（中文需要自定义）
                tokenizer=self._chinese_tokenizer,
                lowercase=True,
                ngram_range=(1, 2)  # 使用1-2gram
            )
            
            self._initialized = True
            logger.info("简化向量数据库初始化成功")
            
        except Exception as e:
            logger.error(f"向量数据库初始化失败: {e}")
            self._initialized = False
    
    def _chinese_tokenizer(self, text: str) -> List[str]:
        """中文分词器"""
        try:
            # 使用jieba进行中文分词
            tokens = list(jieba.cut(text))
            # 过滤掉长度小于2的词和纯数字
            return [token.strip() for token in tokens 
                   if len(token.strip()) >= 2 and not token.strip().isdigit()]
        except:
            # 如果jieba失败，使用简单的字符分割
            return [text[i:i+2] for i in range(len(text)-1)]
    
    def is_available(self) -> bool:
        """检查向量服务是否可用"""
        return VECTOR_DEPENDENCIES_AVAILABLE and self._initialized
    
    def _get_tfidf_embedding(self, text: str, all_texts: List[str] = None) -> List[float]:
        """获取TF-IDF向量表示"""
        try:
            # 如果提供了所有文本，重新训练TF-IDF
            if all_texts:
                self.tfidf_vectorizer.fit(all_texts)
                vector = self.tfidf_vectorizer.transform([text])
            else:
                # 检查TF-IDF是否已训练
                if not hasattr(self.tfidf_vectorizer, 'vocabulary_'):
                    # 如果未训练，使用哈希向量
                    return self._get_hash_embedding(text)
                vector = self.tfidf_vectorizer.transform([text])

            # 转换为密集向量
            dense_vector = vector.toarray()[0]

            # 如果向量全为0或维度不匹配，使用文本哈希
            if np.sum(dense_vector) == 0 or len(dense_vector) != 384:
                return self._get_hash_embedding(text)

            # 归一化
            norm = np.linalg.norm(dense_vector)
            if norm > 0:
                dense_vector = dense_vector / norm

            return dense_vector.tolist()

        except Exception as e:
            logger.warning(f"TF-IDF向量化失败，使用哈希向量: {e}")
            return self._get_hash_embedding(text)
    
    def _get_hash_embedding(self, text: str) -> List[float]:
        """基于哈希的简单向量表示"""
        # 使用文本哈希生成固定维度的向量
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()
        
        # 将哈希字节转换为384维向量
        vector = []
        for i in range(384):
            byte_index = i % len(hash_bytes)
            vector.append((hash_bytes[byte_index] - 128) / 128.0)  # 归一化到[-1,1]
        
        return vector
    
    def add_document(self, doc_id: int, title: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """添加文档到向量数据库"""
        if not self.is_available():
            logger.warning("向量服务不可用，跳过文档向量化")
            return False
        
        try:
            # 分块处理长文本
            chunks = self._split_text(content)

            # 收集所有文本用于TF-IDF训练
            all_texts = [title] + chunks

            # 检查是否需要训练TF-IDF
            need_training = not hasattr(self.tfidf_vectorizer, 'vocabulary_')

            # 为每个块生成向量
            embeddings = []
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []

            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue

                # 生成嵌入向量
                if need_training and i == 0:
                    # 第一次训练TF-IDF，使用所有文本
                    embedding = self._get_tfidf_embedding(chunk, all_texts)
                    need_training = False  # 标记已训练
                else:
                    embedding = self._get_tfidf_embedding(chunk)

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
            query_embedding = self._get_tfidf_embedding(query)
            
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
                    
                    # 过滤低相似度结果（哈希向量相似度更低）
                    if result["similarity"] >= 0.01:  # 进一步降低阈值
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
                "collection_name": self.config.CHROMA_COLLECTION_NAME + "_simple",
                "embedding_model": "TF-IDF + Jieba",
                "embedding_dimension": 384
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
simple_vector_service = SimpleVectorService()


def get_simple_vector_service() -> SimpleVectorService:
    """获取简化向量服务实例"""
    return simple_vector_service

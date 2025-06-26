"""
基于DeepSeek的混合向量数据库服务
"""
import os
import uuid
import hashlib
import requests
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
from app.core.config import settings


class DeepSeekVectorService:
    """基于DeepSeek的混合向量数据库服务"""
    
    def __init__(self):
        self.config = get_vector_config()
        self.client = None
        self.collection = None
        self.tfidf_vectorizer = None
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        self.deepseek_base_url = settings.DEEPSEEK_BASE_URL
        self.deepseek_model = settings.DEEPSEEK_MODEL
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
            collection_name = self.config.CHROMA_COLLECTION_NAME + "_deepseek"
            try:
                self.collection = self.client.get_collection(name=collection_name)
                logger.info(f"加载现有向量集合: {collection_name}")
            except Exception:
                self.collection = self.client.create_collection(
                    name=collection_name,
                    metadata={"description": "教师知识库文档向量(DeepSeek增强版)"}
                )
                logger.info(f"创建新向量集合: {collection_name}")
            
            # 初始化TF-IDF向量化器
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=384,
                stop_words=None,
                tokenizer=self._chinese_tokenizer,
                lowercase=True,
                ngram_range=(1, 2)
            )
            
            self._initialized = True
            logger.info("DeepSeek混合向量数据库初始化成功")
            
        except Exception as e:
            logger.error(f"向量数据库初始化失败: {e}")
            self._initialized = False
    
    def _chinese_tokenizer(self, text: str) -> List[str]:
        """中文分词器"""
        try:
            tokens = list(jieba.cut(text))
            return [token.strip() for token in tokens 
                   if len(token.strip()) >= 2 and not token.strip().isdigit()]
        except:
            return [text[i:i+2] for i in range(len(text)-1)]
    
    def is_available(self) -> bool:
        """检查向量服务是否可用"""
        return (VECTOR_DEPENDENCIES_AVAILABLE and 
                self._initialized and 
                self.deepseek_api_key)
    
    def _extract_keywords_with_deepseek(self, text: str) -> str:
        """使用DeepSeek提取关键词"""
        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""请分析以下文本，提取5-10个最重要的关键词，用逗号分隔。
只返回关键词，不要其他解释。

文本: "{text[:500]}"  """  # 限制文本长度以控制成本
            
            chat_data = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.deepseek_base_url}/chat/completions",
                headers=headers,
                json=chat_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                keywords = result["choices"][0]["message"]["content"].strip()
                logger.info(f"DeepSeek提取关键词: {keywords}")
                return keywords
            else:
                logger.warning(f"DeepSeek关键词提取失败: {response.status_code}")
                return text  # 回退到原文本
                
        except Exception as e:
            logger.warning(f"DeepSeek关键词提取异常: {e}")
            return text  # 回退到原文本
    
    def _get_enhanced_embedding(self, text: str, all_texts: List[str] = None) -> List[float]:
        """获取增强的向量表示（DeepSeek关键词 + TF-IDF）"""
        try:
            # 1. 使用DeepSeek提取关键词
            keywords = self._extract_keywords_with_deepseek(text)
            
            # 2. 结合原文本和关键词
            enhanced_text = f"{text} {keywords}"
            
            # 3. 使用TF-IDF向量化
            if all_texts:
                # 训练模式
                enhanced_all_texts = []
                for t in all_texts:
                    kw = self._extract_keywords_with_deepseek(t)
                    enhanced_all_texts.append(f"{t} {kw}")
                
                self.tfidf_vectorizer.fit(enhanced_all_texts)
                vector = self.tfidf_vectorizer.transform([enhanced_text])
            else:
                # 预测模式
                if not hasattr(self.tfidf_vectorizer, 'vocabulary_'):
                    return self._get_hash_embedding(enhanced_text)
                vector = self.tfidf_vectorizer.transform([enhanced_text])
            
            # 转换为密集向量
            dense_vector = vector.toarray()[0]

            # 确保向量维度为384
            if len(dense_vector) != 384:
                # 如果维度不匹配，使用哈希向量
                logger.warning(f"TF-IDF向量维度不匹配: {len(dense_vector)} != 384，使用哈希向量")
                return self._get_hash_embedding(enhanced_text)

            # 如果向量全为0，使用哈希向量
            if np.sum(dense_vector) == 0:
                logger.warning("TF-IDF向量全为0，使用哈希向量")
                return self._get_hash_embedding(enhanced_text)

            # 归一化
            norm = np.linalg.norm(dense_vector)
            if norm > 0:
                dense_vector = dense_vector / norm
                logger.info(f"TF-IDF向量归一化完成，原模长: {norm:.3f}")
            else:
                logger.warning("TF-IDF向量模长为0，使用哈希向量")
                return self._get_hash_embedding(enhanced_text)

            return dense_vector.tolist()
            
        except Exception as e:
            logger.warning(f"增强向量化失败，使用哈希向量: {e}")
            return self._get_hash_embedding(text)
    
    def _get_hash_embedding(self, text: str) -> List[float]:
        """基于哈希的简单向量表示"""
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()

        vector = []
        for i in range(384):
            byte_index = i % len(hash_bytes)
            vector.append((hash_bytes[byte_index] - 128) / 128.0)

        # 归一化向量
        vector = np.array(vector)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector.tolist()
    
    def add_document(self, doc_id: int, title: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """添加文档到向量数据库"""
        if not self.is_available():
            logger.warning("DeepSeek向量服务不可用，跳过文档向量化")
            return False
        
        try:
            # 分块处理长文本
            chunks = self._split_text(content)
            all_texts = [title] + chunks
            
            # 检查是否需要训练TF-IDF
            need_training = not hasattr(self.tfidf_vectorizer, 'vocabulary_')
            
            embeddings = []
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []
            
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                # 生成增强向量
                if need_training and i == 0:
                    embedding = self._get_enhanced_embedding(chunk, all_texts)
                    need_training = False
                else:
                    embedding = self._get_enhanced_embedding(chunk)
                
                embeddings.append(embedding)
                chunk_id = f"doc_{doc_id}_chunk_{i}"
                chunk_ids.append(chunk_id)
                chunk_texts.append(chunk)
                
                chunk_metadata = {
                    "doc_id": doc_id,
                    "title": title,
                    "chunk_index": i,
                    "chunk_count": len(chunks),
                    "enhanced_by": "deepseek",
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
            
            logger.info(f"文档 {doc_id} DeepSeek增强向量化完成，生成 {len(embeddings)} 个向量块")
            return True
            
        except Exception as e:
            logger.error(f"DeepSeek文档向量化失败: {e}")
            return False
    
    def search_similar(self, query: str, top_k: int = None, filter_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """语义搜索（优化版：减少API调用）"""
        if not self.is_available():
            logger.warning("DeepSeek向量服务不可用，返回空结果")
            return []

        try:
            top_k = top_k or self.config.VECTOR_SEARCH_TOP_K

            # 优化：对于短查询，直接使用TF-IDF，避免每次都调用DeepSeek
            if len(query) <= 10:
                # 短查询直接使用TF-IDF
                if hasattr(self.tfidf_vectorizer, 'vocabulary_'):
                    try:
                        vector = self.tfidf_vectorizer.transform([query])
                        dense_vector = vector.toarray()[0]
                        if len(dense_vector) == 384 and np.sum(dense_vector) > 0:
                            norm = np.linalg.norm(dense_vector)
                            if norm > 0:
                                dense_vector = dense_vector / norm
                            query_embedding = dense_vector.tolist()
                        else:
                            query_embedding = self._get_hash_embedding(query)
                    except:
                        query_embedding = self._get_hash_embedding(query)
                else:
                    query_embedding = self._get_hash_embedding(query)
            else:
                # 长查询使用DeepSeek增强
                query_embedding = self._get_enhanced_embedding(query)
            
            query_params = {
                "query_embeddings": [query_embedding],
                "n_results": top_k
            }
            
            if filter_metadata:
                query_params["where"] = filter_metadata
            
            results = self.collection.query(**query_params)
            
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    distance = results["distances"][0][i]
                    # 对于归一化向量，余弦距离范围是0-2，转换为相似度0-1
                    similarity = max(0, 1 - distance / 2)

                    result = {
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": distance,
                        "similarity": similarity
                    }
                    
                    # 进一步降低阈值，提高召回率
                    if result["similarity"] >= 0.001:
                        formatted_results.append(result)
            
            logger.info(f"DeepSeek语义搜索完成，查询: '{query}'，返回 {len(formatted_results)} 个结果")
            return formatted_results
            
        except Exception as e:
            logger.error(f"DeepSeek语义搜索失败: {e}")
            return []
    
    def delete_document(self, doc_id: int) -> bool:
        """删除文档的所有向量"""
        if not self.is_available():
            return False
        
        try:
            results = self.collection.get(where={"doc_id": doc_id})
            
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"删除文档 {doc_id} 的 {len(results['ids'])} 个DeepSeek向量块")
                return True
            else:
                logger.info(f"文档 {doc_id} 没有找到DeepSeek向量数据")
                return True
                
        except Exception as e:
            logger.error(f"删除DeepSeek文档向量失败: {e}")
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
                "collection_name": self.config.CHROMA_COLLECTION_NAME + "_deepseek",
                "embedding_model": "DeepSeek + TF-IDF + Jieba",
                "embedding_dimension": 384,
                "enhancement": "DeepSeek关键词提取"
            }
        except Exception as e:
            logger.error(f"获取DeepSeek向量统计失败: {e}")
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
            
            if end < len(text):
                last_period = chunk.rfind('。')
                last_newline = chunk.rfind('\n')
                split_point = max(last_period, last_newline)
                
                if split_point > chunk_size * 0.5:
                    chunk = chunk[:split_point + 1]
                    end = start + split_point + 1
            
            chunks.append(chunk.strip())
            start = end - chunk_overlap
            
            if start >= len(text):
                break
        
        return [chunk for chunk in chunks if chunk.strip()]


# 全局向量服务实例
deepseek_vector_service = DeepSeekVectorService()


def get_deepseek_vector_service() -> DeepSeekVectorService:
    """获取DeepSeek向量服务实例"""
    return deepseek_vector_service

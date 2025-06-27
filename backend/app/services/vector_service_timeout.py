"""
带超时控制的向量服务包装器
"""
import time
import threading
from typing import Dict, Any, Optional
from loguru import logger

from app.services.vector_service_deepseek import DeepSeekVectorService


class TimeoutVectorService:
    """带超时控制的向量服务"""
    
    def __init__(self):
        self.vector_service = DeepSeekVectorService()
        self._stop_flag = threading.Event()
    
    def is_available(self) -> bool:
        """检查服务是否可用"""
        return self.vector_service.is_available()
    
    def add_document_with_timeout(
        self, 
        doc_id: int, 
        title: str, 
        content: str, 
        metadata: Dict[str, Any] = None, 
        timeout: int = 180
    ) -> bool:
        """
        带超时控制的文档添加
        
        Args:
            doc_id: 文档ID
            title: 文档标题
            content: 文档内容
            metadata: 元数据
            timeout: 超时时间（秒），默认3分钟
        
        Returns:
            bool: 是否成功
        """
        if not self.is_available():
            logger.warning("向量服务不可用，跳过文档向量化")
            return False
        
        logger.info(f"开始向量化文档 {doc_id}，超时设置: {timeout}秒")
        start_time = time.time()
        
        # 重置停止标志
        self._stop_flag.clear()
        
        # 创建结果容器
        result_container = {"success": False, "error": None}
        
        def vectorize_worker():
            """向量化工作线程"""
            try:
                # 分块处理长文本
                chunks = self.vector_service._split_text(content)
                all_texts = [title] + chunks
                
                # 检查是否需要训练TF-IDF
                need_training = not hasattr(self.vector_service.tfidf_vectorizer, 'vocabulary_')
                
                embeddings = []
                chunk_ids = []
                chunk_texts = []
                chunk_metadatas = []
                
                for i, chunk in enumerate(chunks):
                    # 检查停止标志
                    if self._stop_flag.is_set():
                        logger.warning(f"文档 {doc_id} 向量化被中断，已处理 {i}/{len(chunks)} 个块")
                        break
                    
                    if not chunk.strip():
                        continue
                    
                    # 生成增强向量
                    try:
                        if need_training and i == 0:
                            embedding = self.vector_service._get_enhanced_embedding(chunk, all_texts)
                            need_training = False
                        else:
                            embedding = self.vector_service._get_enhanced_embedding(chunk)
                        
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
                        
                        # 每处理3个块输出一次进度
                        if (i + 1) % 3 == 0:
                            elapsed = time.time() - start_time
                            logger.info(f"文档 {doc_id} 向量化进度: {i+1}/{len(chunks)} 个块，耗时: {elapsed:.1f}秒")
                    
                    except Exception as e:
                        logger.warning(f"文档 {doc_id} 第 {i} 个块向量化失败: {e}")
                        continue
                
                if not embeddings:
                    logger.warning(f"文档 {doc_id} 没有有效内容，跳过向量化")
                    result_container["success"] = False
                    return
                
                # 检查是否被中断
                if self._stop_flag.is_set():
                    logger.warning(f"文档 {doc_id} 向量化被中断，未保存到数据库")
                    result_container["success"] = False
                    return
                
                # 添加到向量数据库
                self.vector_service.collection.add(
                    embeddings=embeddings,
                    documents=chunk_texts,
                    metadatas=chunk_metadatas,
                    ids=chunk_ids
                )
                
                logger.info(f"文档 {doc_id} 向量化完成，生成 {len(embeddings)} 个向量块")
                result_container["success"] = True
                
            except Exception as e:
                logger.error(f"文档 {doc_id} 向量化异常: {e}")
                result_container["error"] = str(e)
                result_container["success"] = False
        
        # 启动向量化线程
        worker_thread = threading.Thread(target=vectorize_worker)
        worker_thread.daemon = True
        worker_thread.start()
        
        # 等待完成或超时
        worker_thread.join(timeout=timeout)
        
        elapsed_time = time.time() - start_time
        
        if worker_thread.is_alive():
            # 超时了，设置停止标志
            self._stop_flag.set()
            logger.warning(f"文档 {doc_id} 向量化超时 ({timeout}秒)，强制停止")
            
            # 再等待一小段时间让线程清理
            worker_thread.join(timeout=5)
            
            return False
        
        # 检查结果
        if result_container["success"]:
            logger.info(f"文档 {doc_id} 向量化成功，总耗时: {elapsed_time:.2f}秒")
            return True
        else:
            error_msg = result_container.get("error", "未知错误")
            logger.error(f"文档 {doc_id} 向量化失败，总耗时: {elapsed_time:.2f}秒，错误: {error_msg}")
            return False
    
    def search_similar(self, query: str, top_k: int = None, filter_metadata: Dict[str, Any] = None):
        """语义搜索（直接调用原服务）"""
        return self.vector_service.search_similar(query, top_k, filter_metadata)
    
    def delete_document(self, doc_id: int) -> bool:
        """删除文档（直接调用原服务）"""
        return self.vector_service.delete_document(doc_id)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """获取统计信息（直接调用原服务）"""
        return self.vector_service.get_collection_stats()


# 全局超时向量服务实例
timeout_vector_service = TimeoutVectorService()


def get_timeout_vector_service() -> TimeoutVectorService:
    """获取带超时控制的向量服务实例"""
    return timeout_vector_service

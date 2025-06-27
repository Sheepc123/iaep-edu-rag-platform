"""
向量数据库配置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class VectorConfig(BaseSettings):
    """向量数据库配置"""
    
    # Chroma数据库配置
    CHROMA_PERSIST_DIRECTORY: str = "data/vector_db"
    CHROMA_COLLECTION_NAME: str = "teacher_knowledge_docs_v2"
    
    # 嵌入模型配置
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    EMBEDDING_DIMENSION: int = 384  # MiniLM-L12-v2的维度
    
    # 文本分块配置
    CHUNK_SIZE: int = 500  # 每个文本块的字符数
    CHUNK_OVERLAP: int = 50  # 文本块之间的重叠字符数
    
    # 搜索配置
    VECTOR_SEARCH_TOP_K: int = 10  # 向量搜索返回的最大结果数
    SIMILARITY_THRESHOLD: float = 0.7  # 相似度阈值
    
    # OpenAI配置（可选，用于更高质量的嵌入）
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的环境变量


# 全局配置实例
vector_config = VectorConfig()


def get_vector_config() -> VectorConfig:
    """获取向量数据库配置"""
    return vector_config


def ensure_chroma_directory():
    """确保Chroma数据库目录存在"""
    # 使用绝对路径，基于当前文件位置
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    persist_dir = os.path.join(current_dir, "data", "vector_db")
    os.makedirs(persist_dir, exist_ok=True)
    return persist_dir

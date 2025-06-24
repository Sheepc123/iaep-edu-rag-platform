"""
核心配置文件
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基本信息
    APP_NAME: str = "智能教育平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./education_platform.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS配置
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"]
    
    # AI配置 (预留)
    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-3.5-turbo"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


# 数据库配置
class DatabaseConfig:
    """数据库配置类"""
    
    @staticmethod
    def get_database_url() -> str:
        """获取数据库连接URL"""
        return settings.DATABASE_URL
    
    @staticmethod
    def get_engine_args() -> dict:
        """获取数据库引擎参数"""
        return {
            "connect_args": {"check_same_thread": False},
            "echo": settings.DEBUG
        }


# JWT配置
class JWTConfig:
    """JWT配置类"""
    
    @staticmethod
    def get_secret_key() -> str:
        return settings.SECRET_KEY
    
    @staticmethod
    def get_algorithm() -> str:
        return settings.ALGORITHM
    
    @staticmethod
    def get_access_token_expire_minutes() -> int:
        return settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    @staticmethod
    def get_refresh_token_expire_days() -> int:
        return settings.REFRESH_TOKEN_EXPIRE_DAYS


# 文件配置
class FileConfig:
    """文件配置类"""
    
    @staticmethod
    def get_upload_dir() -> str:
        upload_dir = settings.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)
        return upload_dir
    
    @staticmethod
    def get_max_file_size() -> int:
        return settings.MAX_FILE_SIZE
    
    @staticmethod
    def get_allowed_file_types() -> list:
        return settings.ALLOWED_FILE_TYPES

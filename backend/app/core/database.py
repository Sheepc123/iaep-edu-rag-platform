"""
数据库连接和会话管理 - 兼容性模块
此文件保持向后兼容，实际功能已迁移到 database 模块
"""

# 从新的数据库模块导入所有功能
import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, backend_dir)

# 直接使用SQLAlchemy，不依赖database模块
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 数据库配置
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """初始化数据库"""
    # 确保数据库目录存在
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "").replace("./", "")
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    # 创建所有表
    Base.metadata.create_all(bind=engine)

def check_database_health():
    """检查数据库健康状态"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """删除数据库表"""
    Base.metadata.drop_all(bind=engine)

class DatabaseManager:
    """数据库管理器"""

    @staticmethod
    def get_session():
        """获取数据库会话"""
        return SessionLocal()

    @staticmethod
    def close_session(db):
        """关闭数据库会话"""
        db.close()

    @staticmethod
    def commit_session(db):
        """提交会话"""
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def rollback_session(db):
        """回滚会话"""
        db.rollback()

# 保持向后兼容性
__all__ = [
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "create_tables",
    "drop_tables",
    "init_database",
    "DatabaseManager",
    "check_database_health"
]

"""
数据库连接和会话管理
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import DatabaseConfig


# 创建数据库引擎
engine = create_engine(
    DatabaseConfig.get_database_url(),
    **DatabaseConfig.get_engine_args()
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    用于依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """创建所有数据表"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """删除所有数据表"""
    Base.metadata.drop_all(bind=engine)


def init_database():
    """初始化数据库"""
    # 确保数据库目录存在
    db_path = DatabaseConfig.get_database_url().replace("sqlite:///", "")
    
    # 如果是相对路径，将数据库文件放在database文件夹中
    if not os.path.isabs(db_path):
        db_dir = os.path.join(os.path.dirname(__file__), "data")
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, os.path.basename(db_path))
        
        # 更新数据库URL
        DatabaseConfig._database_url = f"sqlite:///{db_path}"
        
        # 重新创建引擎
        global engine, SessionLocal
        engine = create_engine(
            DatabaseConfig.get_database_url(),
            **DatabaseConfig.get_engine_args()
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建数据表
    create_tables()
    print(f"数据库初始化完成: {db_path}")


class DatabaseManager:
    """数据库管理器"""
    
    @staticmethod
    def get_session() -> Session:
        """获取数据库会话"""
        return SessionLocal()
    
    @staticmethod
    def close_session(db: Session):
        """关闭数据库会话"""
        db.close()
    
    @staticmethod
    def commit_session(db: Session):
        """提交会话"""
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def rollback_session(db: Session):
        """回滚会话"""
        db.rollback()


# 数据库健康检查
def check_database_health() -> bool:
    """检查数据库连接健康状态"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

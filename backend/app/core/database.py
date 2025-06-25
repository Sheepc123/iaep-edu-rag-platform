"""
数据库连接和会话管理 - 兼容性模块
此文件保持向后兼容，实际功能已迁移到 database 模块
"""

# 从新的数据库模块导入所有功能
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.connection import (
    engine,
    SessionLocal,
    Base,
    get_db,
    create_tables,
    drop_tables,
    init_database,
    DatabaseManager,
    check_database_health
)

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

"""
数据库迁移管理
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .connection import engine, SessionLocal, Base
from app.models import *  # 导入所有模型


class MigrationManager:
    """数据库迁移管理器"""
    
    def __init__(self):
        self.migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
        if not os.path.exists(self.migrations_dir):
            os.makedirs(self.migrations_dir, exist_ok=True)
    
    def create_migration(self, name: str, description: str = "") -> str:
        """创建新的迁移文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.sql"
        filepath = os.path.join(self.migrations_dir, filename)
        
        migration_content = f"""-- Migration: {name}
-- Description: {description}
-- Created: {datetime.now().isoformat()}

-- Add your SQL statements here
-- Example:
-- CREATE TABLE example (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name VARCHAR(100) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(migration_content)
        
        print(f"迁移文件已创建: {filepath}")
        return filepath
    
    def get_applied_migrations(self) -> List[str]:
        """获取已应用的迁移列表"""
        try:
            from sqlalchemy import text
            db = SessionLocal()
            result = db.execute(text("SELECT name FROM migrations ORDER BY applied_at"))
            migrations = [row[0] for row in result.fetchall()]
            db.close()
            return migrations
        except:
            # 如果migrations表不存在，返回空列表
            return []
    
    def create_migrations_table(self):
        """创建迁移记录表"""
        from sqlalchemy import text
        db = SessionLocal()
        try:
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            db.commit()
        finally:
            db.close()
    
    def apply_migration(self, filepath: str) -> bool:
        """应用单个迁移文件"""
        filename = os.path.basename(filepath)
        
        # 检查是否已应用
        applied_migrations = self.get_applied_migrations()
        if filename in applied_migrations:
            print(f"迁移 {filename} 已经应用过了")
            return True
        
        try:
            # 读取迁移文件
            with open(filepath, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 执行迁移
            db = SessionLocal()
            try:
                # 清理SQL内容，移除注释
                lines = sql_content.split('\n')
                clean_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('--'):
                        clean_lines.append(line)

                clean_sql = ' '.join(clean_lines)

                # 分割SQL语句并执行
                statements = [stmt.strip() for stmt in clean_sql.split(';') if stmt.strip()]

                from sqlalchemy import text
                for statement in statements:
                    if statement:
                        print(f"执行SQL: {statement[:100]}...")
                        db.execute(text(statement))
                
                # 记录迁移
                from sqlalchemy import text
                db.execute(
                    text("INSERT INTO migrations (name) VALUES (:name)"),
                    {"name": filename}
                )
                db.commit()
                print(f"迁移 {filename} 应用成功")
                return True
                
            except Exception as e:
                db.rollback()
                print(f"迁移 {filename} 应用失败: {e}")
                return False
            finally:
                db.close()
                
        except Exception as e:
            print(f"读取迁移文件失败: {e}")
            return False
    
    def apply_all_migrations(self) -> bool:
        """应用所有未应用的迁移"""
        # 确保migrations表存在
        self.create_migrations_table()
        
        # 获取所有迁移文件
        migration_files = []
        if os.path.exists(self.migrations_dir):
            for filename in os.listdir(self.migrations_dir):
                if filename.endswith('.sql'):
                    migration_files.append(filename)
        
        migration_files.sort()  # 按时间戳排序
        
        # 获取已应用的迁移
        applied_migrations = self.get_applied_migrations()
        
        # 应用未应用的迁移
        success = True
        for filename in migration_files:
            if filename not in applied_migrations:
                filepath = os.path.join(self.migrations_dir, filename)
                if not self.apply_migration(filepath):
                    success = False
                    break
        
        return success
    
    def rollback_migration(self, migration_name: str) -> bool:
        """回滚指定迁移（需要手动实现回滚逻辑）"""
        print(f"回滚迁移 {migration_name} 需要手动实现")
        return False
    
    def get_migration_status(self) -> Dict[str, Any]:
        """获取迁移状态"""
        # 获取所有迁移文件
        all_migrations = []
        if os.path.exists(self.migrations_dir):
            for filename in os.listdir(self.migrations_dir):
                if filename.endswith('.sql'):
                    all_migrations.append(filename)
        
        all_migrations.sort()
        
        # 获取已应用的迁移
        applied_migrations = self.get_applied_migrations()
        
        # 构建状态信息
        status = {
            "total_migrations": len(all_migrations),
            "applied_migrations": len(applied_migrations),
            "pending_migrations": len(all_migrations) - len(applied_migrations),
            "migrations": []
        }
        
        for migration in all_migrations:
            status["migrations"].append({
                "name": migration,
                "applied": migration in applied_migrations
            })
        
        return status


def init_database_with_migrations():
    """使用迁移系统初始化数据库"""
    from .connection import init_database
    
    # 基础初始化
    init_database()
    
    # 应用迁移
    migration_manager = MigrationManager()
    migration_manager.apply_all_migrations()
    
    print("数据库迁移完成")


# 便捷函数
def create_migration(name: str, description: str = "") -> str:
    """创建迁移文件的便捷函数"""
    manager = MigrationManager()
    return manager.create_migration(name, description)


def apply_migrations() -> bool:
    """应用所有迁移的便捷函数"""
    manager = MigrationManager()
    return manager.apply_all_migrations()


def migration_status() -> Dict[str, Any]:
    """获取迁移状态的便捷函数"""
    manager = MigrationManager()
    return manager.get_migration_status()

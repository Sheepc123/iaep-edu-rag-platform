#!/usr/bin/env python3
"""
修复user_sessions表结构
"""

import os
import sys
import sqlite3
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_user_sessions_table():
    """修复user_sessions表结构"""
    print("🔧 修复user_sessions表结构...")
    
    db_path = Path("data/database/education_platform.db")
    if not db_path.exists():
        print("❌ 数据库文件不存在")
        return False
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 检查当前表结构
        cursor.execute("PRAGMA table_info(user_sessions)")
        columns = cursor.fetchall()
        
        print("当前表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 检查是否缺少字段
        column_names = [col[1] for col in columns]
        missing_fields = []
        
        required_fields = [
            ('session_token', 'VARCHAR(255)'),
            ('last_used', 'DATETIME'),
            ('last_accessed_at', 'DATETIME')
        ]
        
        for field_name, field_type in required_fields:
            if field_name not in column_names:
                missing_fields.append((field_name, field_type))
        
        if missing_fields:
            print(f"\n缺少字段: {[f[0] for f in missing_fields]}")
            
            # 备份现有数据
            cursor.execute("SELECT * FROM user_sessions")
            existing_data = cursor.fetchall()
            print(f"备份现有数据: {len(existing_data)} 条记录")
            
            # 删除旧表
            cursor.execute("DROP TABLE user_sessions")
            print("✅ 删除旧表")
            
            # 创建新表
            cursor.execute("""
                CREATE TABLE user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token VARCHAR(255) UNIQUE NOT NULL,
                    refresh_token VARCHAR(255) UNIQUE NOT NULL,
                    device_info VARCHAR(255),
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    expires_at DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)
            print("✅ 创建新表")
            
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at)")
            print("✅ 创建索引")
            
            conn.commit()
            print("✅ 表结构修复完成")
            
        else:
            print("✅ 表结构正确，无需修复")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 修复失败: {e}")
        return False
    finally:
        conn.close()


def fix_user_activities_table():
    """修复user_activities表结构"""
    print("\n🔧 修复user_activities表结构...")
    
    db_path = Path("data/database/education_platform.db")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_activities'")
        if not cursor.fetchone():
            # 创建user_activities表
            cursor.execute("""
                CREATE TABLE user_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_type VARCHAR(50) NOT NULL,
                    activity_data TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)
            
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_activities_type ON user_activities(activity_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_activities_created_at ON user_activities(created_at)")
            
            conn.commit()
            print("✅ user_activities表创建完成")
        else:
            print("✅ user_activities表已存在")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 修复失败: {e}")
        return False
    finally:
        conn.close()


def verify_tables():
    """验证表结构"""
    print("\n🔍 验证表结构...")
    
    db_path = Path("data/database/education_platform.db")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 检查user_sessions表
        cursor.execute("PRAGMA table_info(user_sessions)")
        columns = cursor.fetchall()
        
        print("user_sessions表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 检查user_activities表
        cursor.execute("PRAGMA table_info(user_activities)")
        columns = cursor.fetchall()
        
        print("\nuser_activities表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    finally:
        conn.close()


def main():
    """主函数"""
    print("🚀 修复数据库表结构")
    print("=" * 50)
    
    # 1. 修复user_sessions表
    sessions_ok = fix_user_sessions_table()
    
    # 2. 修复user_activities表
    activities_ok = fix_user_activities_table()
    
    # 3. 验证表结构
    verify_ok = verify_tables()
    
    print("\n" + "=" * 50)
    print("📋 修复结果:")
    print(f"   user_sessions: {'✅' if sessions_ok else '❌'}")
    print(f"   user_activities: {'✅' if activities_ok else '❌'}")
    print(f"   验证: {'✅' if verify_ok else '❌'}")
    
    if all([sessions_ok, activities_ok, verify_ok]):
        print("\n🎉 表结构修复完成！")
        print("现在可以重新测试登录功能")
    else:
        print("\n❌ 修复过程中出现问题")


if __name__ == "__main__":
    main()

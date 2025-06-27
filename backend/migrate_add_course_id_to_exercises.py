#!/usr/bin/env python3
"""
数据库迁移脚本：为exercises表添加course_id字段
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """执行数据库迁移"""
    
    # 数据库文件路径
    db_path = Path(__file__).parent / "database" / "data" / "education_platform.db"
    
    if not db_path.exists():
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 检查course_id字段是否已存在
        cursor.execute("PRAGMA table_info(exercises)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'course_id' in columns:
            print("course_id字段已存在，无需迁移")
            return True
        
        print("开始迁移：为exercises表添加course_id字段...")
        
        # 添加course_id字段
        cursor.execute("""
            ALTER TABLE exercises 
            ADD COLUMN course_id INTEGER REFERENCES courses(id)
        """)
        
        # 提交更改
        conn.commit()
        
        print("迁移完成：成功为exercises表添加course_id字段")
        
        # 验证迁移结果
        cursor.execute("PRAGMA table_info(exercises)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'course_id' in columns:
            print("验证成功：course_id字段已添加")
            return True
        else:
            print("验证失败：course_id字段未找到")
            return False
            
    except sqlite3.Error as e:
        print(f"数据库迁移失败: {e}")
        return False
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = migrate_database()
    if success:
        print("数据库迁移成功完成")
        exit(0)
    else:
        print("数据库迁移失败")
        exit(1)

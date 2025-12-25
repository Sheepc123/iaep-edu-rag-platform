#!/usr/bin/env python3
"""
检查数据库表结构
"""
import sqlite3
import os

def check_users_table():
    """检查users表结构"""
    db_path = 'data/database/education_platform.db'
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查看users表结构
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 users表结构:")
        print("-" * 50)
        for col in columns:
            null_str = "NOT NULL" if col[3] else "NULL"
            default_str = f"Default: {col[4]}" if col[4] else "No Default"
            print(f"  {col[1]} ({col[2]}) - {null_str} - {default_str}")
        
        # 查看现有用户
        cursor.execute("SELECT id, username, email, full_name, role FROM users LIMIT 5")
        users = cursor.fetchall()
        
        print(f"\n👥 现有用户 (前5个):")
        print("-" * 50)
        for user in users:
            print(f"  ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 姓名: {user[3]}, 角色: {user[4]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")

if __name__ == "__main__":
    check_users_table()

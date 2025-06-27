#!/usr/bin/env python3
"""
修复数据库路径问题
"""

import os
import sqlite3
from pathlib import Path


def main():
    """主函数"""
    print("🔧 修复数据库路径问题...")
    
    # 确保目录存在
    db_dir = Path("data/database")
    db_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 确保目录存在: {db_dir}")
    
    # 数据库文件路径
    db_path = db_dir / "education_platform.db"
    
    # 检查数据库文件是否存在
    if not db_path.exists():
        print("❌ 数据库文件不存在，创建空数据库...")
        
        # 创建空数据库文件
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE IF NOT EXISTS _init (id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()
        print(f"✅ 创建空数据库: {db_path}")
    else:
        print(f"✅ 数据库文件已存在: {db_path}")
    
    # 测试数据库连接
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"📊 数据库表数量: {len(tables)}")
        if tables:
            print("   表列表:")
            for table in tables:
                print(f"     - {table[0]}")
        
        print("✅ 数据库连接测试成功")
        
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
    
    # 显示完整路径信息
    print(f"\n📋 路径信息:")
    print(f"   当前工作目录: {os.getcwd()}")
    print(f"   数据库文件: {db_path.absolute()}")
    print(f"   文件存在: {db_path.exists()}")
    if db_path.exists():
        print(f"   文件大小: {db_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()

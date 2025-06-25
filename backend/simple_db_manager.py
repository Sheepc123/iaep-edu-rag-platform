#!/usr/bin/env python3
"""
简化的数据库管理器
不依赖FastAPI等复杂依赖，直接使用SQLite和SQLAlchemy
"""
import sqlite3
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 数据库配置
DATABASE_URL = "sqlite:///./database/data/education_platform.db"

def get_engine():
    """获取数据库引擎"""
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

def get_session():
    """获取数据库会话"""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def check_database_health():
    """检查数据库健康状态"""
    try:
        session = get_session()
        session.execute(text("SELECT 1"))
        session.close()
        return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

def list_tables():
    """列出所有表"""
    try:
        session = get_session()
        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        session.close()
        return tables
    except Exception as e:
        print(f"获取表列表失败: {e}")
        return []

def get_table_info(table_name):
    """获取表信息"""
    try:
        session = get_session()
        
        # 获取表结构
        result = session.execute(text(f"PRAGMA table_info({table_name})"))
        columns = result.fetchall()
        
        # 获取记录数
        result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.fetchone()[0]
        
        session.close()
        
        return {
            'columns': columns,
            'count': count
        }
    except Exception as e:
        print(f"获取表 {table_name} 信息失败: {e}")
        return None

def create_test_user():
    """创建测试用户"""
    try:
        session = get_session()
        
        # 检查是否已有测试用户
        result = session.execute(text("SELECT COUNT(*) FROM users WHERE username = 'test_student'"))
        if result.fetchone()[0] > 0:
            print("测试用户已存在")
            session.close()
            return
        
        # 创建测试用户
        session.execute(text("""
            INSERT INTO users (username, email, password_hash, role, is_active, created_at)
            VALUES ('test_student', 'test@example.com', 'hashed_password', 'student', 1, datetime('now'))
        """))
        
        session.commit()
        session.close()
        print("✅ 测试用户创建成功")
        
    except Exception as e:
        print(f"❌ 创建测试用户失败: {e}")

def show_database_status():
    """显示数据库状态"""
    print("=" * 50)
    print("📊 数据库状态报告")
    print("=" * 50)
    
    # 检查连接
    if check_database_health():
        print("✅ 数据库连接正常")
    else:
        print("❌ 数据库连接失败")
        return
    
    # 列出所有表
    tables = list_tables()
    print(f"\n📋 数据表总数: {len(tables)}")
    
    # 显示每个表的信息
    for table in tables:
        info = get_table_info(table)
        if info:
            print(f"\n📄 表: {table}")
            print(f"   记录数: {info['count']}")
            print(f"   字段数: {len(info['columns'])}")
            
            # 显示前几个字段
            if info['columns']:
                print("   主要字段:")
                for col in info['columns'][:3]:  # 只显示前3个字段
                    print(f"     - {col[1]} ({col[2]})")
                if len(info['columns']) > 3:
                    print(f"     ... 还有 {len(info['columns']) - 3} 个字段")

def main():
    """主菜单"""
    while True:
        print("\n" + "=" * 50)
        print("🗄️  简化数据库管理器")
        print("=" * 50)
        print("1. 显示数据库状态")
        print("2. 创建测试用户")
        print("3. 检查数据库连接")
        print("4. 退出")
        print("=" * 50)
        
        choice = input("请选择操作 (1-4): ").strip()
        
        if choice == "1":
            show_database_status()
        elif choice == "2":
            create_test_user()
        elif choice == "3":
            if check_database_health():
                print("✅ 数据库连接正常")
            else:
                print("❌ 数据库连接失败")
        elif choice == "4":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()

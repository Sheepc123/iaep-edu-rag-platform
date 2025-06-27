#!/usr/bin/env python3
"""
强制重新加载配置并测试数据库连接
"""

import os
import sys
from pathlib import Path

# 清除Python模块缓存
if 'app.core.config' in sys.modules:
    del sys.modules['app.core.config']
if 'app.core.database' in sys.modules:
    del sys.modules['app.core.database']

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔄 强制重新加载配置...")
    
    # 1. 检查环境变量
    print("\n📋 环境变量检查:")
    env_vars = ['DATABASE_URL', 'DEBUG', 'SECRET_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if var == 'SECRET_KEY':
                print(f"   {var}: {value[:20]}...")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: 未设置")
    
    # 2. 手动加载 .env 文件
    print("\n📄 手动加载 .env 文件:")
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                    if key == 'DATABASE_URL':
                        print(f"   第{line_num}行: {key}={value}")
    
    # 3. 重新测试配置
    print("\n🔍 重新测试配置:")
    try:
        from app.core.config import settings
        print(f"   配置中的数据库URL: {settings.DATABASE_URL}")
        print(f"   环境变量中的数据库URL: {os.getenv('DATABASE_URL')}")
    except Exception as e:
        print(f"   ❌ 配置加载失败: {e}")
    
    # 4. 测试数据库连接
    print("\n🔍 测试数据库连接:")
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./data/database/education_platform.db')
    
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"   ✅ 数据库连接成功: {result.fetchone()}")
            
            # 检查表
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = result.fetchall()
            print(f"   📊 数据库表数量: {len(tables)}")
            
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
    
    # 5. 测试应用数据库模块
    print("\n🔍 测试应用数据库模块:")
    try:
        from app.core.database import check_database_health
        health = check_database_health()
        print(f"   数据库健康检查: {'✅ 成功' if health else '❌ 失败'}")
    except Exception as e:
        print(f"   ❌ 应用数据库模块测试失败: {e}")


if __name__ == "__main__":
    main()

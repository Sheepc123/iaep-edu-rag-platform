#!/usr/bin/env python3
"""
测试配置加载
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔍 测试配置加载...")
    
    try:
        from app.core.config import settings
        print(f"✅ 配置加载成功")
        print(f"数据库URL: {settings.DATABASE_URL}")
        
        # 检查环境变量
        env_db_url = os.getenv('DATABASE_URL')
        if env_db_url:
            print(f"环境变量DATABASE_URL: {env_db_url}")
        else:
            print("环境变量DATABASE_URL: 未设置")
            
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")

if __name__ == "__main__":
    main()

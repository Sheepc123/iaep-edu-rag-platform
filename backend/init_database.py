#!/usr/bin/env python3
"""
数据库初始化脚本
用于快速设置开发环境
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.connection import init_database
from database.migrations import apply_migrations
from database.seeds import seed_database


def main():
    """主函数"""
    print("🚀 开始初始化教育平台数据库")
    print("=" * 50)
    
    try:
        # 1. 初始化数据库结构
        print("📊 1. 初始化数据库结构...")
        init_database()
        
        # 2. 应用迁移
        print("\n🔄 2. 应用数据库迁移...")
        if apply_migrations():
            print("✅ 迁移应用成功")
        else:
            print("⚠️  没有待应用的迁移")
        
        # 3. 填充种子数据
        print("\n🌱 3. 填充种子数据...")
        seed_database()
        
        print("\n" + "=" * 50)
        print("🎉 数据库初始化完成！")
        print("\n📋 创建的测试账号:")
        print("   管理员: admin / admin123456")
        print("   教师: teacher123 / 123456") 
        print("   学生: student123 / 123456")
        print("\n🚀 现在可以启动应用了:")
        print("   python run.py")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
创建测试数据的脚本
用法:
    python create_test_data.py students    # 只创建学生数据
    python create_test_data.py complete    # 创建完整测试数据
    python create_test_data.py users       # 创建基础用户
    python create_test_data.py             # 创建默认数据
"""

import sys
import os

# 添加项目根目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

# 确保工作目录是backend目录
os.chdir(backend_dir)

# 初始化数据库
from database.connection import init_database
from database.seeds import (
    create_test_students,
    create_complete_test_data,
    create_test_users,
    seed_database,
    SeedManager
)


def create_rich_courses():
    """创建丰富的课程数据的便捷函数"""
    with SeedManager() as seed_manager:
        # 确保有教师用户
        teacher = seed_manager.create_test_teacher()
        # 创建多个课程
        courses = seed_manager.create_multiple_courses(teacher)
        # 为每个课程创建课时
        for course in courses:
            seed_manager.create_simple_lessons_for_course(course)
        return courses


def create_sample_exercises():
    """创建示例练习数据"""
    with SeedManager() as seed_manager:
        # 确保有教师用户
        teacher = seed_manager.create_test_teacher()
        # 创建练习数据
        exercises = seed_manager.create_sample_exercises(teacher)
        return exercises


def main():
    """主函数"""
    print("=" * 50)
    print("教育平台测试数据生成工具")
    print("=" * 50)

    # 确保数据库已初始化
    try:
        print("🔧 初始化数据库...")
        init_database()
        print("✅ 数据库初始化完成")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "students":
            print("🎓 创建学生测试数据...")
            students = create_test_students()
            print(f"✅ 完成！创建了 {len(students)} 个学生账户")
            print("\n📋 学生登录信息:")
            print("用户名: student001-student008")
            print("密码: 123456")
            print("邮箱: student001@example.com - student008@example.com")
            
        elif command == "complete":
            print("🏗️ 创建完整测试数据...")
            create_complete_test_data()
            print("✅ 完成！创建了完整的测试数据")
            print("\n📋 登录信息:")
            print("管理员 - 用户名: admin, 密码: admin123456")
            print("教师 - 用户名: teacher123, 密码: 123456")
            print("学生 - 用户名: student001-student008, 密码: 123456")
            
        elif command == "users":
            print("👥 创建基础用户...")
            create_test_users()
            print("✅ 完成！创建了基础用户")
            print("\n📋 登录信息:")
            print("管理员 - 用户名: admin, 密码: admin123456")
            print("教师 - 用户名: teacher123, 密码: 123456")
            print("学生 - 用户名: student123, 密码: 123456")

        elif command == "courses":
            print("📚 创建丰富的课程数据...")
            create_rich_courses()
            print("✅ 完成！创建了丰富的课程数据")
            print("\n📋 包含以下类别的课程:")
            print("- 数学基础 (高等数学、线性代数、概率统计等)")
            print("- 编程语言 (Python、Java、C++、JavaScript)")
            print("- 计算机科学 (数据结构、数据库、操作系统等)")
            print("- Web开发 (前端、后端、全栈项目)")
            print("- 人工智能 (机器学习、深度学习、计算机视觉等)")
            print("- 数据科学 (数据分析、大数据、数据可视化)")

        elif command == "exercises":
            print("📝 创建示例练习数据...")
            create_sample_exercises()
            print("✅ 完成！创建了示例练习数据")
            print("\n📋 包含以下练习:")
            print("- 高等数学基础练习 (函数、极限、导数)")
            print("- 线性代数矩阵运算")
            print("- 概率论基础概念")
            print("- 计算机基础知识")
            print("- 英语语法练习")
            print("\n💡 现在学生可以在练习系统中看到这些练习了！")

        elif command == "help" or command == "-h" or command == "--help":
            show_help()

        else:
            print(f"❌ 未知命令: {command}")
            show_help()
            
    else:
        print("📦 创建默认种子数据...")
        seed_database()
        print("✅ 完成！创建了默认种子数据")
        print("\n📋 登录信息:")
        print("管理员 - 用户名: admin, 密码: admin123456")
        print("教师 - 用户名: teacher123, 密码: 123456")
        print("学生 - 用户名: student123, 密码: 123456")


def show_help():
    """显示帮助信息"""
    print("\n📖 使用说明:")
    print("  python create_test_data.py students  - 创建8个学生测试账户")
    print("  python create_test_data.py complete  - 创建完整测试数据(用户+课程+注册)")
    print("  python create_test_data.py courses   - 创建丰富的课程数据(30+门课程)")
    print("  python create_test_data.py users     - 创建基础用户(管理员+教师+学生)")
    print("  python create_test_data.py           - 创建默认种子数据")
    print("  python create_test_data.py help      - 显示此帮助信息")
    print("\n💡 提示:")
    print("  - 所有学生账户的密码都是: 123456")
    print("  - 学生用户名格式: student001, student002, ..., student008")
    print("  - 学生邮箱格式: student001@example.com, student002@example.com, ...")
    print("  - courses命令会创建6个类别共30+门课程，每门课程包含4-6个课时")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 操作被用户取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("请检查数据库连接和配置")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 操作完成！")
    print("=" * 50)

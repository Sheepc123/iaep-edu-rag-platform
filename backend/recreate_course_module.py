#!/usr/bin/env python3
"""
重新创建课程管理模块数据库表
只创建课程相关的新表，不影响现有的用户表
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def recreate_course_tables():
    """重新创建课程相关表"""
    print("📚 重新创建课程管理模块表...")
    
    try:
        from app.core.database import engine
        from app.models.course import Course, Lesson, CourseEnrollment, LessonProgress
        
        # 删除课程相关表（按依赖关系顺序）
        print("删除现有课程表...")
        LessonProgress.__table__.drop(engine, checkfirst=True)
        print("✅ 删除 lesson_progress 表")
        
        CourseEnrollment.__table__.drop(engine, checkfirst=True)
        print("✅ 删除 course_enrollments 表")
        
        Lesson.__table__.drop(engine, checkfirst=True)
        print("✅ 删除 lessons 表")
        
        Course.__table__.drop(engine, checkfirst=True)
        print("✅ 删除 courses 表")
        
        # 重新创建表
        print("\n创建新的课程表...")
        Course.__table__.create(engine)
        print("✅ 创建 courses 表")
        
        Lesson.__table__.create(engine)
        print("✅ 创建 lessons 表")
        
        CourseEnrollment.__table__.create(engine)
        print("✅ 创建 course_enrollments 表")
        
        LessonProgress.__table__.create(engine)
        print("✅ 创建 lesson_progress 表")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建课程表失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_sample_course():
    """创建示例课程数据"""
    print("\n📖 创建示例课程数据...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course, Lesson
        from app.models.user import User
        
        db = SessionLocal()
        
        # 获取教师用户
        teacher = db.query(User).filter(User.username == "teacher1").first()
        if not teacher:
            print("❌ 未找到教师用户teacher1")
            print("💡 请先运行用户认证模块重构: python recreate_auth_tables.py")
            return False
        
        # 创建示例课程
        course = Course(
            title="Python编程基础",
            description="学习Python编程语言的基础知识，适合初学者入门。本课程将从环境搭建开始，逐步介绍Python的基本语法、数据类型、控制结构等核心概念。",
            cover_image="https://example.com/python-course.jpg",
            category="编程语言",
            difficulty="easy",
            duration=1200,  # 20小时
            total_lessons=0,
            instructor_id=teacher.id,
            instructor_name=teacher.full_name or teacher.username,
            enrolled_students=0,
            rating=4.5,
            rating_count=0,
            is_active=True,
            is_published=True
        )
        db.add(course)
        db.flush()
        
        # 创建示例课时
        lessons_data = [
            {
                "title": "Python环境搭建",
                "description": "学习如何安装和配置Python开发环境，包括Python解释器、IDE选择和虚拟环境管理",
                "content": "本课时将详细介绍Python的安装过程，包括Windows、macOS和Linux系统的安装方法...",
                "lesson_order": 1,
                "duration": 30,
                "lesson_type": "video",
                "is_free": True
            },
            {
                "title": "Python基础语法",
                "description": "学习Python的基本语法规则，包括缩进、注释、变量命名等",
                "content": "Python语法简洁明了，采用缩进来表示代码块...",
                "lesson_order": 2,
                "duration": 45,
                "lesson_type": "video",
                "is_free": False
            },
            {
                "title": "变量和数据类型",
                "description": "了解Python中的变量定义和各种数据类型的使用方法",
                "content": "Python支持多种数据类型，包括数字、字符串、列表、字典等...",
                "lesson_order": 3,
                "duration": 40,
                "lesson_type": "interactive",
                "is_free": False
            },
            {
                "title": "控制结构",
                "description": "学习Python中的条件语句和循环语句",
                "content": "控制结构是编程的基础，包括if语句、for循环、while循环等...",
                "lesson_order": 4,
                "duration": 50,
                "lesson_type": "video",
                "is_free": False
            },
            {
                "title": "函数定义与调用",
                "description": "掌握Python函数的定义、参数传递和返回值",
                "content": "函数是代码复用的重要方式，Python函数定义简单灵活...",
                "lesson_order": 5,
                "duration": 35,
                "lesson_type": "interactive",
                "is_free": False
            }
        ]
        
        for lesson_data in lessons_data:
            lesson = Lesson(
                course_id=course.id,
                title=lesson_data["title"],
                description=lesson_data["description"],
                content=lesson_data["content"],
                lesson_order=lesson_data["lesson_order"],
                duration=lesson_data["duration"],
                lesson_type=lesson_data["lesson_type"],
                is_published=True,
                is_free=lesson_data["is_free"]
            )
            db.add(lesson)
        
        # 更新课程的总课时数
        course.total_lessons = len(lessons_data)

        # 在commit前保存需要显示的信息
        course_info = {
            'title': course.title,
            'category': course.category,
            'difficulty': course.difficulty,
            'total_lessons': course.total_lessons,
            'duration': course.duration,
            'instructor_name': course.instructor_name
        }

        db.commit()
        db.close()

        print("✅ 示例课程创建完成")
        print(f"   课程标题: {course_info['title']}")
        print(f"   课程分类: {course_info['category']}")
        print(f"   难度级别: {course_info['difficulty']}")
        print(f"   总课时数: {course_info['total_lessons']}")
        print(f"   总时长: {course_info['duration']}分钟")
        print(f"   教师: {course_info['instructor_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建示例课程失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_course_tables():
    """验证课程表结构"""
    print("\n🔍 验证课程表结构...")
    
    try:
        import sqlite3
        
        db_path = Path("data/database/education_platform.db")
        if not db_path.exists():
            print("❌ 数据库文件不存在")
            return False
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 检查课程相关表
        tables = ["courses", "lessons", "course_enrollments", "lesson_progress"]
        
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            if columns:
                print(f"✅ {table} 表存在，字段数: {len(columns)}")
                # 显示关键字段
                key_fields = [col[1] for col in columns[:5]]  # 显示前5个字段
                print(f"   关键字段: {', '.join(key_fields)}...")
            else:
                print(f"❌ {table} 表不存在")
                return False
        
        # 检查数据
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        print(f"📊 课程数量: {course_count}")
        
        cursor.execute("SELECT COUNT(*) FROM lessons")
        lesson_count = cursor.fetchone()[0]
        print(f"📊 课时数量: {lesson_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def test_course_api():
    """测试课程API功能"""
    print("\n🧪 测试课程API功能...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course, Lesson
        
        db = SessionLocal()
        
        # 测试课程查询
        courses = db.query(Course).all()
        print(f"✅ 课程查询成功，共 {len(courses)} 门课程")
        
        if courses:
            course = courses[0]
            print(f"   示例课程: {course.title}")
            
            # 测试课时查询
            lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
            print(f"✅ 课时查询成功，共 {len(lessons)} 个课时")
            
            if lessons:
                lesson = lessons[0]
                print(f"   示例课时: {lesson.title}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 课程管理模块数据库重构")
    print("=" * 60)
    
    # 1. 重新创建课程表
    tables_ok = recreate_course_tables()
    
    if not tables_ok:
        print("❌ 表创建失败，停止执行")
        return
    
    # 2. 创建示例课程
    sample_ok = create_sample_course()
    
    # 3. 验证表结构
    verify_ok = verify_course_tables()
    
    # 4. 测试API功能
    api_ok = test_course_api()
    
    print("\n" + "=" * 60)
    print("📋 重构结果:")
    print(f"   数据表创建: {'✅' if tables_ok else '❌'}")
    print(f"   示例数据: {'✅' if sample_ok else '❌'}")
    print(f"   表结构验证: {'✅' if verify_ok else '❌'}")
    print(f"   API功能测试: {'✅' if api_ok else '❌'}")
    
    if all([tables_ok, sample_ok, verify_ok, api_ok]):
        print("\n🎉 课程管理模块重构完成！")
        print("\n📋 创建的表:")
        print("   - courses: 课程基础信息")
        print("   - lessons: 课时内容管理")
        print("   - course_enrollments: 课程注册记录")
        print("   - lesson_progress: 学习进度跟踪")
        print("\n📚 示例数据:")
        print("   - Python编程基础课程")
        print("   - 5个示例课时")
        print("\n🚀 现在可以:")
        print("   1. 启动服务测试课程API")
        print("   2. 在前端测试课程功能")
        print("   3. 继续重构其他模块")
    else:
        print("\n❌ 重构过程中出现问题，请检查错误信息")


if __name__ == "__main__":
    main()

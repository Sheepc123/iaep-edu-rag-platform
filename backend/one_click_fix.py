#!/usr/bin/env python3
"""
一键修复练习系统问题
"""

import os
import sys
import sqlite3

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def ensure_database_tables():
    """确保数据库表存在"""
    print("🔧 确保数据库表存在...")
    
    try:
        from app.core.database import engine
        from app.models import exercise, course, user
        
        # 创建所有表
        exercise.Base.metadata.create_all(bind=engine)
        course.Base.metadata.create_all(bind=engine)
        user.Base.metadata.create_all(bind=engine)
        
        print("✅ 数据库表创建完成")
        return True
        
    except Exception as e:
        print(f"❌ 创建数据库表失败: {e}")
        return False

def create_basic_data():
    """创建基础数据"""
    print("\n📝 创建基础数据...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        from app.models.user import User
        from app.core.security import get_password_hash
        
        db = SessionLocal()
        
        # 1. 确保有教师用户
        teacher = db.query(User).filter(User.role == "teacher").first()
        if not teacher:
            print("创建教师用户...")
            teacher = User(
                username="teacher1",
                email="teacher1@example.com",
                full_name="张老师",
                hashed_password=get_password_hash("123456"),
                role="teacher",
                is_active=True
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print("✅ 教师用户创建完成")
        else:
            print("✅ 教师用户已存在")
        
        # 2. 确保有学生用户
        student = db.query(User).filter(User.role == "student").first()
        if not student:
            print("创建学生用户...")
            student = User(
                username="student1",
                email="student1@example.com",
                full_name="李同学",
                hashed_password=get_password_hash("123456"),
                role="student",
                is_active=True
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            print("✅ 学生用户创建完成")
        else:
            print("✅ 学生用户已存在")
        
        # 3. 确保有课程
        course = db.query(Course).first()
        if not course:
            print("创建示例课程...")
            course = Course(
                title="Python编程基础",
                description="从零开始学习Python编程语言",
                cover_image="https://via.placeholder.com/800x400",
                category="编程",
                difficulty="beginner",
                duration=1200,  # 20小时
                total_lessons=20,
                instructor_id=teacher.id,
                instructor_name=teacher.full_name or teacher.username,
                enrolled_students=0,
                rating=4.5,
                rating_count=10,
                is_active=True,
                is_published=True
            )
            db.add(course)
            db.commit()
            db.refresh(course)
            print("✅ 示例课程创建完成")
        else:
            print("✅ 课程已存在")
        
        # 4. 确保有练习
        existing_exercises = db.query(Exercise).filter(Exercise.course_id == course.id).count()
        if existing_exercises == 0:
            print("创建示例练习...")
            
            # 练习1
            exercise1 = Exercise(
                title="Python基础练习",
                description="测试Python基础语法和概念的练习题",
                category="practice",
                subject="Python编程",
                difficulty="easy",
                time_limit=30,
                course_id=course.id,
                created_by=teacher.id,
                total_questions=3,
                is_published=True,
                is_active=True
            )
            
            # 练习2
            exercise2 = Exercise(
                title="Python进阶作业",
                description="Python面向对象编程和高级特性练习",
                category="homework",
                subject="Python编程",
                difficulty="medium",
                time_limit=60,
                course_id=course.id,
                created_by=teacher.id,
                total_questions=2,
                is_published=True,
                is_active=True
            )
            
            db.add(exercise1)
            db.add(exercise2)
            db.commit()
            db.refresh(exercise1)
            db.refresh(exercise2)
            
            # 为练习1添加题目
            questions1 = [
                Question(
                    exercise_id=exercise1.id,
                    content="Python是什么类型的编程语言？",
                    question_type="multiple_choice",
                    options={"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                    correct_answer="B",
                    explanation="Python是一种解释型的高级编程语言。",
                    points=10,
                    difficulty="easy",
                    subject="Python编程",
                    is_active=True
                ),
                Question(
                    exercise_id=exercise1.id,
                    content="在Python中，用于定义函数的关键字是______。",
                    question_type="fill_blank",
                    options=None,
                    correct_answer="def",
                    explanation="在Python中，使用def关键字来定义函数。",
                    points=10,
                    difficulty="easy",
                    subject="Python编程",
                    is_active=True
                ),
                Question(
                    exercise_id=exercise1.id,
                    content="请解释Python中列表(list)和元组(tuple)的区别。",
                    question_type="essay",
                    options=None,
                    correct_answer="列表是可变的数据类型，元组是不可变的数据类型。",
                    explanation="这是一个开放性问题，主要考查对Python基础数据类型的理解。",
                    points=20,
                    difficulty="easy",
                    subject="Python编程",
                    is_active=True
                )
            ]
            
            # 为练习2添加题目
            questions2 = [
                Question(
                    exercise_id=exercise2.id,
                    content="Python中的装饰器主要用于什么？",
                    question_type="multiple_choice",
                    options={"A": "数据存储", "B": "函数增强", "C": "错误处理", "D": "性能优化"},
                    correct_answer="B",
                    explanation="装饰器主要用于在不修改原函数代码的情况下增强函数功能。",
                    points=15,
                    difficulty="medium",
                    subject="Python编程",
                    is_active=True
                ),
                Question(
                    exercise_id=exercise2.id,
                    content="什么是Python的GIL？请简要说明其作用。",
                    question_type="essay",
                    options=None,
                    correct_answer="GIL是全局解释器锁，确保同一时间只有一个线程执行Python字节码。",
                    explanation="GIL是Python多线程编程中的重要概念。",
                    points=25,
                    difficulty="medium",
                    subject="Python编程",
                    is_active=True
                )
            ]
            
            for question in questions1 + questions2:
                db.add(question)
            
            db.commit()
            print("✅ 示例练习和题目创建完成")
        else:
            print(f"✅ 已有 {existing_exercises} 个练习")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建基础数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_quickly():
    """快速测试API"""
    print("\n🧪 快速测试API...")
    
    try:
        import requests
        
        # 测试登录
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False},
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"❌ 登录失败: {response.status_code}")
            return False
        
        token = response.json()["access_token"]
        
        # 测试课程练习API
        response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            exercises = data.get('exercises', [])
            print(f"✅ API测试成功，获取到 {len(exercises)} 个练习")
            return True
        else:
            print(f"❌ API测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API测试异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 一键修复练习系统")
    print("=" * 50)
    
    # 1. 确保数据库表
    if not ensure_database_tables():
        print("❌ 数据库表创建失败")
        return
    
    # 2. 创建基础数据
    if not create_basic_data():
        print("❌ 基础数据创建失败")
        return
    
    # 3. 测试API
    if test_api_quickly():
        print("\n🎉 修复完成！")
        print("\n💡 下一步:")
        print("1. 重启前端服务: npm run dev")
        print("2. 访问: http://localhost:5173/teacher/courses/1")
        print("3. 查看课程练习标签")
    else:
        print("\n⚠️  基础数据已创建，但API测试失败")
        print("请检查后端服务是否正在运行: python run.py")

if __name__ == "__main__":
    main()

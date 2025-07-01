#!/usr/bin/env python3
"""
测试答案显示修复
"""

import requests
import json

def test_answer_display():
    """测试答案显示功能"""
    print("🧪 测试答案显示修复...")
    
    try:
        # 学生登录
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "student1", "password": "123456", "remember_me": False}
        )
        
        if login_response.status_code != 200:
            print(f"❌ 学生登录失败: {login_response.status_code}")
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ 学生登录成功")
        
        # 获取练习列表
        exercises_response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        if exercises_response.status_code != 200:
            print(f"❌ 获取练习失败: {exercises_response.status_code}")
            return False
        
        exercises_data = exercises_response.json()
        exercises = exercises_data.get('exercises', [])
        
        if not exercises:
            print("❌ 没有练习数据")
            return False
        
        exercise_id = exercises[0]['id']
        print(f"✅ 找到练习: {exercises[0]['title']} (ID: {exercise_id})")
        
        # 获取练习详情
        exercise_detail_response = requests.get(
            f"http://localhost:8000/api/v1/exercises/{exercise_id}",
            headers=headers
        )
        
        if exercise_detail_response.status_code != 200:
            print(f"❌ 获取练习详情失败: {exercise_detail_response.status_code}")
            return False
        
        exercise_detail = exercise_detail_response.json()
        print("✅ 获取练习详情成功")
        
        # 检查题目数据格式
        questions = exercise_detail.get('questions', [])
        print(f"\n📋 题目数据检查 (共 {len(questions)} 题):")
        
        for i, question in enumerate(questions, 1):
            print(f"\n题目 {i}:")
            print(f"  类型: {question.get('question_type')}")
            print(f"  内容: {question.get('content', '')[:50]}...")
            
            # 检查选项格式
            options = question.get('options')
            if options:
                print(f"  选项类型: {type(options)}")
                if isinstance(options, dict):
                    print(f"  选项内容: {options}")
                    # 模拟前端转换
                    formatted_options = [f"{k}. {v}" for k, v in options.items()]
                    print(f"  转换后: {formatted_options}")
                elif isinstance(options, list):
                    print(f"  选项内容: {options}")
            
            print(f"  正确答案: {question.get('correct_answer')}")
            print(f"  分值: {question.get('points')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_data_if_needed():
    """创建测试数据"""
    print("\n📝 创建测试数据...")
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        from app.models.user import User
        
        db = SessionLocal()
        
        # 检查是否已有数据
        exercise = db.query(Exercise).first()
        if exercise:
            print("✅ 已有练习数据")
            db.close()
            return True
        
        # 获取教师和课程
        teacher = db.query(User).filter(User.role == "teacher").first()
        course = db.query(Course).first()
        
        if not teacher or not course:
            print("❌ 缺少基础数据")
            db.close()
            return False
        
        # 创建练习
        exercise = Exercise(
            title="答案显示测试练习",
            description="用于测试答案显示功能的练习",
            category="practice",
            subject="测试",
            difficulty="easy",
            time_limit=30,
            course_id=course.id,
            created_by=teacher.id,
            total_questions=3,
            is_published=True,
            is_active=True
        )
        
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        
        # 创建题目
        questions = [
            {
                "content": "Python是什么类型的编程语言？",
                "question_type": "multiple_choice",
                "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                "correct_answer": "B",
                "explanation": "Python是解释型编程语言",
                "points": 10
            },
            {
                "content": "在Python中，用于定义函数的关键字是______。",
                "question_type": "fill_blank",
                "options": None,
                "correct_answer": "def",
                "explanation": "def是Python中定义函数的关键字",
                "points": 15
            },
            {
                "content": "请简述Python的主要特点。",
                "question_type": "essay",
                "options": None,
                "correct_answer": "Python具有简洁易读、跨平台、丰富的库等特点",
                "explanation": "这是一道主观题，答案可以多样化",
                "points": 20
            }
        ]
        
        for q_data in questions:
            question = Question(
                exercise_id=exercise.id,
                content=q_data["content"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"],
                points=q_data["points"],
                difficulty="easy",
                subject="测试",
                is_active=True
            )
            db.add(question)
        
        db.commit()
        db.close()
        
        print("✅ 测试数据创建完成")
        return True
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 答案显示功能测试")
    print("=" * 50)
    
    # 1. 创建测试数据
    if not create_test_data_if_needed():
        print("❌ 测试数据准备失败")
        return
    
    # 2. 测试答案显示
    if test_answer_display():
        print("\n🎉 答案显示测试通过！")
        print("\n💡 前端测试步骤:")
        print("1. 访问: http://localhost:5173/student/exercises/practice/1")
        print("2. 选择答案（选择题选B，填空题填def）")
        print("3. 点击'提交答案'")
        print("4. 查看是否显示正确/错误标识")
        print("5. 点击'查看详细结果'查看完整结果")
        
        print("\n🔍 预期效果:")
        print("- 选择题选B应该显示绿色✓正确")
        print("- 填空题填def应该显示绿色✓正确")
        print("- 错误答案应该显示红色✗错误")
        print("- 提交后不会立即跳转，可以查看答案")
    else:
        print("\n❌ 答案显示测试失败")

if __name__ == "__main__":
    main()

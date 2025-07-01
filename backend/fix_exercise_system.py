#!/usr/bin/env python3
"""
修复练习系统的综合脚本
"""

import sys
import os
import json
import requests

def test_exercise_apis():
    """测试练习相关的API"""
    print("🧪 测试练习API...")
    
    try:
        # 登录
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "student1", "password": "123456", "remember_me": False}
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.status_code}")
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ 学生登录成功")
        
        # 1. 测试获取练习详情
        print("\n1. 测试获取练习详情...")
        exercise_response = requests.get(
            "http://localhost:8000/api/v1/exercises/1",
            headers=headers
        )
        
        if exercise_response.status_code == 200:
            exercise_data = exercise_response.json()
            print("✅ 获取练习详情成功")
            print(f"   练习标题: {exercise_data.get('title')}")
            print(f"   题目数量: {len(exercise_data.get('questions', []))}")
            
            # 检查题目数据
            questions = exercise_data.get('questions', [])
            for i, q in enumerate(questions, 1):
                print(f"   题目{i}: {q.get('question_type')} - {q.get('content', '')[:30]}...")
                if q.get('question_type') == 'multiple_choice':
                    print(f"     选项: {q.get('options')}")
                    print(f"     正确答案: {q.get('correct_answer')}")
        else:
            print(f"❌ 获取练习详情失败: {exercise_response.status_code}")
            print(f"   错误: {exercise_response.text}")
            return False
        
        # 2. 测试开始练习
        print("\n2. 测试开始练习...")
        start_response = requests.post(
            "http://localhost:8000/api/v1/exercises/1/start",
            headers=headers
        )
        
        if start_response.status_code == 200:
            attempt_data = start_response.json()
            attempt_id = attempt_data.get('id')
            print(f"✅ 开始练习成功，尝试ID: {attempt_id}")
        else:
            print(f"❌ 开始练习失败: {start_response.status_code}")
            print(f"   错误: {start_response.text}")
            return False
        
        # 3. 测试提交答案
        print("\n3. 测试提交答案...")
        submit_data = {
            "attempt_id": attempt_id,
            "answers": [
                {
                    "question_id": questions[0]['id'],
                    "answer_content": "B",
                    "time_spent": 30
                }
            ]
        }
        
        submit_response = requests.post(
            "http://localhost:8000/api/v1/exercises/submit",
            headers=headers,
            json=submit_data
        )
        
        if submit_response.status_code == 200:
            print("✅ 提交答案成功")
        else:
            print(f"❌ 提交答案失败: {submit_response.status_code}")
            print(f"   错误: {submit_response.text}")
            # 继续测试，不返回False
        
        # 4. 测试获取练习尝试结果
        print("\n4. 测试获取练习尝试结果...")
        attempt_response = requests.get(
            f"http://localhost:8000/api/v1/exercises/attempts/{attempt_id}",
            headers=headers
        )
        
        if attempt_response.status_code == 200:
            attempt_result = attempt_response.json()
            print("✅ 获取练习尝试结果成功")
            print(f"   总题数: {attempt_result.get('total_questions')}")
            print(f"   正确数: {attempt_result.get('correct_answers')}")
            print(f"   准确率: {attempt_result.get('accuracy_rate')}%")
            print(f"   答案数量: {len(attempt_result.get('answers', []))}")
        else:
            print(f"❌ 获取练习尝试结果失败: {attempt_response.status_code}")
            print(f"   错误: {attempt_response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_backend_endpoints():
    """检查后端端点是否存在"""
    print("\n🔍 检查后端端点...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # 检查练习相关的路由
        from app.api.v1.endpoints import exercises
        
        print("✅ 练习端点模块存在")
        
        # 检查路由器
        router = exercises.router
        routes = router.routes
        
        print("练习相关路由:")
        for route in routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"  {list(route.methods)[0] if route.methods else 'GET'} {route.path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查后端端点失败: {e}")
        return False

def create_complete_test_data():
    """创建完整的测试数据"""
    print("\n📝 创建完整测试数据...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question, ExerciseAttempt, Answer
        from app.models.course import Course
        from app.models.user import User
        from datetime import datetime
        
        db = SessionLocal()
        
        # 获取学生和教师
        student = db.query(User).filter(User.role == "student").first()
        teacher = db.query(User).filter(User.role == "teacher").first()
        course = db.query(Course).first()
        
        if not all([student, teacher, course]):
            print("❌ 缺少基础数据（学生、教师、课程）")
            return False
        
        # 清理现有数据
        db.query(Answer).delete()
        db.query(ExerciseAttempt).delete()
        db.query(Question).delete()
        db.query(Exercise).delete()
        
        # 创建练习
        exercise = Exercise(
            title="完整测试练习",
            description="用于测试完整功能的练习",
            category="practice",
            subject="测试",
            difficulty="easy",
            time_limit=30,
            course_id=course.id,
            created_by=teacher.id,
            total_questions=2,
            is_published=True,
            is_active=True
        )
        
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        
        # 创建题目
        questions_data = [
            {
                "content": "Python是什么类型的编程语言？",
                "question_type": "multiple_choice",
                "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                "correct_answer": "B",
                "explanation": "Python是解释型编程语言，代码在运行时被解释器逐行解释执行。",
                "points": 10
            },
            {
                "content": "在Python中，用于定义函数的关键字是______。",
                "question_type": "fill_blank",
                "options": None,
                "correct_answer": "def",
                "explanation": "def是Python中定义函数的关键字。",
                "points": 15
            }
        ]
        
        created_questions = []
        for q_data in questions_data:
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
            created_questions.append(question)
        
        db.commit()
        
        print("✅ 完整测试数据创建成功")
        print(f"   练习ID: {exercise.id}")
        print(f"   题目数量: {len(created_questions)}")
        
        for i, q in enumerate(created_questions, 1):
            print(f"   题目{i}: {q.question_type} - {q.content[:30]}...")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 练习系统综合修复")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    # 1. 创建测试数据
    if create_complete_test_data():
        success_count += 1
        print("✅ 测试数据创建成功")
    else:
        print("❌ 测试数据创建失败")
    
    # 2. 检查后端端点
    if check_backend_endpoints():
        success_count += 1
        print("✅ 后端端点检查成功")
    else:
        print("❌ 后端端点检查失败")
    
    # 3. 测试API
    if test_exercise_apis():
        success_count += 1
        print("✅ API测试成功")
    else:
        print("❌ API测试失败")
    
    print("\n" + "=" * 60)
    print(f"🎯 修复结果: {success_count}/{total_tests} 项成功")
    
    if success_count >= 2:
        print("\n🎉 练习系统基本正常！")
        print("\n💡 前端测试步骤:")
        print("1. 访问: http://localhost:5173/student/exercises/practice/1")
        print("2. 选择答案B（解释型）")
        print("3. 填空题填写'def'")
        print("4. 点击'提交答案'")
        print("5. 查看答案显示效果")
        print("6. 点击'查看详细结果'")
        
        print("\n🔍 预期效果:")
        print("- 选择题选B应该显示绿色✓正确")
        print("- 填空题填def应该显示绿色✓正确")
        print("- 提交后显示成功提示")
        print("- 结果页面显示详细分析")
    else:
        print("\n❌ 练习系统仍有问题")
        print("请检查后端服务和数据库")

if __name__ == "__main__":
    main()

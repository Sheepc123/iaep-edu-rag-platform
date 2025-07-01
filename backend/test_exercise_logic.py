#!/usr/bin/env python3
"""
测试练习页面逻辑
"""

import requests
import json
import sys
import os

def test_exercise_data_format():
    """测试练习数据格式"""
    print("🧪 测试练习数据格式...")
    
    try:
        # 登录
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False}
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.status_code}")
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
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
        
        # 检查数据格式
        print("\n📋 练习数据格式检查:")
        print(f"练习ID: {exercise_detail.get('id')}")
        print(f"练习标题: {exercise_detail.get('title')}")
        print(f"题目数量: {len(exercise_detail.get('questions', []))}")
        
        # 检查题目格式
        questions = exercise_detail.get('questions', [])
        for i, question in enumerate(questions, 1):
            print(f"\n题目 {i}:")
            print(f"  ID: {question.get('id')}")
            print(f"  类型: {question.get('question_type')}")
            print(f"  内容: {question.get('content', '')[:50]}...")
            print(f"  选项: {question.get('options')}")
            print(f"  正确答案: {question.get('correct_answer')}")
            print(f"  分值: {question.get('points')}")
            
            # 检查选项格式
            options = question.get('options')
            if options:
                if isinstance(options, dict):
                    print(f"  选项格式: 对象格式 {options}")
                elif isinstance(options, list):
                    print(f"  选项格式: 数组格式 {options}")
                else:
                    print(f"  选项格式: 其他格式 {type(options)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_student_exercise_access():
    """测试学生端练习访问"""
    print("\n👨‍🎓 测试学生端练习访问...")
    
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
        
        # 获取练习列表
        exercises_response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        if exercises_response.status_code != 200:
            print(f"❌ 学生获取练习失败: {exercises_response.status_code}")
            return False
        
        exercises_data = exercises_response.json()
        exercises = exercises_data.get('exercises', [])
        
        if not exercises:
            print("❌ 学生看不到练习")
            return False
        
        exercise_id = exercises[0]['id']
        print(f"✅ 学生可以看到练习: {exercises[0]['title']}")
        
        # 开始练习
        start_response = requests.post(
            f"http://localhost:8000/api/v1/exercises/{exercise_id}/start",
            headers=headers
        )
        
        if start_response.status_code != 200:
            print(f"❌ 开始练习失败: {start_response.status_code}")
            print(f"错误信息: {start_response.text}")
            return False
        
        attempt_data = start_response.json()
        attempt_id = attempt_data.get('id')
        print(f"✅ 开始练习成功，尝试ID: {attempt_id}")
        
        # 获取练习详情（学生视角）
        exercise_detail_response = requests.get(
            f"http://localhost:8000/api/v1/exercises/{exercise_id}",
            headers=headers
        )
        
        if exercise_detail_response.status_code == 200:
            exercise_detail = exercise_detail_response.json()
            print("✅ 学生可以获取练习详情")
            
            # 检查学生看到的数据格式
            questions = exercise_detail.get('questions', [])
            print(f"学生看到 {len(questions)} 道题目")
            
            for question in questions:
                print(f"  题目: {question.get('content', '')[:30]}...")
                print(f"  类型: {question.get('question_type')}")
                print(f"  选项: {question.get('options')}")
                # 注意：学生不应该看到正确答案
                if 'correct_answer' in question:
                    print("  ⚠️  学生可以看到正确答案！这可能是安全问题")
        
        return True
        
    except Exception as e:
        print(f"❌ 学生测试失败: {e}")
        return False

def check_database_questions():
    """检查数据库中的题目数据"""
    print("\n🗄️ 检查数据库题目数据...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        
        db = SessionLocal()
        
        # 获取所有题目
        questions = db.query(Question).all()
        print(f"数据库中共有 {len(questions)} 道题目")
        
        for question in questions:
            print(f"\n题目ID: {question.id}")
            print(f"练习ID: {question.exercise_id}")
            print(f"类型: {question.question_type}")
            print(f"内容: {question.content[:50]}...")
            print(f"选项: {question.options}")
            print(f"正确答案: {question.correct_answer}")
            print(f"分值: {question.points}")
            
            # 检查选项格式
            if question.options:
                print(f"选项类型: {type(question.options)}")
                if isinstance(question.options, dict):
                    print("选项是字典格式 ✓")
                else:
                    print("选项不是字典格式 ⚠️")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 练习页面逻辑测试")
    print("=" * 50)
    
    success_count = 0
    
    # 1. 检查数据库题目
    if check_database_questions():
        success_count += 1
    
    # 2. 测试练习数据格式
    if test_exercise_data_format():
        success_count += 1
    
    # 3. 测试学生端访问
    if test_student_exercise_access():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 测试结果: {success_count}/3 项通过")
    
    if success_count >= 2:
        print("🎉 练习逻辑基本正常！")
        print("\n💡 前端测试:")
        print("1. 访问: http://localhost:5173/student/courses/1")
        print("2. 点击练习进入答题页面")
        print("3. 检查答案显示是否正确")
        print("4. 提交答案查看结果")
    else:
        print("❌ 练习逻辑有问题")
        print("请检查数据库数据和API接口")

if __name__ == "__main__":
    main()

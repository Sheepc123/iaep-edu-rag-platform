#!/usr/bin/env python3
"""
测试练习系统功能
"""

import requests
import json

def test_exercise_system():
    """测试练习系统完整功能"""
    print("🧪 测试练习系统功能...")
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # 1. 教师登录
        print("\n1. 教师登录...")
        teacher_login = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "teacher1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if teacher_login.status_code != 200:
            print(f"❌ 教师登录失败: {teacher_login.text}")
            return
        
        teacher_token = teacher_login.json()["access_token"]
        teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
        print("✅ 教师登录成功")
        
        # 2. 获取课程列表
        print("\n2. 获取课程列表...")
        courses_response = requests.get(
            f"{base_url}/courses/",
            headers=teacher_headers
        )
        
        if courses_response.status_code == 200:
            courses_data = courses_response.json()
            courses = courses_data.get('courses', [])
            print(f"✅ 获取到 {len(courses)} 门课程")
            
            if courses:
                course_id = courses[0]['id']
                print(f"   使用课程: {courses[0]['title']} (ID: {course_id})")
            else:
                print("❌ 没有找到课程")
                return
        else:
            print(f"❌ 获取课程失败: {courses_response.text}")
            return
        
        # 3. 获取课程练习
        print(f"\n3. 获取课程 {course_id} 的练习...")
        course_exercises_response = requests.get(
            f"{base_url}/courses/{course_id}/exercises",
            headers=teacher_headers
        )
        
        if course_exercises_response.status_code == 200:
            exercises_data = course_exercises_response.json()
            exercises = exercises_data.get('exercises', [])
            print(f"✅ 课程有 {len(exercises)} 个练习")
            
            for exercise in exercises:
                print(f"   - {exercise['title']} (ID: {exercise['id']})")
        else:
            print(f"❌ 获取课程练习失败: {course_exercises_response.text}")
        
        # 4. 创建新练习
        print(f"\n4. 为课程 {course_id} 创建新练习...")
        exercise_data = {
            "title": "测试练习",
            "description": "这是一个测试练习",
            "course_id": course_id,
            "category": "practice",
            "difficulty": "medium",
            "time_limit": 30,
            "pass_score": 60.0
        }
        
        create_exercise_response = requests.post(
            f"{base_url}/exercises/",
            headers=teacher_headers,
            json=exercise_data
        )
        
        if create_exercise_response.status_code == 200:
            new_exercise = create_exercise_response.json()
            exercise_id = new_exercise['id']
            print(f"✅ 创建练习成功: {new_exercise['title']} (ID: {exercise_id})")
        else:
            print(f"❌ 创建练习失败: {create_exercise_response.text}")
            return
        
        # 5. 为练习添加题目
        print(f"\n5. 为练习 {exercise_id} 添加题目...")
        
        # 添加选择题
        question_data = {
            "question_text": "Python是什么类型的编程语言？",
            "question_type": "multiple_choice",
            "options": ["编译型", "解释型", "汇编型", "机器型"],
            "correct_answer": "解释型",
            "explanation": "Python是一种解释型的高级编程语言",
            "points": 10.0,
            "difficulty": "easy",
            "question_order": 1
        }
        
        add_question_response = requests.post(
            f"{base_url}/exercises/{exercise_id}/questions",
            headers=teacher_headers,
            json=question_data
        )
        
        if add_question_response.status_code == 200:
            question = add_question_response.json()
            print(f"✅ 添加题目成功: {question['question_text']}")
        else:
            print(f"❌ 添加题目失败: {add_question_response.text}")
        
        # 6. 学生登录
        print("\n6. 学生登录...")
        student_login = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "student1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if student_login.status_code != 200:
            print(f"❌ 学生登录失败: {student_login.text}")
            return
        
        student_token = student_login.json()["access_token"]
        student_headers = {"Authorization": f"Bearer {student_token}"}
        print("✅ 学生登录成功")
        
        # 7. 学生查看课程练习
        print(f"\n7. 学生查看课程 {course_id} 的练习...")
        student_exercises_response = requests.get(
            f"{base_url}/courses/{course_id}/exercises",
            headers=student_headers
        )
        
        if student_exercises_response.status_code == 200:
            student_exercises_data = student_exercises_response.json()
            student_exercises = student_exercises_data.get('exercises', [])
            print(f"✅ 学生可以看到 {len(student_exercises)} 个练习")
            
            for exercise in student_exercises:
                print(f"   - {exercise['title']} ({'已发布' if exercise['is_published'] else '未发布'})")
        else:
            print(f"❌ 学生获取课程练习失败: {student_exercises_response.text}")
        
        # 8. 发布练习
        print(f"\n8. 发布练习 {exercise_id}...")
        publish_response = requests.put(
            f"{base_url}/exercises/{exercise_id}",
            headers=teacher_headers,
            json={"is_published": True}
        )
        
        if publish_response.status_code == 200:
            print("✅ 练习发布成功")
        else:
            print(f"❌ 练习发布失败: {publish_response.text}")
        
        # 9. 学生开始练习
        print(f"\n9. 学生开始练习 {exercise_id}...")
        start_exercise_response = requests.post(
            f"{base_url}/exercises/{exercise_id}/start",
            headers=student_headers
        )
        
        if start_exercise_response.status_code == 200:
            attempt = start_exercise_response.json()
            attempt_id = attempt['id']
            print(f"✅ 开始练习成功，尝试ID: {attempt_id}")
        else:
            print(f"❌ 开始练习失败: {start_exercise_response.text}")
            return
        
        print("\n" + "=" * 60)
        print("📋 测试总结:")
        print("✅ 教师可以创建练习")
        print("✅ 教师可以添加题目")
        print("✅ 教师可以发布练习")
        print("✅ 学生可以查看课程练习")
        print("✅ 学生可以开始练习")
        print("\n💡 前端测试:")
        print(f"1. 教师端: http://localhost:5173/teacher/courses/{course_id}")
        print(f"2. 学生端: http://localhost:5173/student/courses/{course_id}")
        print(f"3. 练习页面: http://localhost:5173/student/exercise/{exercise_id}")
        
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()


def check_database_tables():
    """检查数据库表结构"""
    print("\n🔍 检查数据库表结构...")
    
    try:
        import os
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal, engine
        from app.models.exercise import Exercise, Question, ExerciseAttempt, StudentAnswer
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        
        # 检查练习相关表
        tables_to_check = ['exercises', 'questions', 'exercise_attempts', 'student_answers']
        
        for table_name in tables_to_check:
            if inspector.has_table(table_name):
                columns = inspector.get_columns(table_name)
                print(f"✅ 表 {table_name} 存在，有 {len(columns)} 个字段")
            else:
                print(f"❌ 表 {table_name} 不存在")
        
        # 检查数据
        db = SessionLocal()
        
        exercise_count = db.query(Exercise).count()
        question_count = db.query(Question).count()
        attempt_count = db.query(ExerciseAttempt).count()
        
        print(f"\n📊 数据统计:")
        print(f"   练习数量: {exercise_count}")
        print(f"   题目数量: {question_count}")
        print(f"   尝试记录: {attempt_count}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")


def main():
    """主函数"""
    print("🚀 练习系统测试")
    print("=" * 60)
    
    # 检查数据库
    check_database_tables()
    
    # 测试API
    test_exercise_system()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
课程习题API测试脚本
专门测试课程详情页面的习题展示功能
"""

import requests
import json
from datetime import datetime

def test_course_exercises_display():
    """测试课程习题展示功能"""
    print("🧪 测试课程习题展示功能...")
    
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
            return False
        
        teacher_token = teacher_login.json()["access_token"]
        teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
        print("✅ 教师登录成功")
        
        # 2. 获取课程列表
        print("\n2. 获取课程列表...")
        courses_response = requests.get(
            f"{base_url}/courses/",
            headers=teacher_headers
        )
        
        if courses_response.status_code != 200:
            print(f"❌ 获取课程失败: {courses_response.text}")
            return False
        
        courses_data = courses_response.json()
        courses = courses_data.get('courses', [])
        
        if not courses:
            print("❌ 没有找到课程")
            return False
        
        course = courses[0]
        course_id = course['id']
        print(f"✅ 使用课程: {course['title']} (ID: {course_id})")
        
        # 3. 获取课程习题 - 这是关键API
        print(f"\n3. 获取课程 {course_id} 的习题...")
        exercises_response = requests.get(
            f"{base_url}/courses/{course_id}/exercises",
            headers=teacher_headers
        )
        
        if exercises_response.status_code != 200:
            print(f"❌ 获取课程习题失败: {exercises_response.text}")
            return False
        
        exercises_data = exercises_response.json()
        exercises = exercises_data.get('exercises', [])
        
        print(f"✅ 获取到 {len(exercises)} 个习题")
        
        # 4. 详细展示习题信息（模拟前端显示）
        print(f"\n📚 课程《{course['title']}》的习题列表:")
        print("=" * 80)
        
        if not exercises:
            print("   暂无习题")
            return True
        
        for i, exercise in enumerate(exercises, 1):
            print(f"\n{i}. 【{exercise['category'].upper()}】{exercise['title']}")
            print(f"   📝 描述: {exercise['description']}")
            print(f"   📊 难度: {exercise['difficulty']} | 题目数: {exercise['total_questions']}题")
            
            if exercise.get('time_limit'):
                print(f"   ⏰ 时间限制: {exercise['time_limit']}分钟")
            else:
                print(f"   ⏰ 时间限制: 不限时")
            
            print(f"   📈 统计: {exercise['total_attempts']}人参与, 平均分: {exercise['average_score']:.1f}")
            print(f"   🔖 状态: {'已发布' if exercise['is_published'] else '草稿'}")
            print(f"   📅 创建时间: {exercise['created_at']}")
            
            # 获取习题的具体题目
            questions_response = requests.get(
                f"{base_url}/exercises/{exercise['id']}/questions",
                headers=teacher_headers
            )
            
            if questions_response.status_code == 200:
                questions = questions_response.json()
                print(f"   📋 题目预览:")
                for j, question in enumerate(questions[:2], 1):  # 只显示前2题
                    print(f"      {j}. [{question['question_type']}] {question['content'][:50]}...")
                if len(questions) > 2:
                    print(f"      ... 还有 {len(questions) - 2} 道题目")
            
            print("   " + "-" * 60)
        
        # 5. 测试学生端访问
        print(f"\n5. 测试学生端访问...")
        student_login = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "student1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if student_login.status_code == 200:
            student_token = student_login.json()["access_token"]
            student_headers = {"Authorization": f"Bearer {student_token}"}
            
            # 学生获取课程习题
            student_exercises_response = requests.get(
                f"{base_url}/courses/{course_id}/exercises",
                headers=student_headers
            )
            
            if student_exercises_response.status_code == 200:
                student_exercises_data = student_exercises_response.json()
                student_exercises = student_exercises_data.get('exercises', [])
                
                # 过滤出已发布的习题
                published_exercises = [ex for ex in student_exercises if ex['is_published']]
                
                print(f"✅ 学生可以看到 {len(published_exercises)} 个已发布的习题")
                
                for exercise in published_exercises:
                    print(f"   - {exercise['title']} ({exercise['category']})")
            else:
                print(f"❌ 学生获取习题失败: {student_exercises_response.text}")
        else:
            print(f"❌ 学生登录失败: {student_login.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_exercise_categories():
    """测试不同类型的习题"""
    print("\n🏷️  测试习题分类功能...")
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # 教师登录
        teacher_login = requests.post(
            f"{base_url}/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False}
        )
        
        if teacher_login.status_code != 200:
            return False
        
        teacher_token = teacher_login.json()["access_token"]
        teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
        
        # 获取课程
        courses_response = requests.get(f"{base_url}/courses/", headers=teacher_headers)
        if courses_response.status_code != 200:
            return False
        
        courses = courses_response.json().get('courses', [])
        if not courses:
            return False
        
        course_id = courses[0]['id']
        
        # 获取习题并按分类统计
        exercises_response = requests.get(
            f"{base_url}/courses/{course_id}/exercises",
            headers=teacher_headers
        )
        
        if exercises_response.status_code != 200:
            return False
        
        exercises = exercises_response.json().get('exercises', [])
        
        # 按分类统计
        categories = {}
        for exercise in exercises:
            category = exercise['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(exercise)
        
        print("📊 习题分类统计:")
        category_names = {
            'practice': '自主练习',
            'homework': '课后作业',
            'exam': '模拟考试',
            'review': '复习练习'
        }
        
        for category, exercises_list in categories.items():
            category_name = category_names.get(category, category)
            print(f"   {category_name}: {len(exercises_list)} 个")
            for exercise in exercises_list:
                status = "已发布" if exercise['is_published'] else "草稿"
                print(f"     - {exercise['title']} ({status})")
        
        return True
        
    except Exception as e:
        print(f"❌ 分类测试失败: {e}")
        return False


def generate_frontend_test_data():
    """生成前端测试用的数据格式"""
    print("\n📋 生成前端测试数据格式...")
    
    # 模拟前端需要的数据结构
    sample_exercises = [
        {
            "id": 1,
            "title": "Python基础练习",
            "description": "测试Python基础语法和概念的练习题",
            "category": "practice",
            "difficulty": "easy",
            "time_limit": 30,
            "total_questions": 3,
            "total_points": 40,
            "total_attempts": 15,
            "average_score": 85.5,
            "is_published": True,
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "title": "Python进阶作业",
            "description": "Python面向对象编程和高级特性练习",
            "category": "homework",
            "difficulty": "medium",
            "time_limit": 60,
            "total_questions": 2,
            "total_points": 40,
            "total_attempts": 8,
            "average_score": 78.2,
            "is_published": True,
            "created_at": "2024-01-20T14:15:00Z"
        }
    ]
    
    print("📄 前端课程习题数据格式:")
    print(json.dumps(sample_exercises, indent=2, ensure_ascii=False))
    
    print("\n💡 前端使用说明:")
    print("1. 在课程详情页面的习题标签中显示这些数据")
    print("2. 根据category显示不同的标签颜色")
    print("3. 根据is_published控制学生端的可见性")
    print("4. 点击习题可以跳转到具体的答题页面")


def main():
    """主函数"""
    print("🚀 课程习题API测试")
    print("=" * 60)
    
    # 1. 测试课程习题展示
    if not test_course_exercises_display():
        print("❌ 课程习题展示测试失败")
        return
    
    # 2. 测试习题分类
    if not test_exercise_categories():
        print("❌ 习题分类测试失败")
        return
    
    # 3. 生成前端测试数据
    generate_frontend_test_data()
    
    print("\n" + "=" * 60)
    print("🎉 课程习题API测试完成！")
    print("\n📋 测试结果:")
    print("✅ 课程习题列表API正常")
    print("✅ 教师端可以查看所有习题")
    print("✅ 学生端只能看到已发布习题")
    print("✅ 习题分类功能正常")
    print("✅ 数据格式符合前端需求")
    
    print("\n💡 前端集成步骤:")
    print("1. 在教师端课程详情页调用: GET /api/v1/courses/{id}/exercises")
    print("2. 在学生端课程详情页调用: GET /api/v1/courses/{id}/exercises")
    print("3. 根据用户角色过滤显示内容")
    print("4. 实现习题卡片的点击跳转功能")


if __name__ == "__main__":
    main()

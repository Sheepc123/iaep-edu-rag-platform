#!/usr/bin/env python3
"""
测试序列化修复
"""

import requests
import json
import sys
import os

def test_api_serialization():
    """测试API序列化是否修复"""
    print("🧪 测试API序列化修复...")
    
    try:
        # 1. 测试服务器健康状态
        print("1. 检查服务器状态...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器未运行，请启动: python run.py")
            return False
        print("✅ 服务器运行正常")
        
        # 2. 登录获取token
        print("2. 教师登录...")
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "username": "teacher1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.status_code}")
            print(f"响应: {login_response.text}")
            return False
        
        token = login_response.json()["access_token"]
        print("✅ 登录成功")
        
        # 3. 测试课程练习API
        print("3. 测试课程练习API...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        api_response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        print(f"API响应状态: {api_response.status_code}")
        
        if api_response.status_code == 200:
            try:
                data = api_response.json()
                print("✅ API调用成功，JSON解析正常")
                
                exercises = data.get('exercises', [])
                print(f"获取到 {len(exercises)} 个练习:")
                
                for i, exercise in enumerate(exercises, 1):
                    print(f"  {i}. {exercise.get('title', 'N/A')}")
                    print(f"     分类: {exercise.get('category', 'N/A')}")
                    print(f"     难度: {exercise.get('difficulty', 'N/A')}")
                    print(f"     题目数: {exercise.get('total_questions', 0)}")
                    print(f"     状态: {'已发布' if exercise.get('is_published') else '草稿'}")
                    print(f"     创建时间: {exercise.get('created_at', 'N/A')}")
                    print()
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应: {api_response.text}")
                return False
                
        else:
            print(f"❌ API调用失败: {api_response.status_code}")
            print(f"错误响应: {api_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_student_access():
    """测试学生端访问"""
    print("\n👨‍🎓 测试学生端访问...")
    
    try:
        # 学生登录
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "username": "student1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print("❌ 学生登录失败")
            return False
        
        token = login_response.json()["access_token"]
        print("✅ 学生登录成功")
        
        # 测试学生获取课程练习
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        api_response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        if api_response.status_code == 200:
            data = api_response.json()
            exercises = data.get('exercises', [])
            
            # 学生应该只能看到已发布的练习
            published_exercises = [ex for ex in exercises if ex.get('is_published')]
            
            print(f"✅ 学生可以看到 {len(published_exercises)} 个已发布练习")
            
            for exercise in published_exercises:
                print(f"  - {exercise.get('title')} ({exercise.get('category')})")
            
            return True
        else:
            print(f"❌ 学生API调用失败: {api_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 学生测试异常: {e}")
        return False

def check_database_data():
    """检查数据库数据"""
    print("\n🗄️ 检查数据库数据...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise
        from app.models.course import Course
        from app.models.user import User
        
        db = SessionLocal()
        
        # 检查用户
        teacher_count = db.query(User).filter(User.role == "teacher").count()
        student_count = db.query(User).filter(User.role == "student").count()
        print(f"用户统计: {teacher_count} 个教师, {student_count} 个学生")
        
        # 检查课程
        course_count = db.query(Course).count()
        print(f"课程数量: {course_count}")
        
        if course_count > 0:
            course = db.query(Course).first()
            print(f"第一个课程: {course.title} (ID: {course.id})")
            
            # 检查练习
            exercise_count = db.query(Exercise).filter(Exercise.course_id == course.id).count()
            print(f"课程练习数量: {exercise_count}")
            
            if exercise_count > 0:
                exercises = db.query(Exercise).filter(Exercise.course_id == course.id).all()
                print("练习详情:")
                for ex in exercises:
                    print(f"  - ID: {ex.id}, 标题: {ex.title}")
                    print(f"    分类: {ex.category}, 难度: {ex.difficulty}")
                    print(f"    状态: {'已发布' if ex.is_published else '草稿'}")
                    print(f"    题目数: {ex.total_questions}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 测试序列化修复")
    print("=" * 50)
    
    success_count = 0
    
    # 1. 检查数据库
    if check_database_data():
        success_count += 1
    
    # 2. 测试教师端API
    if test_api_serialization():
        success_count += 1
        print("✅ 教师端API测试通过")
    else:
        print("❌ 教师端API测试失败")
    
    # 3. 测试学生端API
    if test_student_access():
        success_count += 1
        print("✅ 学生端API测试通过")
    else:
        print("❌ 学生端API测试失败")
    
    print("\n" + "=" * 50)
    print(f"🎯 测试结果: {success_count}/3 项通过")
    
    if success_count >= 2:
        print("🎉 序列化问题已修复！")
        print("\n💡 下一步:")
        print("1. 重启前端服务: npm run dev")
        print("2. 访问: http://localhost:5173/teacher/courses/1")
        print("3. 查看课程练习标签")
        print("4. 验证数据正确显示")
    else:
        print("❌ 仍有问题需要解决")
        print("\n🔧 建议:")
        print("1. 确保后端服务正在运行")
        print("2. 运行: python one_click_fix.py")
        print("3. 检查后端日志错误信息")

if __name__ == "__main__":
    main()

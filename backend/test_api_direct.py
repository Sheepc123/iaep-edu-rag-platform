#!/usr/bin/env python3
"""
直接测试API接口
"""

import requests
import json
import time

def test_api_step_by_step():
    """逐步测试API"""
    print("🧪 逐步测试API接口...")
    
    base_url = "http://localhost:8000"
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"健康检查: {response.status_code}")
        if response.status_code != 200:
            print("❌ 服务器未正常运行")
            return False
    except Exception as e:
        print(f"❌ 无法连接服务器: {e}")
        return False
    
    # 2. 测试教师登录
    print("\n2. 测试教师登录...")
    try:
        login_data = {
            "username": "teacher1",
            "password": "123456",
            "remember_me": False
        }
        
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"登录响应: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print(f"✅ 登录成功，Token: {token[:20]}...")
        else:
            print(f"❌ 登录失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return False
    
    # 3. 测试获取课程列表
    print("\n3. 测试获取课程列表...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{base_url}/api/v1/courses/",
            headers=headers
        )
        
        print(f"课程列表响应: {response.status_code}")
        if response.status_code == 200:
            courses_data = response.json()
            courses = courses_data.get('courses', [])
            print(f"✅ 获取到 {len(courses)} 门课程")
            if courses:
                course_id = courses[0]['id']
                print(f"使用课程ID: {course_id}")
            else:
                print("❌ 没有课程数据")
                return False
        else:
            print(f"❌ 获取课程失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 获取课程异常: {e}")
        return False
    
    # 4. 测试获取课程练习 - 关键测试
    print(f"\n4. 测试获取课程 {course_id} 的练习...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/courses/{course_id}/exercises",
            headers=headers
        )
        
        print(f"练习API响应状态: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            exercises_data = response.json()
            print(f"✅ API调用成功")
            print(f"响应数据结构: {type(exercises_data)}")
            print(f"响应内容: {json.dumps(exercises_data, indent=2, ensure_ascii=False)}")
            
            exercises = exercises_data.get('exercises', [])
            print(f"练习数量: {len(exercises)}")
            
            for i, exercise in enumerate(exercises):
                print(f"  {i+1}. {exercise.get('title', 'N/A')} ({exercise.get('category', 'N/A')})")
            
            return True
        else:
            print(f"❌ API调用失败")
            print(f"错误状态码: {response.status_code}")
            print(f"错误响应: {response.text}")
            
            # 尝试解析错误信息
            try:
                error_data = response.json()
                print(f"错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                pass
            
            return False
            
    except Exception as e:
        print(f"❌ 练习API异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_curl():
    """生成curl命令用于手动测试"""
    print("\n🔧 生成curl测试命令...")
    
    print("1. 测试登录:")
    print("""curl -X POST "http://localhost:8000/api/v1/auth/login" \\
     -H "Content-Type: application/json" \\
     -d '{"username": "teacher1", "password": "123456", "remember_me": false}'""")
    
    print("\n2. 测试获取课程练习 (需要替换TOKEN):")
    print("""curl -X GET "http://localhost:8000/api/v1/courses/1/exercises" \\
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \\
     -H "Content-Type: application/json" \\
     -v""")

def check_database_directly():
    """直接检查数据库"""
    print("\n🗄️ 直接检查数据库...")
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise
        from app.models.course import Course
        from app.models.user import User
        
        db = SessionLocal()
        
        # 检查是否有教师用户
        teacher = db.query(User).filter(User.role == "teacher").first()
        if teacher:
            print(f"✅ 找到教师: {teacher.username}")
        else:
            print("❌ 没有找到教师用户")
            return False
        
        # 检查是否有课程
        course = db.query(Course).first()
        if course:
            print(f"✅ 找到课程: {course.title} (ID: {course.id})")
        else:
            print("❌ 没有找到课程")
            return False
        
        # 检查课程是否有练习
        exercises = db.query(Exercise).filter(Exercise.course_id == course.id).all()
        print(f"📚 课程练习数量: {len(exercises)}")
        
        for exercise in exercises:
            print(f"  - {exercise.title} ({exercise.category}, {'已发布' if exercise.is_published else '草稿'})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 直接API测试")
    print("=" * 50)
    
    # 1. 检查数据库
    if not check_database_directly():
        print("❌ 数据库检查失败，请先运行: python quick_exercise_test.py")
        return
    
    # 2. 测试API
    if test_api_step_by_step():
        print("\n✅ API测试成功！")
    else:
        print("\n❌ API测试失败")
        
        # 3. 提供curl命令
        test_with_curl()
        
        print("\n💡 调试建议:")
        print("1. 检查后端日志是否有错误信息")
        print("2. 确认数据库中有练习数据")
        print("3. 使用curl命令手动测试API")
        print("4. 检查CORS配置")

if __name__ == "__main__":
    main()

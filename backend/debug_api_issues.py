#!/usr/bin/env python3
"""
调试API问题脚本
"""

import requests
import json
import sys
import os

def check_server_status():
    """检查服务器状态"""
    print("🔍 检查服务器状态...")
    
    try:
        # 检查健康状态
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("请确保后端服务已启动: python run.py")
        return False

def test_cors_headers():
    """测试CORS头"""
    print("\n🌐 测试CORS配置...")
    
    try:
        response = requests.options("http://localhost:8000/api/v1/courses/1/exercises")
        print(f"OPTIONS请求状态码: {response.status_code}")
        print("响应头:")
        for key, value in response.headers.items():
            if 'cors' in key.lower() or 'access-control' in key.lower():
                print(f"  {key}: {value}")
        
        # 检查是否有CORS头
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods', 
            'Access-Control-Allow-Headers'
        ]
        
        missing_headers = []
        for header in cors_headers:
            if header not in response.headers:
                missing_headers.append(header)
        
        if missing_headers:
            print(f"❌ 缺少CORS头: {missing_headers}")
            return False
        else:
            print("✅ CORS配置正常")
            return True
            
    except Exception as e:
        print(f"❌ CORS测试失败: {e}")
        return False

def test_login_and_get_token():
    """测试登录并获取token"""
    print("\n🔐 测试用户登录...")
    
    try:
        # 教师登录
        login_data = {
            "username": "teacher1",
            "password": "123456",
            "remember_me": False
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ 教师登录成功")
            print(f"Token: {token[:20]}...")
            return token
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        return None

def test_course_exercises_api(token):
    """测试课程练习API"""
    print("\n📚 测试课程练习API...")
    
    if not token:
        print("❌ 没有有效token，跳过API测试")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 测试获取课程练习
        response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        print(f"API响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API调用成功")
            print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
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
            
            # 检查该课程的练习
            exercise_count = db.query(Exercise).filter(Exercise.course_id == course.id).count()
            print(f"课程练习数量: {exercise_count}")
            
            if exercise_count > 0:
                exercises = db.query(Exercise).filter(Exercise.course_id == course.id).all()
                for ex in exercises:
                    print(f"  - {ex.title} ({ex.category}, {'已发布' if ex.is_published else '草稿'})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_api_endpoint_exists():
    """检查API端点是否存在"""
    print("\n🔍 检查API端点...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # 检查路由文件
        from app.api.v1.endpoints.courses import router
        
        # 获取所有路由
        routes = []
        for route in router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append(f"{list(route.methods)[0]} {route.path}")
        
        print("已注册的课程相关路由:")
        for route in routes:
            print(f"  {route}")
        
        # 检查是否有exercises端点
        exercises_routes = [r for r in routes if 'exercises' in r]
        if exercises_routes:
            print("✅ 找到练习相关路由:")
            for route in exercises_routes:
                print(f"  {route}")
            return True
        else:
            print("❌ 没有找到练习相关路由")
            return False
            
    except Exception as e:
        print(f"❌ 检查API端点失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 API问题调试")
    print("=" * 50)
    
    # 1. 检查服务器状态
    if not check_server_status():
        return
    
    # 2. 检查数据库数据
    check_database_data()
    
    # 3. 检查API端点
    check_api_endpoint_exists()
    
    # 4. 测试CORS
    test_cors_headers()
    
    # 5. 测试登录
    token = test_login_and_get_token()
    
    # 6. 测试API
    test_course_exercises_api(token)
    
    print("\n" + "=" * 50)
    print("🎯 调试完成")
    print("\n💡 如果发现问题:")
    print("1. CORS问题 - 检查 app/core/config.py 中的CORS设置")
    print("2. 500错误 - 检查后端日志和数据库连接")
    print("3. 数据问题 - 运行 python quick_exercise_test.py")
    print("4. API端点问题 - 检查路由注册")

if __name__ == "__main__":
    main()

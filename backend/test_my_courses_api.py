"""
测试我的课程API
"""
import requests
import json


def test_my_courses_api():
    """测试我的课程API"""
    base_url = "http://localhost:8000"
    
    # 1. 先登录获取token
    print("=== 登录测试 ===")
    login_url = f"{base_url}/api/v1/auth/login"
    login_data = {
        "username": "student",
        "password": "password"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print(f"登录状态: {response.status_code}")
        
        if response.status_code != 200:
            print(f"登录失败: {response.text}")
            return
        
        token = response.json().get("access_token")
        print("✅ 登录成功")
        
    except Exception as e:
        print(f"❌ 登录请求失败: {str(e)}")
        return
    
    # 2. 测试获取我的课程
    print("\n=== 测试获取我的课程 ===")
    my_courses_url = f"{base_url}/api/v1/courses/my-courses"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(my_courses_url, headers=headers)
        print(f"请求状态: {response.status_code}")
        print(f"响应内容: {response.text[:500]}...")
        
        if response.status_code == 200:
            courses = response.json()
            print(f"✅ 获取成功，共 {len(courses)} 门课程")
            
            for i, course in enumerate(courses, 1):
                print(f"\n课程 {i}:")
                print(f"  注册ID: {course.get('id')}")
                print(f"  课程ID: {course.get('course_id')}")
                print(f"  进度: {course.get('progress_percentage', 0)}%")
                print(f"  注册时间: {course.get('enrolled_at')}")
                
                # 检查是否包含课程详情
                if 'course' in course and course['course']:
                    course_detail = course['course']
                    print(f"  课程标题: {course_detail.get('title')}")
                    print(f"  课程分类: {course_detail.get('category')}")
                    print(f"  难度: {course_detail.get('difficulty')}")
                    print(f"  总课时: {course_detail.get('total_lessons')}")
                else:
                    print("  ⚠️  缺少课程详情")
        else:
            print(f"❌ 获取失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
    
    # 3. 测试注册一门课程（如果还没有注册的话）
    print("\n=== 测试注册课程 ===")
    enroll_url = f"{base_url}/api/v1/courses/1/enroll"
    
    try:
        response = requests.post(enroll_url, headers=headers)
        print(f"注册状态: {response.status_code}")
        
        if response.status_code == 200:
            enrollment = response.json()
            print(f"✅ 注册成功: {enrollment.get('id')}")
        elif response.status_code == 400:
            print("ℹ️  可能已经注册过了")
        else:
            print(f"❌ 注册失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 注册请求失败: {str(e)}")
    
    # 4. 再次测试获取我的课程
    print("\n=== 再次测试获取我的课程 ===")
    try:
        response = requests.get(my_courses_url, headers=headers)
        if response.status_code == 200:
            courses = response.json()
            print(f"✅ 现在共有 {len(courses)} 门课程")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")


def test_database_enrollments():
    """直接查询数据库中的注册记录"""
    print("\n=== 数据库注册记录检查 ===")
    print("请在SQLite中执行以下查询:")
    print("SELECT * FROM course_enrollments;")
    print("SELECT ce.*, c.title, c.category FROM course_enrollments ce LEFT JOIN courses c ON ce.course_id = c.id;")


if __name__ == "__main__":
    print("🔍 开始测试我的课程API...")
    test_my_courses_api()
    test_database_enrollments()
    print("\n✅ 测试完成!")

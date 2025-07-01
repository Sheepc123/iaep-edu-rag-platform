#!/usr/bin/env python3
"""
测试课程API差异
"""

import requests
import json

def test_student_course_api():
    """测试学生端课程API"""
    print("🎓 测试学生端课程API...")
    
    url = "http://localhost:8000/api/v1/courses/"
    params = {
        "is_published": True,
        "limit": 10
    }
    
    try:
        # 先获取学生token
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "username": "student1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print(f"❌ 学生登录失败: {login_response.text}")
            return
        
        student_token = login_response.json()["access_token"]
        
        # 测试课程列表API
        response = requests.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        print(f"学生端API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 学生端API成功")
            print(f"   课程数量: {len(data.get('courses', []))}")
            print(f"   总数: {data.get('total', 0)}")
            
            if data.get('courses'):
                course = data['courses'][0]
                print(f"   示例课程: {course.get('title')}")
                print(f"   教师: {course.get('instructor_name')}")
                print(f"   发布状态: {course.get('is_published')}")
        else:
            print(f"❌ 学生端API失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 学生端API测试失败: {e}")


def test_teacher_course_api():
    """测试教师端课程API"""
    print("\n👨‍🏫 测试教师端课程API...")
    
    url = "http://localhost:8000/api/v1/courses/teacher/courses"
    params = {
        "limit": 10
    }
    
    try:
        # 先获取教师token
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "username": "teacher1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print(f"❌ 教师登录失败: {login_response.text}")
            return
        
        teacher_token = login_response.json()["access_token"]
        
        # 测试教师课程列表API
        response = requests.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        
        print(f"教师端API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 教师端API成功")
            print(f"   课程数量: {len(data) if isinstance(data, list) else 0}")
            
            if data and isinstance(data, list):
                course = data[0]
                print(f"   示例课程: {course.get('title')}")
                print(f"   教师: {course.get('instructor_name')}")
                print(f"   发布状态: {course.get('is_published')}")
                print(f"   课时数: {course.get('total_lessons')}")
        else:
            print(f"❌ 教师端API失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 教师端API测试失败: {e}")


def test_general_course_api():
    """测试通用课程API"""
    print("\n🌐 测试通用课程API...")
    
    url = "http://localhost:8000/api/v1/courses/"
    params = {
        "limit": 10
    }
    
    try:
        # 不带token测试
        response = requests.get(url, params=params)
        
        print(f"通用API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 通用API成功")
            print(f"   课程数量: {len(data.get('courses', []))}")
            print(f"   总数: {data.get('total', 0)}")
        else:
            print(f"❌ 通用API失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 通用API测试失败: {e}")


def compare_api_responses():
    """比较不同API的响应差异"""
    print("\n🔍 比较API响应差异...")
    
    try:
        # 获取tokens
        student_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "student1", "password": "123456", "remember_me": False}
        )
        teacher_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False}
        )
        
        if student_login.status_code != 200 or teacher_login.status_code != 200:
            print("❌ 登录失败，无法比较")
            return
        
        student_token = student_login.json()["access_token"]
        teacher_token = teacher_login.json()["access_token"]
        
        # 学生端API
        student_response = requests.get(
            "http://localhost:8000/api/v1/courses/",
            params={"is_published": True, "limit": 10},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # 教师端API
        teacher_response = requests.get(
            "http://localhost:8000/api/v1/courses/teacher/courses",
            params={"limit": 10},
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        
        print("📊 API响应对比:")
        
        if student_response.status_code == 200:
            student_data = student_response.json()
            student_courses = student_data.get('courses', [])
            print(f"   学生端: {len(student_courses)} 门课程")
            if student_courses:
                print(f"     示例: {student_courses[0].get('title')}")
        
        if teacher_response.status_code == 200:
            teacher_data = teacher_response.json()
            teacher_courses = teacher_data if isinstance(teacher_data, list) else []
            print(f"   教师端: {len(teacher_courses)} 门课程")
            if teacher_courses:
                print(f"     示例: {teacher_courses[0].get('title')}")
        
        # 分析差异
        if student_response.status_code == 200 and teacher_response.status_code == 200:
            student_data = student_response.json()
            teacher_data = teacher_response.json()
            
            student_courses = student_data.get('courses', [])
            teacher_courses = teacher_data if isinstance(teacher_data, list) else []
            
            print("\n🔍 差异分析:")
            print(f"   学生端课程数: {len(student_courses)}")
            print(f"   教师端课程数: {len(teacher_courses)}")
            
            if len(student_courses) != len(teacher_courses):
                print("   ⚠️  课程数量不同 - 这是正常的，因为:")
                print("     - 学生端只显示已发布的课程")
                print("     - 教师端只显示自己创建的课程")
            
            # 检查数据结构
            if student_courses and teacher_courses:
                student_fields = set(student_courses[0].keys())
                teacher_fields = set(teacher_courses[0].keys())
                
                if student_fields == teacher_fields:
                    print("   ✅ 数据结构一致")
                else:
                    print("   ⚠️  数据结构差异:")
                    only_student = student_fields - teacher_fields
                    only_teacher = teacher_fields - student_fields
                    if only_student:
                        print(f"     学生端独有: {only_student}")
                    if only_teacher:
                        print(f"     教师端独有: {only_teacher}")
        
    except Exception as e:
        print(f"❌ 比较失败: {e}")


def main():
    """主函数"""
    print("🚀 课程API测试")
    print("=" * 60)
    
    # 测试各个API
    test_general_course_api()
    test_student_course_api()
    test_teacher_course_api()
    compare_api_responses()
    
    print("\n" + "=" * 60)
    print("📋 测试总结:")
    print("1. 学生端应该调用: /api/v1/courses/ (通用API)")
    print("2. 教师端应该调用: /api/v1/courses/teacher/courses (专用API)")
    print("3. 两个API返回的数据结构应该一致")
    print("4. 但内容可能不同(权限和过滤条件不同)")


if __name__ == "__main__":
    main()

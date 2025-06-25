#!/usr/bin/env python3
"""
测试课程API的简单脚本
"""
import requests
import json

def test_courses_api():
    """测试课程列表API"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 测试课程列表API...")
    
    try:
        # 测试健康检查
        print("1. 测试健康检查...")
        response = requests.get(f"{base_url}/health")
        print(f"   健康检查状态: {response.status_code}")
        if response.status_code == 200:
            print(f"   响应: {response.json()}")
        else:
            print(f"   错误: {response.text}")
            return
        
        # 测试课程列表API
        print("\n2. 测试课程列表API...")
        response = requests.get(f"{base_url}/api/v1/courses/")
        print(f"   API状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   成功! 返回 {data.get('total', 0)} 门课程")
            print(f"   当前页课程数: {len(data.get('courses', []))}")
            
            # 显示前几门课程的信息
            courses = data.get('courses', [])
            if courses:
                print("\n   前3门课程:")
                for i, course in enumerate(courses[:3]):
                    print(f"     {i+1}. {course.get('title', 'N/A')} - {course.get('category', 'N/A')} - {course.get('difficulty', 'N/A')}")
        else:
            print(f"   错误: {response.status_code}")
            print(f"   响应: {response.text}")
        
        # 测试带参数的API调用
        print("\n3. 测试带参数的API调用...")
        params = {
            'is_published': True,
            'limit': 5
        }
        response = requests.get(f"{base_url}/api/v1/courses/", params=params)
        print(f"   带参数API状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   成功! 返回 {len(data.get('courses', []))} 门已发布课程")
        else:
            print(f"   错误: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_courses_api()

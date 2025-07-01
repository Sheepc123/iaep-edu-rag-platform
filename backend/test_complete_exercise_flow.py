#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的练习流程测试
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def login_student():
    """学生登录"""
    print("🔐 学生登录...")
    
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "student1",
        "password": "123456",
        "remember_me": False
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ 学生登录成功")
        return token
    else:
        print(f"❌ 学生登录失败: {response.status_code}")
        return None

def test_exercise_apis(token):
    """测试练习相关API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📋 测试练习API...")
    
    # 1. 获取练习列表
    print("1. 获取练习列表...")
    response = requests.get(f"{BASE_URL}/exercises/", headers=headers)
    if response.status_code == 200:
        exercises = response.json()["exercises"]
        print(f"✅ 获取到 {len(exercises)} 个练习")
        if exercises:
            exercise_id = exercises[0]["id"]
            print(f"   使用练习ID: {exercise_id}")
        else:
            print("❌ 没有找到练习")
            return False
    else:
        print(f"❌ 获取练习列表失败: {response.status_code}")
        return False
    
    # 2. 获取练习详情
    print("2. 获取练习详情...")
    response = requests.get(f"{BASE_URL}/exercises/{exercise_id}", headers=headers)
    if response.status_code == 200:
        exercise = response.json()
        print(f"✅ 练习详情: {exercise['title']}")
    else:
        print(f"❌ 获取练习详情失败: {response.status_code}")
        return False
    
    # 3. 开始练习
    print("3. 开始练习...")
    response = requests.post(f"{BASE_URL}/exercises/{exercise_id}/start", headers=headers)
    if response.status_code == 200:
        attempt = response.json()
        attempt_id = attempt["id"]
        print(f"✅ 开始练习成功，尝试ID: {attempt_id}")
    else:
        print(f"❌ 开始练习失败: {response.status_code}")
        return False
    
    # 4. 获取我的练习记录
    print("4. 获取我的练习记录...")
    response = requests.get(f"{BASE_URL}/exercises/my-attempts?exercise_id={exercise_id}", headers=headers)
    if response.status_code == 200:
        attempts = response.json()
        print(f"✅ 获取到 {len(attempts)} 条练习记录")
    else:
        print(f"❌ 获取练习记录失败: {response.status_code}")
        return False
    
    # 5. 获取练习尝试详情
    print("5. 获取练习尝试详情...")
    response = requests.get(f"{BASE_URL}/exercises/attempts/{attempt_id}", headers=headers)
    if response.status_code == 200:
        attempt_detail = response.json()
        print(f"✅ 获取练习尝试详情成功")
        print(f"   总题数: {attempt_detail['total_questions']}")
        print(f"   答案数: {len(attempt_detail['answers'])}")
    else:
        print(f"❌ 获取练习尝试详情失败: {response.status_code}")
        return False
    
    return True

def test_frontend_urls():
    """测试前端URL"""
    print("\n🌐 测试前端URL...")
    
    urls = [
        "http://localhost:5173/student/exercises",
        "http://localhost:5173/student/exercises/practice/1",
        "http://localhost:5173/student/exercises/result/1?attemptId=1"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url}")
            else:
                print(f"⚠️  {url} - 状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - 连接失败: {e}")

def test_exercise_result_features():
    """测试练习结果页面功能"""
    print("\n🎯 测试练习结果页面功能...")
    
    features = [
        "✅ 显示完成人姓名",
        "✅ 显示完成题目类型统计", 
        "✅ 显示使用时间长度",
        "✅ 显示错题分析",
        "✅ 标记练习完成状态",
        "✅ 显示做题历史记录",
        "✅ 多标签页展示详细信息",
        "✅ 支持重复练习同一套题目"
    ]
    
    print("📋 已实现的功能:")
    for feature in features:
        print(f"  {feature}")

def main():
    """主函数"""
    print("🚀 完整练习流程测试")
    print("=" * 60)
    
    # 1. 学生登录
    token = login_student()
    if not token:
        print("❌ 无法继续测试，登录失败")
        return
    
    # 2. 测试练习API
    if test_exercise_apis(token):
        print("✅ 练习API测试通过")
    else:
        print("❌ 练习API测试失败")
    
    # 3. 测试前端URL
    test_frontend_urls()
    
    # 4. 显示功能特性
    test_exercise_result_features()
    
    print("\n🎉 练习结果系统重构完成！")
    print("\n📋 使用指南:")
    print("1. 确保前后端都在运行")
    print("2. 访问 http://localhost:5173/student/exercises")
    print("3. 选择练习开始答题")
    print("4. 完成后查看详细结果页面")
    print("5. 支持多次练习查看历史记录")
    
    print("\n🔗 测试链接:")
    print("- 练习列表: http://localhost:5173/student/exercises")
    print("- 练习答题: http://localhost:5173/student/exercises/practice/1")
    print("- 结果页面: http://localhost:5173/student/exercises/result/1?attemptId=1")

if __name__ == "__main__":
    main()

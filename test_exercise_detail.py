#!/usr/bin/env python3
"""
测试练习详情API
"""
import requests
import json

# 配置
BASE_URL = "http://127.0.0.1:8000"
TEACHER_USERNAME = "teacher123"
TEACHER_PASSWORD = "123456"
STUDENT_USERNAME = "student001"
STUDENT_PASSWORD = "123456"

def login(username: str, password: str):
    """登录获取token"""
    url = f"{BASE_URL}/api/v1/auth/login"
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["access_token"]
    else:
        print(f"登录失败: {response.text}")
        return None

def get_exercises(token: str):
    """获取练习列表"""
    url = f"{BASE_URL}/api/v1/exercises/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取练习列表失败: {response.text}")
        return None

def get_exercise_detail(exercise_id: int, token: str):
    """获取练习详情"""
    url = f"{BASE_URL}/api/v1/exercises/{exercise_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取练习详情失败: {response.text}")
        return None

def main():
    print("=== 测试练习详情API ===")
    
    # 学生登录
    print("\n1. 学生登录...")
    student_token = login(STUDENT_USERNAME, STUDENT_PASSWORD)
    if not student_token:
        print("学生登录失败，退出测试")
        return
    print("学生登录成功")
    
    # 获取练习列表
    print("\n2. 获取练习列表...")
    exercises = get_exercises(student_token)
    if not exercises:
        print("获取练习列表失败，退出测试")
        return
    
    print(f"找到 {len(exercises)} 个练习")
    
    # 获取第一个练习的详情
    if exercises:
        exercise_id = exercises[0]["id"]
        print(f"\n3. 获取练习详情 (ID: {exercise_id})...")
        
        detail = get_exercise_detail(exercise_id, student_token)
        if detail:
            print(f"练习标题: {detail['title']}")
            print(f"练习科目: {detail['subject']}")
            print(f"练习难度: {detail['difficulty']}")
            print(f"题目数量: {detail['total_questions']}")
            
            if 'questions' in detail:
                print(f"实际题目数量: {len(detail['questions'])}")
                if detail['questions']:
                    first_question = detail['questions'][0]
                    print(f"第一题内容: {first_question.get('content', 'N/A')}")
                    print(f"第一题类型: {first_question.get('question_type', 'N/A')}")
                    print(f"第一题选项: {first_question.get('options', 'N/A')}")
            else:
                print("没有找到题目数据")
        else:
            print("获取练习详情失败")
    else:
        print("没有找到练习")

if __name__ == "__main__":
    main()

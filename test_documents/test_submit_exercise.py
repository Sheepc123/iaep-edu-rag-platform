#!/usr/bin/env python3
"""
测试练习提交功能
"""
import requests
import json

# 配置
BASE_URL = "http://127.0.0.1:8000"
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

def start_exercise(exercise_id: int, token: str):
    """开始练习"""
    url = f"{BASE_URL}/api/v1/exercises/{exercise_id}/start"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"开始练习失败: {response.text}")
        return None

def submit_exercise(attempt_id: int, answers: list, token: str):
    """提交练习"""
    url = f"{BASE_URL}/api/v1/exercises/submit-exercise"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "attempt_id": attempt_id,
        "answers": answers
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"提交练习失败: {response.text}")
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

def get_exercise_attempt(attempt_id: int, token: str):
    """获取练习尝试结果"""
    url = f"{BASE_URL}/api/v1/exercises/attempts/{attempt_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取练习尝试失败: {response.text}")
        return None

def main():
    print("=== 测试练习提交功能 ===")
    
    # 学生登录
    print("\n1. 学生登录...")
    student_token = login(STUDENT_USERNAME, STUDENT_PASSWORD)
    if not student_token:
        print("学生登录失败，退出测试")
        return
    print("学生登录成功")
    
    # 开始练习 (使用练习ID 44)
    exercise_id = 44
    print(f"\n2. 获取练习详情 (ID: {exercise_id})...")
    exercise_detail = get_exercise_detail(exercise_id, student_token)
    if not exercise_detail:
        print("获取练习详情失败，退出测试")
        return

    print(f"练习标题: {exercise_detail['title']}")
    print(f"题目数量: {len(exercise_detail.get('questions', []))}")

    if not exercise_detail.get('questions'):
        print("练习中没有题目，退出测试")
        return

    first_question = exercise_detail['questions'][0]
    question_id = first_question['id']
    print(f"第一题ID: {question_id}")
    print(f"第一题内容: {first_question.get('content', 'N/A')}")

    print(f"\n3. 开始练习...")
    attempt = start_exercise(exercise_id, student_token)
    if not attempt:
        print("开始练习失败，退出测试")
        return

    attempt_id = attempt["id"]
    print(f"练习尝试ID: {attempt_id}")
    print(f"总题目数: {attempt['total_questions']}")

    # 模拟提交答案
    print(f"\n4. 提交答案...")
    answers = [
        {
            "question_id": question_id,  # 使用实际的题目ID
            "answer_content": "123",    # 选择第一个选项
            "time_spent": 30
        }
    ]
    
    submit_result = submit_exercise(attempt_id, answers, student_token)
    if submit_result:
        print("提交成功!")
        print(f"总题目数: {submit_result['total_questions']}")
        print(f"回答题目数: {submit_result['answered_questions']}")
        print(f"正确答案数: {submit_result['correct_answers']}")
        print(f"得分: {submit_result['score']}")
        print(f"准确率: {submit_result['accuracy_rate']}%")
        
        # 获取详细结果
        print(f"\n5. 获取详细结果...")
        detailed_result = get_exercise_attempt(attempt_id, student_token)
        if detailed_result:
            print("获取详细结果成功!")
            print(f"练习标题: {detailed_result['exercise']['title']}")
            print(f"是否完成: {detailed_result['is_completed']}")
            print(f"是否提交: {detailed_result['is_submitted']}")
            if detailed_result['answers']:
                for answer in detailed_result['answers']:
                    print(f"题目 {answer['question_id']}: {answer['answer']} ({'正确' if answer['is_correct'] else '错误'})")
    else:
        print("提交失败")

if __name__ == "__main__":
    main()

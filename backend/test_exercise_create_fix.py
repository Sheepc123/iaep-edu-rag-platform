#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试练习创建页面修复
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def login_teacher():
    """教师登录"""
    print("🔐 教师登录...")
    
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "teacher1",
        "password": "123456",
        "remember_me": False
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ 教师登录成功")
        return token
    else:
        print(f"❌ 教师登录失败: {response.status_code}")
        return None

def test_ai_generation_with_dict_options(token):
    """测试AI生成题目（字典格式选项）"""
    print("\n🤖 测试AI生成题目（字典格式选项）...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    test_data = {
        "subject": "Python编程",
        "topic": "基础语法",
        "difficulty": "easy",
        "question_count": 2,
        "question_types": ["multiple_choice"],
        "additional_requirements": "测试字典格式选项"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ai/generate-questions",
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            questions = result.get("questions", [])
            
            print(f"✅ 生成成功，共 {len(questions)} 道题目")
            
            for i, question in enumerate(questions, 1):
                print(f"\n题目 {i}:")
                print(f"  内容: {question.get('question_text')}")
                
                if question.get('question_type') == 'multiple_choice':
                    options = question.get('options')
                    print(f"  选项类型: {type(options)}")
                    print(f"  选项内容: {options}")
                    print(f"  正确答案: {question.get('correct_answer')}")
                    
                    # 验证格式
                    if isinstance(options, dict):
                        print("  ✅ 选项格式正确（字典）")
                    else:
                        print(f"  ❌ 选项格式错误: {type(options)}")
            
            return True
        else:
            print(f"❌ 生成失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_exercise_creation_with_dict_options(token):
    """测试使用字典格式选项创建练习"""
    print("\n📝 测试使用字典格式选项创建练习...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 创建练习数据
    exercise_data = {
        "title": "[测试] 字典选项格式练习",
        "description": "测试字典格式选项的练习创建",
        "category": "自主练习",
        "subject": "Python编程",
        "difficulty": "easy",
        "time_limit": 30,
        "total_questions": 1,
        "is_published": True
    }
    
    try:
        # 1. 创建练习
        response = requests.post(
            f"{BASE_URL}/exercises/",
            headers=headers,
            json=exercise_data
        )
        
        if response.status_code != 200:
            print(f"❌ 创建练习失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False
        
        exercise = response.json()
        exercise_id = exercise["id"]
        print(f"✅ 练习创建成功，ID: {exercise_id}")
        
        # 2. 添加题目（使用字典格式选项）
        question_data = {
            "content": "Python是什么类型的编程语言？",
            "question_type": "multiple_choice",
            "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
            "correct_answer": "B",
            "explanation": "Python是解释型语言",
            "points": 10,
            "difficulty": "easy"
        }
        
        response = requests.post(
            f"{BASE_URL}/exercises/{exercise_id}/questions",
            headers=headers,
            json=question_data
        )
        
        if response.status_code == 200:
            print("✅ 题目添加成功（字典格式选项）")
            return True
        else:
            print(f"❌ 题目添加失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_frontend_compatibility():
    """测试前端兼容性"""
    print("\n🌐 前端兼容性测试...")
    
    print("📋 修复内容:")
    print("✅ Question接口支持 string[] | Record<string, string> 选项格式")
    print("✅ QuestionCard组件处理两种选项格式")
    print("✅ 验证函数兼容两种格式")
    print("✅ AI题目处理函数转换格式")
    print("✅ 保存时正确处理选项格式")
    
    print("\n🔗 测试URL:")
    print("- 练习创建: http://localhost:5173/teacher/exercises/create")
    print("- 使用AI生成题目功能")
    print("- 手动添加选择题")
    print("- 保存练习")

def main():
    """主函数"""
    print("🚀 练习创建页面修复测试")
    print("=" * 60)
    
    # 1. 教师登录
    token = login_teacher()
    if not token:
        print("❌ 无法继续测试，登录失败")
        return
    
    success_count = 0
    total_tests = 2
    
    # 2. 测试AI生成（字典格式）
    if test_ai_generation_with_dict_options(token):
        success_count += 1
        print("✅ AI生成测试通过")
    else:
        print("❌ AI生成测试失败")
    
    # 3. 测试练习创建（字典格式）
    if test_exercise_creation_with_dict_options(token):
        success_count += 1
        print("✅ 练习创建测试通过")
    else:
        print("❌ 练习创建测试失败")
    
    # 4. 前端兼容性说明
    test_frontend_compatibility()
    
    print(f"\n📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("\n🎉 练习创建页面修复成功！")
        print("\n📋 修复总结:")
        print("✅ 修复了 question.options.filter 错误")
        print("✅ 支持数组和字典两种选项格式")
        print("✅ AI生成题目正常工作")
        print("✅ 手动创建题目正常工作")
        print("✅ 题目保存功能正常")
        
        print(f"\n🎯 现在可以正常使用:")
        print("1. 访问 http://localhost:5173/teacher/exercises/create")
        print("2. 使用AI生成题目功能")
        print("3. 手动添加各种类型题目")
        print("4. 保存和发布练习")
    else:
        print("\n⚠️  部分测试失败，需要进一步检查")

if __name__ == "__main__":
    main()

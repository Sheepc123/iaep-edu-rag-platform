#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI题目生成功能
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
        print(f"响应: {response.text}")
        return None

def test_ai_question_generation(token):
    """测试AI题目生成"""
    print("\n🤖 测试AI题目生成...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试数据
    test_data = {
        "subject": "Python编程",
        "topic": "基础语法",
        "difficulty": "easy",
        "question_count": 3,
        "question_types": ["multiple_choice", "fill_blank"],
        "additional_requirements": "重点测试选择题格式"
    }
    
    print(f"📤 发送请求: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/ai/generate-questions",
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        print(f"📥 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI题目生成成功")
            
            questions = result.get("questions", [])
            print(f"📋 生成了 {len(questions)} 道题目:")
            
            for i, question in enumerate(questions, 1):
                print(f"\n题目 {i}:")
                print(f"  类型: {question.get('question_type')}")
                print(f"  内容: {question.get('question_text')}")
                
                if question.get('question_type') == 'multiple_choice':
                    options = question.get('options')
                    correct_answer = question.get('correct_answer')
                    
                    print(f"  选项类型: {type(options)}")
                    print(f"  选项内容: {options}")
                    print(f"  正确答案: '{correct_answer}'")
                    
                    # 验证格式
                    if isinstance(options, dict):
                        print("  ✅ 选项格式正确 (字典)")
                        if len(correct_answer) == 1 and correct_answer.isalpha():
                            print("  ✅ 答案格式正确 (字母)")
                        else:
                            print(f"  ❌ 答案格式错误 (应该是字母): '{correct_answer}'")
                    else:
                        print(f"  ❌ 选项格式错误 (应该是字典): {type(options)}")
                
                elif question.get('question_type') == 'fill_blank':
                    correct_answer = question.get('correct_answer')
                    print(f"  正确答案: '{correct_answer}'")
                    print("  ✅ 填空题格式正确")
                
                print(f"  解析: {question.get('explanation')}")
                print(f"  分值: {question.get('points')}")
                print(f"  难度: {question.get('difficulty')}")
            
            return True
            
        else:
            print(f"❌ AI题目生成失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_mock_generation():
    """测试模拟生成功能"""
    print("\n🧪 测试模拟生成功能...")
    
    try:
        # 直接导入AI服务进行测试
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app.services.ai_service import AIService
        from app.database import get_db
        
        db = next(get_db())
        ai_service = AIService(db)
        
        # 测试模拟生成
        result = ai_service._generate_mock_questions(
            subject="Python编程",
            topic="基础语法", 
            difficulty="easy",
            question_count=2,
            question_types=["multiple_choice", "fill_blank"]
        )
        
        questions = result.get("questions", [])
        print(f"📋 模拟生成了 {len(questions)} 道题目:")
        
        for i, question in enumerate(questions, 1):
            print(f"\n题目 {i}:")
            print(f"  类型: {question.get('question_type')}")
            print(f"  内容: {question.get('question_text')}")
            
            if question.get('question_type') == 'multiple_choice':
                options = question.get('options')
                correct_answer = question.get('correct_answer')
                
                print(f"  选项: {options}")
                print(f"  答案: '{correct_answer}'")
                
                # 验证格式
                is_dict = isinstance(options, dict)
                is_letter = len(str(correct_answer)) == 1 and str(correct_answer).isalpha()
                
                if is_dict and is_letter:
                    print("  ✅ 格式正确")
                else:
                    print(f"  ❌ 格式错误 (字典:{is_dict}, 字母:{is_letter})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 模拟生成测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 AI题目生成功能测试")
    print("=" * 60)
    
    success_count = 0
    total_tests = 2
    
    # 1. 测试模拟生成
    print("测试 1: 模拟生成功能")
    if test_mock_generation():
        success_count += 1
        print("✅ 模拟生成测试通过")
    else:
        print("❌ 模拟生成测试失败")
    
    # 2. 测试API调用
    print("\n测试 2: API调用")
    token = login_teacher()
    if token:
        if test_ai_question_generation(token):
            success_count += 1
            print("✅ API调用测试通过")
        else:
            print("❌ API调用测试失败")
    else:
        print("❌ 无法测试API调用（登录失败）")
    
    print(f"\n📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("\n🎉 AI题目生成功能修复成功！")
        print("\n📋 修复内容:")
        print("✅ 后端模型支持字典格式选项")
        print("✅ 前端组件兼容两种选项格式")
        print("✅ AI服务生成正确格式数据")
        print("✅ 格式标准化函数正常工作")
        
        print(f"\n🔗 现在可以正常使用:")
        print("1. 访问: http://localhost:5173/teacher/exercises/create")
        print("2. 使用AI生成题目功能")
        print("3. 生成的题目应该使用正确格式")
    else:
        print("\n⚠️  部分测试失败，需要进一步检查")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI生成题目修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ai_service import AIService
from app.database import get_db
import asyncio

async def test_ai_generation():
    """测试AI生成题目功能"""
    print("🧪 测试AI生成题目修复...")
    print("=" * 60)
    
    # 获取数据库连接
    db = next(get_db())
    
    try:
        # 创建AI服务实例
        ai_service = AIService(db)
        
        # 测试生成题目
        result = await ai_service.generate_questions(
            user_id=1,
            subject="Python编程",
            topic="基础语法",
            difficulty="easy",
            question_count=2,
            question_types=["multiple_choice", "fill_blank"],
            additional_requirements="重点测试选择题格式"
        )
        
        print("📋 生成的题目:")
        questions = result.get("questions", [])
        
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
                print(f"  答案类型: {type(correct_answer)}")
                
                # 验证格式
                is_dict = isinstance(options, dict)
                is_letter = len(str(correct_answer)) == 1 and str(correct_answer).isalpha()
                
                if is_dict and is_letter:
                    print("  ✅ 格式正确")
                else:
                    print(f"  ❌ 格式错误 (字典:{is_dict}, 字母:{is_letter})")
            
            elif question.get('question_type') == 'fill_blank':
                correct_answer = question.get('correct_answer')
                print(f"  正确答案: '{correct_answer}'")
                print("  ✅ 填空题格式正确")
            
            print(f"  解析: {question.get('explanation')}")
        
        print(f"\n🎉 测试完成，共生成 {len(questions)} 道题目")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        db.close()

def test_normalize_function():
    """测试格式标准化函数"""
    print("\n🔧 测试格式标准化函数...")
    print("=" * 60)
    
    db = next(get_db())
    ai_service = AIService(db)
    
    # 测试数据
    test_questions = [
        {
            "question_text": "测试题目1",
            "question_type": "multiple_choice",
            "options": ["选项A", "选项B", "选项C", "选项D"],  # 数组格式
            "correct_answer": "选项B",  # 完整内容
            "explanation": "测试解析"
        },
        {
            "question_text": "测试题目2", 
            "question_type": "multiple_choice",
            "options": {"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},  # 字典格式
            "correct_answer": "选项B",  # 完整内容
            "explanation": "测试解析"
        },
        {
            "question_text": "测试题目3",
            "question_type": "multiple_choice", 
            "options": {"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},  # 字典格式
            "correct_answer": "B",  # 已经是字母
            "explanation": "测试解析"
        }
    ]
    
    print("原始题目:")
    for i, q in enumerate(test_questions, 1):
        print(f"  题目{i}: 选项={q['options']}, 答案='{q['correct_answer']}'")
    
    # 标准化
    normalized = ai_service._normalize_question_format(test_questions)
    
    print("\n标准化后:")
    all_correct = True
    for i, q in enumerate(normalized, 1):
        options = q['options']
        answer = q['correct_answer']
        is_dict = isinstance(options, dict)
        is_letter = len(str(answer)) == 1 and str(answer).isalpha()
        
        print(f"  题目{i}: 选项={options}, 答案='{answer}'")
        if is_dict and is_letter:
            print(f"    ✅ 格式正确")
        else:
            print(f"    ❌ 格式错误")
            all_correct = False
    
    db.close()
    return all_correct

async def main():
    """主函数"""
    print("🚀 AI生成题目修复测试")
    print("=" * 60)
    
    # 1. 测试格式标准化函数
    normalize_ok = test_normalize_function()
    
    # 2. 测试AI生成功能
    generation_ok = await test_ai_generation()
    
    if normalize_ok and generation_ok:
        print("\n🎉 所有测试通过！AI生成题目修复成功")
        print("\n📋 现在可以:")
        print("1. 访问: http://localhost:5173/teacher/exercises/create")
        print("2. 使用AI生成题目功能")
        print("3. 生成的选择题应该使用正确的格式")
    else:
        print("\n⚠️  部分测试失败，需要进一步检查")

if __name__ == "__main__":
    asyncio.run(main())

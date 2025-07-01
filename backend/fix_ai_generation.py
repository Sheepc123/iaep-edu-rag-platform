#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复AI生成题目的格式问题
"""

import sqlite3
import json
import os

# 数据库路径
DB_PATH = r"D:\project\softwareCup\backend\data\database\education_platform.db"

def fix_ai_generated_questions():
    """修复AI生成的题目格式"""
    print("🔧 修复AI生成的题目格式...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 查找所有选择题
        cursor.execute("""
            SELECT id, content, options, correct_answer 
            FROM questions 
            WHERE question_type = 'multiple_choice'
        """)
        
        questions = cursor.fetchall()
        fixed_count = 0
        
        for question_id, content, options_str, correct_answer in questions:
            print(f"\n处理题目{question_id}: {content[:30]}...")
            
            # 解析选项
            try:
                if options_str.startswith('['):
                    # 数组格式，需要转换为字典
                    options_list = json.loads(options_str)
                    if isinstance(options_list, list):
                        # 转换为字典格式
                        options_dict = {}
                        for i, option in enumerate(options_list):
                            letter = chr(65 + i)  # A, B, C, D
                            options_dict[letter] = option
                        
                        # 找到正确答案对应的字母
                        new_correct_answer = None
                        for letter, option_text in options_dict.items():
                            if option_text == correct_answer:
                                new_correct_answer = letter
                                break
                        
                        if new_correct_answer:
                            # 更新数据库
                            cursor.execute("""
                                UPDATE questions 
                                SET options = ?, correct_answer = ?
                                WHERE id = ?
                            """, (json.dumps(options_dict), new_correct_answer, question_id))
                            
                            print(f"  ✅ 修复成功: {correct_answer} -> {new_correct_answer}")
                            fixed_count += 1
                        else:
                            print(f"  ❌ 找不到匹配的答案: {correct_answer}")
                    else:
                        print(f"  ⚠️  选项不是数组格式")
                elif options_str.startswith('{'):
                    # 已经是字典格式
                    options_dict = json.loads(options_str)
                    if isinstance(options_dict, dict):
                        # 检查答案格式
                        if len(correct_answer) == 1 and correct_answer.isalpha():
                            print(f"  ✅ 格式已正确")
                        else:
                            # 查找正确答案对应的字母
                            new_correct_answer = None
                            for letter, option_text in options_dict.items():
                                if option_text == correct_answer:
                                    new_correct_answer = letter
                                    break
                            
                            if new_correct_answer:
                                cursor.execute("""
                                    UPDATE questions 
                                    SET correct_answer = ?
                                    WHERE id = ?
                                """, (new_correct_answer, question_id))
                                
                                print(f"  ✅ 修复答案: {correct_answer} -> {new_correct_answer}")
                                fixed_count += 1
                            else:
                                print(f"  ❌ 找不到匹配的答案: {correct_answer}")
                    else:
                        print(f"  ❌ 选项不是字典格式")
                else:
                    print(f"  ❌ 无法识别选项格式: {options_str[:50]}...")
                    
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON解析失败: {e}")
            except Exception as e:
                print(f"  ❌ 处理失败: {e}")
        
        # 提交更改
        conn.commit()
        print(f"\n✅ 修复完成，共修复 {fixed_count} 道题目")
        
        # 验证结果
        print("\n🔍 验证修复结果...")
        cursor.execute("""
            SELECT id, options, correct_answer 
            FROM questions 
            WHERE question_type = 'multiple_choice'
            ORDER BY id
        """)
        
        all_correct = True
        for question_id, options_str, correct_answer in cursor.fetchall():
            try:
                options = json.loads(options_str)
                is_dict = isinstance(options, dict)
                is_letter = len(correct_answer) == 1 and correct_answer.isalpha()
                
                if is_dict and is_letter:
                    print(f"✅ 题目{question_id}: 格式正确")
                else:
                    print(f"❌ 题目{question_id}: 格式错误 (字典:{is_dict}, 字母:{is_letter})")
                    all_correct = False
            except:
                print(f"❌ 题目{question_id}: JSON解析失败")
                all_correct = False
        
        return all_correct
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 修复过程失败: {e}")
        return False
    finally:
        conn.close()

def create_standard_test_questions():
    """创建标准格式的测试题目"""
    print("\n🧪 创建标准格式的测试题目...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 测试题目数据
        test_questions = [
            {
                "title": "Python基础测试1",
                "content": "Python是什么类型的编程语言？",
                "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                "correct_answer": "B",
                "explanation": "Python是一种解释型的高级编程语言"
            },
            {
                "title": "Python基础测试2", 
                "content": "以下哪个是Python的特点？",
                "options": {"A": "语法复杂", "B": "语法简洁", "C": "运行速度快", "D": "内存占用小"},
                "correct_answer": "B",
                "explanation": "Python以语法简洁著称"
            }
        ]
        
        created_count = 0
        for i, q in enumerate(test_questions):
            # 检查是否已存在
            cursor.execute("SELECT id FROM questions WHERE content = ?", (q["content"],))
            if cursor.fetchone():
                print(f"  题目已存在，跳过: {q['content'][:30]}...")
                continue
            
            # 插入新题目
            cursor.execute("""
                INSERT INTO questions (
                    exercise_id, title, content, question_type,
                    options, correct_answer, explanation,
                    difficulty, points
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                1,  # 练习ID
                q["title"],
                q["content"],
                "multiple_choice",
                json.dumps(q["options"]),
                q["correct_answer"],
                q["explanation"],
                "easy",
                10
            ))
            
            created_count += 1
            print(f"  ✅ 创建题目: {q['content'][:30]}...")
        
        conn.commit()
        print(f"✅ 创建了 {created_count} 道标准格式的测试题目")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 创建测试题目失败: {e}")
    finally:
        conn.close()

def main():
    print("🚀 修复AI生成题目格式问题")
    print("=" * 60)
    
    # 1. 修复现有题目
    success = fix_ai_generated_questions()
    
    # 2. 创建标准测试题目
    create_standard_test_questions()
    
    if success:
        print("\n🎉 所有题目格式修复完成！")
        print("\n📋 现在可以测试:")
        print("1. 访问: http://localhost:5173/student/exercises/practice/1")
        print("2. 选择任意答案并提交")
        print("3. 查看答案显示是否正确")
        print("\n💡 AI生成题目的问题已修复，新生成的题目应该使用正确格式")
    else:
        print("\n⚠️  部分题目仍需手动检查")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选择题答案逻辑修复脚本

问题：选择题的正确答案应该是选项字母（A、B、C、D），
但数据库中存储的可能是完整的选项内容。

解决方案：
1. 检查现有数据格式
2. 修复数据库中的答案格式
3. 验证修复结果
"""

import sqlite3
import json
import os
import sys

# 数据库路径
DB_PATH = r"D:\project\softwareCup\backend\data\database\education_platform.db"

def get_connection():
    """获取数据库连接"""
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        return None
    return sqlite3.connect(DB_PATH)

def analyze_question_data():
    """分析题目数据格式"""
    print("🔍 分析选择题数据格式...")
    print("=" * 60)

    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # 获取所有选择题
        cursor.execute("""
            SELECT id, content, options, correct_answer
            FROM questions
            WHERE question_type = 'multiple_choice'
        """)

        questions = cursor.fetchall()
        print(f"📊 找到 {len(questions)} 道选择题")

        for question_id, content, options_str, correct_answer in questions:
            print(f"\n题目ID: {question_id}")
            print(f"内容: {content[:50]}...")
            print(f"正确答案: '{correct_answer}'")

            # 解析选项
            options = None
            if options_str:
                try:
                    options = json.loads(options_str)
                    print(f"选项类型: {type(options)}")
                    print(f"选项内容: {options}")
                except json.JSONDecodeError:
                    print(f"❌ 选项JSON解析失败: {options_str}")
                    continue

            # 分析选项格式
            if options:
                if isinstance(options, dict):
                    print("✅ 选项格式: 字典 (正确)")
                    for key, value in options.items():
                        is_correct = key == correct_answer
                        print(f"  {key}: {value} {'✓' if is_correct else ''}")
                elif isinstance(options, list):
                    print("⚠️  选项格式: 列表")
                    for i, option in enumerate(options):
                        letter = chr(65 + i)  # A, B, C, D
                        is_correct = option == correct_answer or letter == correct_answer
                        print(f"  {letter}: {option} {'✓' if is_correct else ''}")
                else:
                    print(f"❌ 未知选项格式: {type(options)}")

            # 检查答案格式
            if len(correct_answer) == 1 and correct_answer.isalpha():
                print("✅ 答案格式: 字母 (正确)")
            else:
                print("❌ 答案格式: 非字母 (需要修复)")

            print("-" * 40)

    finally:
        conn.close()

def fix_answer_format():
    """修复答案格式"""
    print("\n🔧 修复选择题答案格式...")
    print("=" * 60)

    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # 获取需要修复的选择题
        cursor.execute("""
            SELECT id, options, correct_answer
            FROM questions
            WHERE question_type = 'multiple_choice'
        """)

        questions = cursor.fetchall()
        fixed_count = 0

        for question_id, options_str, correct_answer in questions:
            print(f"\n处理题目ID: {question_id}")
            print(f"当前答案: '{correct_answer}'")

            # 如果答案已经是单个字母，跳过
            if len(correct_answer) == 1 and correct_answer.isalpha():
                print("✅ 答案格式已正确，跳过")
                continue

            # 解析选项
            options = None
            if options_str:
                try:
                    options = json.loads(options_str)
                except json.JSONDecodeError:
                    print(f"❌ 选项JSON解析失败，跳过")
                    continue

            # 尝试修复答案格式
            new_answer = None

            if options:
                if isinstance(options, dict):
                    # 字典格式：查找匹配的键
                    for key, value in options.items():
                        if value == correct_answer:
                            new_answer = key
                            break
                elif isinstance(options, list):
                    # 列表格式：查找匹配的索引
                    for i, option in enumerate(options):
                        if option == correct_answer:
                            new_answer = chr(65 + i)  # A, B, C, D
                            break

            if new_answer:
                print(f"🔄 修复答案: '{correct_answer}' -> '{new_answer}'")
                cursor.execute("""
                    UPDATE questions
                    SET correct_answer = ?
                    WHERE id = ?
                """, (new_answer, question_id))
                fixed_count += 1
            else:
                print(f"❌ 无法修复答案: {correct_answer}")

        if fixed_count > 0:
            conn.commit()
            print(f"\n✅ 成功修复 {fixed_count} 道题目的答案格式")
        else:
            print("\n✅ 所有题目答案格式都正确，无需修复")

    except Exception as e:
        conn.rollback()
        print(f"❌ 修复过程中出错: {e}")
    finally:
        conn.close()

def verify_fix():
    """验证修复结果"""
    print("\n✅ 验证修复结果...")
    print("=" * 60)

    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, correct_answer
            FROM questions
            WHERE question_type = 'multiple_choice'
        """)

        questions = cursor.fetchall()
        correct_count = 0
        total_count = len(questions)

        for question_id, correct_answer in questions:
            is_correct_format = (
                len(correct_answer) == 1 and
                correct_answer.isalpha()
            )

            if is_correct_format:
                correct_count += 1
                print(f"✅ 题目{question_id}: 答案'{correct_answer}' - 格式正确")
            else:
                print(f"❌ 题目{question_id}: 答案'{correct_answer}' - 格式错误")

        print(f"\n📊 验证结果: {correct_count}/{total_count} 题目答案格式正确")

        if correct_count == total_count:
            print("🎉 所有选择题答案格式都正确！")
            return True
        else:
            print("⚠️  仍有题目需要手动修复")
            return False

    finally:
        conn.close()

def create_test_question():
    """创建测试题目"""
    print("\n🧪 创建测试题目...")
    print("=" * 60)

    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        # 检查是否已存在测试题目
        cursor.execute("""
            SELECT id FROM questions
            WHERE content LIKE '%测试选择题%'
        """)
        existing = cursor.fetchone()

        if existing:
            print("✅ 测试题目已存在，跳过创建")
            return existing[0]

        # 创建新的测试题目
        options_json = json.dumps({"A": "编译型语言", "B": "解释型语言", "C": "汇编语言", "D": "机器语言"})

        cursor.execute("""
            INSERT INTO questions (
                exercise_id, title, content, question_type,
                options, correct_answer, explanation,
                difficulty, points
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1,  # 假设练习ID为1
            "测试选择题",
            "以下哪个是Python的特点？",
            "multiple_choice",
            options_json,
            "B",  # 正确的字母格式
            "Python是一种解释型的高级编程语言",
            "easy",
            10
        ))

        conn.commit()
        test_id = cursor.lastrowid

        print(f"✅ 创建测试题目成功，ID: {test_id}")
        return test_id

    except Exception as e:
        conn.rollback()
        print(f"❌ 创建测试题目失败: {e}")
        return None
    finally:
        conn.close()

def main():
    """主函数"""
    print("🚀 选择题答案逻辑修复脚本")
    print("=" * 60)
    
    try:
        # 1. 分析现有数据
        analyze_question_data()
        
        # 2. 修复答案格式
        fix_answer_format()
        
        # 3. 验证修复结果
        is_fixed = verify_fix()
        
        # 4. 创建测试题目
        test_id = create_test_question()
        
        print("\n🎯 修复完成！")
        print("=" * 60)
        print("📋 后续步骤:")
        print("1. 重启前端服务")
        print("2. 访问: http://localhost:5173/student/exercises/practice/1")
        print("3. 选择答案B（解释型语言）")
        print("4. 提交答案查看结果")
        
        if test_id:
            print(f"5. 测试题目ID: {test_id}")
        
        return is_fixed
        
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

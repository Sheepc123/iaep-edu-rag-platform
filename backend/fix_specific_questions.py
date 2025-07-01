#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复特定题目的选项和答案格式
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

def fix_question_9():
    """修复题目9"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # 题目9的正确格式
        options = {
            "A": "引用必须在声明时初始化",
            "B": "引用可以在声明后初始化", 
            "C": "引用可以指向NULL",
            "D": "引用可以改变指向的对象"
        }
        correct_answer = "A"  # 第一个选项是正确的
        
        cursor.execute("""
            UPDATE questions 
            SET options = ?, correct_answer = ?
            WHERE id = 9
        """, (json.dumps(options), correct_answer))
        
        print("✅ 修复题目9成功")
        return True
        
    except Exception as e:
        print(f"❌ 修复题目9失败: {e}")
        return False
    finally:
        conn.close()

def fix_question_10():
    """修复题目10"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # 题目10的正确格式
        options = {
            "A": "static",
            "B": "const",
            "C": "new",
            "D": "auto"
        }
        correct_answer = "C"  # new是正确答案
        
        cursor.execute("""
            UPDATE questions 
            SET options = ?, correct_answer = ?
            WHERE id = 10
        """, (json.dumps(options), correct_answer))
        
        print("✅ 修复题目10成功")
        return True
        
    except Exception as e:
        print(f"❌ 修复题目10失败: {e}")
        return False
    finally:
        conn.close()

def fix_question_11():
    """修复题目11"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # 题目11的正确格式
        options = {
            "A": "5",
            "B": "10",
            "C": "编译错误",
            "D": "运行时错误"
        }
        correct_answer = "B"  # 10是正确答案
        
        cursor.execute("""
            UPDATE questions 
            SET options = ?, correct_answer = ?
            WHERE id = 11
        """, (json.dumps(options), correct_answer))
        
        print("✅ 修复题目11成功")
        return True
        
    except Exception as e:
        print(f"❌ 修复题目11失败: {e}")
        return False
    finally:
        conn.close()

def verify_all_questions():
    """验证所有题目"""
    print("\n🔍 验证所有选择题...")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, content, options, correct_answer 
            FROM questions 
            WHERE question_type = 'multiple_choice'
            ORDER BY id
        """)
        
        questions = cursor.fetchall()
        all_correct = True
        
        for question_id, content, options_str, correct_answer in questions:
            print(f"\n题目ID: {question_id}")
            print(f"内容: {content[:50]}...")
            
            # 检查选项格式
            try:
                options = json.loads(options_str)
                if isinstance(options, dict):
                    print("✅ 选项格式: 字典 (正确)")
                    for key, value in options.items():
                        is_correct = key == correct_answer
                        print(f"  {key}: {value} {'✓' if is_correct else ''}")
                else:
                    print("❌ 选项格式: 非字典")
                    all_correct = False
            except:
                print("❌ 选项JSON解析失败")
                all_correct = False
            
            # 检查答案格式
            if len(correct_answer) == 1 and correct_answer.isalpha():
                print(f"✅ 答案格式: '{correct_answer}' (正确)")
            else:
                print(f"❌ 答案格式: '{correct_answer}' (错误)")
                all_correct = False
            
            print("-" * 40)
        
        return all_correct
        
    finally:
        conn.close()

def main():
    """主函数"""
    print("🔧 修复特定题目的选项和答案格式")
    print("=" * 60)
    
    success_count = 0
    
    # 修复题目9
    if fix_question_9():
        success_count += 1
    
    # 修复题目10  
    if fix_question_10():
        success_count += 1
    
    # 修复题目11
    if fix_question_11():
        success_count += 1
    
    # 提交所有更改
    conn = get_connection()
    if conn:
        try:
            conn.commit()
            print(f"\n✅ 成功修复 {success_count} 道题目")
        except Exception as e:
            conn.rollback()
            print(f"❌ 提交更改失败: {e}")
        finally:
            conn.close()
    
    # 验证所有题目
    all_correct = verify_all_questions()
    
    if all_correct:
        print("\n🎉 所有选择题格式都正确！")
        print("\n📋 现在可以测试前端:")
        print("1. 访问: http://localhost:5173/student/exercises/practice/1")
        print("2. 选择任意答案并提交")
        print("3. 查看是否正确显示答案结果")
    else:
        print("\n⚠️  仍有题目需要手动检查")
    
    return all_correct

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

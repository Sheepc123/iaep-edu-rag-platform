#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查现有练习数据 - 不修改数据库
"""

import sqlite3
import json
from datetime import datetime

# 数据库路径
DB_PATH = r"D:\project\softwareCup\backend\data\database\education_platform.db"

def check_database_structure():
    """检查数据库结构"""
    print("🔍 检查数据库结构...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查表是否存在
        tables = ['exercises', 'questions', 'exercise_attempts', 'student_answers', 'users']
        
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ {table}: {count} 条记录")
            else:
                print(f"❌ {table}: 表不存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False
    finally:
        conn.close()

def check_existing_exercises():
    """检查现有练习数据"""
    print("\n📚 检查现有练习...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 查看练习列表
        cursor.execute("""
            SELECT e.id, e.title, e.category, e.subject, e.total_questions, 
                   e.is_published, COUNT(ea.id) as attempt_count
            FROM exercises e
            LEFT JOIN exercise_attempts ea ON e.id = ea.exercise_id
            GROUP BY e.id
            ORDER BY e.id
        """)
        
        exercises = cursor.fetchall()
        
        if not exercises:
            print("❌ 没有找到练习数据")
            return None
        
        print(f"找到 {len(exercises)} 个练习:")
        for ex in exercises:
            status = "已发布" if ex[5] else "未发布"
            print(f"  ID:{ex[0]} - {ex[1]} ({ex[2]}/{ex[3]}) - {ex[4]}题 - {status} - {ex[6]}次尝试")
        
        return exercises[0][0]  # 返回第一个练习ID
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None
    finally:
        conn.close()

def check_exercise_attempts(exercise_id):
    """检查练习尝试记录"""
    print(f"\n🎯 检查练习 {exercise_id} 的尝试记录...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT ea.id, ea.student_id, ea.total_questions, ea.correct_answers, 
                   ea.score, ea.time_spent, ea.is_completed, ea.submitted_at,
                   u.username
            FROM exercise_attempts ea
            LEFT JOIN users u ON ea.student_id = u.id
            WHERE ea.exercise_id = ?
            ORDER BY ea.id DESC
        """, (exercise_id,))
        
        attempts = cursor.fetchall()
        
        if not attempts:
            print("❌ 没有找到练习尝试记录")
            return None
        
        print(f"找到 {len(attempts)} 条尝试记录:")
        for att in attempts:
            completed = "已完成" if att[6] else "未完成"
            username = att[8] or f"用户{att[1]}"
            print(f"  尝试ID:{att[0]} - {username} - {att[3]}/{att[2]}题正确 - {att[4]}分 - {att[5]}秒 - {completed}")
        
        return attempts[0][0]  # 返回最新的尝试ID
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None
    finally:
        conn.close()

def check_student_answers(attempt_id):
    """检查学生答案"""
    print(f"\n📝 检查尝试 {attempt_id} 的答案记录...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT sa.id, sa.question_id, sa.answer_content, sa.is_correct, 
                   sa.points_earned, q.content, q.correct_answer, q.question_type
            FROM student_answers sa
            JOIN questions q ON sa.question_id = q.id
            WHERE sa.attempt_id = ?
            ORDER BY sa.question_id
        """, (attempt_id,))
        
        answers = cursor.fetchall()
        
        if not answers:
            print("❌ 没有找到答案记录")
            return False
        
        print(f"找到 {len(answers)} 条答案记录:")
        for ans in answers:
            status = "✅" if ans[3] else "❌"
            print(f"  {status} 题目{ans[1]}: 学生答案='{ans[2]}' 正确答案='{ans[6]}' 得分={ans[4]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False
    finally:
        conn.close()

def suggest_test_urls(exercise_id, attempt_id):
    """建议测试URL"""
    print(f"\n🔗 可以测试的URL:")
    print(f"  练习列表: http://localhost:5173/student/exercises")
    print(f"  练习详情: http://localhost:5173/student/exercises/practice/{exercise_id}")
    if attempt_id:
        print(f"  结果页面: http://localhost:5173/student/exercises/result/{exercise_id}?attemptId={attempt_id}")

def check_users():
    """检查用户数据"""
    print("\n👥 检查用户数据...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        user_stats = cursor.fetchall()
        
        print("用户统计:")
        for role, count in user_stats:
            print(f"  {role}: {count} 人")
        
        # 检查是否有学生和教师
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher'")
        teacher_count = cursor.fetchone()[0]
        
        if student_count == 0:
            print("⚠️  警告: 没有学生用户")
        if teacher_count == 0:
            print("⚠️  警告: 没有教师用户")
        
        return student_count > 0 and teacher_count > 0
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False
    finally:
        conn.close()

def main():
    """主函数"""
    print("🔍 检查现有练习数据")
    print("=" * 60)
    print("✅ 此脚本只读取数据，不会修改数据库")
    
    # 1. 检查数据库结构
    if not check_database_structure():
        print("❌ 数据库结构检查失败")
        return
    
    # 2. 检查用户数据
    if not check_users():
        print("⚠️  用户数据不完整，可能影响测试")
    
    # 3. 检查现有练习
    exercise_id = check_existing_exercises()
    if not exercise_id:
        print("\n💡 建议:")
        print("1. 先通过教师端创建一些练习")
        print("2. 或者运行 safe_test_exercise_data.py 创建测试数据")
        return
    
    # 4. 检查练习尝试
    attempt_id = check_exercise_attempts(exercise_id)
    if not attempt_id:
        print("\n💡 建议:")
        print("1. 先通过学生端完成一些练习")
        print("2. 或者运行 safe_test_exercise_data.py 创建测试数据")
    else:
        # 5. 检查学生答案
        check_student_answers(attempt_id)
    
    # 6. 建议测试URL
    suggest_test_urls(exercise_id, attempt_id)
    
    print(f"\n🎯 测试建议:")
    if attempt_id:
        print("✅ 数据完整，可以直接测试练习结果页面")
        print("✅ 重构的功能应该能正常工作")
    else:
        print("⚠️  缺少练习尝试数据，建议先完成一些练习")
    
    print(f"\n📋 重构功能清单:")
    features = [
        "✅ 多标签页展示（结果/错题/历史/详情）",
        "✅ 显示完成人姓名和基本信息", 
        "✅ 显示题目类型统计",
        "✅ 显示使用时间长度",
        "✅ 错题分析和解析",
        "✅ 练习历史记录",
        "✅ 练习完成状态标记"
    ]
    
    for feature in features:
        print(f"  {feature}")

if __name__ == "__main__":
    main()

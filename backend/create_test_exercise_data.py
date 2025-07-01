#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试练习数据
"""

import sqlite3
import json
from datetime import datetime

# 数据库路径
DB_PATH = r"D:\project\softwareCup\backend\data\database\education_platform.db"

def create_test_data():
    """创建完整的测试数据"""
    print("🧪 创建测试练习数据...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        now = datetime.now().isoformat()
        
        # 1. 检查是否有用户数据
        cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 1")
        student = cursor.fetchone()
        if not student:
            print("❌ 没有找到学生用户，请先创建用户")
            return False
        student_id = student[0]
        
        cursor.execute("SELECT id FROM users WHERE role = 'teacher' LIMIT 1")
        teacher = cursor.fetchone()
        if not teacher:
            print("❌ 没有找到教师用户，请先创建用户")
            return False
        teacher_id = teacher[0]
        
        # 2. 创建测试练习
        cursor.execute("""
            INSERT OR REPLACE INTO exercises (
                id, title, description, category, subject, difficulty, 
                time_limit, created_by, total_questions, is_active, is_published, 
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1, "Python基础测试", "测试Python基础语法和概念", "practice", 
            "Python编程", "easy", 30, teacher_id, 3, True, True, now, now
        ))
        
        print("✅ 创建测试练习成功")
        
        # 3. 创建测试题目
        questions_data = [
            {
                "id": 12,
                "title": "Python语言类型",
                "content": "Python是什么类型的编程语言？",
                "question_type": "multiple_choice",
                "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                "correct_answer": "B",
                "explanation": "Python是一种解释型的高级编程语言",
                "points": 10
            },
            {
                "id": 13,
                "title": "Python特点",
                "content": "以下哪个是Python的特点？",
                "question_type": "multiple_choice", 
                "options": {"A": "语法复杂", "B": "语法简洁", "C": "运行很快", "D": "内存很小"},
                "correct_answer": "B",
                "explanation": "Python以语法简洁著称",
                "points": 10
            },
            {
                "id": 14,
                "title": "Python变量",
                "content": "在Python中，变量名可以以什么开头？",
                "question_type": "multiple_choice",
                "options": {"A": "数字", "B": "字母或下划线", "C": "特殊符号", "D": "空格"},
                "correct_answer": "B", 
                "explanation": "Python变量名必须以字母或下划线开头",
                "points": 10
            }
        ]
        
        for q in questions_data:
            cursor.execute("""
                INSERT OR REPLACE INTO questions (
                    id, exercise_id, title, content, question_type, options, 
                    correct_answer, explanation, difficulty, points, 
                    is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q["id"], 1, q["title"], q["content"], q["question_type"],
                json.dumps(q["options"]), q["correct_answer"], q["explanation"],
                "easy", q["points"], True, now, now
            ))
        
        print("✅ 创建测试题目成功")
        
        # 4. 创建练习尝试
        cursor.execute("""
            INSERT OR REPLACE INTO exercise_attempts (
                id, exercise_id, student_id, total_questions, answered_questions,
                correct_answers, score, max_score, time_spent, is_completed, 
                is_submitted, started_at, completed_at, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1, 1, student_id, 3, 3, 2, 66.67, 100, 300,
            True, True, now, now, now
        ))
        
        print("✅ 创建练习尝试成功")
        
        # 5. 创建学生答案
        answers_data = [
            {"question_id": 12, "answer": "B", "is_correct": True, "points": 10, "time": 60},
            {"question_id": 13, "answer": "A", "is_correct": False, "points": 0, "time": 90},
            {"question_id": 14, "answer": "B", "is_correct": True, "points": 10, "time": 150}
        ]
        
        for answer in answers_data:
            cursor.execute("""
                INSERT OR REPLACE INTO student_answers (
                    attempt_id, question_id, student_id, answer_content, 
                    is_correct, points_earned, time_spent, answered_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                1, answer["question_id"], student_id, answer["answer"],
                answer["is_correct"], answer["points"], answer["time"], now
            ))
        
        print("✅ 创建学生答案成功")
        
        # 6. 创建第二次练习尝试（历史记录）
        cursor.execute("""
            INSERT OR REPLACE INTO exercise_attempts (
                id, exercise_id, student_id, total_questions, answered_questions,
                correct_answers, score, max_score, time_spent, is_completed, 
                is_submitted, started_at, completed_at, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            2, 1, student_id, 3, 3, 3, 100, 100, 250,
            True, True, now, now, now
        ))
        
        # 第二次的答案（全对）
        for i, answer in enumerate(answers_data):
            cursor.execute("""
                INSERT OR REPLACE INTO student_answers (
                    attempt_id, question_id, student_id, answer_content, 
                    is_correct, points_earned, time_spent, answered_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                2, answer["question_id"], student_id, 
                questions_data[i]["correct_answer"],  # 使用正确答案
                True, 10, answer["time"] - 20, now
            ))
        
        print("✅ 创建第二次练习尝试成功")
        
        conn.commit()
        
        print("\n🎉 测试数据创建完成！")
        print("📋 创建的数据:")
        print(f"  - 练习ID: 1 (Python基础测试)")
        print(f"  - 题目ID: 12, 13, 14")
        print(f"  - 练习尝试ID: 1 (66.67分), 2 (100分)")
        print(f"  - 学生ID: {student_id}")
        
        print(f"\n🔗 测试链接:")
        print(f"  第一次练习结果: http://localhost:5173/student/exercises/result/1?attemptId=1")
        print(f"  第二次练习结果: http://localhost:5173/student/exercises/result/1?attemptId=2")
        print(f"  练习页面: http://localhost:5173/student/exercises/practice/1")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 创建失败: {e}")
        return False
    finally:
        conn.close()

def verify_data():
    """验证创建的数据"""
    print("\n🔍 验证创建的数据...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查练习
        cursor.execute("SELECT id, title, total_questions FROM exercises WHERE id = 1")
        exercise = cursor.fetchone()
        if exercise:
            print(f"✅ 练习: {exercise[1]} ({exercise[2]}道题)")
        
        # 检查题目
        cursor.execute("SELECT COUNT(*) FROM questions WHERE exercise_id = 1")
        question_count = cursor.fetchone()[0]
        print(f"✅ 题目数量: {question_count}")
        
        # 检查练习尝试
        cursor.execute("SELECT COUNT(*) FROM exercise_attempts WHERE exercise_id = 1")
        attempt_count = cursor.fetchone()[0]
        print(f"✅ 练习尝试: {attempt_count}次")
        
        # 检查学生答案
        cursor.execute("SELECT COUNT(*) FROM student_answers WHERE attempt_id IN (1, 2)")
        answer_count = cursor.fetchone()[0]
        print(f"✅ 学生答案: {answer_count}条")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    finally:
        conn.close()

def main():
    """主函数"""
    print("🚀 创建练习结果测试数据")
    print("=" * 60)
    
    # 创建测试数据
    if create_test_data():
        # 验证数据
        verify_data()
        
        print("\n🎯 现在可以测试练习结果页面:")
        print("1. 启动前端: cd frontend && pnpm dev")
        print("2. 启动后端: cd backend && python main.py")
        print("3. 访问测试链接查看效果")
    else:
        print("\n❌ 测试数据创建失败")

if __name__ == "__main__":
    main()

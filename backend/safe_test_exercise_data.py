#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的练习数据测试 - 不污染数据库
"""

import sqlite3
import json
import tempfile
import shutil
import os
from datetime import datetime

# 原始数据库路径
ORIGINAL_DB_PATH = r"D:\project\softwareCup\backend\data\database\education_platform.db"

class SafeExerciseTest:
    def __init__(self):
        self.temp_db_path = None
        self.backup_created = False
        
    def create_backup(self):
        """创建数据库备份"""
        print("📦 创建数据库备份...")
        
        if not os.path.exists(ORIGINAL_DB_PATH):
            print("❌ 原始数据库不存在")
            return False
            
        try:
            # 创建临时备份文件
            backup_path = ORIGINAL_DB_PATH + ".backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(ORIGINAL_DB_PATH, backup_path)
            
            print(f"✅ 备份创建成功: {backup_path}")
            self.backup_path = backup_path
            self.backup_created = True
            return True
            
        except Exception as e:
            print(f"❌ 备份创建失败: {e}")
            return False
    
    def create_temp_database(self):
        """创建临时测试数据库"""
        print("🧪 创建临时测试数据库...")
        
        try:
            # 复制原始数据库到临时位置
            temp_dir = tempfile.mkdtemp()
            self.temp_db_path = os.path.join(temp_dir, "test_education_platform.db")
            shutil.copy2(ORIGINAL_DB_PATH, self.temp_db_path)
            
            print(f"✅ 临时数据库创建成功: {self.temp_db_path}")
            return True
            
        except Exception as e:
            print(f"❌ 临时数据库创建失败: {e}")
            return False
    
    def add_test_data(self):
        """向临时数据库添加测试数据"""
        print("📝 添加测试数据...")
        
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        
        try:
            now = datetime.now().isoformat()
            
            # 获取现有用户
            cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 1")
            student = cursor.fetchone()
            cursor.execute("SELECT id FROM users WHERE role = 'teacher' LIMIT 1")
            teacher = cursor.fetchone()
            
            if not student or not teacher:
                print("❌ 数据库中缺少用户数据")
                return False
                
            student_id, teacher_id = student[0], teacher[0]
            
            # 查找可用的ID
            cursor.execute("SELECT MAX(id) FROM exercises")
            max_exercise_id = cursor.fetchone()[0] or 0
            exercise_id = max_exercise_id + 1
            
            cursor.execute("SELECT MAX(id) FROM questions")
            max_question_id = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT MAX(id) FROM exercise_attempts")
            max_attempt_id = cursor.fetchone()[0] or 0
            
            # 创建测试练习
            cursor.execute("""
                INSERT INTO exercises (
                    id, title, description, category, subject, difficulty, 
                    time_limit, created_by, total_questions, is_active, is_published, 
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                exercise_id, "[测试] Python基础测试", "这是一个测试练习，可以安全删除", 
                "practice", "Python编程", "easy", 30, teacher_id, 3, True, True, now, now
            ))
            
            # 创建测试题目
            questions_data = [
                {
                    "title": "[测试] Python语言类型",
                    "content": "Python是什么类型的编程语言？",
                    "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                    "correct_answer": "B"
                },
                {
                    "title": "[测试] Python特点", 
                    "content": "以下哪个是Python的特点？",
                    "options": {"A": "语法复杂", "B": "语法简洁", "C": "运行很快", "D": "内存很小"},
                    "correct_answer": "B"
                },
                {
                    "title": "[测试] Python变量",
                    "content": "在Python中，变量名可以以什么开头？",
                    "options": {"A": "数字", "B": "字母或下划线", "C": "特殊符号", "D": "空格"},
                    "correct_answer": "B"
                }
            ]
            
            question_ids = []
            for i, q in enumerate(questions_data):
                question_id = max_question_id + i + 1
                question_ids.append(question_id)
                
                cursor.execute("""
                    INSERT INTO questions (
                        id, exercise_id, title, content, question_type, options, 
                        correct_answer, explanation, difficulty, points, 
                        is_active, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    question_id, exercise_id, q["title"], q["content"], "multiple_choice",
                    json.dumps(q["options"]), q["correct_answer"], "测试解析",
                    "easy", 10, True, now, now
                ))
            
            # 创建练习尝试
            attempt_id = max_attempt_id + 1
            cursor.execute("""
                INSERT INTO exercise_attempts (
                    id, exercise_id, student_id, total_questions, answered_questions,
                    correct_answers, score, max_score, time_spent, is_completed, 
                    is_submitted, started_at, completed_at, submitted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attempt_id, exercise_id, student_id, 3, 3, 2, 66.67, 100, 300,
                True, True, now, now, now
            ))
            
            # 创建学生答案
            answers = ["B", "A", "B"]  # 第二题答错
            for i, (question_id, answer) in enumerate(zip(question_ids, answers)):
                is_correct = answer == questions_data[i]["correct_answer"]
                points = 10 if is_correct else 0
                
                cursor.execute("""
                    INSERT INTO student_answers (
                        attempt_id, question_id, student_id, answer_content, 
                        is_correct, points_earned, time_spent, answered_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    attempt_id, question_id, student_id, answer,
                    is_correct, points, 60 + i * 30, now
                ))
            
            conn.commit()
            
            print("✅ 测试数据添加成功")
            print(f"📋 测试数据信息:")
            print(f"  - 练习ID: {exercise_id}")
            print(f"  - 题目ID: {question_ids}")
            print(f"  - 练习尝试ID: {attempt_id}")
            print(f"  - 学生ID: {student_id}")
            
            return exercise_id, attempt_id
            
        except Exception as e:
            conn.rollback()
            print(f"❌ 添加测试数据失败: {e}")
            return False
        finally:
            conn.close()
    
    def cleanup(self):
        """清理临时文件"""
        print("🧹 清理临时文件...")
        
        if self.temp_db_path and os.path.exists(self.temp_db_path):
            try:
                # 删除临时数据库文件
                temp_dir = os.path.dirname(self.temp_db_path)
                shutil.rmtree(temp_dir)
                print("✅ 临时文件清理完成")
            except Exception as e:
                print(f"⚠️  临时文件清理失败: {e}")
    
    def show_test_info(self, exercise_id, attempt_id):
        """显示测试信息"""
        print(f"\n🎯 测试信息:")
        print(f"📍 临时数据库: {self.temp_db_path}")
        print(f"🔗 如果要在前端测试，需要临时修改数据库路径")
        print(f"\n📋 测试数据:")
        print(f"  - 练习ID: {exercise_id}")
        print(f"  - 练习尝试ID: {attempt_id}")
        
        print(f"\n🌐 前端测试URL (需要修改数据库路径):")
        print(f"  - 结果页面: http://localhost:5173/student/exercises/result/{exercise_id}?attemptId={attempt_id}")

def main():
    """主函数"""
    print("🛡️  安全的练习结果测试")
    print("=" * 60)
    print("⚠️  注意: 此测试使用临时数据库，不会污染原始数据")
    
    test = SafeExerciseTest()
    
    try:
        # 1. 创建备份（可选）
        choice = input("\n是否创建数据库备份？(y/n): ").lower().strip()
        if choice == 'y':
            test.create_backup()
        
        # 2. 创建临时数据库
        if not test.create_temp_database():
            return
        
        # 3. 添加测试数据
        result = test.add_test_data()
        if not result:
            return
            
        exercise_id, attempt_id = result
        
        # 4. 显示测试信息
        test.show_test_info(exercise_id, attempt_id)
        
        print(f"\n✅ 安全测试准备完成！")
        print(f"💡 提示: 测试完成后会自动清理临时文件")
        
        input("\n按回车键清理临时文件...")
        
    finally:
        # 5. 清理临时文件
        test.cleanup()

if __name__ == "__main__":
    main()

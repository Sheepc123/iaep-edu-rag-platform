#!/usr/bin/env python3
"""
数据库清理脚本：删除所有课程及相关数据
"""

import sqlite3
import os
from pathlib import Path

def cleanup_courses():
    """清理所有课程相关数据"""
    
    # 数据库文件路径
    db_path = Path(__file__).parent / "database" / "data" / "education_platform.db"
    
    if not db_path.exists():
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        print("开始清理课程相关数据...")
        
        # 1. 删除课程进度记录
        cursor.execute("DELETE FROM lesson_progress")
        deleted_progress = cursor.rowcount
        print(f"删除了 {deleted_progress} 条课程进度记录")
        
        # 2. 删除课程注册记录
        cursor.execute("DELETE FROM course_enrollments")
        deleted_enrollments = cursor.rowcount
        print(f"删除了 {deleted_enrollments} 条课程注册记录")
        
        # 3. 删除练习答题记录
        cursor.execute("DELETE FROM exercise_attempts")
        deleted_attempts = cursor.rowcount
        print(f"删除了 {deleted_attempts} 条练习答题记录")
        
        # 4. 删除答案记录
        cursor.execute("DELETE FROM answers")
        deleted_answers = cursor.rowcount
        print(f"删除了 {deleted_answers} 条答案记录")
        
        # 5. 删除题目
        cursor.execute("DELETE FROM questions")
        deleted_questions = cursor.rowcount
        print(f"删除了 {deleted_questions} 道题目")
        
        # 6. 删除练习
        cursor.execute("DELETE FROM exercises")
        deleted_exercises = cursor.rowcount
        print(f"删除了 {deleted_exercises} 个练习")
        
        # 7. 删除课时
        cursor.execute("DELETE FROM lessons")
        deleted_lessons = cursor.rowcount
        print(f"删除了 {deleted_lessons} 个课时")
        
        # 8. 删除课程
        cursor.execute("DELETE FROM courses")
        deleted_courses = cursor.rowcount
        print(f"删除了 {deleted_courses} 个课程")
        
        # 提交更改
        conn.commit()
        
        print("\n清理完成！数据库统计：")
        
        # 验证清理结果
        tables_to_check = [
            ("courses", "课程"),
            ("lessons", "课时"),
            ("exercises", "练习"),
            ("questions", "题目"),
            ("answers", "答案"),
            ("exercise_attempts", "练习答题记录"),
            ("course_enrollments", "课程注册记录"),
            ("lesson_progress", "课程进度记录")
        ]
        
        for table, name in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"- {name}: {count} 条记录")
        
        return True
            
    except sqlite3.Error as e:
        print(f"数据库清理失败: {e}")
        conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()

def confirm_cleanup():
    """确认是否执行清理操作"""
    print("⚠️  警告：此操作将删除所有课程及相关数据，包括：")
    print("   - 所有课程")
    print("   - 所有课时")
    print("   - 所有练习和题目")
    print("   - 所有学生的学习进度")
    print("   - 所有课程注册记录")
    print("   - 所有练习答题记录")
    print()
    
    response = input("确定要继续吗？请输入 'YES' 来确认: ")
    
    if response.strip().upper() == 'YES':
        return True
    else:
        print("操作已取消")
        return False

if __name__ == "__main__":
    if confirm_cleanup():
        success = cleanup_courses()
        if success:
            print("\n✅ 数据库清理成功完成")
            exit(0)
        else:
            print("\n❌ 数据库清理失败")
            exit(1)
    else:
        exit(0)

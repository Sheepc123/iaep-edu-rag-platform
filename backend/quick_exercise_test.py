#!/usr/bin/env python3
"""
快速习题系统测试脚本
专门用于验证习题数据块的建立
"""

import os
import sys
import sqlite3

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_structure():
    """检查数据库结构"""
    print("🔍 检查数据库结构...")
    
    db_path = 'data/database/education_platform.db'
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查习题相关表
        exercise_tables = {
            'exercises': '习题集表',
            'questions': '题目表', 
            'exercise_attempts': '答题尝试表',
            'student_answers': '学生答案表'
        }
        
        print("📊 习题相关表检查:")
        all_exist = True
        
        for table_name, description in exercise_tables.items():
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            exists = cursor.fetchone()
            
            if exists:
                cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
                count = cursor.fetchone()[0]
                print(f"  ✅ {table_name} ({description}): {count} 条记录")
            else:
                print(f"  ❌ {table_name} ({description}): 不存在")
                all_exist = False
        
        conn.close()
        return all_exist
        
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")
        return False


def create_exercise_tables_if_needed():
    """如果需要，创建习题表"""
    print("\n🔧 创建习题表...")
    
    try:
        from app.core.database import engine
        from app.models import exercise
        
        # 创建所有表
        exercise.Base.metadata.create_all(bind=engine)
        print("✅ 习题表创建成功")
        return True
        
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        return False


def create_sample_data():
    """创建示例习题数据"""
    print("\n📝 创建示例习题数据...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        from app.models.user import User
        
        db = SessionLocal()
        
        # 获取第一个教师和课程
        teacher = db.query(User).filter(User.role == "teacher").first()
        course = db.query(Course).first()
        
        if not teacher:
            print("❌ 没有找到教师用户")
            db.close()
            return False
            
        if not course:
            print("❌ 没有找到课程")
            db.close()
            return False
        
        print(f"👨‍🏫 使用教师: {teacher.username}")
        print(f"📚 使用课程: {course.title}")
        
        # 检查是否已有示例习题
        existing_count = db.query(Exercise).filter(Exercise.course_id == course.id).count()
        if existing_count > 0:
            print(f"ℹ️  课程已有 {existing_count} 个习题")
            db.close()
            return True
        
        # 创建示例习题
        exercise1 = Exercise(
            title="Python基础练习",
            description="测试Python基础语法和概念的练习题",
            category="practice",
            subject="Python编程",
            difficulty="easy",
            time_limit=30,
            course_id=course.id,
            created_by=teacher.id,
            total_questions=3,
            is_published=True,
            is_active=True
        )
        
        exercise2 = Exercise(
            title="Python进阶作业",
            description="Python面向对象编程和高级特性练习",
            category="homework", 
            subject="Python编程",
            difficulty="medium",
            time_limit=60,
            course_id=course.id,
            created_by=teacher.id,
            total_questions=2,
            is_published=True,
            is_active=True
        )
        
        db.add(exercise1)
        db.add(exercise2)
        db.commit()
        db.refresh(exercise1)
        db.refresh(exercise2)
        
        print(f"✅ 创建习题: {exercise1.title} (ID: {exercise1.id})")
        print(f"✅ 创建习题: {exercise2.title} (ID: {exercise2.id})")
        
        # 为第一个习题添加题目
        questions1 = [
            {
                "content": "Python是什么类型的编程语言？",
                "question_type": "multiple_choice",
                "options": {"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                "correct_answer": "B",
                "explanation": "Python是一种解释型的高级编程语言。",
                "points": 10
            },
            {
                "content": "在Python中，用于定义函数的关键字是______。",
                "question_type": "fill_blank", 
                "options": None,
                "correct_answer": "def",
                "explanation": "在Python中，使用def关键字来定义函数。",
                "points": 10
            },
            {
                "content": "请解释Python中列表(list)和元组(tuple)的区别。",
                "question_type": "essay",
                "options": None,
                "correct_answer": "列表是可变的数据类型，元组是不可变的数据类型。",
                "explanation": "这是一个开放性问题，主要考查对Python基础数据类型的理解。",
                "points": 20
            }
        ]
        
        for q_data in questions1:
            question = Question(
                exercise_id=exercise1.id,
                content=q_data["content"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"],
                points=q_data["points"],
                difficulty="easy",
                subject="Python编程",
                is_active=True
            )
            db.add(question)
        
        # 为第二个习题添加题目
        questions2 = [
            {
                "content": "Python中的装饰器主要用于什么？",
                "question_type": "multiple_choice",
                "options": {"A": "数据存储", "B": "函数增强", "C": "错误处理", "D": "性能优化"},
                "correct_answer": "B",
                "explanation": "装饰器主要用于在不修改原函数代码的情况下增强函数功能。",
                "points": 15
            },
            {
                "content": "什么是Python的GIL？请简要说明其作用。",
                "question_type": "essay",
                "options": None,
                "correct_answer": "GIL是全局解释器锁，确保同一时间只有一个线程执行Python字节码。",
                "explanation": "GIL是Python多线程编程中的重要概念。",
                "points": 25
            }
        ]
        
        for q_data in questions2:
            question = Question(
                exercise_id=exercise2.id,
                content=q_data["content"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"],
                points=q_data["points"],
                difficulty="medium",
                subject="Python编程",
                is_active=True
            )
            db.add(question)
        
        db.commit()
        db.close()
        
        print("✅ 示例题目创建完成")
        return True
        
    except Exception as e:
        print(f"❌ 创建示例数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_course_exercises():
    """验证课程习题数据"""
    print("\n🔍 验证课程习题数据...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        
        db = SessionLocal()
        
        # 获取所有课程
        courses = db.query(Course).all()
        
        for course in courses:
            exercises = db.query(Exercise).filter(Exercise.course_id == course.id).all()
            print(f"\n📚 课程: {course.title} (ID: {course.id})")
            print(f"   习题数量: {len(exercises)}")
            
            for exercise in exercises:
                questions = db.query(Question).filter(Question.exercise_id == exercise.id).all()
                print(f"   - {exercise.title} ({exercise.category})")
                print(f"     题目数: {len(questions)}, 难度: {exercise.difficulty}")
                print(f"     状态: {'已发布' if exercise.is_published else '草稿'}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 快速习题系统测试")
    print("=" * 50)
    
    # 1. 检查数据库结构
    if not check_database_structure():
        # 2. 创建表
        if not create_exercise_tables_if_needed():
            print("❌ 无法创建习题表")
            return
    
    # 3. 创建示例数据
    if not create_sample_data():
        print("❌ 无法创建示例数据")
        return
    
    # 4. 验证数据
    if not verify_course_exercises():
        print("❌ 数据验证失败")
        return
    
    print("\n" + "=" * 50)
    print("🎉 习题数据块建立完成！")
    print("\n💡 下一步:")
    print("1. 启动后端: python run.py")
    print("2. 启动前端: npm run dev") 
    print("3. 访问: http://localhost:5173/teacher/courses/1")
    print("4. 查看课程详情页的'课程练习'标签")
    print("5. 验证习题数据正确显示")


if __name__ == "__main__":
    main()

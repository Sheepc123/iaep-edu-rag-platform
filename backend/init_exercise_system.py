#!/usr/bin/env python3
"""
初始化练习系统数据库
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_exercise_tables():
    """初始化练习系统表"""
    print("🔧 初始化练习系统数据库表...")
    
    try:
        from app.core.database import engine, SessionLocal
        from app.models.exercise import Exercise, Question, ExerciseAttempt, StudentAnswer, WrongQuestion
        from app.models.course import Course
        from app.models.user import User
        from sqlalchemy import text
        
        # 创建所有表
        from app.models import exercise, course, user
        exercise.Base.metadata.create_all(bind=engine)
        
        print("✅ 练习系统表创建成功")
        
        # 检查表结构
        db = SessionLocal()
        
        # 检查是否需要添加外键约束
        try:
            # 检查课程表是否有exercises关系
            result = db.execute(text("PRAGMA foreign_key_list(exercises)"))
            foreign_keys = result.fetchall()
            
            print(f"📋 exercises表外键约束: {len(foreign_keys)} 个")
            for fk in foreign_keys:
                print(f"   - {fk}")
                
        except Exception as e:
            print(f"⚠️  检查外键约束失败: {e}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()


def create_sample_exercises():
    """创建示例练习数据"""
    print("\n📝 创建示例练习数据...")
    
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
            return
            
        if not course:
            print("❌ 没有找到课程")
            return
        
        print(f"👨‍🏫 使用教师: {teacher.username}")
        print(f"📚 使用课程: {course.title}")
        
        # 检查是否已有练习
        existing_exercise = db.query(Exercise).filter(
            Exercise.course_id == course.id,
            Exercise.title == "Python基础练习"
        ).first()
        
        if existing_exercise:
            print("ℹ️  示例练习已存在")
            db.close()
            return
        
        # 创建示例练习
        exercise = Exercise(
            title="Python基础练习",
            description="测试Python基础知识的练习，包含选择题、填空题和问答题",
            course_id=course.id,
            category="practice",
            difficulty="medium",
            time_limit=30,
            total_questions=0,
            total_points=0.0,
            pass_score=60.0,
            is_published=True,
            is_active=True,
            created_by=teacher.id
        )
        
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        
        print(f"✅ 创建练习: {exercise.title} (ID: {exercise.id})")
        
        # 创建示例题目
        questions_data = [
            {
                "question_text": "Python是什么类型的编程语言？",
                "question_type": "multiple_choice",
                "options": ["编译型", "解释型", "汇编型", "机器型"],
                "correct_answer": "解释型",
                "explanation": "Python是一种解释型的高级编程语言，代码在运行时由解释器逐行执行。",
                "points": 10.0,
                "difficulty": "easy",
                "question_order": 1
            },
            {
                "question_text": "在Python中，用于定义函数的关键字是______。",
                "question_type": "fill_blank",
                "options": None,
                "correct_answer": "def",
                "explanation": "在Python中，使用def关键字来定义函数。",
                "points": 10.0,
                "difficulty": "easy",
                "question_order": 2
            },
            {
                "question_text": "请解释Python中列表(list)和元组(tuple)的区别。",
                "question_type": "essay",
                "options": None,
                "correct_answer": "列表是可变的数据类型，可以修改其中的元素；元组是不可变的数据类型，一旦创建就不能修改。列表使用方括号[]，元组使用圆括号()。",
                "explanation": "这是一个开放性问题，主要考查对Python基础数据类型的理解。",
                "points": 20.0,
                "difficulty": "medium",
                "question_order": 3
            }
        ]
        
        total_points = 0
        for q_data in questions_data:
            question = Question(
                exercise_id=exercise.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"],
                points=q_data["points"],
                difficulty=q_data["difficulty"],
                question_order=q_data["question_order"],
                is_active=True
            )
            db.add(question)
            total_points += q_data["points"]
            
            print(f"   ✅ 添加题目: {q_data['question_text'][:30]}...")
        
        # 更新练习统计
        exercise.total_questions = len(questions_data)
        exercise.total_points = total_points
        
        db.commit()
        
        print(f"✅ 示例练习创建完成，共 {len(questions_data)} 道题目，总分 {total_points} 分")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 创建示例数据失败: {e}")
        import traceback
        traceback.print_exc()


def verify_exercise_system():
    """验证练习系统"""
    print("\n🔍 验证练习系统...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        
        db = SessionLocal()
        
        # 统计数据
        exercise_count = db.query(Exercise).count()
        question_count = db.query(Question).count()
        course_count = db.query(Course).count()
        
        print(f"📊 系统统计:")
        print(f"   课程数量: {course_count}")
        print(f"   练习数量: {exercise_count}")
        print(f"   题目数量: {question_count}")
        
        # 检查课程-练习关联
        if exercise_count > 0:
            exercises = db.query(Exercise).all()
            for exercise in exercises:
                course = db.query(Course).filter(Course.id == exercise.course_id).first()
                print(f"   练习 '{exercise.title}' 关联课程 '{course.title if course else '未找到'}'")
        
        db.close()
        
        print("✅ 练习系统验证完成")
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")


def main():
    """主函数"""
    print("🚀 练习系统初始化")
    print("=" * 60)
    
    # 1. 初始化表结构
    init_exercise_tables()
    
    # 2. 创建示例数据
    create_sample_exercises()
    
    # 3. 验证系统
    verify_exercise_system()
    
    print("\n" + "=" * 60)
    print("🎉 练习系统初始化完成！")
    print("\n💡 下一步:")
    print("1. 启动后端服务: python run.py")
    print("2. 启动前端服务: npm run dev")
    print("3. 运行测试: python test_exercise_system.py")
    print("4. 访问教师端: http://localhost:5173/teacher/courses/1")
    print("5. 访问学生端: http://localhost:5173/student/courses/1")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
检查数据库中的练习数据
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.exercise import Exercise, Question
from app.models.user import User
from sqlalchemy import func

def check_exercises():
    """检查数据库中的练习数据"""
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("📊 数据库练习数据检查")
        print("=" * 50)
        
        # 检查用户数据
        total_users = db.query(User).count()
        teachers = db.query(User).filter(User.role == "teacher").count()
        students = db.query(User).filter(User.role == "student").count()
        
        print(f"\n👥 用户统计:")
        print(f"   总用户数: {total_users}")
        print(f"   教师数量: {teachers}")
        print(f"   学生数量: {students}")
        
        # 检查练习数据
        total_exercises = db.query(Exercise).count()
        published_exercises = db.query(Exercise).filter(Exercise.is_published == True).count()
        draft_exercises = db.query(Exercise).filter(Exercise.is_published == False).count()
        
        print(f"\n📚 练习统计:")
        print(f"   总练习数: {total_exercises}")
        print(f"   已发布: {published_exercises}")
        print(f"   草稿: {draft_exercises}")
        
        # 检查题目数据
        total_questions = db.query(Question).count()
        
        print(f"\n❓ 题目统计:")
        print(f"   总题目数: {total_questions}")
        
        # 显示最近的练习
        if total_exercises > 0:
            print(f"\n📋 最近的练习:")
            recent_exercises = db.query(Exercise).order_by(Exercise.created_at.desc()).limit(5).all()
            
            for i, exercise in enumerate(recent_exercises, 1):
                creator = db.query(User).filter(User.id == exercise.created_by).first()
                question_count = db.query(Question).filter(Question.exercise_id == exercise.id).count()
                
                status = "✅ 已发布" if exercise.is_published else "📝 草稿"
                print(f"   {i}. {exercise.title}")
                print(f"      创建者: {creator.username if creator else '未知'}")
                print(f"      分类: {exercise.category}")
                print(f"      科目: {exercise.subject}")
                print(f"      难度: {exercise.difficulty}")
                print(f"      题目数: {question_count}")
                print(f"      状态: {status}")
                print(f"      创建时间: {exercise.created_at}")
                print()
        
        # 按分类统计
        if total_exercises > 0:
            print(f"\n📊 分类统计:")
            categories = db.query(Exercise.category, func.count(Exercise.id)).group_by(Exercise.category).all()
            for category, count in categories:
                print(f"   {category}: {count} 个练习")
        
        # 按难度统计
        if total_exercises > 0:
            print(f"\n🎯 难度统计:")
            difficulties = db.query(Exercise.difficulty, func.count(Exercise.id)).group_by(Exercise.difficulty).all()
            for difficulty, count in difficulties:
                difficulty_label = {"easy": "简单", "medium": "中等", "hard": "困难"}.get(difficulty, difficulty)
                print(f"   {difficulty_label}: {count} 个练习")
        
        # 检查题目类型分布
        if total_questions > 0:
            print(f"\n🔍 题目类型统计:")
            question_types = db.query(Question.question_type, func.count(Question.id)).group_by(Question.question_type).all()
            for qtype, count in question_types:
                type_label = {
                    "multiple_choice": "选择题",
                    "fill_blank": "填空题", 
                    "essay": "问答题"
                }.get(qtype, qtype)
                print(f"   {type_label}: {count} 道题目")
        
        print("\n" + "=" * 50)
        
        if total_exercises == 0:
            print("⚠️  数据库中没有练习数据")
            print("💡 建议:")
            print("   1. 使用教师账号登录系统")
            print("   2. 创建一些练习和题目")
            print("   3. 发布练习供学生使用")
        elif published_exercises == 0:
            print("⚠️  数据库中没有已发布的练习")
            print("💡 建议:")
            print("   1. 登录教师端")
            print("   2. 将现有练习设置为发布状态")
        else:
            print("✅ 数据库状态正常")
            print(f"   学生可以看到 {published_exercises} 个已发布的练习")
        
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    check_exercises()

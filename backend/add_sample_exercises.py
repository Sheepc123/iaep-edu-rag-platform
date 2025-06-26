#!/usr/bin/env python3
"""
添加示例练习数据到数据库
"""
import sys
import os
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.exercise import Exercise, Question
from app.models.user import User

def add_sample_exercises():
    """添加示例练习数据"""
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("📚 添加示例练习数据")
        print("=" * 50)
        
        # 查找教师用户
        teacher = db.query(User).filter(User.role == "teacher").first()
        if not teacher:
            print("❌ 没有找到教师用户，请先创建教师账号")
            return
        
        print(f"✅ 找到教师用户: {teacher.username}")
        
        # 示例练习数据
        sample_exercises = [
            {
                "title": "高等数学基础练习",
                "description": "包含函数、极限、导数等基础概念的练习题目",
                "category": "自主练习",
                "subject": "数学",
                "difficulty": "medium",
                "time_limit": 60,
                "is_published": True,
                "questions": [
                    {
                        "content": "函数f(x)=x²在x=2处的极限值是？",
                        "question_type": "multiple_choice",
                        "options": ["2", "4", "8", "不存在"],
                        "correct_answer": "4",
                        "explanation": "根据极限的定义，当x趋向于2时，f(x)=x²的极限值为2²=4",
                        "difficulty": "easy",
                        "points": 10
                    },
                    {
                        "content": "当x趋向于0时，sin(x)/x的极限值是____。",
                        "question_type": "fill_blank",
                        "correct_answer": "1",
                        "explanation": "这是重要极限公式，lim(x→0) sin(x)/x = 1",
                        "difficulty": "medium",
                        "points": 15
                    },
                    {
                        "content": "请解释函数连续性的定义，并举例说明。",
                        "question_type": "essay",
                        "correct_answer": "函数在某点连续需要满足三个条件：1)函数在该点有定义；2)函数在该点的极限存在；3)函数值等于极限值。例如：f(x)=x在任意点都连续。",
                        "explanation": "连续性是微积分中的重要概念，要求学生理解其定义和应用",
                        "difficulty": "hard",
                        "points": 20
                    }
                ]
            },
            {
                "title": "线性代数矩阵运算",
                "description": "矩阵的基本运算和性质练习",
                "category": "课后作业",
                "subject": "数学",
                "difficulty": "hard",
                "time_limit": 90,
                "is_published": True,
                "questions": [
                    {
                        "content": "两个2×2矩阵相乘的结果矩阵的维度是？",
                        "question_type": "multiple_choice",
                        "options": ["1×1", "2×2", "2×4", "4×2"],
                        "correct_answer": "2×2",
                        "explanation": "两个2×2矩阵相乘，结果仍然是2×2矩阵",
                        "difficulty": "easy",
                        "points": 8
                    },
                    {
                        "content": "单位矩阵的行列式值是____。",
                        "question_type": "fill_blank",
                        "correct_answer": "1",
                        "explanation": "单位矩阵的行列式值恒为1",
                        "difficulty": "medium",
                        "points": 12
                    }
                ]
            },
            {
                "title": "概率论基础概念",
                "description": "概率的基本概念和计算方法",
                "category": "模拟考试",
                "subject": "数学",
                "difficulty": "medium",
                "time_limit": 45,
                "is_published": True,
                "questions": [
                    {
                        "content": "抛掷一枚公平硬币，正面朝上的概率是？",
                        "question_type": "multiple_choice",
                        "options": ["0.25", "0.5", "0.75", "1"],
                        "correct_answer": "0.5",
                        "explanation": "公平硬币正面朝上的概率是1/2=0.5",
                        "difficulty": "easy",
                        "points": 10
                    },
                    {
                        "content": "从52张牌中抽取一张红桃的概率是____。",
                        "question_type": "fill_blank",
                        "correct_answer": "1/4",
                        "explanation": "52张牌中有13张红桃，所以概率是13/52=1/4",
                        "difficulty": "medium",
                        "points": 15
                    }
                ]
            },
            {
                "title": "计算机基础知识",
                "description": "计算机科学基础概念和编程基础",
                "category": "自主练习",
                "subject": "计算机",
                "difficulty": "easy",
                "time_limit": 30,
                "is_published": True,
                "questions": [
                    {
                        "content": "以下哪种不是编程语言？",
                        "question_type": "multiple_choice",
                        "options": ["Python", "Java", "HTML", "C++"],
                        "correct_answer": "HTML",
                        "explanation": "HTML是标记语言，不是编程语言",
                        "difficulty": "easy",
                        "points": 5
                    },
                    {
                        "content": "二进制数1010转换为十进制数是____。",
                        "question_type": "fill_blank",
                        "correct_answer": "10",
                        "explanation": "1010(2) = 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 8 + 0 + 2 + 0 = 10",
                        "difficulty": "medium",
                        "points": 10
                    }
                ]
            },
            {
                "title": "英语语法练习",
                "description": "英语基础语法和词汇练习",
                "category": "课后作业",
                "subject": "英语",
                "difficulty": "medium",
                "time_limit": 40,
                "is_published": True,
                "questions": [
                    {
                        "content": "Which of the following is correct?",
                        "question_type": "multiple_choice",
                        "options": ["He don't like apples", "He doesn't like apples", "He not like apples", "He no like apples"],
                        "correct_answer": "He doesn't like apples",
                        "explanation": "第三人称单数的否定形式应该用doesn't",
                        "difficulty": "easy",
                        "points": 8
                    },
                    {
                        "content": "The past tense of 'go' is ____.",
                        "question_type": "fill_blank",
                        "correct_answer": "went",
                        "explanation": "go的过去式是went，这是不规则动词变化",
                        "difficulty": "easy",
                        "points": 6
                    }
                ]
            }
        ]
        
        # 添加练习数据
        for exercise_data in sample_exercises:
            print(f"\n📝 创建练习: {exercise_data['title']}")
            
            # 创建练习
            exercise = Exercise(
                title=exercise_data["title"],
                description=exercise_data["description"],
                category=exercise_data["category"],
                subject=exercise_data["subject"],
                difficulty=exercise_data["difficulty"],
                time_limit=exercise_data["time_limit"],
                created_by=teacher.id,
                is_published=exercise_data["is_published"],
                total_questions=len(exercise_data["questions"])
            )
            
            db.add(exercise)
            db.flush()  # 获取exercise.id
            
            # 添加题目
            for i, question_data in enumerate(exercise_data["questions"], 1):
                question = Question(
                    exercise_id=exercise.id,
                    title=f"题目 {i}",
                    content=question_data["content"],
                    question_type=question_data["question_type"],
                    options=json.dumps(question_data.get("options"), ensure_ascii=False) if question_data.get("options") else None,
                    correct_answer=question_data["correct_answer"],
                    explanation=question_data["explanation"],
                    difficulty=question_data["difficulty"],
                    points=question_data["points"],
                    subject=exercise_data["subject"],
                    question_order=i
                )
                db.add(question)
            
            print(f"   ✅ 添加了 {len(exercise_data['questions'])} 道题目")
        
        # 提交事务
        db.commit()
        
        print("\n" + "=" * 50)
        print("🎉 示例数据添加完成！")
        print("\n📊 添加的数据统计:")
        print(f"   练习数量: {len(sample_exercises)}")
        total_questions = sum(len(ex["questions"]) for ex in sample_exercises)
        print(f"   题目数量: {total_questions}")
        print(f"   涵盖科目: 数学、计算机、英语")
        print(f"   练习类型: 自主练习、课后作业、模拟考试")
        
        print("\n💡 现在您可以:")
        print("   1. 使用学生账号登录查看练习")
        print("   2. 在学生端练习页面看到这些练习")
        print("   3. 开始练习并提交答案")
        
    except Exception as e:
        print(f"❌ 添加数据失败: {str(e)}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_exercises()

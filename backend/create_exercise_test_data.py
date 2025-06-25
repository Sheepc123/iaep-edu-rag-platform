"""
创建练习系统测试数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.exercise import Exercise, Question, ExerciseAttempt, StudentAnswer, WrongQuestion
from app.models.user import User
from app.models import Base
import json
from datetime import datetime, timedelta


def create_test_exercises(db: Session):
    """创建测试练习数据"""
    
    # 获取测试用户（假设已存在）
    teacher = db.query(User).filter(User.role == "teacher").first()
    student = db.query(User).filter(User.role == "student").first()
    
    if not teacher or not student:
        print("请先创建测试用户（教师和学生）")
        return
    
    print(f"使用教师: {teacher.username}, 学生: {student.username}")
    
    # 创建练习1：高等数学基础练习
    exercise1 = Exercise(
        title="函数与极限 - 基础练习",
        description="本练习包含函数与极限的基础概念和计算题目，适合初学者巩固基础知识。",
        category="自主练习",
        subject="高等数学",
        difficulty="medium",
        time_limit=60,
        created_by=teacher.id,
        total_questions=0,
        is_published=True
    )
    db.add(exercise1)
    db.commit()
    db.refresh(exercise1)
    
    # 为练习1添加题目
    questions1 = [
        {
            "title": "函数极限的定义",
            "content": "下列关于函数极限的描述，正确的是：",
            "question_type": "multiple_choice",
            "options": [
                "A. 函数在某点的极限值等于函数在该点的函数值",
                "B. 函数极限存在当且仅当左极限和右极限都存在且相等",
                "C. 函数极限不存在时，函数在该点一定不连续",
                "D. 函数极限的值与函数在该点是否有定义无关"
            ],
            "correct_answer": "B",
            "explanation": "函数极限存在的充要条件是左极限和右极限都存在且相等。极限值与函数在该点的函数值可能不同。",
            "difficulty": "medium",
            "points": 10
        },
        {
            "title": "极限计算",
            "content": "计算极限：lim(x→0) (sin x)/x = ____",
            "question_type": "fill_blank",
            "options": None,
            "correct_answer": "1",
            "explanation": "这是一个重要的极限公式：lim(x→0) (sin x)/x = 1",
            "difficulty": "easy",
            "points": 8
        },
        {
            "title": "连续性证明",
            "content": "证明函数 f(x) = x² 在 x = 2 处连续。",
            "question_type": "essay",
            "options": None,
            "correct_answer": "需要证明：1) f(2)存在；2) lim(x→2) f(x)存在；3) lim(x→2) f(x) = f(2)",
            "explanation": "连续性的定义需要满足三个条件：函数在该点有定义、极限存在、极限值等于函数值。",
            "difficulty": "hard",
            "points": 15
        },
        {
            "title": "导数定义",
            "content": "函数 f(x) = x³ 在 x = 1 处的导数值是：",
            "question_type": "multiple_choice",
            "options": [
                "A. 1",
                "B. 2", 
                "C. 3",
                "D. 4"
            ],
            "correct_answer": "C",
            "explanation": "f'(x) = 3x²，所以 f'(1) = 3×1² = 3",
            "difficulty": "medium",
            "points": 10
        },
        {
            "title": "积分计算",
            "content": "计算不定积分：∫ 2x dx = ____",
            "question_type": "fill_blank",
            "options": None,
            "correct_answer": "x² + C",
            "explanation": "根据幂函数积分公式：∫ x^n dx = x^(n+1)/(n+1) + C",
            "difficulty": "easy",
            "points": 8
        }
    ]
    
    for q_data in questions1:
        question = Question(
            exercise_id=exercise1.id,
            title=q_data["title"],
            content=q_data["content"],
            question_type=q_data["question_type"],
            options=json.dumps(q_data["options"], ensure_ascii=False) if q_data["options"] else None,
            correct_answer=q_data["correct_answer"],
            explanation=q_data["explanation"],
            difficulty=q_data["difficulty"],
            points=q_data["points"],
            subject="高等数学"
        )
        db.add(question)
    
    # 更新练习1的题目数量
    exercise1.total_questions = len(questions1)
    
    # 创建练习2：线性代数练习
    exercise2 = Exercise(
        title="矩阵运算 - 综合练习",
        description="矩阵的基本运算和性质练习，包括矩阵乘法、行列式计算等。",
        category="课后作业",
        subject="线性代数",
        difficulty="hard",
        time_limit=90,
        created_by=teacher.id,
        total_questions=0,
        is_published=True
    )
    db.add(exercise2)
    db.commit()
    db.refresh(exercise2)
    
    # 为练习2添加题目
    questions2 = [
        {
            "title": "矩阵乘法",
            "content": "设 A = [[1,2],[3,4]]，B = [[2,0],[1,3]]，则 AB = ？",
            "question_type": "multiple_choice",
            "options": [
                "A. [[4,6],[10,12]]",
                "B. [[4,6],[10,11]]",
                "C. [[3,6],[10,12]]",
                "D. [[4,5],[10,12]]"
            ],
            "correct_answer": "A",
            "explanation": "矩阵乘法：AB的第i行第j列元素等于A的第i行与B的第j列对应元素乘积之和。",
            "difficulty": "medium",
            "points": 12
        },
        {
            "title": "行列式计算",
            "content": "计算二阶行列式 |1 2; 3 4| = ____",
            "question_type": "fill_blank",
            "options": None,
            "correct_answer": "-2",
            "explanation": "二阶行列式 |a b; c d| = ad - bc = 1×4 - 2×3 = -2",
            "difficulty": "easy",
            "points": 10
        },
        {
            "title": "矩阵的逆",
            "content": "证明矩阵 A = [[2,1],[1,1]] 可逆，并求其逆矩阵。",
            "question_type": "essay",
            "options": None,
            "correct_answer": "det(A) = 2×1 - 1×1 = 1 ≠ 0，所以A可逆。A^(-1) = [[1,-1],[-1,2]]",
            "explanation": "矩阵可逆的充要条件是行列式不为零。逆矩阵可通过伴随矩阵法求得。",
            "difficulty": "hard",
            "points": 18
        }
    ]
    
    for q_data in questions2:
        question = Question(
            exercise_id=exercise2.id,
            title=q_data["title"],
            content=q_data["content"],
            question_type=q_data["question_type"],
            options=json.dumps(q_data["options"], ensure_ascii=False) if q_data["options"] else None,
            correct_answer=q_data["correct_answer"],
            explanation=q_data["explanation"],
            difficulty=q_data["difficulty"],
            points=q_data["points"],
            subject="线性代数"
        )
        db.add(question)
    
    # 更新练习2的题目数量
    exercise2.total_questions = len(questions2)
    
    # 创建练习3：概率论练习
    exercise3 = Exercise(
        title="概率分布 - 应用题",
        description="概率分布的基本概念和应用，包括离散分布和连续分布。",
        category="模拟考试",
        subject="概率论",
        difficulty="medium",
        time_limit=45,
        created_by=teacher.id,
        total_questions=0,
        is_published=True
    )
    db.add(exercise3)
    db.commit()
    db.refresh(exercise3)
    
    # 为练习3添加题目
    questions3 = [
        {
            "title": "概率基本性质",
            "content": "设事件A和B互斥，P(A) = 0.3，P(B) = 0.4，则P(A∪B) = ？",
            "question_type": "multiple_choice",
            "options": [
                "A. 0.7",
                "B. 0.12",
                "C. 0.1",
                "D. 1.0"
            ],
            "correct_answer": "A",
            "explanation": "互斥事件的并事件概率等于各事件概率之和：P(A∪B) = P(A) + P(B) = 0.3 + 0.4 = 0.7",
            "difficulty": "easy",
            "points": 8
        },
        {
            "title": "条件概率",
            "content": "设P(A) = 0.6，P(B|A) = 0.8，则P(AB) = ____",
            "question_type": "fill_blank",
            "options": None,
            "correct_answer": "0.48",
            "explanation": "根据条件概率公式：P(AB) = P(A) × P(B|A) = 0.6 × 0.8 = 0.48",
            "difficulty": "medium",
            "points": 10
        }
    ]
    
    for q_data in questions3:
        question = Question(
            exercise_id=exercise3.id,
            title=q_data["title"],
            content=q_data["content"],
            question_type=q_data["question_type"],
            options=json.dumps(q_data["options"], ensure_ascii=False) if q_data["options"] else None,
            correct_answer=q_data["correct_answer"],
            explanation=q_data["explanation"],
            difficulty=q_data["difficulty"],
            points=q_data["points"],
            subject="概率论"
        )
        db.add(question)
    
    # 更新练习3的题目数量
    exercise3.total_questions = len(questions3)
    
    db.commit()
    
    print(f"创建练习成功:")
    print(f"- {exercise1.title}: {exercise1.total_questions} 题")
    print(f"- {exercise2.title}: {exercise2.total_questions} 题") 
    print(f"- {exercise3.title}: {exercise3.total_questions} 题")
    
    return [exercise1, exercise2, exercise3], student


def create_test_attempts(db: Session, exercises, student):
    """创建测试练习尝试数据"""
    
    # 为第一个练习创建完整的尝试记录
    exercise1 = exercises[0]
    questions1 = db.query(Question).filter(Question.exercise_id == exercise1.id).all()
    
    # 创建练习尝试
    attempt1 = ExerciseAttempt(
        exercise_id=exercise1.id,
        student_id=student.id,
        total_questions=len(questions1),
        max_score=sum(q.points for q in questions1),
        is_completed=True,
        is_submitted=True,
        started_at=datetime.now() - timedelta(hours=2),
        completed_at=datetime.now() - timedelta(hours=1, minutes=30),
        submitted_at=datetime.now() - timedelta(hours=1, minutes=30)
    )
    db.add(attempt1)
    db.commit()
    db.refresh(attempt1)
    
    # 创建答案记录
    answers_data = [
        {"question_idx": 0, "answer": "B", "is_correct": True, "time_spent": 120},
        {"question_idx": 1, "answer": "1", "is_correct": True, "time_spent": 90},
        {"question_idx": 2, "answer": "需要证明三个条件", "is_correct": False, "time_spent": 300},
        {"question_idx": 3, "answer": "C", "is_correct": True, "time_spent": 100},
        {"question_idx": 4, "answer": "x² + C", "is_correct": True, "time_spent": 80}
    ]
    
    total_score = 0
    correct_count = 0
    total_time = 0
    
    for i, answer_data in enumerate(answers_data):
        question = questions1[answer_data["question_idx"]]
        
        answer = StudentAnswer(
            attempt_id=attempt1.id,
            question_id=question.id,
            student_id=student.id,
            answer_content=answer_data["answer"],
            is_correct=answer_data["is_correct"],
            points_earned=question.points if answer_data["is_correct"] else 0,
            time_spent=answer_data["time_spent"],
            answered_at=attempt1.started_at + timedelta(seconds=sum(a["time_spent"] for a in answers_data[:i+1]))
        )
        db.add(answer)
        
        if answer_data["is_correct"]:
            correct_count += 1
            total_score += question.points
        else:
            # 创建错题记录
            wrong_question = WrongQuestion(
                student_id=student.id,
                question_id=question.id,
                wrong_answer=answer_data["answer"],
                correct_answer=question.correct_answer,
                first_wrong_at=answer.answered_at
            )
            db.add(wrong_question)
        
        total_time += answer_data["time_spent"]
    
    # 更新尝试统计
    attempt1.answered_questions = len(answers_data)
    attempt1.correct_answers = correct_count
    attempt1.score = total_score
    attempt1.time_spent = total_time
    
    db.commit()
    
    print(f"创建练习尝试成功:")
    print(f"- 练习: {exercise1.title}")
    print(f"- 学生: {student.username}")
    print(f"- 得分: {total_score}/{attempt1.max_score}")
    print(f"- 正确率: {correct_count}/{len(answers_data)}")
    print(f"- 用时: {total_time}秒")


def main():
    """主函数"""
    print("开始创建练习系统测试数据...")
    
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建测试练习
        exercises, student = create_test_exercises(db)
        
        # 创建测试尝试记录
        create_test_attempts(db, exercises, student)
        
        print("\n✅ 练习系统测试数据创建完成！")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

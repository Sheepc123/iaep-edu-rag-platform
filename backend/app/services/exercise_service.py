"""
练习系统服务层
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc, func
from fastapi import HTTPException, status
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, timedelta
import json

from ..models.exercise import (
    Exercise, Question, ExerciseAttempt, StudentAnswer, 
    WrongQuestion, ExerciseStatistics
)
from ..models.user import User
from ..schemas.exercise import (
    ExerciseCreate, ExerciseUpdate, QuestionCreate, QuestionUpdate,
    ExerciseAttemptCreate, StudentAnswerCreate, SubmitAnswerRequest,
    SubmitExerciseRequest, WrongQuestionCreate, ExerciseListQuery,
    QuestionListQuery, ExerciseCategory, QuestionType, DifficultyLevel
)


class ExerciseService:
    """练习服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ==================== 练习管理 ====================
    
    def create_exercise(self, exercise_data: ExerciseCreate, creator_id: int) -> Exercise:
        """创建练习"""
        # 验证创建者存在
        creator = self.db.query(User).filter(User.id == creator_id).first()
        if not creator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="创建者不存在"
            )
        
        # 创建练习
        exercise = Exercise(
            title=exercise_data.title,
            description=exercise_data.description,
            category=exercise_data.category,
            subject=exercise_data.subject,
            difficulty=exercise_data.difficulty,
            time_limit=exercise_data.time_limit,
            course_id=exercise_data.course_id,
            created_by=creator_id,
            is_published=exercise_data.is_published
        )
        
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        
        return exercise
    
    def get_exercise_by_id(self, exercise_id: int, include_questions: bool = False) -> Optional[Exercise]:
        """根据ID获取练习"""
        query = self.db.query(Exercise).filter(Exercise.id == exercise_id)
        
        if include_questions:
            query = query.options(joinedload(Exercise.questions))
        
        return query.first()
    
    def get_exercises(self, query_params: ExerciseListQuery, user_id: Optional[int] = None) -> Tuple[List[Exercise], int]:
        """获取练习列表"""
        query = self.db.query(Exercise).filter(Exercise.is_active == True)
        
        # 应用筛选条件
        if query_params.category:
            query = query.filter(Exercise.category == query_params.category)

        if query_params.subject:
            query = query.filter(Exercise.subject == query_params.subject)

        if query_params.difficulty:
            query = query.filter(Exercise.difficulty == query_params.difficulty)
        
        if query_params.is_published is not None:
            query = query.filter(Exercise.is_published == query_params.is_published)
        
        # 如果指定了用户ID，只返回该用户创建的练习或已发布的练习
        if user_id:
            query = query.filter(
                or_(
                    Exercise.created_by == user_id,
                    Exercise.is_published == True
                )
            )
        else:
            # 未指定用户时，只返回已发布的练习
            query = query.filter(Exercise.is_published == True)
        
        # 获取总数
        total = query.count()
        
        # 分页和排序
        exercises = query.order_by(desc(Exercise.created_at)).offset(
            (query_params.page - 1) * query_params.page_size
        ).limit(query_params.page_size).all()
        
        return exercises, total
    
    def update_exercise(self, exercise_id: int, exercise_data: ExerciseUpdate, user_id: int) -> Exercise:
        """更新练习"""
        exercise = self.get_exercise_by_id(exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )
        
        # 检查权限
        if exercise.created_by != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改此练习"
            )
        
        # 更新字段
        update_data = exercise_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(exercise, field):
                setattr(exercise, field, value)
        
        self.db.commit()
        self.db.refresh(exercise)
        
        return exercise
    
    def delete_exercise(self, exercise_id: int, user_id: int) -> bool:
        """删除练习（软删除）"""
        exercise = self.get_exercise_by_id(exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )
        
        # 检查权限
        if exercise.created_by != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此练习"
            )
        
        # 软删除
        exercise.is_active = False
        self.db.commit()
        
        return True

    def get_course_exercises(self, course_id: int, user_role: str = None) -> List[Exercise]:
        """获取指定课程的练习列表"""
        query = self.db.query(Exercise).options(
            joinedload(Exercise.questions)
        ).filter(
            and_(
                Exercise.course_id == course_id,
                Exercise.is_active == True
            )
        )

        # 学生只能看到已发布的练习，教师可以看到所有练习
        if user_role == "student":
            query = query.filter(Exercise.is_published == True)

        exercises = query.order_by(desc(Exercise.created_at)).all()
        return exercises

    # ==================== 题目管理 ====================
    
    def create_question(self, question_data: QuestionCreate, creator_id: int) -> Question:
        """创建题目"""
        # 如果指定了练习ID，验证练习存在且用户有权限
        if question_data.exercise_id:
            exercise = self.get_exercise_by_id(question_data.exercise_id)
            if not exercise:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="练习不存在"
                )
            
            if exercise.created_by != creator_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限向此练习添加题目"
                )
        
        # 创建题目
        question = Question(
            exercise_id=question_data.exercise_id,
            title=question_data.title,
            content=question_data.content,
            question_type=question_data.question_type,
            options=json.dumps(question_data.options, ensure_ascii=False) if question_data.options else None,
            correct_answer=question_data.correct_answer,
            explanation=question_data.explanation,
            difficulty=question_data.difficulty,
            points=question_data.points,
            subject=question_data.subject,
            tags=json.dumps(question_data.tags, ensure_ascii=False) if question_data.tags else None
        )
        
        self.db.add(question)
        
        # 更新练习的题目数量
        if question_data.exercise_id:
            exercise = self.get_exercise_by_id(question_data.exercise_id)
            if exercise:
                exercise.total_questions = self.db.query(Question).filter(
                    Question.exercise_id == question_data.exercise_id,
                    Question.is_active == True
                ).count() + 1
        
        self.db.commit()
        self.db.refresh(question)
        
        return question
    
    def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """根据ID获取题目"""
        return self.db.query(Question).filter(
            Question.id == question_id,
            Question.is_active == True
        ).first()
    
    def get_questions(self, query_params: QuestionListQuery) -> Tuple[List[Question], int]:
        """获取题目列表"""
        query = self.db.query(Question).filter(Question.is_active == True)
        
        # 应用筛选条件
        if query_params.exercise_id:
            query = query.filter(Question.exercise_id == query_params.exercise_id)

        if query_params.question_type:
            query = query.filter(Question.question_type == query_params.question_type)

        if query_params.difficulty:
            query = query.filter(Question.difficulty == query_params.difficulty)
        
        if query_params.subject:
            query = query.filter(Question.subject == query_params.subject)
        
        # 获取总数
        total = query.count()
        
        # 分页和排序
        questions = query.order_by(Question.id).offset(
            (query_params.page - 1) * query_params.page_size
        ).limit(query_params.page_size).all()
        
        return questions, total
    
    def update_question(self, question_id: int, question_data: QuestionUpdate, user_id: int) -> Question:
        """更新题目"""
        question = self.get_question_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="题目不存在"
            )
        
        # 检查权限（通过练习检查）
        if question.exercise_id:
            exercise = self.get_exercise_by_id(question.exercise_id)
            if exercise and exercise.created_by != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限修改此题目"
                )
        
        # 更新字段
        update_data = question_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(question, field) and value is not None:
                if field == 'options':
                    setattr(question, field, json.dumps(value, ensure_ascii=False))
                elif field == 'tags':
                    setattr(question, field, json.dumps(value, ensure_ascii=False))
                else:
                    setattr(question, field, value)
        
        self.db.commit()
        self.db.refresh(question)
        
        return question
    
    def delete_question(self, question_id: int, user_id: int) -> bool:
        """删除题目（软删除）"""
        question = self.get_question_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="题目不存在"
            )
        
        # 检查权限
        if question.exercise_id:
            exercise = self.get_exercise_by_id(question.exercise_id)
            if exercise and exercise.created_by != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限删除此题目"
                )
        
        # 软删除
        question.is_active = False
        
        # 更新练习的题目数量
        if question.exercise_id:
            exercise = self.get_exercise_by_id(question.exercise_id)
            if exercise:
                exercise.total_questions = self.db.query(Question).filter(
                    Question.exercise_id == question.exercise_id,
                    Question.is_active == True
                ).count() - 1
        
        self.db.commit()

        return True

    # ==================== 练习尝试管理 ====================

    def start_exercise_attempt(self, exercise_id: int, student_id: int) -> ExerciseAttempt:
        """开始练习尝试"""
        # 验证练习存在且已发布
        exercise = self.get_exercise_by_id(exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )

        if not exercise.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="练习尚未发布"
            )

        # 检查是否已有未完成的尝试
        existing_attempt = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.exercise_id == exercise_id,
            ExerciseAttempt.student_id == student_id,
            ExerciseAttempt.is_completed == False
        ).first()

        if existing_attempt:
            return existing_attempt

        # 计算最大分数
        max_score = self.db.query(func.sum(Question.points)).filter(
            Question.exercise_id == exercise_id,
            Question.is_active == True
        ).scalar() or 0

        # 创建新的练习尝试
        attempt = ExerciseAttempt(
            exercise_id=exercise_id,
            student_id=student_id,
            total_questions=exercise.total_questions,
            max_score=float(max_score)
        )

        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)

        return attempt

    def get_exercise_attempt(self, attempt_id: int, student_id: int) -> Optional[ExerciseAttempt]:
        """获取练习尝试"""
        return self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.id == attempt_id,
            ExerciseAttempt.student_id == student_id
        ).first()

    def get_student_attempts(self, student_id: int, exercise_id: Optional[int] = None) -> List[ExerciseAttempt]:
        """获取学生的练习尝试记录"""
        query = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.student_id == student_id
        )

        if exercise_id:
            query = query.filter(ExerciseAttempt.exercise_id == exercise_id)

        return query.order_by(desc(ExerciseAttempt.started_at)).all()

    # ==================== 答题管理 ====================

    def submit_answer(self, answer_data: SubmitAnswerRequest, student_id: int) -> StudentAnswer:
        """提交单个答案"""
        # 验证练习尝试
        attempt = self.get_exercise_attempt(answer_data.attempt_id, student_id)
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习尝试不存在"
            )

        if attempt.is_submitted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="练习已提交，无法修改答案"
            )

        # 验证题目
        question = self.get_question_by_id(answer_data.question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="题目不存在"
            )

        if question.exercise_id != attempt.exercise_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="题目不属于当前练习"
            )

        # 检查是否已有答案
        existing_answer = self.db.query(StudentAnswer).filter(
            StudentAnswer.attempt_id == answer_data.attempt_id,
            StudentAnswer.question_id == answer_data.question_id,
            StudentAnswer.student_id == student_id
        ).first()

        if existing_answer:
            # 更新现有答案
            existing_answer.answer_content = answer_data.answer_content
            existing_answer.time_spent = answer_data.time_spent
            existing_answer.answered_at = datetime.utcnow()

            # 重新评分
            self._grade_answer(existing_answer, question)

            self.db.commit()
            self.db.refresh(existing_answer)

            # 更新尝试统计
            self._update_attempt_stats(attempt)

            return existing_answer
        else:
            # 创建新答案
            answer = StudentAnswer(
                attempt_id=answer_data.attempt_id,
                question_id=answer_data.question_id,
                student_id=student_id,
                answer_content=answer_data.answer_content,
                time_spent=answer_data.time_spent
            )

            # 评分
            self._grade_answer(answer, question)

            self.db.add(answer)
            self.db.commit()
            self.db.refresh(answer)

            # 更新尝试统计
            self._update_attempt_stats(attempt)

            return answer

    def submit_exercise(self, submit_data: SubmitExerciseRequest, student_id: int) -> ExerciseAttempt:
        """提交整个练习"""
        # 验证练习尝试
        attempt = self.get_exercise_attempt(submit_data.attempt_id, student_id)
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习尝试不存在"
            )

        if attempt.is_submitted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="练习已提交"
            )

        # 批量提交答案
        for answer_data in submit_data.answers:
            answer_request = SubmitAnswerRequest(
                attempt_id=submit_data.attempt_id,
                question_id=answer_data.question_id,
                answer_content=answer_data.answer_content,
                time_spent=answer_data.time_spent
            )
            self.submit_answer(answer_request, student_id)

        # 标记为已提交
        attempt.is_submitted = True
        attempt.is_completed = True
        attempt.submitted_at = datetime.utcnow()
        attempt.completed_at = datetime.utcnow()

        # 最终统计更新
        self._update_attempt_stats(attempt)

        # 更新练习统计
        self._update_exercise_stats(attempt.exercise_id)

        # 更新题目统计
        self._update_question_stats(attempt)

        # 处理错题
        self._process_wrong_answers(attempt)

        self.db.commit()
        self.db.refresh(attempt)

        return attempt

    # ==================== 辅助方法 ====================

    def _grade_answer(self, answer: StudentAnswer, question: Question):
        """评分答案"""
        # 简单的字符串匹配评分（可以扩展为更复杂的评分逻辑）
        if question.question_type == "multiple_choice":
            # 选择题：完全匹配
            is_correct = answer.answer_content.strip().upper() == question.correct_answer.strip().upper()
        elif question.question_type == "fill_blank":
            # 填空题：去除空格后匹配
            is_correct = answer.answer_content.strip() == question.correct_answer.strip()
        else:
            # 问答题：需要人工评分，暂时标记为None
            is_correct = None

        answer.is_correct = is_correct
        answer.points_earned = question.points if is_correct else 0.0

    def _update_attempt_stats(self, attempt: ExerciseAttempt):
        """更新练习尝试统计"""
        # 获取所有答案
        answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.attempt_id == attempt.id
        ).all()

        # 统计数据
        attempt.answered_questions = len(answers)
        attempt.correct_answers = sum(1 for a in answers if a.is_correct)
        attempt.score = sum(a.points_earned for a in answers)
        attempt.time_spent = sum(a.time_spent for a in answers)

    def _update_exercise_stats(self, exercise_id: int):
        """更新练习统计"""
        exercise = self.get_exercise_by_id(exercise_id)
        if not exercise:
            return

        # 获取所有已提交的尝试
        attempts = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.exercise_id == exercise_id,
            ExerciseAttempt.is_submitted == True
        ).all()

        if attempts:
            exercise.total_attempts = len(attempts)
            exercise.average_score = sum(a.score for a in attempts) / len(attempts)

    def _update_question_stats(self, attempt: ExerciseAttempt):
        """更新题目统计"""
        answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.attempt_id == attempt.id
        ).all()

        for answer in answers:
            question = self.get_question_by_id(answer.question_id)
            if question:
                question.total_attempts += 1
                if answer.is_correct:
                    question.correct_attempts += 1

    def _process_wrong_answers(self, attempt: ExerciseAttempt):
        """处理错题，添加到错题本"""
        wrong_answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.attempt_id == attempt.id,
            StudentAnswer.is_correct == False
        ).all()

        for answer in wrong_answers:
            question = self.get_question_by_id(answer.question_id)
            if question:
                # 检查是否已存在错题记录
                existing_wrong = self.db.query(WrongQuestion).filter(
                    WrongQuestion.student_id == attempt.student_id,
                    WrongQuestion.question_id == answer.question_id
                ).first()

                if not existing_wrong:
                    # 创建新的错题记录
                    wrong_question = WrongQuestion(
                        student_id=attempt.student_id,
                        question_id=answer.question_id,
                        wrong_answer=answer.answer_content,
                        correct_answer=question.correct_answer
                    )
                    self.db.add(wrong_question)

    # ==================== 错题本管理 ====================

    def get_wrong_questions(self, student_id: int, subject: Optional[str] = None) -> List[WrongQuestion]:
        """获取学生错题本"""
        query = self.db.query(WrongQuestion).filter(
            WrongQuestion.student_id == student_id,
            WrongQuestion.is_mastered == False
        )

        if subject:
            # 通过关联的题目筛选科目
            query = query.join(Question).filter(Question.subject == subject)

        return query.order_by(desc(WrongQuestion.first_wrong_at)).all()

    def mark_question_mastered(self, student_id: int, question_id: int) -> bool:
        """标记题目已掌握"""
        wrong_question = self.db.query(WrongQuestion).filter(
            WrongQuestion.student_id == student_id,
            WrongQuestion.question_id == question_id
        ).first()

        if wrong_question:
            wrong_question.is_mastered = True
            wrong_question.mastered_at = datetime.now()
            self.db.commit()
            return True

        return False

    def review_wrong_question(self, student_id: int, question_id: int) -> bool:
        """复习错题"""
        wrong_question = self.db.query(WrongQuestion).filter(
            WrongQuestion.student_id == student_id,
            WrongQuestion.question_id == question_id
        ).first()

        if wrong_question:
            wrong_question.review_count += 1
            wrong_question.last_review_at = datetime.now()
            self.db.commit()
            return True

        return False

    # ==================== 统计分析 ====================

    def get_exercise_stats(self, student_id: int) -> Dict[str, Any]:
        """获取学生练习统计"""
        # 基础统计
        total_attempts = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.student_id == student_id
        ).count()

        completed_attempts = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.student_id == student_id,
            ExerciseAttempt.is_completed == True
        ).count()

        # 答题统计
        total_answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.student_id == student_id
        ).count()

        correct_answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.student_id == student_id,
            StudentAnswer.is_correct == True
        ).count()

        # 时间统计（分钟）
        total_time = self.db.query(func.sum(ExerciseAttempt.time_spent)).filter(
            ExerciseAttempt.student_id == student_id,
            ExerciseAttempt.is_completed == True
        ).scalar() or 0
        total_time_minutes = total_time // 60

        # 计算平均正确率
        accuracy_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0.0

        # 按科目统计
        subject_stats = self._get_subject_stats(student_id)

        return {
            "total_exercises": total_attempts,
            "completed_exercises": completed_attempts,
            "total_questions": total_answers,
            "correct_questions": correct_answers,
            "total_time": total_time_minutes,
            "average_accuracy": round(accuracy_rate, 2),
            "subject_stats": subject_stats
        }

    def get_daily_stats(self, student_id: int, date: datetime) -> Dict[str, Any]:
        """获取指定日期的练习统计"""
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)

        # 当日完成的练习
        completed_exercises = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.student_id == student_id,
            ExerciseAttempt.is_completed == True,
            ExerciseAttempt.completed_at >= start_date,
            ExerciseAttempt.completed_at < end_date
        ).count()

        # 当日答题统计
        daily_answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.student_id == student_id,
            StudentAnswer.answered_at >= start_date,
            StudentAnswer.answered_at < end_date
        ).all()

        questions_answered = len(daily_answers)
        correct_answers = sum(1 for a in daily_answers if a.is_correct)
        time_spent = sum(a.time_spent for a in daily_answers) // 60  # 转换为分钟

        accuracy_rate = (correct_answers / questions_answered * 100) if questions_answered > 0 else 0.0

        return {
            "date": date,
            "exercises_completed": completed_exercises,
            "questions_answered": questions_answered,
            "correct_answers": correct_answers,
            "time_spent": time_spent,
            "accuracy_rate": round(accuracy_rate, 2)
        }

    def get_category_stats(self, student_id: int) -> List[Dict[str, Any]]:
        """获取按分类的练习统计"""
        stats = []

        for category in ExerciseCategory:
            # 该分类的练习尝试
            attempts = self.db.query(ExerciseAttempt).join(Exercise).filter(
                ExerciseAttempt.student_id == student_id,
                Exercise.category == category
            ).all()

            completed_attempts = [a for a in attempts if a.is_completed]

            # 计算统计数据
            total_count = len(attempts)
            completed_count = len(completed_attempts)

            if completed_attempts:
                total_time = sum(a.time_spent for a in completed_attempts) // 60
                accuracy_rates = []
                for attempt in completed_attempts:
                    if attempt.answered_questions > 0:
                        accuracy_rates.append(attempt.correct_answers / attempt.answered_questions * 100)

                average_accuracy = sum(accuracy_rates) / len(accuracy_rates) if accuracy_rates else 0.0
            else:
                total_time = 0
                average_accuracy = 0.0

            stats.append({
                "category": category,
                "total_count": total_count,
                "completed_count": completed_count,
                "average_accuracy": round(average_accuracy, 2),
                "total_time": total_time
            })

        return stats

    def _get_subject_stats(self, student_id: int) -> Dict[str, Any]:
        """获取按科目的统计"""
        # 获取所有科目
        subjects = self.db.query(Exercise.subject).distinct().all()
        subject_stats = {}

        for (subject,) in subjects:
            # 该科目的练习尝试
            attempts = self.db.query(ExerciseAttempt).join(Exercise).filter(
                ExerciseAttempt.student_id == student_id,
                Exercise.subject == subject,
                ExerciseAttempt.is_completed == True
            ).all()

            if attempts:
                total_questions = sum(a.answered_questions for a in attempts)
                correct_questions = sum(a.correct_answers for a in attempts)
                total_time = sum(a.time_spent for a in attempts) // 60

                accuracy = (correct_questions / total_questions * 100) if total_questions > 0 else 0.0

                subject_stats[subject] = {
                    "exercises": len(attempts),
                    "questions": total_questions,
                    "correct": correct_questions,
                    "accuracy": round(accuracy, 2),
                    "time": total_time
                }

        return subject_stats

    def get_learning_progress(self, student_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """获取学习进度趋势"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        progress = []
        current_date = start_date

        while current_date <= end_date:
            daily_stats = self.get_daily_stats(student_id, current_date)
            progress.append(daily_stats)
            current_date += timedelta(days=1)

        return progress

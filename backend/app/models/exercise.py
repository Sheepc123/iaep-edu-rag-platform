"""
练习系统相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Exercise(Base):
    """练习集模型"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # 练习属性
    category = Column(String(50), nullable=False)  # 自主练习、课后作业、错题本、模拟考试
    subject = Column(String(50), nullable=False)   # 科目
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    
    # 时间限制
    time_limit = Column(Integer, nullable=True)  # 时间限制(分钟)
    
    # 创建者
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 统计信息
    total_questions = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    questions = relationship("Question", back_populates="exercise")
    attempts = relationship("ExerciseAttempt", back_populates="exercise")


class Question(Base):
    """题目模型"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=True)
    
    # 题目内容
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)  # multiple_choice, fill_blank, essay
    
    # 选择题选项 (JSON格式)
    options = Column(JSON, nullable=True)
    
    # 答案和解析
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    
    # 题目属性
    difficulty = Column(String(20), default="medium")
    points = Column(Integer, default=10)
    subject = Column(String(50), nullable=True)
    tags = Column(Text, nullable=True)  # JSON格式存储标签
    
    # 统计信息
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    exercise = relationship("Exercise", back_populates="questions")
    answers = relationship("StudentAnswer", back_populates="question")


class ExerciseAttempt(Base):
    """练习尝试记录模型"""
    __tablename__ = "exercise_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 答题信息
    total_questions = Column(Integer, nullable=False)
    answered_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    
    # 分数和时间
    score = Column(Float, default=0.0)
    max_score = Column(Float, nullable=False)
    time_spent = Column(Integer, default=0)  # 用时(秒)
    
    # 状态
    is_completed = Column(Boolean, default=False)
    is_submitted = Column(Boolean, default=False)
    
    # 时间戳
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    exercise = relationship("Exercise", back_populates="attempts")
    answers = relationship("StudentAnswer", back_populates="attempt")


class StudentAnswer(Base):
    """学生答案模型"""
    __tablename__ = "student_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exercise_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 答案内容
    answer_content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=True)
    points_earned = Column(Float, default=0.0)
    
    # 答题时间
    time_spent = Column(Integer, default=0)  # 答题用时(秒)
    
    # 时间戳
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    attempt = relationship("ExerciseAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")


class WrongQuestion(Base):
    """错题本模型"""
    __tablename__ = "wrong_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    
    # 错误信息
    wrong_answer = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    mistake_type = Column(String(50), nullable=True)  # 错误类型
    
    # 复习状态
    review_count = Column(Integer, default=0)
    is_mastered = Column(Boolean, default=False)
    
    # 时间戳
    first_wrong_at = Column(DateTime(timezone=True), server_default=func.now())
    last_review_at = Column(DateTime(timezone=True), nullable=True)
    mastered_at = Column(DateTime(timezone=True), nullable=True)


class ExerciseStatistics(Base):
    """练习统计模型"""
    __tablename__ = "exercise_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 日期
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # 统计数据
    total_exercises = Column(Integer, default=0)
    completed_exercises = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    correct_questions = Column(Integer, default=0)
    total_time = Column(Integer, default=0)  # 总用时(分钟)
    
    # 按科目统计 (JSON格式)
    subject_stats = Column(JSON, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

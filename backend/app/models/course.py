"""
课程相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Course(Base):
    """课程模型"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    cover_image = Column(String(255), nullable=True)
    
    # 课程属性
    category = Column(String(50), nullable=True)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    duration = Column(Integer, nullable=True)  # 课程总时长(分钟)
    total_lessons = Column(Integer, default=0)
    
    # 教师信息
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instructor_name = Column(String(100), nullable=False)
    
    # 统计信息
    enrolled_students = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("CourseEnrollment", back_populates="course")
    exercises = relationship("Exercise", back_populates="course")


class Lesson(Base):
    """课时模型"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # 基本信息
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    
    # 课时属性
    lesson_order = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=True)  # 课时时长(分钟)
    lesson_type = Column(String(20), default="video")  # video, text, interactive
    
    # 资源文件
    video_url = Column(String(255), nullable=True)
    materials = Column(Text, nullable=True)  # JSON格式存储材料列表
    
    # 状态
    is_published = Column(Boolean, default=False)
    is_free = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    course = relationship("Course", back_populates="lessons")
    progress_records = relationship("LessonProgress", back_populates="lesson")


class CourseEnrollment(Base):
    """课程注册模型"""
    __tablename__ = "course_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 学习进度
    progress_percentage = Column(Float, default=0.0)
    completed_lessons = Column(Integer, default=0)
    total_study_time = Column(Integer, default=0)  # 学习时间(分钟)
    
    # 评价
    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)
    
    # 状态
    is_completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    course = relationship("Course", back_populates="enrollments")


class LessonProgress(Base):
    """课时学习进度模型"""
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 进度信息
    progress_percentage = Column(Float, default=0.0)
    watch_time = Column(Integer, default=0)  # 观看时间(秒)
    is_completed = Column(Boolean, default=False)
    
    # 学习记录
    notes = Column(Text, nullable=True)
    bookmarks = Column(Text, nullable=True)  # JSON格式存储书签
    
    # 时间戳
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    lesson = relationship("Lesson", back_populates="progress_records")


class CourseCategory(Base):
    """课程分类模型"""
    __tablename__ = "course_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 分类信息
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    color = Column(String(20), nullable=True)
    
    # 层级关系
    parent_id = Column(Integer, ForeignKey("course_categories.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StudyPlan(Base):
    """学习计划模型"""
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 计划信息
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_courses = Column(Text, nullable=True)  # JSON格式存储目标课程
    
    # 时间安排
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    daily_study_time = Column(Integer, default=60)  # 每日学习时间(分钟)
    
    # 进度
    progress_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

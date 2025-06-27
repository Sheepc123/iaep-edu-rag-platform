"""
用户相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    """用户基础模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 基本信息
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar = Column(String(255), nullable=True)
    
    # 角色和状态
    role = Column(String(20), default="student", nullable=False)  # student, teacher, admin
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    teacher_profile = relationship("TeacherProfile", back_populates="user", uselist=False)
    knowledge_docs = relationship("TeacherKnowledgeDoc", back_populates="teacher")


class StudentProfile(Base):
    """学生档案模型"""
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # 学生信息
    student_id = Column(String(20), unique=True, nullable=True)  # 学号
    school = Column(String(100), nullable=True)
    college = Column(String(100), nullable=True)
    major = Column(String(100), nullable=True)
    grade = Column(String(20), nullable=True)
    class_name = Column(String(50), nullable=True)
    
    # 学习统计
    total_study_time = Column(Integer, default=0)  # 总学习时间(分钟)
    total_exercises = Column(Integer, default=0)   # 总练习题数
    correct_exercises = Column(Integer, default=0) # 正确题数
    total_courses = Column(Integer, default=0)     # 总课程数
    completed_courses = Column(Integer, default=0) # 完成课程数
    
    # 学习偏好
    preferred_subjects = Column(Text, nullable=True)  # JSON格式存储
    learning_goals = Column(Text, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="student_profile")


class TeacherProfile(Base):
    """教师档案模型"""
    __tablename__ = "teacher_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # 教师信息
    teacher_id = Column(String(20), unique=True, nullable=True)  # 工号
    department = Column(String(100), nullable=True)
    title = Column(String(50), nullable=True)  # 职称
    specialization = Column(String(200), nullable=True)  # 专业领域
    
    # 教学统计
    total_courses = Column(Integer, default=0)
    total_students = Column(Integer, default=0)
    teaching_years = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # 简介
    bio = Column(Text, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="teacher_profile")


class UserSession(Base):
    """用户会话模型"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 会话信息
    session_token = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(500), nullable=False)
    device_info = Column(String(200), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_used = Column(DateTime(timezone=True), server_default=func.now())


class UserActivity(Base):
    """用户活动记录模型"""
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 活动信息
    activity_type = Column(String(50), nullable=False)  # login, logout, study, exercise, etc.
    activity_data = Column(Text, nullable=True)  # JSON格式存储详细数据
    duration = Column(Integer, nullable=True)  # 活动持续时间(秒)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())

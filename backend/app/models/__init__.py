"""
数据模型模块初始化
"""

# 导入所有模型类，确保SQLAlchemy能够发现它们
from .user import User, StudentProfile, TeacherProfile, UserSession, UserActivity
from .course import Course, Lesson, CourseEnrollment, LessonProgress, CourseCategory, StudyPlan
from .exercise import Exercise, Question, ExerciseAttempt, StudentAnswer, WrongQuestion, ExerciseStatistics
from .chat import (
    ChatRoom, ChatMember, ChatMessage, UserContact,
    AIConversation, AIMessage, AIRecommendation, UserOnlineStatus
)

# 导出所有模型类
__all__ = [
    # 用户相关模型
    "User",
    "StudentProfile", 
    "TeacherProfile",
    "UserSession",
    "UserActivity",
    
    # 课程相关模型
    "Course",
    "Lesson",
    "CourseEnrollment",
    "LessonProgress",
    "CourseCategory",
    "StudyPlan",
    
    # 练习相关模型
    "Exercise",
    "Question",
    "ExerciseAttempt",
    "StudentAnswer",
    "WrongQuestion",
    "ExerciseStatistics",
    
    # 聊天和AI相关模型
    "ChatRoom",
    "ChatMember", 
    "ChatMessage",
    "UserContact",
    "AIConversation",
    "AIMessage",
    "AIRecommendation",
    "UserOnlineStatus",
]

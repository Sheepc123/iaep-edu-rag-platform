"""
数据验证模式模块初始化
"""

from .auth import (
    UserRegister, UserLogin, TokenResponse, TokenRefresh,
    PasswordChange, UserInfo, AuthResponse, UserUpdate,
    StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse
)

from .course import (
    CourseCreate, CourseUpdate, CourseResponse, CourseListQuery,
    LessonCreate, LessonUpdate, LessonResponse,
    CourseEnrollRequest, CourseEnrollResponse,
    LessonProgressUpdate, LessonProgressResponse,
    CourseRatingCreate, CourseStatistics, StudyPlanCreate,
    DifficultyLevel, LessonType
)

__all__ = [
    # 认证相关
    "UserRegister",
    "UserLogin",
    "TokenResponse",
    "TokenRefresh",
    "PasswordChange",
    "UserInfo",
    "AuthResponse",
    "UserUpdate",
    "StudentProfileCreate",
    "StudentProfileUpdate",
    "StudentProfileResponse",

    # 课程相关
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "CourseListQuery",
    "LessonCreate",
    "LessonUpdate",
    "LessonResponse",
    "CourseEnrollRequest",
    "CourseEnrollResponse",
    "LessonProgressUpdate",
    "LessonProgressResponse",
    "CourseRatingCreate",
    "CourseStatistics",
    "StudyPlanCreate",
    "DifficultyLevel",
    "LessonType"
]

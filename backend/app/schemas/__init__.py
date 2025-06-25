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

from .exercise import (
    # 枚举类型
    QuestionType, ExerciseCategory, ExerciseStatus,
    # 题目相关
    QuestionBase, QuestionCreate, QuestionUpdate, QuestionResponse,
    # 练习相关
    ExerciseBase, ExerciseCreate, ExerciseUpdate, ExerciseResponse, ExerciseDetailResponse,
    # 答题相关
    StudentAnswerBase, StudentAnswerCreate, StudentAnswerUpdate, StudentAnswerResponse,
    # 练习尝试相关
    ExerciseAttemptBase, ExerciseAttemptCreate, ExerciseAttemptUpdate,
    ExerciseAttemptResponse, ExerciseAttemptDetailResponse,
    # 提交相关
    SubmitAnswerRequest, SubmitExerciseRequest, SubmitExerciseResponse,
    # 错题本相关
    WrongQuestionBase, WrongQuestionCreate, WrongQuestionResponse,
    # 统计相关
    ExerciseStatsResponse, DailyStatsResponse, ExerciseCategoryStatsResponse,
    # 查询参数
    ExerciseListQuery, QuestionListQuery
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
    "LessonType",

    # 练习系统相关
    # 枚举类型
    "QuestionType",
    "ExerciseCategory",
    "ExerciseStatus",
    # 题目相关
    "QuestionBase",
    "QuestionCreate",
    "QuestionUpdate",
    "QuestionResponse",
    # 练习相关
    "ExerciseBase",
    "ExerciseCreate",
    "ExerciseUpdate",
    "ExerciseResponse",
    "ExerciseDetailResponse",
    # 答题相关
    "StudentAnswerBase",
    "StudentAnswerCreate",
    "StudentAnswerUpdate",
    "StudentAnswerResponse",
    # 练习尝试相关
    "ExerciseAttemptBase",
    "ExerciseAttemptCreate",
    "ExerciseAttemptUpdate",
    "ExerciseAttemptResponse",
    "ExerciseAttemptDetailResponse",
    # 提交相关
    "SubmitAnswerRequest",
    "SubmitExerciseRequest",
    "SubmitExerciseResponse",
    # 错题本相关
    "WrongQuestionBase",
    "WrongQuestionCreate",
    "WrongQuestionResponse",
    # 统计相关
    "ExerciseStatsResponse",
    "DailyStatsResponse",
    "ExerciseCategoryStatsResponse",
    # 查询参数
    "ExerciseListQuery",
    "QuestionListQuery"
]

"""
练习系统数据验证模式
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    """难度级别枚举"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    """题目类型枚举"""
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"


class ExerciseCategory(str, Enum):
    """练习分类枚举"""
    SELF_PRACTICE = "自主练习"
    HOMEWORK = "课后作业"
    WRONG_QUESTIONS = "错题本"
    MOCK_EXAM = "模拟考试"


class ExerciseStatus(str, Enum):
    """练习状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"


# ==================== 题目相关模式 ====================

class QuestionBase(BaseModel):
    """题目基础模式"""
    title: Optional[str] = Field(None, max_length=200, description="题目标题")
    content: str = Field(..., description="题目内容")
    question_type: QuestionType = Field(..., description="题目类型")
    options: Optional[List[str]] = Field(None, description="选择题选项")
    correct_answer: str = Field(..., description="正确答案")
    explanation: Optional[str] = Field(None, description="答案解析")
    difficulty: DifficultyLevel = Field(DifficultyLevel.MEDIUM, description="难度级别")
    points: int = Field(10, ge=1, le=100, description="题目分值")
    subject: Optional[str] = Field(None, max_length=50, description="科目")
    tags: Optional[List[str]] = Field(None, description="题目标签")

    @validator('options')
    def validate_options(cls, v, values):
        """验证选择题选项"""
        if values.get('question_type') == QuestionType.MULTIPLE_CHOICE:
            if not v or len(v) < 2:
                raise ValueError('选择题必须至少有2个选项')
        return v


class QuestionCreate(QuestionBase):
    """创建题目模式"""
    exercise_id: Optional[int] = Field(None, description="所属练习ID")


class QuestionUpdate(BaseModel):
    """更新题目模式"""
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    question_type: Optional[QuestionType] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    points: Optional[int] = Field(None, ge=1, le=100)
    subject: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class QuestionResponse(QuestionBase):
    """题目响应模式"""
    id: int
    exercise_id: Optional[int]
    total_attempts: int = 0
    correct_attempts: int = 0
    accuracy_rate: float = 0.0
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

    @property
    def accuracy_rate(self) -> float:
        """计算正确率"""
        if self.total_attempts == 0:
            return 0.0
        return round((self.correct_attempts / self.total_attempts) * 100, 2)


# ==================== 练习相关模式 ====================

class ExerciseBase(BaseModel):
    """练习基础模式"""
    title: str = Field(..., max_length=200, description="练习标题")
    description: Optional[str] = Field(None, description="练习描述")
    category: ExerciseCategory = Field(..., description="练习分类")
    subject: str = Field(..., max_length=50, description="科目")
    difficulty: DifficultyLevel = Field(DifficultyLevel.MEDIUM, description="难度级别")
    time_limit: Optional[int] = Field(None, ge=1, description="时间限制(分钟)")


class ExerciseCreate(ExerciseBase):
    """创建练习模式"""
    is_published: bool = Field(False, description="是否发布")


class ExerciseUpdate(BaseModel):
    """更新练习模式"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category: Optional[ExerciseCategory] = None
    subject: Optional[str] = Field(None, max_length=50)
    difficulty: Optional[DifficultyLevel] = None
    time_limit: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None


class ExerciseResponse(ExerciseBase):
    """练习响应模式"""
    id: int
    created_by: int
    total_questions: int = 0
    total_attempts: int = 0
    average_score: float = 0.0
    is_active: bool = True
    is_published: bool = False
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ExerciseDetailResponse(ExerciseResponse):
    """练习详情响应模式"""
    questions: List[QuestionResponse] = []


# ==================== 答题相关模式 ====================

class StudentAnswerBase(BaseModel):
    """学生答案基础模式"""
    question_id: int = Field(..., description="题目ID")
    answer_content: str = Field(..., description="答案内容")
    time_spent: int = Field(0, ge=0, description="答题用时(秒)")


class StudentAnswerCreate(StudentAnswerBase):
    """创建学生答案模式"""
    pass


class StudentAnswerUpdate(BaseModel):
    """更新学生答案模式"""
    answer_content: Optional[str] = None
    time_spent: Optional[int] = Field(None, ge=0)


class StudentAnswerResponse(StudentAnswerBase):
    """学生答案响应模式"""
    id: int
    attempt_id: int
    student_id: int
    is_correct: Optional[bool]
    points_earned: float = 0.0
    answered_at: datetime

    class Config:
        from_attributes = True


# ==================== 练习尝试相关模式 ====================

class ExerciseAttemptBase(BaseModel):
    """练习尝试基础模式"""
    exercise_id: int = Field(..., description="练习ID")


class ExerciseAttemptCreate(ExerciseAttemptBase):
    """创建练习尝试模式"""
    pass


class ExerciseAttemptUpdate(BaseModel):
    """更新练习尝试模式"""
    is_completed: Optional[bool] = None
    is_submitted: Optional[bool] = None


class ExerciseAttemptResponse(ExerciseAttemptBase):
    """练习尝试响应模式"""
    id: int
    student_id: int
    total_questions: int
    answered_questions: int = 0
    correct_answers: int = 0
    score: float = 0.0
    max_score: float
    time_spent: int = 0
    is_completed: bool = False
    is_submitted: bool = False
    started_at: datetime
    completed_at: Optional[datetime]
    submitted_at: Optional[datetime]

    class Config:
        from_attributes = True

    @property
    def accuracy_rate(self) -> float:
        """计算正确率"""
        if self.answered_questions == 0:
            return 0.0
        return round((self.correct_answers / self.answered_questions) * 100, 2)

    @property
    def completion_rate(self) -> float:
        """计算完成率"""
        if self.total_questions == 0:
            return 0.0
        return round((self.answered_questions / self.total_questions) * 100, 2)


class ExerciseAttemptDetailResponse(ExerciseAttemptResponse):
    """练习尝试详情响应模式"""
    exercise: ExerciseResponse
    answers: List[StudentAnswerResponse] = []


# ==================== 提交答案相关模式 ====================

class SubmitAnswerRequest(BaseModel):
    """提交答案请求模式"""
    attempt_id: int = Field(..., description="练习尝试ID")
    question_id: int = Field(..., description="题目ID")
    answer_content: str = Field(..., description="答案内容")
    time_spent: int = Field(0, ge=0, description="答题用时(秒)")


class SubmitExerciseRequest(BaseModel):
    """提交练习请求模式"""
    attempt_id: int = Field(..., description="练习尝试ID")
    answers: List[StudentAnswerCreate] = Field(..., description="所有答案")


class SubmitExerciseResponse(BaseModel):
    """提交练习响应模式"""
    attempt_id: int
    total_questions: int
    answered_questions: int
    correct_answers: int
    score: float
    max_score: float
    accuracy_rate: float
    time_spent: int
    submitted_at: datetime


# ==================== 错题本相关模式 ====================

class WrongQuestionBase(BaseModel):
    """错题基础模式"""
    question_id: int = Field(..., description="题目ID")
    wrong_answer: str = Field(..., description="错误答案")
    correct_answer: str = Field(..., description="正确答案")
    mistake_type: Optional[str] = Field(None, max_length=50, description="错误类型")


class WrongQuestionCreate(WrongQuestionBase):
    """创建错题模式"""
    pass


class WrongQuestionResponse(WrongQuestionBase):
    """错题响应模式"""
    id: int
    student_id: int
    review_count: int = 0
    is_mastered: bool = False
    first_wrong_at: datetime
    last_review_at: Optional[datetime]
    mastered_at: Optional[datetime]

    class Config:
        from_attributes = True


# ==================== 统计相关模式 ====================

class ExerciseStatsResponse(BaseModel):
    """练习统计响应模式"""
    total_exercises: int = 0
    completed_exercises: int = 0
    total_questions: int = 0
    correct_questions: int = 0
    total_time: int = 0  # 分钟
    average_accuracy: float = 0.0
    subject_stats: Dict[str, Any] = {}


class DailyStatsResponse(BaseModel):
    """每日统计响应模式"""
    date: datetime
    exercises_completed: int = 0
    questions_answered: int = 0
    correct_answers: int = 0
    time_spent: int = 0  # 分钟
    accuracy_rate: float = 0.0


class ExerciseCategoryStatsResponse(BaseModel):
    """练习分类统计响应模式"""
    category: ExerciseCategory
    total_count: int = 0
    completed_count: int = 0
    average_accuracy: float = 0.0
    total_time: int = 0  # 分钟


# ==================== 查询参数模式 ====================

class ExerciseListQuery(BaseModel):
    """练习列表查询参数"""
    category: Optional[ExerciseCategory] = None
    subject: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    status: Optional[ExerciseStatus] = None
    is_published: Optional[bool] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class QuestionListQuery(BaseModel):
    """题目列表查询参数"""
    exercise_id: Optional[int] = None
    question_type: Optional[QuestionType] = None
    difficulty: Optional[DifficultyLevel] = None
    subject: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

"""
课程相关的数据验证模式
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    """难度级别枚举"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class LessonType(str, Enum):
    """课时类型枚举"""
    VIDEO = "video"
    TEXT = "text"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"


class CourseCreate(BaseModel):
    """课程创建请求模式"""
    title: str = Field(..., min_length=1, max_length=200, description="课程标题")
    description: Optional[str] = Field(None, max_length=2000, description="课程描述")
    category: Optional[str] = Field(None, max_length=50, description="课程分类")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="难度级别")
    duration: Optional[int] = Field(None, gt=0, description="课程总时长(分钟)")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图片URL")
    is_published: bool = Field(default=False, description="是否发布")
    
    @validator('title')
    def validate_title(cls, v):
        """验证课程标题"""
        if not v.strip():
            raise ValueError('课程标题不能为空')
        return v.strip()


class CourseUpdate(BaseModel):
    """课程更新请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="课程标题")
    description: Optional[str] = Field(None, max_length=2000, description="课程描述")
    category: Optional[str] = Field(None, max_length=50, description="课程分类")
    difficulty: Optional[DifficultyLevel] = Field(None, description="难度级别")
    duration: Optional[int] = Field(None, gt=0, description="课程总时长(分钟)")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图片URL")
    is_published: Optional[bool] = Field(None, description="是否发布")
    
    @validator('title')
    def validate_title(cls, v):
        """验证课程标题"""
        if v is not None and not v.strip():
            raise ValueError('课程标题不能为空')
        return v.strip() if v else v


class CourseResponse(BaseModel):
    """课程响应模式"""
    id: int = Field(..., description="课程ID")
    title: str = Field(..., description="课程标题")
    description: Optional[str] = Field(None, description="课程描述")
    cover_image: Optional[str] = Field(None, description="封面图片URL")
    category: Optional[str] = Field(None, description="课程分类")
    difficulty: str = Field(..., description="难度级别")
    duration: Optional[int] = Field(None, description="课程总时长(分钟)")
    total_lessons: int = Field(..., description="总课时数")
    instructor_id: int = Field(..., description="教师ID")
    instructor_name: str = Field(..., description="教师姓名")
    enrolled_students: int = Field(..., description="注册学生数")
    rating: float = Field(..., description="课程评分")
    rating_count: int = Field(..., description="评分人数")
    is_active: bool = Field(..., description="是否激活")
    is_published: bool = Field(..., description="是否发布")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True


class LessonCreate(BaseModel):
    """课时创建请求模式"""
    title: str = Field(..., min_length=1, max_length=200, description="课时标题")
    description: Optional[str] = Field(None, max_length=1000, description="课时描述")
    content: Optional[str] = Field(None, description="课时内容")
    lesson_order: int = Field(..., ge=1, description="课时顺序")
    duration: Optional[int] = Field(None, gt=0, description="课时时长(分钟)")
    lesson_type: LessonType = Field(default=LessonType.VIDEO, description="课时类型")
    video_url: Optional[str] = Field(None, max_length=255, description="视频URL")
    materials: Optional[str] = Field(None, description="学习材料(JSON格式)")
    is_published: bool = Field(default=False, description="是否发布")
    is_free: bool = Field(default=False, description="是否免费")
    
    @validator('title')
    def validate_title(cls, v):
        """验证课时标题"""
        if not v.strip():
            raise ValueError('课时标题不能为空')
        return v.strip()


class LessonUpdate(BaseModel):
    """课时更新请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="课时标题")
    description: Optional[str] = Field(None, max_length=1000, description="课时描述")
    content: Optional[str] = Field(None, description="课时内容")
    lesson_order: Optional[int] = Field(None, ge=1, description="课时顺序")
    duration: Optional[int] = Field(None, gt=0, description="课时时长(分钟)")
    lesson_type: Optional[LessonType] = Field(None, description="课时类型")
    video_url: Optional[str] = Field(None, max_length=255, description="视频URL")
    materials: Optional[str] = Field(None, description="学习材料(JSON格式)")
    is_published: Optional[bool] = Field(None, description="是否发布")
    is_free: Optional[bool] = Field(None, description="是否免费")
    
    @validator('title')
    def validate_title(cls, v):
        """验证课时标题"""
        if v is not None and not v.strip():
            raise ValueError('课时标题不能为空')
        return v.strip() if v else v


class LessonResponse(BaseModel):
    """课时响应模式"""
    id: int = Field(..., description="课时ID")
    course_id: int = Field(..., description="课程ID")
    title: str = Field(..., description="课时标题")
    description: Optional[str] = Field(None, description="课时描述")
    content: Optional[str] = Field(None, description="课时内容")
    lesson_order: int = Field(..., description="课时顺序")
    duration: Optional[int] = Field(None, description="课时时长(分钟)")
    lesson_type: str = Field(..., description="课时类型")
    video_url: Optional[str] = Field(None, description="视频URL")
    materials: Optional[str] = Field(None, description="学习材料")
    is_published: bool = Field(..., description="是否发布")
    is_free: bool = Field(..., description="是否免费")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True


class CourseEnrollRequest(BaseModel):
    """课程注册请求模式"""
    course_id: int = Field(..., description="课程ID")


class CourseEnrollResponse(BaseModel):
    """课程注册响应模式"""
    id: int = Field(..., description="注册ID")
    course_id: int = Field(..., description="课程ID")
    student_id: int = Field(..., description="学生ID")
    progress_percentage: float = Field(..., description="学习进度百分比")
    completed_lessons: int = Field(..., description="已完成课时数")
    total_study_time: int = Field(..., description="总学习时间(分钟)")
    is_completed: bool = Field(..., description="是否完成")
    enrolled_at: datetime = Field(..., description="注册时间")
    last_accessed: Optional[datetime] = Field(None, description="最后访问时间")
    
    class Config:
        from_attributes = True


class LessonProgressUpdate(BaseModel):
    """课时进度更新请求模式"""
    progress_percentage: float = Field(..., ge=0, le=100, description="进度百分比")
    watch_time: Optional[int] = Field(None, ge=0, description="观看时间(秒)")
    is_completed: bool = Field(default=False, description="是否完成")
    notes: Optional[str] = Field(None, max_length=1000, description="学习笔记")


class LessonProgressResponse(BaseModel):
    """课时进度响应模式"""
    id: int = Field(..., description="进度ID")
    lesson_id: int = Field(..., description="课时ID")
    student_id: int = Field(..., description="学生ID")
    progress_percentage: float = Field(..., description="进度百分比")
    watch_time: int = Field(..., description="观看时间(秒)")
    is_completed: bool = Field(..., description="是否完成")
    notes: Optional[str] = Field(None, description="学习笔记")
    started_at: datetime = Field(..., description="开始时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    last_accessed: datetime = Field(..., description="最后访问时间")
    
    class Config:
        from_attributes = True


class CourseRatingCreate(BaseModel):
    """课程评分创建请求模式"""
    rating: float = Field(..., ge=1, le=5, description="评分(1-5)")
    review: Optional[str] = Field(None, max_length=500, description="评价内容")


class CourseListQuery(BaseModel):
    """课程列表查询参数"""
    category: Optional[str] = Field(None, description="课程分类")
    difficulty: Optional[DifficultyLevel] = Field(None, description="难度级别")
    instructor_id: Optional[int] = Field(None, description="教师ID")
    search: Optional[str] = Field(None, min_length=1, description="搜索关键词")
    is_published: Optional[bool] = Field(None, description="是否发布")
    skip: int = Field(default=0, ge=0, description="跳过数量")
    limit: int = Field(default=20, ge=1, le=100, description="限制数量")
    sort_by: Optional[str] = Field(default="created_at", description="排序字段")
    sort_order: Optional[str] = Field(default="desc", description="排序方向")


class CourseStatistics(BaseModel):
    """课程统计信息"""
    total_courses: int = Field(..., description="总课程数")
    published_courses: int = Field(..., description="已发布课程数")
    total_students: int = Field(..., description="总学生数")
    total_lessons: int = Field(..., description="总课时数")
    average_rating: float = Field(..., description="平均评分")
    completion_rate: float = Field(..., description="完成率")


class StudyPlanCreate(BaseModel):
    """学习计划创建请求模式"""
    title: str = Field(..., min_length=1, max_length=200, description="计划标题")
    description: Optional[str] = Field(None, max_length=1000, description="计划描述")
    target_courses: List[int] = Field(..., description="目标课程ID列表")
    start_date: datetime = Field(..., description="开始日期")
    end_date: datetime = Field(..., description="结束日期")
    daily_study_time: int = Field(default=60, gt=0, description="每日学习时间(分钟)")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        """验证结束日期"""
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('结束日期必须晚于开始日期')
        return v

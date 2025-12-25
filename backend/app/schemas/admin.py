"""
管理员相关的数据模式
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr


class AdminDashboardStats(BaseModel):
    """管理员仪表板统计数据"""
    total_users: int = Field(..., description="总用户数")
    total_students: int = Field(..., description="学生数量")
    total_teachers: int = Field(..., description="教师数量")
    active_users: int = Field(..., description="活跃用户数")
    total_courses: int = Field(..., description="课程总数")
    total_exercises: int = Field(..., description="练习总数")
    ai_usage_today: int = Field(..., description="今日AI使用量")
    ai_usage_this_month: int = Field(..., description="本月AI使用量")


class UserCreateRequest(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    full_name: str = Field(..., min_length=1, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    role: str = Field(..., description="用户角色", pattern="^(student|teacher)$")


class UserUpdateRequest(BaseModel):
    """更新用户请求"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_verified: Optional[bool] = Field(None, description="是否验证")


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应"""
    users: List[UserInfo]
    total: int
    page: int
    size: int
    pages: int


class UserUsageStats(BaseModel):
    """用户AI使用统计"""
    id: int
    username: str
    full_name: str
    role: str
    total_messages: int = Field(..., description="总消息数")
    total_tokens: int = Field(..., description="总Token数")
    last_usage: Optional[datetime] = Field(None, description="最后使用时间")
    daily_average: float = Field(..., description="日均使用量")


class DailyUsageStats(BaseModel):
    """每日使用统计"""
    date: str = Field(..., description="日期")
    messages: int = Field(..., description="消息数")
    tokens: int = Field(..., description="Token数")
    users: int = Field(..., description="用户数")


class UsageStatsResponse(BaseModel):
    """AI使用统计响应"""
    user_stats: List[UserUsageStats]
    daily_stats: List[Dict[str, Any]]
    time_range: str = Field(..., description="时间范围")


class SystemStatsResponse(BaseModel):
    """系统状态响应"""
    database_status: str = Field(..., description="数据库状态")
    ai_service_status: str = Field(..., description="AI服务状态")
    storage_status: str = Field(..., description="存储状态")
    email_service_status: str = Field(..., description="邮件服务状态")


class ActivityRecord(BaseModel):
    """活动记录"""
    id: int
    type: str = Field(..., description="活动类型")
    user: str = Field(..., description="用户名")
    action: str = Field(..., description="操作描述")
    timestamp: datetime = Field(..., description="时间戳")
    ip_address: Optional[str] = Field(None, description="IP地址")


class TeacherStats(BaseModel):
    """教师统计信息"""
    id: int
    username: str
    full_name: str
    email: str
    courses_created: int = Field(0, description="创建的课程数")
    students_taught: int = Field(0, description="教授的学生数")
    total_teaching_hours: int = Field(0, description="总教学时长")
    ai_usage_count: int = Field(0, description="AI使用次数")
    last_active: Optional[datetime] = Field(None, description="最后活跃时间")


class StudentStats(BaseModel):
    """学生统计信息"""
    id: int
    username: str
    full_name: str
    email: str
    total_study_time: int = Field(0, description="总学习时间")
    total_exercises: int = Field(0, description="总练习数")
    correct_exercises: int = Field(0, description="正确练习数")
    total_courses: int = Field(0, description="总课程数")
    completed_courses: int = Field(0, description="完成课程数")
    ai_usage_count: int = Field(0, description="AI使用次数")
    last_active: Optional[datetime] = Field(None, description="最后活跃时间")


class TeacherListResponse(BaseModel):
    """教师列表响应"""
    teachers: List[TeacherStats]
    total: int
    page: int
    size: int
    pages: int


class StudentListResponse(BaseModel):
    """学生列表响应"""
    students: List[StudentStats]
    total: int
    page: int
    size: int
    pages: int


class UserActivitySummary(BaseModel):
    """用户活动摘要"""
    user_id: int
    username: str
    full_name: str
    role: str
    login_count: int = Field(0, description="登录次数")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    course_activities: int = Field(0, description="课程活动数")
    exercise_activities: int = Field(0, description="练习活动数")
    ai_activities: int = Field(0, description="AI活动数")
    total_activities: int = Field(0, description="总活动数")


class PlatformAnalytics(BaseModel):
    """平台分析数据"""
    user_growth: List[Dict[str, Any]] = Field(..., description="用户增长趋势")
    course_popularity: List[Dict[str, Any]] = Field(..., description="课程热度")
    exercise_completion: List[Dict[str, Any]] = Field(..., description="练习完成率")
    ai_usage_trends: List[Dict[str, Any]] = Field(..., description="AI使用趋势")
    peak_hours: List[Dict[str, Any]] = Field(..., description="使用高峰时段")


class SystemHealthCheck(BaseModel):
    """系统健康检查"""
    overall_status: str = Field(..., description="整体状态")
    database: Dict[str, Any] = Field(..., description="数据库状态")
    ai_service: Dict[str, Any] = Field(..., description="AI服务状态")
    storage: Dict[str, Any] = Field(..., description="存储状态")
    memory_usage: float = Field(..., description="内存使用率")
    cpu_usage: float = Field(..., description="CPU使用率")
    disk_usage: float = Field(..., description="磁盘使用率")
    uptime: str = Field(..., description="运行时间")


class BackupInfo(BaseModel):
    """备份信息"""
    id: int
    name: str = Field(..., description="备份名称")
    type: str = Field(..., description="备份类型")
    size: int = Field(..., description="备份大小(字节)")
    created_at: datetime = Field(..., description="创建时间")
    status: str = Field(..., description="备份状态")
    file_path: Optional[str] = Field(None, description="文件路径")


class SystemConfig(BaseModel):
    """系统配置"""
    site_name: str = Field(..., description="站点名称")
    site_description: str = Field(..., description="站点描述")
    max_file_size: int = Field(..., description="最大文件大小")
    allowed_file_types: List[str] = Field(..., description="允许的文件类型")
    ai_model_config: Dict[str, Any] = Field(..., description="AI模型配置")
    email_config: Dict[str, Any] = Field(..., description="邮件配置")
    storage_config: Dict[str, Any] = Field(..., description="存储配置")


class SystemConfigUpdate(BaseModel):
    """系统配置更新"""
    site_name: Optional[str] = Field(None, description="站点名称")
    site_description: Optional[str] = Field(None, description="站点描述")
    max_file_size: Optional[int] = Field(None, description="最大文件大小")
    allowed_file_types: Optional[List[str]] = Field(None, description="允许的文件类型")
    ai_model_config: Optional[Dict[str, Any]] = Field(None, description="AI模型配置")
    email_config: Optional[Dict[str, Any]] = Field(None, description="邮件配置")
    storage_config: Optional[Dict[str, Any]] = Field(None, description="存储配置")

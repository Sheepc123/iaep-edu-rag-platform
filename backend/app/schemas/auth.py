"""
用户认证相关的数据验证模式
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """用户注册请求模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    full_name: str = Field(..., min_length=2, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    role: str = Field(default="student", description="用户角色")
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('用户名只能包含字母、数字、下划线和连字符')
        return v.lower()
    
    @validator('phone')
    def validate_phone(cls, v):
        """验证手机号格式"""
        if v and not v.replace('-', '').replace(' ', '').isdigit():
            raise ValueError('手机号格式不正确')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        """验证用户角色"""
        allowed_roles = ['student', 'teacher', 'admin']
        if v not in allowed_roles:
            raise ValueError(f'角色必须是以下之一: {", ".join(allowed_roles)}')
        return v


class UserLogin(BaseModel):
    """用户登录请求模式"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    remember_me: bool = Field(default=False, description="记住我")
    device_info: Optional[str] = Field(None, description="设备信息")


class TokenResponse(BaseModel):
    """令牌响应模式"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")
    user_info: 'UserInfo' = Field(..., description="用户信息")


class TokenRefresh(BaseModel):
    """令牌刷新请求模式"""
    refresh_token: str = Field(..., description="刷新令牌")


class UserInfo(BaseModel):
    """用户信息响应模式"""
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    full_name: str = Field(..., description="真实姓名")
    phone: Optional[str] = Field(None, description="手机号")
    avatar: Optional[str] = Field(None, description="头像URL")
    role: str = Field(..., description="用户角色")
    is_active: bool = Field(..., description="是否激活")
    is_verified: bool = Field(..., description="是否验证")
    created_at: datetime = Field(..., description="创建时间")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    
    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """密码修改请求模式"""
    current_password: str = Field(..., description="当前密码")
    new_password: str = Field(..., min_length=6, max_length=128, description="新密码")
    confirm_password: str = Field(..., description="确认新密码")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """验证密码确认"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('两次输入的密码不一致')
        return v


class PasswordReset(BaseModel):
    """密码重置请求模式"""
    email: EmailStr = Field(..., description="邮箱地址")


class PasswordResetConfirm(BaseModel):
    """密码重置确认模式"""
    token: str = Field(..., description="重置令牌")
    new_password: str = Field(..., min_length=6, max_length=128, description="新密码")
    confirm_password: str = Field(..., description="确认新密码")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """验证密码确认"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('两次输入的密码不一致')
        return v


class EmailVerification(BaseModel):
    """邮箱验证请求模式"""
    token: str = Field(..., description="验证令牌")


class UserUpdate(BaseModel):
    """用户信息更新模式"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    avatar: Optional[str] = Field(None, description="头像URL")
    
    @validator('phone')
    def validate_phone(cls, v):
        """验证手机号格式"""
        if v and not v.replace('-', '').replace(' ', '').isdigit():
            raise ValueError('手机号格式不正确')
        return v


class StudentProfileCreate(BaseModel):
    """学生档案创建模式"""
    student_id: Optional[str] = Field(None, max_length=20, description="学号")
    school: Optional[str] = Field(None, max_length=100, description="学校")
    college: Optional[str] = Field(None, max_length=100, description="学院")
    major: Optional[str] = Field(None, max_length=100, description="专业")
    grade: Optional[str] = Field(None, max_length=20, description="年级")
    class_name: Optional[str] = Field(None, max_length=50, description="班级")


class StudentProfileUpdate(BaseModel):
    """学生档案更新模式"""
    student_id: Optional[str] = Field(None, max_length=20, description="学号")
    school: Optional[str] = Field(None, max_length=100, description="学校")
    college: Optional[str] = Field(None, max_length=100, description="学院")
    major: Optional[str] = Field(None, max_length=100, description="专业")
    grade: Optional[str] = Field(None, max_length=20, description="年级")
    class_name: Optional[str] = Field(None, max_length=50, description="班级")
    preferred_subjects: Optional[str] = Field(None, description="偏好科目(JSON)")
    learning_goals: Optional[str] = Field(None, description="学习目标")


class StudentProfileResponse(BaseModel):
    """学生档案响应模式"""
    id: int
    user_id: int
    student_id: Optional[str]
    school: Optional[str]
    college: Optional[str]
    major: Optional[str]
    grade: Optional[str]
    class_name: Optional[str]
    total_study_time: int
    total_exercises: int
    correct_exercises: int
    total_courses: int
    completed_courses: int
    preferred_subjects: Optional[str]
    learning_goals: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """通用认证响应模式"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[dict] = Field(None, description="响应数据")


# 更新TokenResponse的前向引用
TokenResponse.model_rebuild()

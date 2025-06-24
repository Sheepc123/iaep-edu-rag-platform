"""
数据验证模式模块初始化
"""

from .auth import (
    UserRegister, UserLogin, TokenResponse, TokenRefresh,
    PasswordChange, UserInfo, AuthResponse, UserUpdate,
    StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse
)

__all__ = [
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
    "StudentProfileResponse"
]

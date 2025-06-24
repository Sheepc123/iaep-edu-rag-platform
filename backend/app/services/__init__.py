"""
业务服务模块初始化
"""

from .auth_service import AuthService
from .student_service import StudentService

__all__ = [
    "AuthService",
    "StudentService"
]

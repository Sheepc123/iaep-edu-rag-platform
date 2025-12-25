"""
API依赖注入
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.security import JWTManager, TokenData, PermissionChecker
from ..models.user import User
from ..services.auth_service import AuthService


# HTTP Bearer认证方案
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前认证用户"""
    try:
        # 验证令牌
        token_data = JWTManager.verify_token(credentials.credentials, "access")
        
        # 获取用户信息
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(token_data.user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户账户已被禁用",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    return current_user


def get_current_student(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前学生用户"""
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要学生权限"
        )
    return current_user


def get_current_teacher(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前教师用户"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要教师权限"
        )
    return current_user


def get_current_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前管理员用户"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选的当前用户（用于可选认证的端点）"""
    if not credentials:
        return None
    
    try:
        token_data = JWTManager.verify_token(credentials.credentials, "access")
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(token_data.user_id)
        
        if user and user.is_active:
            return user
        
    except Exception:
        pass
    
    return None


class RoleChecker:
    """角色检查器"""
    
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要以下角色之一: {', '.join(self.allowed_roles)}"
            )
        return current_user


# 预定义的角色检查器
require_student = RoleChecker(["student", "admin"])
require_teacher = RoleChecker(["teacher", "admin"])
require_admin = RoleChecker(["admin"])
require_student_or_teacher = RoleChecker(["student", "teacher", "admin"])


def get_token_data(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """获取令牌数据"""
    try:
        return JWTManager.verify_token(credentials.credentials, "access")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_user_access(user_id: int):
    """验证用户访问权限的依赖工厂"""
    def _verify_access(current_user: User = Depends(get_current_active_user)):
        # 管理员可以访问所有用户数据
        if current_user.role == "admin":
            return current_user
        
        # 用户只能访问自己的数据
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问其他用户的数据"
            )
        
        return current_user
    
    return _verify_access


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """获取认证服务实例"""
    return AuthService(db)


def get_pagination_params(
    page: int = 1,
    size: int = 20
):
    """获取分页参数"""
    if page < 1:
        page = 1
    if size <= 0 or size > 100:
        size = 20

    skip = (page - 1) * size
    return {
        "page": page,
        "limit": size,
        "skip": skip
    }

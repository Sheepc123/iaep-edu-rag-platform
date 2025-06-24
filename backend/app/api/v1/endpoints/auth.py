"""
用户认证API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Any

from ....core.database import get_db
from ....schemas.auth import (
    UserRegister, UserLogin, TokenResponse, TokenRefresh, 
    PasswordChange, UserInfo, AuthResponse
)
from ....services.auth_service import AuthService
from ....models.user import User
from ...dependencies import get_current_active_user, get_auth_service


router = APIRouter()


@router.post("/register", response_model=AuthResponse, summary="用户注册")
async def register(
    user_data: UserRegister,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    用户注册
    
    - **username**: 用户名（3-50字符，只能包含字母、数字、下划线、连字符）
    - **email**: 邮箱地址
    - **password**: 密码（至少6字符）
    - **full_name**: 真实姓名
    - **phone**: 手机号码（可选）
    - **role**: 用户角色（student/teacher，默认student）
    """
    try:
        # 记录客户端IP
        client_ip = request.client.host
        
        # 注册用户
        user = auth_service.register_user(user_data)
        
        return AuthResponse(
            success=True,
            message="注册成功",
            data={
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败，请稍后重试"
        )


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(
    login_data: UserLogin,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    用户登录
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    - **remember_me**: 是否记住登录状态
    - **device_info**: 设备信息（可选）
    """
    try:
        # 记录客户端信息
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # 如果没有提供设备信息，使用User-Agent
        if not login_data.device_info:
            login_data.device_info = user_agent[:200]  # 限制长度
        
        # 认证用户
        user, tokens = auth_service.authenticate_user(login_data)
        
        # 构建用户信息
        user_info = UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            avatar=user.avatar,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )
        
        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
            expires_in=tokens["expires_in"],
            user_info=user_info
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录失败，请稍后重试"
        )


@router.post("/refresh", response_model=dict, summary="刷新令牌")
async def refresh_token(
    token_data: TokenRefresh,
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    """
    try:
        new_tokens = auth_service.refresh_token(token_data.refresh_token)
        return {
            "success": True,
            "message": "令牌刷新成功",
            "data": new_tokens
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="令牌刷新失败"
        )


@router.post("/logout", response_model=AuthResponse, summary="用户登出")
async def logout(
    token_data: TokenRefresh = None,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    用户登出
    
    - **refresh_token**: 刷新令牌（可选，不提供则注销所有会话）
    """
    try:
        refresh_token = token_data.refresh_token if token_data else None
        auth_service.logout_user(current_user.id, refresh_token)
        
        return AuthResponse(
            success=True,
            message="登出成功"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登出失败"
        )


@router.get("/me", response_model=UserInfo, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取当前登录用户的详细信息
    """
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        avatar=current_user.avatar,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.post("/change-password", response_model=AuthResponse, summary="修改密码")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    修改用户密码
    
    - **current_password**: 当前密码
    - **new_password**: 新密码（至少6字符）
    - **confirm_password**: 确认新密码
    """
    try:
        auth_service.change_password(
            current_user.id,
            password_data.current_password,
            password_data.new_password
        )
        
        return AuthResponse(
            success=True,
            message="密码修改成功，请重新登录"
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码修改失败"
        )


@router.get("/verify-token", response_model=dict, summary="验证令牌")
async def verify_token(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    验证当前令牌是否有效
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "message": "令牌有效"
    }

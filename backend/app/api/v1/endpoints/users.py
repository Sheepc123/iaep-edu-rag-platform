"""
用户管理API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from ....core.database import get_db
from ....schemas.auth import (
    UserUpdate, UserInfo, StudentProfileCreate, StudentProfileUpdate, 
    StudentProfileResponse, AuthResponse
)
from ....services.auth_service import AuthService
from ....services.student_service import StudentService
from ....models.user import User
from ...dependencies import (
    get_current_active_user, get_current_student, get_current_admin,
    get_auth_service, get_pagination_params
)


router = APIRouter()


@router.get("/profile", response_model=UserInfo, summary="获取用户资料")
async def get_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """获取当前用户的详细资料"""
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


@router.put("/profile", response_model=UserInfo, summary="更新用户资料")
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    更新用户基本资料
    
    - **full_name**: 真实姓名
    - **phone**: 手机号码
    - **avatar**: 头像URL
    """
    try:
        updated_user = auth_service.update_user_info(current_user.id, user_data)
        
        return UserInfo(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            full_name=updated_user.full_name,
            phone=updated_user.phone,
            avatar=updated_user.avatar,
            role=updated_user.role,
            is_active=updated_user.is_active,
            is_verified=updated_user.is_verified,
            created_at=updated_user.created_at,
            last_login=updated_user.last_login
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户资料失败"
        )


@router.get("/student-profile", response_model=StudentProfileResponse, summary="获取学生档案")
async def get_student_profile(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前学生的详细档案"""
    try:
        student_service = StudentService(db)
        profile = student_service.get_student_profile(current_user.id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生档案不存在"
            )
        
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学生档案失败"
        )


@router.post("/student-profile", response_model=StudentProfileResponse, summary="创建学生档案")
async def create_student_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    创建学生档案
    
    - **student_id**: 学号
    - **school**: 学校
    - **college**: 学院
    - **major**: 专业
    - **grade**: 年级
    - **class_name**: 班级
    """
    try:
        student_service = StudentService(db)
        profile = student_service.create_student_profile(current_user.id, profile_data)
        
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建学生档案失败"
        )


@router.put("/student-profile", response_model=StudentProfileResponse, summary="更新学生档案")
async def update_student_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新学生档案
    
    - **student_id**: 学号
    - **school**: 学校
    - **college**: 学院
    - **major**: 专业
    - **grade**: 年级
    - **class_name**: 班级
    - **preferred_subjects**: 偏好科目
    - **learning_goals**: 学习目标
    """
    try:
        student_service = StudentService(db)
        profile = student_service.update_student_profile(current_user.id, profile_data)
        
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新学生档案失败"
        )


@router.get("/learning-stats", response_model=dict, summary="获取学习统计")
async def get_learning_stats(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取学生学习统计数据"""
    try:
        student_service = StudentService(db)
        stats = student_service.get_learning_stats(current_user.id)
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学习统计失败"
        )


@router.get("/learning-preferences", response_model=dict, summary="获取学习偏好")
async def get_learning_preferences(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取学生学习偏好设置"""
    try:
        student_service = StudentService(db)
        preferences = student_service.get_learning_preferences(current_user.id)
        
        return {
            "success": True,
            "data": preferences
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学习偏好失败"
        )


@router.post("/learning-preferences", response_model=AuthResponse, summary="设置学习偏好")
async def set_learning_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    设置学生学习偏好
    
    - **subjects**: 偏好科目列表
    - **goals**: 学习目标
    """
    try:
        student_service = StudentService(db)
        student_service.set_learning_preferences(current_user.id, preferences)
        
        return AuthResponse(
            success=True,
            message="学习偏好设置成功"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="设置学习偏好失败"
        )


# 管理员功能
@router.get("/list", response_model=List[UserInfo], summary="获取用户列表")
async def get_user_list(
    pagination: dict = Depends(get_pagination_params),
    current_user: User = Depends(get_current_admin),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """获取用户列表（管理员功能）"""
    try:
        # 这里需要在AuthService中添加获取用户列表的方法
        # users = auth_service.get_user_list(pagination["skip"], pagination["limit"])
        # 暂时返回空列表
        return []
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表失败"
        )


@router.get("/{user_id}", response_model=UserInfo, summary="获取指定用户信息")
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """获取指定用户的详细信息"""
    try:
        # 权限检查：管理员可以访问所有用户数据，普通用户只能访问自己的数据
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问其他用户的数据"
            )

        user = auth_service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return UserInfo(
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

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )

"""
管理员API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import Any, List, Optional, Dict
from datetime import datetime, timedelta

from ....core.database import get_db
from ....schemas.admin import (
    AdminDashboardStats, UserListResponse, UserCreateRequest, UserUpdateRequest,
    UsageStatsResponse, UserUsageStats, SystemStatsResponse
)
from ....models.user import User
from ....services.auth_service import AuthService
from ...dependencies import get_current_admin, get_pagination_params, get_auth_service

router = APIRouter()


@router.get("/dashboard/stats", response_model=AdminDashboardStats, summary="获取仪表板统计数据")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """获取管理员仪表板统计数据"""
    try:
        # 用户统计
        total_users = db.query(User).count()
        total_students = db.query(User).filter(User.role == 'student').count()
        total_teachers = db.query(User).filter(User.role == 'teacher').count()
        
        # 活跃用户（最近7天有登录）
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users = db.query(User).filter(
            User.last_login >= seven_days_ago
        ).count()
        
        # 课程和练习统计（模拟数据）
        total_courses = 89
        total_exercises = 456

        # AI使用统计（模拟数据）
        ai_usage_today = 1234
        ai_usage_this_month = 45678
        
        return AdminDashboardStats(
            total_users=total_users,
            total_students=total_students,
            total_teachers=total_teachers,
            active_users=active_users,
            total_courses=total_courses,
            total_exercises=total_exercises,
            ai_usage_today=ai_usage_today,
            ai_usage_this_month=ai_usage_this_month
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        )


@router.get("/users", response_model=UserListResponse, summary="获取用户列表")
async def get_users(
    pagination: dict = Depends(get_pagination_params),
    role: Optional[str] = Query(None, description="用户角色筛选"),
    is_active: Optional[bool] = Query(None, description="用户状态筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """获取用户列表（支持筛选和搜索）"""
    try:
        query = db.query(User)
        
        # 角色筛选
        if role and role != 'all':
            query = query.filter(User.role == role)
        
        # 状态筛选
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # 搜索
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_term),
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )
        
        # 总数
        total = query.count()
        
        # 分页
        users = query.offset(pagination["skip"]).limit(pagination["limit"]).all()
        
        return UserListResponse(
            users=users,
            total=total,
            page=pagination["page"],
            size=pagination["limit"],
            pages=(total + pagination["limit"] - 1) // pagination["limit"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户列表失败: {str(e)}"
        )


@router.post("/users", summary="创建用户")
async def create_user(
    user_data: UserCreateRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """创建新用户"""
    try:
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 创建用户
        new_user = auth_service.register_user(user_data)
        
        return {
            "success": True,
            "message": "用户创建成功",
            "user_id": new_user.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建用户失败: {str(e)}"
        )


@router.put("/users/{user_id}", summary="更新用户信息")
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """更新用户信息"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新用户信息
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return {
            "success": True,
            "message": "用户信息更新成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户失败: {str(e)}"
        )


@router.delete("/users/{user_id}", summary="删除用户")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """删除用户"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 防止删除管理员
        if user.role == 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="不能删除管理员账户"
            )
        
        # 软删除：设置为非活跃状态
        user.is_active = False
        db.commit()
        
        return {
            "success": True,
            "message": "用户删除成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除用户失败: {str(e)}"
        )


@router.post("/users/{user_id}/toggle-status", summary="切换用户状态")
async def toggle_user_status(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """切换用户激活状态"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 防止禁用管理员
        if user.role == 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="不能禁用管理员账户"
            )
        
        user.is_active = not user.is_active
        db.commit()
        
        return {
            "success": True,
            "message": f"用户已{'激活' if user.is_active else '禁用'}",
            "is_active": user.is_active
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户状态失败: {str(e)}"
        )


@router.get("/usage-stats", response_model=UsageStatsResponse, summary="获取AI使用统计")
async def get_usage_stats(
    days: int = Query(7, description="统计天数"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """获取AI使用统计数据"""
    try:
        # 计算时间范围
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # 模拟用户AI使用统计
        user_stats = [
            UserUsageStats(
                id=1,
                username="student001",
                full_name="张同学",
                role="student",
                total_messages=245,
                total_tokens=12500,
                last_usage=datetime.utcnow(),
                daily_average=35.0
            ),
            UserUsageStats(
                id=2,
                username="teacher001",
                full_name="李老师",
                role="teacher",
                total_messages=189,
                total_tokens=15600,
                last_usage=datetime.utcnow(),
                daily_average=27.0
            )
        ]

        # 模拟每日使用趋势
        daily_stats = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            daily_stats.append({
                "date": date.strftime("%m-%d"),
                "messages": 150 + i * 10,
                "tokens": 8000 + i * 500,
                "users": 20 + i * 2
            })
        
        return UsageStatsResponse(
            user_stats=user_stats,
            daily_stats=daily_stats,
            time_range=f"{days}天"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取使用统计失败: {str(e)}"
        )


@router.get("/system/stats", response_model=SystemStatsResponse, summary="获取系统统计")
async def get_system_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """获取系统运行统计"""
    try:
        # 这里可以添加系统监控数据
        # 例如：数据库连接数、内存使用、磁盘空间等
        
        return SystemStatsResponse(
            database_status="healthy",
            ai_service_status="healthy",
            storage_status="healthy",
            email_service_status="maintenance"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取系统统计失败: {str(e)}"
        )


@router.get("/activities", summary="获取最近活动")
async def get_recent_activities(
    limit: int = Query(20, description="返回数量"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """获取最近的用户活动"""
    try:
        # 模拟活动数据
        result = [
            {
                "id": 1,
                "type": "user_register",
                "user": "张同学",
                "action": "注册了新账户",
                "timestamp": datetime.utcnow() - timedelta(minutes=2),
                "ip_address": "192.168.1.100"
            },
            {
                "id": 2,
                "type": "course_create",
                "user": "李老师",
                "action": "创建了新课程《Python基础》",
                "timestamp": datetime.utcnow() - timedelta(minutes=5),
                "ip_address": "192.168.1.101"
            }
        ]

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取活动记录失败: {str(e)}"
        )


@router.post("/users/{user_id}/change-password", summary="修改用户密码")
async def change_user_password(
    user_id: int,
    password_data: dict,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    管理员修改用户密码
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        new_password = password_data.get("new_password")
        if not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="新密码不能为空"
            )

        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码长度至少为6位"
            )

        # 使用密码管理器哈希新密码
        from app.core.security import PasswordManager
        user.hashed_password = PasswordManager.hash_password(new_password)
        db.commit()

        return {
            "success": True,
            "message": "密码修改成功",
            "user_id": user_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"修改密码失败: {str(e)}"
        )


@router.get("/users/{user_id}/detail", summary="获取用户详细信息")
async def get_user_detail(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取用户详细信息（管理员权限）
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户详情失败: {str(e)}"
        )

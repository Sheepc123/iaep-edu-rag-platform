"""
用户认证服务层
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional, Tuple
import secrets

from ..models.user import User, StudentProfile, TeacherProfile, UserSession, UserActivity
from ..core.security import PasswordManager, JWTManager, TokenData
from ..schemas.auth import UserRegister, UserLogin, UserUpdate, StudentProfileCreate, StudentProfileUpdate
from ..core.config import settings


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: UserRegister) -> User:
        """用户注册"""
        # 检查用户名是否已存在
        if self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 创建用户
        hashed_password = PasswordManager.hash_password(user_data.password)
        
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role,
            is_active=True,
            is_verified=False
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # 根据角色创建对应的档案
        if user_data.role == "student":
            self._create_student_profile(db_user.id)
        elif user_data.role == "teacher":
            self._create_teacher_profile(db_user.id)
        
        # 记录用户活动
        self._log_user_activity(db_user.id, "register", {"role": user_data.role})
        
        return db_user
    
    def authenticate_user(self, login_data: UserLogin) -> Tuple[User, dict]:
        """用户认证"""
        # 支持用户名或邮箱登录
        user = self.db.query(User).filter(
            or_(
                User.username == login_data.username.lower(),
                User.email == login_data.username.lower()
            )
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账户已被禁用"
            )
        
        if not PasswordManager.verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        # 创建令牌
        tokens = JWTManager.create_tokens(user.id, user.username, user.role)
        
        # 创建用户会话
        session_data = self._create_user_session(
            user.id, 
            tokens.refresh_token,
            login_data.device_info,
            login_data.remember_me
        )
        
        # 记录登录活动
        self._log_user_activity(user.id, "login", {
            "device_info": login_data.device_info,
            "remember_me": login_data.remember_me
        })
        
        return user, tokens.dict()
    
    def refresh_token(self, refresh_token: str) -> dict:
        """刷新令牌"""
        try:
            # 验证刷新令牌
            token_data = JWTManager.verify_token(refresh_token, "refresh")
            
            # 检查会话是否有效
            session = self.db.query(UserSession).filter(
                UserSession.user_id == token_data.user_id,
                UserSession.refresh_token == refresh_token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="会话已过期，请重新登录"
                )
            
            # 获取用户信息
            user = self.get_user_by_id(token_data.user_id)
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="用户不存在或已被禁用"
                )
            
            # 生成新的令牌
            new_tokens = JWTManager.create_tokens(user.id, user.username, user.role)
            
            # 更新会话
            session.refresh_token = new_tokens.refresh_token
            session.last_used = datetime.utcnow()
            self.db.commit()
            
            return new_tokens.dict()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌刷新失败"
            )
    
    def logout_user(self, user_id: int, refresh_token: Optional[str] = None):
        """用户登出"""
        if refresh_token:
            # 注销特定会话
            session = self.db.query(UserSession).filter(
                UserSession.user_id == user_id,
                UserSession.refresh_token == refresh_token
            ).first()
            
            if session:
                session.is_active = False
                self.db.commit()
        else:
            # 注销所有会话
            self.db.query(UserSession).filter(
                UserSession.user_id == user_id
            ).update({"is_active": False})
            self.db.commit()
        
        # 记录登出活动
        self._log_user_activity(user_id, "logout")
    
    def change_password(self, user_id: int, current_password: str, new_password: str):
        """修改密码"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 验证当前密码
        if not PasswordManager.verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码错误"
            )
        
        # 更新密码
        user.hashed_password = PasswordManager.hash_password(new_password)
        self.db.commit()
        
        # 注销所有会话，强制重新登录
        self.logout_user(user_id)
        
        # 记录密码修改活动
        self._log_user_activity(user_id, "password_change")
    
    def update_user_info(self, user_id: int, user_data: UserUpdate) -> User:
        """更新用户信息"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新用户信息
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        
        # 记录信息更新活动
        self._log_user_activity(user_id, "profile_update", update_data)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username.lower()).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email.lower()).first()
    
    def _create_student_profile(self, user_id: int):
        """创建学生档案"""
        profile = StudentProfile(user_id=user_id)
        self.db.add(profile)
        self.db.commit()
    
    def _create_teacher_profile(self, user_id: int):
        """创建教师档案"""
        profile = TeacherProfile(user_id=user_id)
        self.db.add(profile)
        self.db.commit()
    
    def _create_user_session(self, user_id: int, refresh_token: str, 
                           device_info: Optional[str], remember_me: bool) -> UserSession:
        """创建用户会话"""
        expires_days = settings.REFRESH_TOKEN_EXPIRE_DAYS if remember_me else 1
        expires_at = datetime.utcnow() + timedelta(days=expires_days)
        
        session = UserSession(
            user_id=user_id,
            refresh_token=refresh_token,
            device_info=device_info,
            expires_at=expires_at,
            is_active=True
        )
        
        self.db.add(session)
        self.db.commit()
        return session
    
    def _log_user_activity(self, user_id: int, activity_type: str, 
                          activity_data: Optional[dict] = None):
        """记录用户活动"""
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            activity_data=str(activity_data) if activity_data else None
        )
        
        self.db.add(activity)
        self.db.commit()

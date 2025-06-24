"""
安全认证相关工具
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import BaseModel

from .config import JWTConfig


# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """Token数据模型"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None


class Token(BaseModel):
    """Token响应模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class PasswordManager:
    """密码管理器"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """加密密码"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)


class JWTManager:
    """JWT管理器"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=JWTConfig.get_access_token_expire_minutes()
            )
        
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            JWTConfig.get_secret_key(), 
            algorithm=JWTConfig.get_algorithm()
        )
        
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """创建刷新令牌"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            days=JWTConfig.get_refresh_token_expire_days()
        )
        
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(
            to_encode,
            JWTConfig.get_secret_key(),
            algorithm=JWTConfig.get_algorithm()
        )
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> TokenData:
        """验证令牌"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(
                token,
                JWTConfig.get_secret_key(),
                algorithms=[JWTConfig.get_algorithm()]
            )
            
            # 检查令牌类型
            if payload.get("type") != token_type:
                raise credentials_exception
            
            user_id: int = payload.get("sub")
            username: str = payload.get("username")
            role: str = payload.get("role")
            
            if user_id is None:
                raise credentials_exception
                
            token_data = TokenData(
                user_id=int(user_id),
                username=username,
                role=role
            )
            
        except JWTError:
            raise credentials_exception
            
        return token_data
    
    @staticmethod
    def create_tokens(user_id: int, username: str, role: str = "student") -> Token:
        """创建完整的令牌对"""
        token_data = {
            "sub": str(user_id),
            "username": username,
            "role": role
        }
        
        access_token = JWTManager.create_access_token(token_data)
        refresh_token = JWTManager.create_refresh_token(token_data)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=JWTConfig.get_access_token_expire_minutes() * 60
        )


# 权限验证装饰器
class PermissionChecker:
    """权限检查器"""
    
    @staticmethod
    def check_student_permission(token_data: TokenData) -> bool:
        """检查学生权限"""
        return token_data.role in ["student", "admin"]
    
    @staticmethod
    def check_teacher_permission(token_data: TokenData) -> bool:
        """检查教师权限"""
        return token_data.role in ["teacher", "admin"]
    
    @staticmethod
    def check_admin_permission(token_data: TokenData) -> bool:
        """检查管理员权限"""
        return token_data.role == "admin"

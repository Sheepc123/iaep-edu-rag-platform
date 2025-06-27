#!/usr/bin/env python3
"""
直接测试登录逻辑
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auth_service():
    """直接测试认证服务"""
    print("🔍 直接测试认证服务...")
    
    try:
        from app.core.database import SessionLocal
        from app.services.auth_service import AuthService
        from app.schemas.auth import UserLogin
        
        # 创建数据库会话
        db = SessionLocal()
        auth_service = AuthService(db)
        
        # 测试登录数据
        login_data = UserLogin(
            username="teacher1",
            password="123456",
            remember_me=False,
            device_info="test_device"
        )
        
        print(f"测试登录: {login_data.username}")
        
        # 直接调用认证方法
        user, tokens = auth_service.authenticate_user(login_data)
        
        print("✅ 认证成功")
        print(f"   用户ID: {user.id}")
        print(f"   用户名: {user.username}")
        print(f"   角色: {user.role}")
        print(f"   令牌类型: {tokens.get('token_type')}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 认证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_user_query():
    """测试用户查询"""
    print("\n🔍 测试用户查询...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.user import User
        from sqlalchemy import or_
        
        db = SessionLocal()
        
        # 查询用户
        username = "teacher1"
        user = db.query(User).filter(
            or_(
                User.username == username.lower(),
                User.email == username.lower()
            )
        ).first()
        
        if user:
            print("✅ 用户查询成功")
            print(f"   ID: {user.id}")
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
            print(f"   角色: {user.role}")
            print(f"   激活状态: {user.is_active}")
            print(f"   密码哈希: {user.hashed_password[:50]}...")
        else:
            print("❌ 用户不存在")
        
        db.close()
        return user is not None
        
    except Exception as e:
        print(f"❌ 用户查询失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_password_verification():
    """测试密码验证"""
    print("\n🔍 测试密码验证...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.user import User
        from app.core.security import PasswordManager
        from sqlalchemy import or_
        
        db = SessionLocal()
        
        # 获取用户
        username = "teacher1"
        user = db.query(User).filter(
            or_(
                User.username == username.lower(),
                User.email == username.lower()
            )
        ).first()
        
        if not user:
            print("❌ 用户不存在")
            return False
        
        # 验证密码
        password = "123456"
        is_valid = PasswordManager.verify_password(password, user.hashed_password)
        
        print(f"密码验证结果: {'✅ 成功' if is_valid else '❌ 失败'}")
        print(f"   输入密码: {password}")
        print(f"   存储哈希: {user.hashed_password[:50]}...")
        
        db.close()
        return is_valid
        
    except Exception as e:
        print(f"❌ 密码验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_token_creation():
    """测试令牌创建"""
    print("\n🔍 测试令牌创建...")
    
    try:
        from app.core.security import JWTManager
        
        # 创建令牌
        user_id = 1
        username = "teacher1"
        role = "teacher"
        
        tokens = JWTManager.create_tokens(user_id, username, role)
        
        print("✅ 令牌创建成功")
        print(f"   访问令牌: {tokens.access_token[:50]}...")
        print(f"   刷新令牌: {tokens.refresh_token[:50]}...")
        print(f"   令牌类型: {tokens.token_type}")
        print(f"   过期时间: {tokens.expires_in}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 令牌创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("🚀 登录逻辑直接测试")
    print("=" * 50)
    
    # 1. 测试用户查询
    user_ok = test_user_query()
    
    # 2. 测试密码验证
    password_ok = test_password_verification()
    
    # 3. 测试令牌创建
    token_ok = test_token_creation()
    
    # 4. 测试完整认证服务
    auth_ok = test_auth_service()
    
    print("\n" + "=" * 50)
    print("📋 测试结果:")
    print(f"   用户查询: {'✅' if user_ok else '❌'}")
    print(f"   密码验证: {'✅' if password_ok else '❌'}")
    print(f"   令牌创建: {'✅' if token_ok else '❌'}")
    print(f"   认证服务: {'✅' if auth_ok else '❌'}")
    
    if all([user_ok, password_ok, token_ok, auth_ok]):
        print("\n🎉 所有测试通过！登录逻辑正常")
        print("问题可能在API层面，请检查服务器日志")
    else:
        print("\n❌ 发现问题，请根据上述错误信息修复")


if __name__ == "__main__":
    main()

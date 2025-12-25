#!/usr/bin/env python3
"""
创建管理员账户
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import PasswordManager
from datetime import datetime

def create_admin_user():
    """创建管理员用户"""
    print("🔧 创建管理员账户")
    print("=" * 50)
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 检查是否已有管理员账户
        existing_admin = db.query(User).filter(User.role == 'admin').first()
        
        if existing_admin:
            print(f"✅ 已存在管理员账户:")
            print(f"   用户名: {existing_admin.username}")
            print(f"   邮箱: {existing_admin.email}")
            print(f"   姓名: {existing_admin.full_name}")
            print(f"   状态: {'活跃' if existing_admin.is_active else '禁用'}")
            
            # 询问是否重置密码
            reset = input("\n是否重置管理员密码？(y/N): ")
            if reset.lower() == 'y':
                new_password = "admin123"
                existing_admin.password_hash = PasswordManager.hash_password(new_password)
                db.commit()
                print(f"✅ 管理员密码已重置为: {new_password}")
            
            return existing_admin.username, "admin123"
        
        # 创建新的管理员账户
        admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "full_name": "系统管理员"
        }
        
        print("创建新的管理员账户...")
        print(f"用户名: {admin_data['username']}")
        print(f"密码: {admin_data['password']}")
        print(f"邮箱: {admin_data['email']}")
        print(f"姓名: {admin_data['full_name']}")
        
        # 创建管理员用户
        admin_user = User(
            username=admin_data["username"],
            email=admin_data["email"],
            password_hash=PasswordManager.hash_password(admin_data["password"]),
            full_name=admin_data["full_name"],
            role="admin",
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ 管理员账户创建成功！")
        print(f"   ID: {admin_user.id}")
        print(f"   用户名: {admin_user.username}")
        print(f"   密码: {admin_data['password']}")
        
        return admin_data["username"], admin_data["password"]
        
    except Exception as e:
        print(f"❌ 创建管理员账户失败: {e}")
        db.rollback()
        return None, None
    finally:
        db.close()

def test_admin_login(username, password):
    """测试管理员登录"""
    if not username or not password:
        return
    
    print(f"\n🧪 测试管理员登录")
    print("=" * 50)
    
    import requests
    
    try:
        # 测试登录
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post("http://localhost:8000/api/v1/auth/login", data=login_data)
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            
            print(f"✅ 登录测试成功！")
            print(f"   用户: {user.get('username')}")
            print(f"   角色: {user.get('role')}")
            print(f"   姓名: {user.get('full_name')}")
            print(f"   令牌: {data.get('access_token', '')[:20]}...")
            
            if user.get('role') == 'admin':
                print(f"✅ 管理员权限验证通过")
            else:
                print(f"❌ 权限验证失败，角色为: {user.get('role')}")
                
        else:
            print(f"❌ 登录测试失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 登录测试异常: {e}")

def main():
    """主函数"""
    print("🚀 管理员账户管理")
    print("=" * 50)
    
    # 创建管理员账户
    username, password = create_admin_user()
    
    # 测试登录
    test_admin_login(username, password)
    
    print("\n" + "=" * 50)
    print("🎯 完成")
    
    if username and password:
        print(f"\n📋 管理员登录信息:")
        print(f"   用户名: {username}")
        print(f"   密码: {password}")
        print(f"   登录地址: http://localhost:5173/admin/login")
        
        print(f"\n💡 使用说明:")
        print(f"1. 访问 http://localhost:5173")
        print(f"2. 点击右上角的'管理员'按钮")
        print(f"3. 使用上述账户信息登录")
        print(f"4. 进入管理员控制台")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
测试用户显示名称
"""

import requests
import json

def test_user_display():
    """测试用户显示名称"""
    print("🧪 测试用户显示名称...")
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # 1. 学生登录
        print("\n1. 学生登录...")
        login_response = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "student1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.text}")
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ 登录成功")
        
        # 2. 获取用户信息
        print("\n2. 获取用户信息...")
        profile_response = requests.get(
            f"{base_url}/users/profile",
            headers=headers
        )
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print("✅ 获取用户信息成功")
            print(f"   用户名: {profile_data.get('username')}")
            print(f"   真实姓名: {profile_data.get('full_name')}")
            print(f"   邮箱: {profile_data.get('email')}")
            
            # 确定显示名称
            display_name = profile_data.get('full_name') or profile_data.get('username') or "学生"
            print(f"   前端应显示: {display_name}")
            
            # 如果没有真实姓名，建议设置一个
            if not profile_data.get('full_name'):
                print("\n💡 建议设置真实姓名...")
                update_response = requests.put(
                    f"{base_url}/users/profile",
                    headers=headers,
                    json={"full_name": "张同学"}
                )
                
                if update_response.status_code == 200:
                    updated_data = update_response.json()
                    print(f"✅ 已设置真实姓名: {updated_data.get('full_name')}")
                    print(f"   现在前端应显示: {updated_data.get('full_name')}")
                else:
                    print(f"❌ 设置真实姓名失败: {update_response.text}")
        else:
            print(f"❌ 获取用户信息失败: {profile_response.text}")
        
        # 3. 测试教师用户
        print("\n\n3. 测试教师用户...")
        teacher_login_response = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "teacher1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if teacher_login_response.status_code == 200:
            teacher_token = teacher_login_response.json()["access_token"]
            teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
            
            teacher_profile_response = requests.get(
                f"{base_url}/users/profile",
                headers=teacher_headers
            )
            
            if teacher_profile_response.status_code == 200:
                teacher_data = teacher_profile_response.json()
                print("✅ 获取教师信息成功")
                print(f"   用户名: {teacher_data.get('username')}")
                print(f"   真实姓名: {teacher_data.get('full_name')}")
                
                teacher_display_name = teacher_data.get('full_name') or teacher_data.get('username') or "教师"
                print(f"   教师端应显示: {teacher_display_name}")
            else:
                print(f"❌ 获取教师信息失败: {teacher_profile_response.text}")
        else:
            print(f"❌ 教师登录失败: {teacher_login_response.text}")
        
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")


def check_database_users():
    """检查数据库中的用户数据"""
    print("\n\n🔍 检查数据库中的用户数据...")
    
    try:
        import os
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.user import User
        
        db = SessionLocal()
        
        users = db.query(User).all()
        
        print(f"数据库中共有 {len(users)} 个用户:")
        for user in users:
            print(f"   - {user.username} ({user.role})")
            print(f"     真实姓名: {user.full_name or '未设置'}")
            print(f"     邮箱: {user.email}")
            print(f"     显示名称: {user.full_name or user.username}")
            print()
        
        db.close()
        
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")


def main():
    """主函数"""
    print("🚀 用户显示名称测试")
    print("=" * 60)
    
    # 检查数据库用户
    check_database_users()
    
    # 测试API
    test_user_display()
    
    print("\n" + "=" * 60)
    print("📋 测试总结:")
    print("1. StudentLayout 现在会显示真实姓名或用户名")
    print("2. 优先级: full_name > username > '学生'")
    print("3. 如果API调用失败，显示默认值'学生'")
    print("4. 加载时显示'加载中...'")
    print("\n💡 前端修改:")
    print("- 添加了 useEffect 获取用户信息")
    print("- 添加了加载状态显示")
    print("- 动态显示用户真实姓名")


if __name__ == "__main__":
    main()

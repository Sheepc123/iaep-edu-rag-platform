#!/usr/bin/env python3
"""
简单创建管理员账户
"""
import sqlite3
import hashlib
import os
from datetime import datetime

def hash_password(password: str) -> str:
    """简单的密码哈希"""
    # 使用bcrypt风格的哈希（简化版）
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_admin_account():
    """创建管理员账户"""
    print("🔧 创建管理员账户")
    print("=" * 50)
    
    # 数据库路径
    db_path = 'backend/data/database/education_platform.db'
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return None, None
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查是否已有管理员
        cursor.execute("SELECT id, username, email, full_name FROM users WHERE role = 'admin'")
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print(f"✅ 已存在管理员账户:")
            print(f"   ID: {existing_admin[0]}")
            print(f"   用户名: {existing_admin[1]}")
            print(f"   邮箱: {existing_admin[2]}")
            print(f"   姓名: {existing_admin[3]}")
            
            # 重置密码
            reset = input("\n是否重置管理员密码为 'admin123'？(y/N): ")
            if reset.lower() == 'y':
                new_password_hash = hash_password("admin123")
                cursor.execute(
                    "UPDATE users SET hashed_password = ? WHERE id = ?",
                    (new_password_hash, existing_admin[0])
                )
                conn.commit()
                print("✅ 密码已重置为: admin123")
            
            conn.close()
            return existing_admin[1], "admin123"
        
        # 创建新管理员
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
        
        # 哈希密码
        password_hash = hash_password(admin_data["password"])
        
        # 插入管理员记录
        cursor.execute("""
            INSERT INTO users (
                username, email, hashed_password, full_name, role,
                is_active, is_verified, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            admin_data["username"],
            admin_data["email"], 
            password_hash,
            admin_data["full_name"],
            "admin",
            1,  # is_active
            1,  # is_verified
            datetime.utcnow().isoformat()
        ))
        
        conn.commit()
        admin_id = cursor.lastrowid
        
        print(f"✅ 管理员账户创建成功！")
        print(f"   ID: {admin_id}")
        print(f"   用户名: {admin_data['username']}")
        print(f"   密码: {admin_data['password']}")
        
        conn.close()
        return admin_data["username"], admin_data["password"]
        
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        if 'conn' in locals():
            conn.close()
        return None, None

def test_admin_login(username, password):
    """测试管理员登录"""
    if not username or not password:
        return
    
    print(f"\n🧪 测试管理员登录")
    print("=" * 50)
    
    try:
        import requests
        
        # 测试登录
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post("http://localhost:8000/api/v1/auth/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            
            print(f"✅ 登录测试成功！")
            print(f"   用户: {user.get('username')}")
            print(f"   角色: {user.get('role')}")
            print(f"   姓名: {user.get('full_name')}")
            
            if user.get('role') == 'admin':
                print(f"✅ 管理员权限验证通过")
            else:
                print(f"❌ 权限验证失败，角色为: {user.get('role')}")
                
        else:
            print(f"❌ 登录测试失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️ 无法连接到后端服务: {e}")
        print("   请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 登录测试异常: {e}")

def main():
    """主函数"""
    print("🚀 管理员账户管理")
    print("=" * 50)
    
    # 检查bcrypt
    try:
        import bcrypt
    except ImportError:
        print("❌ 缺少bcrypt库，正在安装...")
        os.system("pip install bcrypt")
        try:
            import bcrypt
            print("✅ bcrypt安装成功")
        except ImportError:
            print("❌ bcrypt安装失败，请手动安装: pip install bcrypt")
            return
    
    # 创建管理员账户
    username, password = create_admin_account()
    
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
        print(f"1. 确保前端服务运行: npm run dev")
        print(f"2. 确保后端服务运行: uvicorn app.main:app --reload")
        print(f"3. 访问 http://localhost:5173")
        print(f"4. 点击右上角的'管理员'按钮")
        print(f"5. 使用上述账户信息登录")
        print(f"6. 进入管理员控制台")

if __name__ == "__main__":
    main()

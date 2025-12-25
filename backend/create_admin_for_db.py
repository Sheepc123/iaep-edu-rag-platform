#!/usr/bin/env python3
"""
为现有数据库创建管理员账户
"""
import sqlite3
import os
from datetime import datetime

def hash_password_simple(password: str) -> str:
    """简单的密码哈希（使用bcrypt）"""
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except ImportError:
        # 如果没有bcrypt，使用简单的哈希（仅用于测试）
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def create_admin_account():
    """创建管理员账户"""
    print("🔧 为现有数据库创建管理员账户")
    print("=" * 60)
    
    # 数据库路径
    db_path = 'data/database/education_platform.db'
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return None, None
    
    print(f"📁 数据库路径: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 首先查看表结构
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"📋 users表字段: {', '.join(column_names)}")
        
        # 检查是否已有管理员
        cursor.execute("SELECT id, username, email, full_name, role FROM users WHERE role = 'admin'")
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print(f"\n✅ 已存在管理员账户:")
            print(f"   ID: {existing_admin[0]}")
            print(f"   用户名: {existing_admin[1]}")
            print(f"   邮箱: {existing_admin[2]}")
            print(f"   姓名: {existing_admin[3]}")
            print(f"   角色: {existing_admin[4]}")
            
            # 询问是否重置密码
            print(f"\n🔑 管理员登录信息:")
            print(f"   用户名: {existing_admin[1]}")
            print(f"   密码: 123456 (如果之前重置过)")

            reset = input("\n是否重置管理员密码为 '123456'？(y/N): ")
            if reset.lower() == 'y':
                new_password_hash = hash_password_simple("123456")
                cursor.execute(
                    "UPDATE users SET hashed_password = ? WHERE id = ?",
                    (new_password_hash, existing_admin[0])
                )
                conn.commit()
                print("✅ 密码已重置为: 123456")

            conn.close()
            return existing_admin[1], "123456"
        
        # 创建新管理员
        admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "123456",
            "full_name": "系统管理员"
        }
        
        print(f"\n🆕 创建新的管理员账户...")
        print(f"   用户名: {admin_data['username']}")
        print(f"   密码: {admin_data['password']}")
        print(f"   邮箱: {admin_data['email']}")
        print(f"   姓名: {admin_data['full_name']}")
        
        # 哈希密码
        password_hash = hash_password_simple(admin_data["password"])
        
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
        
        print(f"\n✅ 管理员账户创建成功！")
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

def verify_admin_in_db():
    """验证管理员账户是否在数据库中"""
    print(f"\n🔍 验证管理员账户...")
    
    db_path = 'data/database/education_platform.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询管理员账户
        cursor.execute("SELECT id, username, email, full_name, role, is_active FROM users WHERE role = 'admin'")
        admins = cursor.fetchall()
        
        if admins:
            print(f"✅ 数据库中的管理员账户:")
            for admin in admins:
                status = "活跃" if admin[5] else "禁用"
                print(f"   ID: {admin[0]}, 用户名: {admin[1]}, 邮箱: {admin[2]}")
                print(f"   姓名: {admin[3]}, 角色: {admin[4]}, 状态: {status}")
        else:
            print(f"❌ 数据库中没有管理员账户")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")

def main():
    """主函数"""
    print("🚀 管理员账户管理工具")
    print("=" * 60)
    
    # 检查bcrypt
    try:
        import bcrypt
        print("✅ bcrypt库可用")
    except ImportError:
        print("⚠️ bcrypt库不可用，将使用简单哈希（仅用于测试）")
        print("   建议安装bcrypt: pip install bcrypt")
    
    # 创建管理员账户
    username, password = create_admin_account()
    
    # 验证账户
    verify_admin_in_db()
    
    print("\n" + "=" * 60)
    print("🎯 操作完成")
    
    if username and password:
        print(f"\n📋 管理员登录信息:")
        print(f"   用户名: {username}")
        print(f"   密码: {password}")
        print(f"   登录地址: http://localhost:5173/admin/login")
        
        print(f"\n💡 使用步骤:")
        print(f"1. 确保前端服务运行: cd frontend && npm run dev")
        print(f"2. 确保后端服务运行: cd backend && uvicorn app.main:app --reload")
        print(f"3. 访问 http://localhost:5173")
        print(f"4. 点击右上角的'管理员'按钮")
        print(f"5. 使用上述账户信息登录")
        print(f"6. 进入管理员控制台")
        
        print(f"\n🔧 如果登录失败，请检查:")
        print(f"   - 后端服务是否正常运行")
        print(f"   - 数据库连接是否正常")
        print(f"   - 用户名和密码是否正确")

if __name__ == "__main__":
    main()

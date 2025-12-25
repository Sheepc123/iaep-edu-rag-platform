#!/usr/bin/env python3
"""
快速创建管理员账户
"""
import sqlite3
from datetime import datetime

def bcrypt_hash(password):
    """使用bcrypt哈希密码"""
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except ImportError:
        print("❌ 需要安装bcrypt: pip install bcrypt")
        return None

def create_admin():
    """创建管理员"""
    db_path = 'data/database/education_platform.db'
    
    print("🔧 快速创建管理员账户")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查是否已有管理员
        cursor.execute("SELECT username FROM users WHERE role = 'admin'")
        existing = cursor.fetchone()
        
        # 生成bcrypt哈希
        password_hash = bcrypt_hash("123456")
        if not password_hash:
            return False

        if existing:
            print(f"✅ 管理员已存在: {existing[0]}")
            # 重置密码
            cursor.execute(
                "UPDATE users SET hashed_password = ? WHERE role = 'admin'",
                (password_hash,)
            )
            conn.commit()
            print("✅ 密码已重置为: 123456")
            username = existing[0]
        else:
            # 创建新管理员
            cursor.execute("""
                INSERT INTO users (
                    username, email, hashed_password, full_name, 
                    role, is_active, is_verified, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "admin",
                "admin@example.com",
                password_hash,
                "系统管理员",
                "admin",
                1,
                1,
                datetime.now().isoformat()
            ))
            conn.commit()
            print("✅ 管理员账户创建成功")
            username = "admin"
        
        conn.close()
        
        print("\n📋 管理员登录信息:")
        print(f"   用户名: {username}")
        print(f"   密码: 123456")
        print(f"   登录地址: http://localhost:5173/admin/login")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

if __name__ == "__main__":
    create_admin()

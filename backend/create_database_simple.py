#!/usr/bin/env python3
"""
简单的数据库创建脚本
直接创建数据库到正确位置
"""

import os
import sqlite3
from pathlib import Path
import hashlib


def cleanup_old_database():
    """清理旧的数据库文件"""
    print("🧹 清理旧数据库文件...")
    
    old_files = [
        "education_platform.db",
        "database/data/education_platform.db"
    ]
    
    for file_path in old_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ 删除旧文件: {file_path}")


def ensure_database_directory():
    """确保数据库目录存在"""
    print("📁 确保数据库目录存在...")
    
    db_dir = Path("data/database")
    db_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 数据库目录已准备: {db_dir}")
    
    return db_dir / "education_platform.db"


def hash_password(password: str) -> str:
    """简单的密码哈希"""
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except ImportError:
        # 如果bcrypt不可用，使用简单的哈希（仅用于测试）
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


def create_database_tables(db_path):
    """创建数据库表"""
    print("🔧 创建数据库表...")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                phone VARCHAR(20),
                avatar VARCHAR(255),
                role VARCHAR(20) NOT NULL DEFAULT 'student',
                is_active BOOLEAN NOT NULL DEFAULT 1,
                is_verified BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        print("✅ 创建表: users")
        
        # 创建学生档案表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                student_id VARCHAR(20) UNIQUE,
                school VARCHAR(100),
                major VARCHAR(100),
                grade VARCHAR(20),
                class_name VARCHAR(50),
                enrollment_year INTEGER,
                total_study_time INTEGER DEFAULT 0,
                courses_completed INTEGER DEFAULT 0,
                exercises_completed INTEGER DEFAULT 0,
                average_score DECIMAL(5,2) DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ 创建表: student_profiles")
        
        # 创建教师档案表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                employee_id VARCHAR(20) UNIQUE,
                department VARCHAR(100),
                title VARCHAR(50),
                bio TEXT,
                office_location VARCHAR(100),
                courses_created INTEGER DEFAULT 0,
                students_taught INTEGER DEFAULT 0,
                total_teaching_hours INTEGER DEFAULT 0,
                rating DECIMAL(3,2) DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ 创建表: teacher_profiles")
        
        # 创建用户会话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token VARCHAR(255) UNIQUE NOT NULL,
                refresh_token VARCHAR(255) UNIQUE NOT NULL,
                device_info VARCHAR(255),
                ip_address VARCHAR(45),
                user_agent TEXT,
                is_active BOOLEAN DEFAULT 1,
                expires_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ 创建表: user_sessions")
        
        # 创建用户活动表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type VARCHAR(50) NOT NULL,
                activity_data TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        print("✅ 创建表: user_activities")
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_profiles_student_id ON student_profiles(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_teacher_profiles_employee_id ON teacher_profiles(employee_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id)")
        print("✅ 创建索引完成")
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 创建表失败: {e}")
        raise
    finally:
        conn.close()


def create_default_users(db_path):
    """创建默认用户"""
    print("👥 创建默认用户...")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 创建测试教师
        teacher_password = hash_password("123456")
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, ("teacher1", "teacher1@example.com", teacher_password, "teacher", 1))
        
        teacher_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO teacher_profiles (user_id, department, title, bio)
            VALUES (?, ?, ?, ?)
        """, (teacher_id, "计算机科学", "副教授", "专注于机器学习和数据科学教学"))
        
        print("✅ 创建测试教师: teacher1 (密码: 123456)")
        
        # 创建测试学生
        student_password = hash_password("123456")
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, ("student1", "student1@example.com", student_password, "student", 1))
        
        student_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO student_profiles (user_id, student_id, major, grade)
            VALUES (?, ?, ?, ?)
        """, (student_id, "2024001", "计算机科学与技术", "大三"))
        
        print("✅ 创建测试学生: student1 (密码: 123456)")
        
        conn.commit()
        print("✅ 默认用户创建完成")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 创建默认用户失败: {e}")
        raise
    finally:
        conn.close()


def verify_database(db_path):
    """验证数据库"""
    print("🔍 验证数据库...")
    
    if db_path.exists():
        print(f"✅ 数据库文件存在: {db_path}")
        print(f"📊 文件大小: {db_path.stat().st_size} bytes")
        
        # 验证用户数据
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT username, role, email FROM users")
            users = cursor.fetchall()
            print(f"👥 用户总数: {len(users)}")
            
            for username, role, email in users:
                print(f"   - {username} ({role}) - {email}")
                
                if role == "teacher":
                    cursor.execute("""
                        SELECT department, title FROM teacher_profiles 
                        WHERE user_id = (SELECT id FROM users WHERE username = ?)
                    """, (username,))
                    profile = cursor.fetchone()
                    if profile:
                        print(f"     教师档案: {profile[0]} - {profile[1]}")
                        
                elif role == "student":
                    cursor.execute("""
                        SELECT student_id, major FROM student_profiles 
                        WHERE user_id = (SELECT id FROM users WHERE username = ?)
                    """, (username,))
                    profile = cursor.fetchone()
                    if profile:
                        print(f"     学生档案: {profile[0]} - {profile[1]}")
        finally:
            conn.close()
    else:
        print(f"❌ 数据库文件不存在: {db_path}")


def main():
    """主函数"""
    print("🚀 创建数据库到正确位置")
    print("=" * 60)
    
    try:
        # 1. 清理旧数据库文件
        cleanup_old_database()
        
        # 2. 确保数据库目录存在
        db_path = ensure_database_directory()
        
        # 3. 创建数据库表
        create_database_tables(db_path)
        
        # 4. 创建默认用户
        create_default_users(db_path)
        
        # 5. 验证数据库
        verify_database(db_path)
        
        print("\n" + "=" * 60)
        print("🎉 数据库创建完成!")
        print("\n📋 数据库信息:")
        print(f"   位置: {db_path}")
        print("   默认用户:")
        print("     - teacher1 / 123456 (教师)")
        print("     - student1 / 123456 (学生)")
        
        print("\n🚀 现在可以:")
        print("1. 启动后端服务: python run.py")
        print("2. 测试登录功能")
        print("3. 继续重构其他模块")
        
    except Exception as e:
        print(f"\n❌ 数据库创建失败: {e}")
        print("请检查错误信息并重试")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
重新创建认证相关的数据库表
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def recreate_auth_tables():
    """重新创建认证相关表"""
    print("🔄 重新创建认证相关表...")
    
    try:
        from app.core.database import engine
        from app.models.user import User, StudentProfile, TeacherProfile, UserSession, UserActivity
        
        # 删除相关表
        print("删除现有表...")
        UserActivity.__table__.drop(engine, checkfirst=True)
        UserSession.__table__.drop(engine, checkfirst=True)
        StudentProfile.__table__.drop(engine, checkfirst=True)
        TeacherProfile.__table__.drop(engine, checkfirst=True)
        User.__table__.drop(engine, checkfirst=True)
        
        # 重新创建表
        print("创建新表...")
        User.__table__.create(engine)
        print("✅ 创建 users 表")
        
        StudentProfile.__table__.create(engine)
        print("✅ 创建 student_profiles 表")
        
        TeacherProfile.__table__.create(engine)
        print("✅ 创建 teacher_profiles 表")
        
        UserSession.__table__.create(engine)
        print("✅ 创建 user_sessions 表")
        
        UserActivity.__table__.create(engine)
        print("✅ 创建 user_activities 表")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_default_users():
    """创建默认用户"""
    print("\n👥 创建默认用户...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.user import User, StudentProfile, TeacherProfile
        from app.core.security import PasswordManager
        
        db = SessionLocal()
        
        # 创建教师用户
        teacher_user = User(
            username="teacher1",
            email="teacher1@example.com",
            hashed_password=PasswordManager.hash_password("123456"),
            role="teacher",
            is_active=True
        )
        db.add(teacher_user)
        db.flush()
        
        teacher_profile = TeacherProfile(
            user_id=teacher_user.id,
            department="计算机科学",
            title="副教授",
            bio="专注于机器学习和数据科学教学"
        )
        db.add(teacher_profile)
        print("✅ 创建教师用户: teacher1")
        
        # 创建学生用户
        student_user = User(
            username="student1",
            email="student1@example.com",
            hashed_password=PasswordManager.hash_password("123456"),
            role="student",
            is_active=True
        )
        db.add(student_user)
        db.flush()
        
        student_profile = StudentProfile(
            user_id=student_user.id,
            student_id="2024001",
            major="计算机科学与技术",
            grade="大三"
        )
        db.add(student_profile)
        print("✅ 创建学生用户: student1")
        
        db.commit()
        db.close()
        
        print("✅ 默认用户创建完成")
        return True
        
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_tables():
    """验证表结构"""
    print("\n🔍 验证表结构...")
    
    try:
        import sqlite3
        
        db_path = Path("data/database/education_platform.db")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 检查user_sessions表结构
        cursor.execute("PRAGMA table_info(user_sessions)")
        columns = cursor.fetchall()
        
        print("user_sessions表字段:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 检查是否有session_token字段
        column_names = [col[1] for col in columns]
        if 'session_token' in column_names:
            print("✅ session_token字段存在")
        else:
            print("❌ session_token字段缺失")
        
        conn.close()
        return 'session_token' in column_names
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def test_login():
    """测试登录功能"""
    print("\n🔍 测试登录功能...")
    
    try:
        from app.core.database import SessionLocal
        from app.services.auth_service import AuthService
        from app.schemas.auth import UserLogin
        
        db = SessionLocal()
        auth_service = AuthService(db)
        
        login_data = UserLogin(
            username="teacher1",
            password="123456",
            remember_me=False,
            device_info="test_device"
        )
        
        user, tokens = auth_service.authenticate_user(login_data)
        
        print("✅ 登录测试成功")
        print(f"   用户: {user.username}")
        print(f"   角色: {user.role}")
        print(f"   令牌类型: {tokens.get('token_type')}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("🚀 重新创建认证系统")
    print("=" * 50)
    
    # 1. 重新创建表
    tables_ok = recreate_auth_tables()
    
    if not tables_ok:
        print("❌ 表创建失败，停止执行")
        return
    
    # 2. 创建默认用户
    users_ok = create_default_users()
    
    # 3. 验证表结构
    verify_ok = verify_tables()
    
    # 4. 测试登录
    login_ok = test_login()
    
    print("\n" + "=" * 50)
    print("📋 重建结果:")
    print(f"   数据表: {'✅' if tables_ok else '❌'}")
    print(f"   默认用户: {'✅' if users_ok else '❌'}")
    print(f"   表结构验证: {'✅' if verify_ok else '❌'}")
    print(f"   登录测试: {'✅' if login_ok else '❌'}")
    
    if all([tables_ok, users_ok, verify_ok, login_ok]):
        print("\n🎉 认证系统重建完成！")
        print("\n📋 测试账户:")
        print("   教师: teacher1 / 123456")
        print("   学生: student1 / 123456")
        print("\n🚀 现在可以启动服务并测试登录功能")
    else:
        print("\n❌ 重建过程中出现问题")


if __name__ == "__main__":
    main()

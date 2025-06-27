#!/usr/bin/env python3
"""
功能模块重构器
按功能模块逐步重构数据库和代码
"""

import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import engine, Base
from sqlalchemy import text


class ModuleReconstructor:
    """功能模块重构器"""
    
    def __init__(self):
        self.db_path = Path("data/database/education_platform.db")
        self.modules = {
            "auth": "用户认证模块",
            "course": "课程管理模块", 
            "exercise": "练习系统模块",
            "knowledge": "知识库模块",
            "chat": "聊天AI模块"
        }
        
    def show_available_modules(self):
        """显示可用的功能模块"""
        print("📋 可重构的功能模块:")
        print("=" * 40)
        for key, name in self.modules.items():
            print(f"  {key:<12} - {name}")
        print("=" * 40)
    
    def reconstruct_auth_module(self):
        """重构用户认证模块"""
        print("🔐 重构用户认证模块...")
        
        # 导入用户相关模型
        from app.models.user import User, StudentProfile, TeacherProfile, UserSession, UserActivity
        
        # 创建用户相关表
        tables_to_create = [User, StudentProfile, TeacherProfile, UserSession, UserActivity]
        
        for table in tables_to_create:
            table.__table__.create(engine, checkfirst=True)
            print(f"✅ 创建表: {table.__tablename__}")
        
        # 创建默认用户数据
        self._create_default_users()
        
        print("✅ 用户认证模块重构完成")
    
    def reconstruct_course_module(self):
        """重构课程管理模块"""
        print("📚 重构课程管理模块...")
        
        # 导入课程相关模型
        from app.models.course import Course, Lesson, CourseEnrollment, LessonProgress, CourseCategory, StudyPlan
        
        # 创建课程相关表
        tables_to_create = [CourseCategory, Course, Lesson, CourseEnrollment, LessonProgress, StudyPlan]
        
        for table in tables_to_create:
            table.__table__.create(engine, checkfirst=True)
            print(f"✅ 创建表: {table.__tablename__}")
        
        # 创建默认课程数据
        self._create_default_courses()
        
        print("✅ 课程管理模块重构完成")
    
    def reconstruct_exercise_module(self):
        """重构练习系统模块"""
        print("📝 重构练习系统模块...")
        
        # 导入练习相关模型
        from app.models.exercise import (
            Exercise, Question, ExerciseAttempt, StudentAnswer, WrongQuestion, 
            ExerciseStatistics, GradeAnalysis, StudentPerformance, ClassGradeReport
        )
        
        # 创建练习相关表
        tables_to_create = [
            Exercise, Question, ExerciseAttempt, StudentAnswer, WrongQuestion,
            ExerciseStatistics, GradeAnalysis, StudentPerformance, ClassGradeReport
        ]
        
        for table in tables_to_create:
            table.__table__.create(engine, checkfirst=True)
            print(f"✅ 创建表: {table.__tablename__}")
        
        print("✅ 练习系统模块重构完成")
    
    def reconstruct_knowledge_module(self):
        """重构知识库模块"""
        print("📖 重构知识库模块...")
        
        # 导入知识库相关模型
        from app.models.knowledge_base import TeacherKnowledgeDoc
        
        # 创建知识库相关表
        TeacherKnowledgeDoc.__table__.create(engine, checkfirst=True)
        print(f"✅ 创建表: {TeacherKnowledgeDoc.__tablename__}")
        
        # 创建FTS5全文搜索表
        self._create_fts_tables()
        
        print("✅ 知识库模块重构完成")
    
    def reconstruct_chat_module(self):
        """重构聊天AI模块"""
        print("💬 重构聊天AI模块...")
        
        # 导入聊天相关模型
        from app.models.chat import (
            ChatRoom, ChatMember, ChatMessage, UserContact,
            AIConversation, AIMessage, AIRecommendation, UserOnlineStatus
        )
        
        # 创建聊天相关表
        tables_to_create = [
            ChatRoom, ChatMember, ChatMessage, UserContact,
            AIConversation, AIMessage, AIRecommendation, UserOnlineStatus
        ]
        
        for table in tables_to_create:
            table.__table__.create(engine, checkfirst=True)
            print(f"✅ 创建表: {table.__tablename__}")
        
        print("✅ 聊天AI模块重构完成")
    
    def _create_default_users(self):
        """创建默认用户数据"""
        print("👥 创建默认用户数据...")
        
        from database.connection import SessionLocal
        from app.models.user import User, StudentProfile, TeacherProfile
        from app.core.security import PasswordManager
        
        db = SessionLocal()
        try:
            # 检查并创建测试教师
            existing_teacher = db.query(User).filter(User.username == "teacher1").first()
            if not existing_teacher:
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
                print("✅ 创建测试教师: teacher1")
            else:
                print("ℹ️  测试教师已存在: teacher1")

            # 检查并创建测试学生
            existing_student = db.query(User).filter(User.username == "student1").first()
            if not existing_student:
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
                print("✅ 创建测试学生: student1")
            else:
                print("ℹ️  测试学生已存在: student1")

            db.commit()
            print("✅ 默认用户数据检查完成")
            
        except Exception as e:
            db.rollback()
            print(f"❌ 创建默认用户失败: {e}")
        finally:
            db.close()
    
    def _create_default_courses(self):
        """创建默认课程数据"""
        print("📚 创建默认课程数据...")
        
        from database.connection import SessionLocal
        from app.models.course import CourseCategory, Course
        from app.models.user import User
        
        db = SessionLocal()
        try:
            # 创建课程分类
            category = CourseCategory(
                name="计算机科学",
                description="计算机科学相关课程",
                is_active=True
            )
            db.add(category)
            db.flush()
            
            # 获取教师用户
            teacher = db.query(User).filter(User.username == "teacher1").first()
            if teacher:
                # 创建示例课程
                course = Course(
                    title="Python编程基础",
                    description="学习Python编程语言的基础知识",
                    teacher_id=teacher.id,
                    category_id=category.id,
                    difficulty_level="beginner",
                    is_published=True
                )
                db.add(course)
            
            db.commit()
            print("✅ 默认课程创建完成")
            
        except Exception as e:
            db.rollback()
            print(f"❌ 创建默认课程失败: {e}")
        finally:
            db.close()
    
    def _create_fts_tables(self):
        """创建FTS5全文搜索表"""
        print("🔍 创建FTS5全文搜索表...")
        
        try:
            with engine.connect() as conn:
                # 创建FTS5虚拟表
                conn.execute(text("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS teacher_knowledge_docs_fts 
                    USING fts5(
                        title, 
                        content, 
                        keywords,
                        content='teacher_knowledge_docs',
                        content_rowid='id'
                    )
                """))
                
                # 创建触发器保持FTS表同步
                conn.execute(text("""
                    CREATE TRIGGER IF NOT EXISTS teacher_knowledge_docs_ai AFTER INSERT ON teacher_knowledge_docs BEGIN
                        INSERT INTO teacher_knowledge_docs_fts(rowid, title, content, keywords) 
                        VALUES (new.id, new.title, new.content, new.keywords);
                    END
                """))
                
                conn.execute(text("""
                    CREATE TRIGGER IF NOT EXISTS teacher_knowledge_docs_ad AFTER DELETE ON teacher_knowledge_docs BEGIN
                        INSERT INTO teacher_knowledge_docs_fts(teacher_knowledge_docs_fts, rowid, title, content, keywords) 
                        VALUES('delete', old.id, old.title, old.content, old.keywords);
                    END
                """))
                
                conn.execute(text("""
                    CREATE TRIGGER IF NOT EXISTS teacher_knowledge_docs_au AFTER UPDATE ON teacher_knowledge_docs BEGIN
                        INSERT INTO teacher_knowledge_docs_fts(teacher_knowledge_docs_fts, rowid, title, content, keywords) 
                        VALUES('delete', old.id, old.title, old.content, old.keywords);
                        INSERT INTO teacher_knowledge_docs_fts(rowid, title, content, keywords) 
                        VALUES (new.id, new.title, new.content, new.keywords);
                    END
                """))
                
                conn.commit()
                print("✅ FTS5表和触发器创建完成")
                
        except Exception as e:
            print(f"❌ 创建FTS5表失败: {e}")
    
    def reconstruct_module(self, module_name: str):
        """重构指定模块"""
        if module_name not in self.modules:
            print(f"❌ 未知模块: {module_name}")
            self.show_available_modules()
            return False
        
        print(f"\n🔄 开始重构模块: {self.modules[module_name]}")
        print("=" * 50)
        
        try:
            if module_name == "auth":
                self.reconstruct_auth_module()
            elif module_name == "course":
                self.reconstruct_course_module()
            elif module_name == "exercise":
                self.reconstruct_exercise_module()
            elif module_name == "knowledge":
                self.reconstruct_knowledge_module()
            elif module_name == "chat":
                self.reconstruct_chat_module()
            
            print(f"✅ 模块 {self.modules[module_name]} 重构完成")
            return True
            
        except Exception as e:
            print(f"❌ 模块重构失败: {e}")
            return False


def main():
    """主函数"""
    print("🔧 功能模块重构器")
    print("=" * 50)
    
    reconstructor = ModuleReconstructor()
    
    if len(sys.argv) > 1:
        # 命令行参数指定模块
        module_name = sys.argv[1]
        reconstructor.reconstruct_module(module_name)
    else:
        # 交互式选择模块
        reconstructor.show_available_modules()
        print("\n请选择要重构的模块 (输入模块代码):")
        module_name = input("模块代码: ").strip().lower()
        
        if module_name:
            reconstructor.reconstruct_module(module_name)
        else:
            print("❌ 未选择模块")


if __name__ == "__main__":
    main()

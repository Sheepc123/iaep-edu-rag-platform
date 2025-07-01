#!/usr/bin/env python3
"""
为课程创建测试注册数据的脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.course import Course, CourseEnrollment
from app.models.user import User
from sqlalchemy.orm import Session
from datetime import datetime, timezone

def create_test_enrollments():
    """创建测试课程注册数据"""
    db = next(get_db())
    
    try:
        # 检查课程是否存在
        course = db.query(Course).filter(Course.id == 1).first()
        if not course:
            print("课程ID=1不存在，请先创建课程")
            return
        
        print(f"找到课程: {course.title} (教师ID: {course.instructor_id})")
        
        # 检查是否已有注册数据
        existing_enrollments = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == 1
        ).count()

        if existing_enrollments >= 3:
            print(f"课程已有 {existing_enrollments} 个注册记录，足够测试使用")
            return
        
        # 查找学生用户
        students = db.query(User).filter(User.role == 'student').limit(5).all()
        if len(students) == 0:
            print("没有找到学生用户，创建一些测试学生...")
            
            # 创建测试学生
            test_students = [
                {
                    "username": "student1",
                    "email": "student1@example.com",
                    "full_name": "张三",
                    "hashed_password": "$2b$12$dummy_hash",
                    "role": "student",
                    "is_active": True,
                    "is_verified": True
                },
                {
                    "username": "student2", 
                    "email": "student2@example.com",
                    "full_name": "李四",
                    "hashed_password": "$2b$12$dummy_hash",
                    "role": "student",
                    "is_active": True,
                    "is_verified": True
                },
                {
                    "username": "student3",
                    "email": "student3@example.com", 
                    "full_name": "王五",
                    "hashed_password": "$2b$12$dummy_hash",
                    "role": "student",
                    "is_active": True,
                    "is_verified": True
                }
            ]
            
            for student_data in test_students:
                # 检查用户是否已存在
                existing_user = db.query(User).filter(User.username == student_data["username"]).first()
                if not existing_user:
                    student = User(**student_data)
                    db.add(student)
            
            db.commit()
            
            # 重新获取学生列表
            students = db.query(User).filter(User.role == 'student').limit(5).all()
        
        print(f"找到 {len(students)} 个学生用户")
        
        # 为每个学生创建注册记录
        enrollments_created = 0
        for i, student in enumerate(students):
            # 检查是否已经注册
            existing = db.query(CourseEnrollment).filter(
                CourseEnrollment.course_id == 1,
                CourseEnrollment.student_id == student.id
            ).first()
            
            if not existing:
                enrollment = CourseEnrollment(
                    course_id=1,
                    student_id=student.id,
                    progress_percentage=float(i * 20 + 10),  # 10%, 30%, 50%, 70%, 90%
                    completed_lessons=i,
                    total_study_time=i * 45 + 30,  # 30, 75, 120, 165, 210 分钟
                    is_completed=False,
                    is_active=True,
                    enrolled_at=datetime.now(timezone.utc)
                )
                db.add(enrollment)
                enrollments_created += 1
                print(f"为学生 {student.full_name} 创建注册记录")
        
        if enrollments_created > 0:
            # 更新课程的注册人数
            course.enrolled_students = enrollments_created
            
            db.commit()
            print(f"成功创建了 {enrollments_created} 个课程注册记录")
        else:
            print("所有学生都已注册此课程")
            
    except Exception as e:
        print(f"创建测试数据时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_enrollments()

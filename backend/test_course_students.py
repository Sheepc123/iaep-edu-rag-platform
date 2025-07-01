#!/usr/bin/env python3
"""
测试课程学生API的脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.course import Course, CourseEnrollment
from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import and_

def test_course_students():
    """测试课程学生数据"""
    db = next(get_db())
    
    try:
        # 检查课程是否存在
        course = db.query(Course).filter(Course.id == 1).first()
        if not course:
            print("课程ID=1不存在")
            return
        
        print(f"找到课程: {course.title} (教师ID: {course.instructor_id})")
        
        # 检查是否有学生注册
        enrollments = db.query(CourseEnrollment).filter(
            and_(
                CourseEnrollment.course_id == 1,
                CourseEnrollment.is_active == True
            )
        ).all()
        
        print(f"找到 {len(enrollments)} 个注册记录")
        
        if len(enrollments) == 0:
            print("没有学生注册此课程，创建测试数据...")
            
            # 查找学生用户
            students = db.query(User).filter(User.role == 'student').limit(3).all()
            if len(students) == 0:
                print("没有找到学生用户")
                return
            
            # 为每个学生创建注册记录
            for i, student in enumerate(students):
                enrollment = CourseEnrollment(
                    course_id=1,
                    student_id=student.id,
                    progress_percentage=float(i * 25),
                    completed_lessons=i,
                    total_study_time=i * 60,
                    is_completed=False,
                    is_active=True
                )
                db.add(enrollment)
            
            db.commit()
            print(f"创建了 {len(students)} 个测试注册记录")
        
        # 再次查询验证
        students_query = db.query(
            User.id,
            User.username,
            User.full_name,
            User.email,
            User.avatar,
            CourseEnrollment.enrolled_at,
            CourseEnrollment.progress_percentage,
            CourseEnrollment.completed_lessons,
            CourseEnrollment.total_study_time,
            CourseEnrollment.is_completed,
            CourseEnrollment.last_accessed
        ).join(
            CourseEnrollment, User.id == CourseEnrollment.student_id
        ).filter(
            and_(
                CourseEnrollment.course_id == 1,
                CourseEnrollment.is_active == True
            )
        ).all()
        
        print(f"最终查询结果: {len(students_query)} 个学生")
        for student in students_query:
            print(f"  - {student.full_name} ({student.username}) - 进度: {student.progress_percentage}%")
            
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_course_students()

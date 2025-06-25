"""
创建课程注册测试数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.course import Course, CourseEnrollment
from app.models.user import User
from datetime import datetime, timedelta


def create_enrollment_test_data():
    """创建课程注册测试数据"""
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 获取学生用户
        student = db.query(User).filter(User.role == "student").first()
        if not student:
            print("❌ 未找到学生用户")
            return
        
        print(f"✅ 找到学生用户: {student.username} (ID: {student.id})")
        
        # 获取前几门课程
        courses = db.query(Course).filter(Course.is_published == True).limit(5).all()
        if not courses:
            print("❌ 未找到已发布的课程")
            return
        
        print(f"✅ 找到 {len(courses)} 门课程")
        
        # 检查现有注册记录
        existing_enrollments = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id == student.id
        ).all()
        
        print(f"ℹ️  学生已注册 {len(existing_enrollments)} 门课程")
        
        # 为学生注册前3门课程
        enrolled_count = 0
        for i, course in enumerate(courses[:3]):
            # 检查是否已经注册
            existing = db.query(CourseEnrollment).filter(
                CourseEnrollment.student_id == student.id,
                CourseEnrollment.course_id == course.id
            ).first()
            
            if existing:
                print(f"⚠️  课程 '{course.title}' 已经注册过了")
                continue
            
            # 创建注册记录
            enrollment = CourseEnrollment(
                course_id=course.id,
                student_id=student.id,
                progress_percentage=20.0 + (i * 15),  # 模拟不同的学习进度
                completed_lessons=i + 1,
                total_study_time=(i + 1) * 60,  # 模拟学习时间
                is_completed=False,
                enrolled_at=datetime.now() - timedelta(days=7 - i),
                last_accessed=datetime.now() - timedelta(hours=i + 1)
            )
            
            db.add(enrollment)
            enrolled_count += 1
            print(f"✅ 注册课程: {course.title}")
        
        # 提交更改
        db.commit()
        
        print(f"\n🎉 成功创建 {enrolled_count} 个注册记录")
        
        # 验证创建的数据
        print("\n=== 验证创建的数据 ===")
        enrollments = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id == student.id
        ).all()
        
        for enrollment in enrollments:
            course = db.query(Course).filter(Course.id == enrollment.course_id).first()
            print(f"- 课程: {course.title if course else '未知'}")
            print(f"  进度: {enrollment.progress_percentage}%")
            print(f"  注册时间: {enrollment.enrolled_at}")
            print()
        
        print("✅ 数据创建完成！")
        
    except Exception as e:
        print(f"❌ 创建数据失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def check_existing_data():
    """检查现有数据"""
    db = SessionLocal()
    
    try:
        print("=== 检查现有数据 ===")
        
        # 检查用户
        users = db.query(User).all()
        print(f"用户总数: {len(users)}")
        for user in users:
            print(f"  - {user.username} ({user.role})")
        
        # 检查课程
        courses = db.query(Course).all()
        print(f"\n课程总数: {len(courses)}")
        for course in courses[:5]:  # 只显示前5个
            print(f"  - {course.title} (ID: {course.id})")
        
        # 检查注册记录
        enrollments = db.query(CourseEnrollment).all()
        print(f"\n注册记录总数: {len(enrollments)}")
        for enrollment in enrollments:
            course = db.query(Course).filter(Course.id == enrollment.course_id).first()
            user = db.query(User).filter(User.id == enrollment.student_id).first()
            print(f"  - {user.username if user else '未知用户'} -> {course.title if course else '未知课程'}")
        
    except Exception as e:
        print(f"❌ 检查数据失败: {str(e)}")
    finally:
        db.close()


def main():
    """主函数"""
    print("🚀 开始创建课程注册测试数据...")
    
    # 检查现有数据
    check_existing_data()
    
    # 创建测试数据
    create_enrollment_test_data()
    
    print("\n📋 建议接下来的操作:")
    print("1. 启动后端服务: cd backend && python run.py")
    print("2. 测试API: python backend/test_my_courses_api.py")
    print("3. 检查前端页面: 访问个人中心 -> 我的课程")


if __name__ == "__main__":
    main()

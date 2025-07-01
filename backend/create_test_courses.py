#!/usr/bin/env python3
"""
创建测试课程数据来验证学生端和教师端的差异
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_courses():
    """创建多个测试课程"""
    print("📚 创建测试课程数据...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course, Lesson
        from app.models.user import User
        from app.core.security import PasswordManager
        
        db = SessionLocal()
        
        # 获取现有教师
        teacher1 = db.query(User).filter(User.username == "teacher1").first()
        if not teacher1:
            print("❌ 未找到teacher1用户")
            return False
        
        # 创建第二个教师用户（如果不存在）
        teacher2 = db.query(User).filter(User.username == "teacher2").first()
        if not teacher2:
            teacher2 = User(
                username="teacher2",
                email="teacher2@example.com",
                hashed_password=PasswordManager.hash_password("123456"),
                role="teacher",
                is_active=True
            )
            db.add(teacher2)
            db.flush()
            
            # 创建教师档案
            from app.models.user import TeacherProfile
            teacher2_profile = TeacherProfile(
                user_id=teacher2.id,
                department="数学系",
                title="讲师",
                bio="专注于数学基础教学"
            )
            db.add(teacher2_profile)
            print("✅ 创建teacher2用户")
        
        # 课程数据
        courses_data = [
            {
                "title": "Java编程进阶",
                "description": "深入学习Java编程的高级特性和企业级开发",
                "category": "编程语言",
                "difficulty": "medium",
                "duration": 1800,
                "instructor": teacher1,
                "is_published": True
            },
            {
                "title": "数据结构与算法",
                "description": "计算机科学基础课程，学习常用数据结构和算法",
                "category": "计算机基础",
                "difficulty": "hard",
                "duration": 2400,
                "instructor": teacher1,
                "is_published": False  # 未发布
            },
            {
                "title": "高等数学基础",
                "description": "大学数学基础课程，包括微积分、线性代数等",
                "category": "数学",
                "difficulty": "medium",
                "duration": 3600,
                "instructor": teacher2,
                "is_published": True
            },
            {
                "title": "概率论与数理统计",
                "description": "概率论基础和统计学应用",
                "category": "数学",
                "difficulty": "hard",
                "duration": 2000,
                "instructor": teacher2,
                "is_published": False  # 未发布
            }
        ]
        
        created_courses = []
        
        for course_data in courses_data:
            # 检查课程是否已存在
            existing = db.query(Course).filter(Course.title == course_data["title"]).first()
            if existing:
                print(f"ℹ️  课程已存在: {course_data['title']}")
                continue
            
            course = Course(
                title=course_data["title"],
                description=course_data["description"],
                category=course_data["category"],
                difficulty=course_data["difficulty"],
                duration=course_data["duration"],
                total_lessons=3,  # 默认3个课时
                instructor_id=course_data["instructor"].id,
                instructor_name=course_data["instructor"].full_name or course_data["instructor"].username,
                enrolled_students=0,
                rating=4.0,
                rating_count=0,
                is_active=True,
                is_published=course_data["is_published"]
            )
            db.add(course)
            db.flush()
            
            # 为每个课程创建3个示例课时
            for i in range(1, 4):
                lesson = Lesson(
                    course_id=course.id,
                    title=f"{course.title} - 第{i}课时",
                    description=f"第{i}个课时的内容介绍",
                    content=f"这是{course.title}的第{i}个课时内容...",
                    lesson_order=i,
                    duration=course.duration // 3,  # 平均分配时长
                    lesson_type="video" if i % 2 == 1 else "interactive",
                    is_published=course.is_published,
                    is_free=(i == 1)  # 第一课时免费
                )
                db.add(lesson)
            
            created_courses.append(course.title)
            print(f"✅ 创建课程: {course.title} ({'已发布' if course.is_published else '草稿'})")
        
        db.commit()
        db.close()
        
        print(f"\n✅ 测试课程创建完成，共创建 {len(created_courses)} 门课程")
        return True
        
    except Exception as e:
        print(f"❌ 创建测试课程失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_course_summary():
    """显示课程统计"""
    print("\n📊 课程统计...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course
        
        db = SessionLocal()
        
        # 总课程数
        total_courses = db.query(Course).count()
        print(f"总课程数: {total_courses}")
        
        # 已发布课程数
        published_courses = db.query(Course).filter(Course.is_published == True).count()
        print(f"已发布课程: {published_courses}")
        
        # 草稿课程数
        draft_courses = db.query(Course).filter(Course.is_published == False).count()
        print(f"草稿课程: {draft_courses}")
        
        # 按教师分组
        print("\n按教师分组:")
        teachers = db.query(Course.instructor_name, Course.is_published).all()
        teacher_stats = {}
        
        for instructor_name, is_published in teachers:
            if instructor_name not in teacher_stats:
                teacher_stats[instructor_name] = {"published": 0, "draft": 0}
            
            if is_published:
                teacher_stats[instructor_name]["published"] += 1
            else:
                teacher_stats[instructor_name]["draft"] += 1
        
        for teacher, stats in teacher_stats.items():
            print(f"  {teacher}: {stats['published']}门已发布, {stats['draft']}门草稿")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 统计失败: {e}")


def test_api_differences():
    """测试API差异"""
    print("\n🔍 测试API差异...")
    
    import requests
    
    try:
        # 登录获取tokens
        student_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "student1", "password": "123456", "remember_me": False}
        )
        teacher1_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False}
        )
        teacher2_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher2", "password": "123456", "remember_me": False}
        )
        
        if student_login.status_code == 200:
            student_token = student_login.json()["access_token"]
            
            # 学生端API - 只看已发布课程
            student_response = requests.get(
                "http://localhost:8000/api/v1/courses/",
                params={"is_published": True, "limit": 20},
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            if student_response.status_code == 200:
                student_data = student_response.json()
                student_courses = student_data.get('courses', [])
                print(f"🎓 学生端看到 {len(student_courses)} 门课程:")
                for course in student_courses:
                    print(f"   - {course['title']} (教师: {course['instructor_name']})")
        
        if teacher1_login.status_code == 200:
            teacher1_token = teacher1_login.json()["access_token"]
            
            # teacher1的课程
            teacher1_response = requests.get(
                "http://localhost:8000/api/v1/courses/teacher/courses",
                headers={"Authorization": f"Bearer {teacher1_token}"}
            )
            
            if teacher1_response.status_code == 200:
                teacher1_courses = teacher1_response.json()
                print(f"\n👨‍🏫 teacher1看到 {len(teacher1_courses)} 门课程:")
                for course in teacher1_courses:
                    status = "已发布" if course['is_published'] else "草稿"
                    print(f"   - {course['title']} ({status})")
        
        if teacher2_login.status_code == 200:
            teacher2_token = teacher2_login.json()["access_token"]
            
            # teacher2的课程
            teacher2_response = requests.get(
                "http://localhost:8000/api/v1/courses/teacher/courses",
                headers={"Authorization": f"Bearer {teacher2_token}"}
            )
            
            if teacher2_response.status_code == 200:
                teacher2_courses = teacher2_response.json()
                print(f"\n👩‍🏫 teacher2看到 {len(teacher2_courses)} 门课程:")
                for course in teacher2_courses:
                    status = "已发布" if course['is_published'] else "草稿"
                    print(f"   - {course['title']} ({status})")
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")


def main():
    """主函数"""
    print("🚀 创建测试课程数据")
    print("=" * 60)
    
    # 1. 创建测试课程
    success = create_test_courses()
    
    if success:
        # 2. 显示统计
        show_course_summary()
        
        # 3. 测试API差异
        test_api_differences()
        
        print("\n" + "=" * 60)
        print("🎉 测试数据创建完成！")
        print("\n现在您可以:")
        print("1. 访问 http://localhost:5173/student/courses - 学生端只看已发布课程")
        print("2. 访问 http://localhost:5173/teacher/courses - 教师端只看自己的课程")
        print("3. 用teacher1登录看到3门课程(2门已发布+1门草稿)")
        print("4. 用teacher2登录看到2门课程(1门已发布+1门草稿)")
        print("5. 学生端看到3门已发布课程")
    else:
        print("❌ 测试数据创建失败")


if __name__ == "__main__":
    main()

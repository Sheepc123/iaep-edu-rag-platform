#!/usr/bin/env python3
"""
检查和清理课程数据
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_all_courses():
    """检查所有课程数据"""
    print("🔍 检查数据库中的所有课程...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course, Lesson
        from app.models.user import User
        
        db = SessionLocal()
        
        # 检查所有用户
        print("\n👥 数据库中的用户:")
        users = db.query(User).all()
        for user in users:
            print(f"   - {user.username} ({user.role}) - ID: {user.id}")
        
        # 检查所有课程
        print("\n📚 数据库中的所有课程:")
        courses = db.query(Course).all()
        
        if not courses:
            print("   ❌ 数据库中没有课程")
            return
        
        for course in courses:
            instructor = db.query(User).filter(User.id == course.instructor_id).first()
            instructor_name = instructor.username if instructor else "未知教师"
            
            print(f"   课程ID: {course.id}")
            print(f"   标题: {course.title}")
            print(f"   教师ID: {course.instructor_id} ({instructor_name})")
            print(f"   教师姓名字段: {course.instructor_name}")
            print(f"   分类: {course.category}")
            print(f"   发布状态: {'已发布' if course.is_published else '草稿'}")
            print(f"   创建时间: {course.created_at}")
            
            # 检查课时
            lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
            print(f"   课时数: {len(lessons)}")
            for lesson in lessons:
                print(f"     - {lesson.title}")
            print("   " + "-" * 50)
        
        # 按教师分组统计
        print("\n📊 按教师分组统计:")
        teacher_stats = {}
        for course in courses:
            instructor = db.query(User).filter(User.id == course.instructor_id).first()
            teacher_key = f"{course.instructor_id}({instructor.username if instructor else '未知'})"
            
            if teacher_key not in teacher_stats:
                teacher_stats[teacher_key] = []
            
            teacher_stats[teacher_key].append({
                'title': course.title,
                'published': course.is_published,
                'id': course.id
            })
        
        for teacher, course_list in teacher_stats.items():
            print(f"\n   教师 {teacher}:")
            for course_info in course_list:
                status = "已发布" if course_info['published'] else "草稿"
                print(f"     - {course_info['title']} (ID:{course_info['id']}, {status})")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()


def clean_old_courses():
    """清理旧的课程数据"""
    print("\n🧹 清理旧课程数据...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course, Lesson, CourseEnrollment, LessonProgress
        
        db = SessionLocal()
        
        # 获取所有课程
        courses = db.query(Course).all()
        
        # 识别可能的旧数据（没有对应教师的课程）
        orphan_courses = []
        valid_courses = []
        
        for course in courses:
            from app.models.user import User
            instructor = db.query(User).filter(User.id == course.instructor_id).first()
            
            if not instructor:
                orphan_courses.append(course)
                print(f"   发现孤儿课程: {course.title} (教师ID: {course.instructor_id} 不存在)")
            else:
                valid_courses.append(course)
        
        if orphan_courses:
            print(f"\n发现 {len(orphan_courses)} 门孤儿课程，是否删除？")
            for course in orphan_courses:
                print(f"   - {course.title} (ID: {course.id})")
            
            confirm = input("\n删除这些孤儿课程? (y/N): ")
            if confirm.lower() == 'y':
                for course in orphan_courses:
                    # 删除相关数据
                    db.query(LessonProgress).filter(
                        LessonProgress.lesson_id.in_(
                            db.query(Lesson.id).filter(Lesson.course_id == course.id)
                        )
                    ).delete(synchronize_session=False)
                    
                    db.query(CourseEnrollment).filter(CourseEnrollment.course_id == course.id).delete()
                    db.query(Lesson).filter(Lesson.course_id == course.id).delete()
                    db.query(Course).filter(Course.id == course.id).delete()
                    
                    print(f"   ✅ 删除课程: {course.title}")
                
                db.commit()
                print("✅ 孤儿课程清理完成")
        
        # 检查是否有重复课程
        print(f"\n📋 有效课程 ({len(valid_courses)} 门):")
        title_count = {}
        for course in valid_courses:
            if course.title in title_count:
                title_count[course.title].append(course)
            else:
                title_count[course.title] = [course]
        
        duplicates = {title: courses for title, courses in title_count.items() if len(courses) > 1}
        
        if duplicates:
            print(f"\n发现重复课程:")
            for title, course_list in duplicates.items():
                print(f"   课程: {title}")
                for course in course_list:
                    from app.models.user import User
                    instructor = db.query(User).filter(User.id == course.instructor_id).first()
                    print(f"     - ID: {course.id}, 教师: {instructor.username if instructor else '未知'}, 创建时间: {course.created_at}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        import traceback
        traceback.print_exc()


def reset_course_data():
    """完全重置课程数据"""
    print("\n🔄 完全重置课程数据...")
    
    print("⚠️  警告: 此操作将删除所有课程相关数据!")
    confirm = input("确认重置所有课程数据? (输入 'RESET' 确认): ")
    
    if confirm != "RESET":
        print("❌ 操作已取消")
        return
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course, Lesson, CourseEnrollment, LessonProgress
        
        db = SessionLocal()
        
        # 按依赖关系删除
        print("删除学习进度...")
        db.query(LessonProgress).delete()
        
        print("删除课程注册...")
        db.query(CourseEnrollment).delete()
        
        print("删除课时...")
        db.query(Lesson).delete()
        
        print("删除课程...")
        db.query(Course).delete()
        
        db.commit()
        db.close()
        
        print("✅ 所有课程数据已清理")
        
        # 重新创建示例数据
        print("\n📚 重新创建示例课程...")
        from recreate_course_module import create_sample_course
        create_sample_course()
        
    except Exception as e:
        print(f"❌ 重置失败: {e}")
        import traceback
        traceback.print_exc()


def test_api_after_cleanup():
    """清理后测试API"""
    print("\n🧪 测试清理后的API...")
    
    import requests
    
    try:
        # 登录获取tokens
        student_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "student1", "password": "123456", "remember_me": False}
        )
        teacher_login = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False}
        )
        
        if student_login.status_code == 200 and teacher_login.status_code == 200:
            student_token = student_login.json()["access_token"]
            teacher_token = teacher_login.json()["access_token"]
            
            # 学生端API
            student_response = requests.get(
                "http://localhost:8000/api/v1/courses/",
                params={"is_published": True, "limit": 20},
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            # 教师端API
            teacher_response = requests.get(
                "http://localhost:8000/api/v1/courses/teacher/courses",
                headers={"Authorization": f"Bearer {teacher_token}"}
            )
            
            print("📊 API测试结果:")
            
            if student_response.status_code == 200:
                student_data = student_response.json()
                student_courses = student_data.get('courses', [])
                print(f"   🎓 学生端: {len(student_courses)} 门课程")
                for course in student_courses:
                    print(f"     - {course['title']} (教师: {course['instructor_name']})")
            
            if teacher_response.status_code == 200:
                teacher_data = teacher_response.json()
                teacher_courses = teacher_data.get('courses', [])
                print(f"   👨‍🏫 教师端: {len(teacher_courses)} 门课程")
                for course in teacher_courses:
                    status = "已发布" if course['is_published'] else "草稿"
                    print(f"     - {course['title']} ({status})")
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")


def main():
    """主函数"""
    print("🚀 课程数据检查和清理工具")
    print("=" * 60)
    
    while True:
        print("\n请选择操作:")
        print("1. 检查所有课程数据")
        print("2. 清理孤儿课程")
        print("3. 完全重置课程数据")
        print("4. 测试API")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            check_all_courses()
        elif choice == "2":
            clean_old_courses()
        elif choice == "3":
            reset_course_data()
        elif choice == "4":
            test_api_after_cleanup()
        elif choice == "5":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选项，请重新选择")


if __name__ == "__main__":
    main()

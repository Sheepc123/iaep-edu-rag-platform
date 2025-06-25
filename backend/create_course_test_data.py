"""
创建课程系统测试数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.course import Course, Lesson, CourseEnrollment, LessonProgress
from app.models.user import User
from app.models import Base
from datetime import datetime, timedelta


def create_test_courses(db: Session):
    """创建测试课程数据"""
    
    # 获取测试用户（假设已存在）
    teacher = db.query(User).filter(User.role == "teacher").first()
    student = db.query(User).filter(User.role == "student").first()
    
    if not teacher:
        print("❌ 未找到教师用户，请先创建测试用户")
        return
    
    if not student:
        print("❌ 未找到学生用户，请先创建测试用户")
        return
    
    print(f"✅ 使用教师: {teacher.username}, 学生: {student.username}")
    
    # 检查是否已有课程数据
    existing_courses = db.query(Course).count()
    if existing_courses > 0:
        print(f"⚠️  数据库中已有 {existing_courses} 个课程")
        response = input("是否要清除现有课程数据并重新创建？(y/N): ")
        if response.lower() == 'y':
            # 清除现有数据
            db.query(LessonProgress).delete()
            db.query(CourseEnrollment).delete()
            db.query(Lesson).delete()
            db.query(Course).delete()
            db.commit()
            print("✅ 已清除现有课程数据")
        else:
            print("保留现有数据，退出...")
            return
    
    # 创建课程1：Python编程基础
    course1 = Course(
        title="Python编程基础",
        description="从零开始学习Python编程，掌握基础语法和编程思维。适合编程初学者，通过实际项目练习巩固知识。",
        cover_image="https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&h=400&fit=crop",
        category="编程语言",
        difficulty="easy",
        duration=1800,  # 30小时
        instructor_id=teacher.id,
        instructor_name=teacher.full_name or teacher.username,
        total_lessons=0,
        enrolled_students=0,
        rating=4.5,
        rating_count=128,
        is_published=True
    )
    db.add(course1)
    db.commit()
    db.refresh(course1)
    
    # 为课程1添加课时
    lessons1 = [
        {
            "title": "Python简介与环境搭建",
            "description": "了解Python语言特点，学习如何安装和配置Python开发环境",
            "content": "本课时将介绍Python的历史、特点和应用领域，并指导学生完成Python开发环境的搭建。",
            "lesson_order": 1,
            "duration": 45,
            "lesson_type": "video",
            "video_url": "https://example.com/video1.mp4",
            "is_free": True
        },
        {
            "title": "变量与数据类型",
            "description": "学习Python中的基本数据类型和变量的使用方法",
            "content": "深入了解Python的数字、字符串、列表、元组、字典等数据类型。",
            "lesson_order": 2,
            "duration": 60,
            "lesson_type": "video",
            "video_url": "https://example.com/video2.mp4",
            "is_free": False
        },
        {
            "title": "控制流程：条件语句",
            "description": "掌握if-elif-else条件语句的使用",
            "content": "学习如何使用条件语句控制程序的执行流程。",
            "lesson_order": 3,
            "duration": 50,
            "lesson_type": "video",
            "video_url": "https://example.com/video3.mp4",
            "is_free": False
        },
        {
            "title": "循环语句：for和while",
            "description": "学习for循环和while循环的使用方法",
            "content": "掌握循环语句的语法和应用场景。",
            "lesson_order": 4,
            "duration": 55,
            "lesson_type": "video",
            "video_url": "https://example.com/video4.mp4",
            "is_free": False
        },
        {
            "title": "函数定义与调用",
            "description": "学习如何定义和使用函数",
            "content": "了解函数的概念、参数传递、返回值等。",
            "lesson_order": 5,
            "duration": 70,
            "lesson_type": "video",
            "video_url": "https://example.com/video5.mp4",
            "is_free": False
        }
    ]
    
    for lesson_data in lessons1:
        lesson = Lesson(
            course_id=course1.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            content=lesson_data["content"],
            lesson_order=lesson_data["lesson_order"],
            duration=lesson_data["duration"],
            lesson_type=lesson_data["lesson_type"],
            video_url=lesson_data["video_url"],
            is_published=True,
            is_free=lesson_data["is_free"]
        )
        db.add(lesson)
    
    # 更新课程1的课时数量
    course1.total_lessons = len(lessons1)
    
    # 创建课程2：Web开发入门
    course2 = Course(
        title="Web开发入门",
        description="学习HTML、CSS、JavaScript基础知识，掌握前端开发技能。通过实际项目构建完整的网页应用。",
        cover_image="https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&h=400&fit=crop",
        category="Web开发",
        difficulty="medium",
        duration=2400,  # 40小时
        instructor_id=teacher.id,
        instructor_name=teacher.full_name or teacher.username,
        total_lessons=0,
        enrolled_students=0,
        rating=4.3,
        rating_count=89,
        is_published=True
    )
    db.add(course2)
    db.commit()
    db.refresh(course2)
    
    # 为课程2添加课时
    lessons2 = [
        {
            "title": "HTML基础结构",
            "description": "学习HTML标签和文档结构",
            "content": "了解HTML的基本语法和常用标签。",
            "lesson_order": 1,
            "duration": 60,
            "lesson_type": "video",
            "video_url": "https://example.com/web1.mp4",
            "is_free": True
        },
        {
            "title": "CSS样式设计",
            "description": "掌握CSS样式表的使用方法",
            "content": "学习CSS选择器、属性和布局技巧。",
            "lesson_order": 2,
            "duration": 75,
            "lesson_type": "video",
            "video_url": "https://example.com/web2.mp4",
            "is_free": False
        },
        {
            "title": "JavaScript基础语法",
            "description": "学习JavaScript编程基础",
            "content": "掌握JavaScript变量、函数、事件处理等。",
            "lesson_order": 3,
            "duration": 80,
            "lesson_type": "video",
            "video_url": "https://example.com/web3.mp4",
            "is_free": False
        }
    ]
    
    for lesson_data in lessons2:
        lesson = Lesson(
            course_id=course2.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            content=lesson_data["content"],
            lesson_order=lesson_data["lesson_order"],
            duration=lesson_data["duration"],
            lesson_type=lesson_data["lesson_type"],
            video_url=lesson_data["video_url"],
            is_published=True,
            is_free=lesson_data["is_free"]
        )
        db.add(lesson)
    
    # 更新课程2的课时数量
    course2.total_lessons = len(lessons2)
    
    # 创建课程3：数据科学导论
    course3 = Course(
        title="数据科学导论",
        description="介绍数据科学的基本概念和工具，学习数据分析和可视化技术。适合对数据分析感兴趣的学习者。",
        cover_image="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop",
        category="数据科学",
        difficulty="hard",
        duration=3000,  # 50小时
        instructor_id=teacher.id,
        instructor_name=teacher.full_name or teacher.username,
        total_lessons=0,
        enrolled_students=0,
        rating=4.7,
        rating_count=156,
        is_published=True
    )
    db.add(course3)
    db.commit()
    db.refresh(course3)
    
    # 为课程3添加课时
    lessons3 = [
        {
            "title": "数据科学概述",
            "description": "了解数据科学的定义和应用领域",
            "content": "介绍数据科学的发展历程和核心概念。",
            "lesson_order": 1,
            "duration": 45,
            "lesson_type": "video",
            "video_url": "https://example.com/ds1.mp4",
            "is_free": True
        },
        {
            "title": "Python数据分析库",
            "description": "学习pandas、numpy等数据分析工具",
            "content": "掌握Python数据分析的核心库。",
            "lesson_order": 2,
            "duration": 90,
            "lesson_type": "video",
            "video_url": "https://example.com/ds2.mp4",
            "is_free": False
        }
    ]
    
    for lesson_data in lessons3:
        lesson = Lesson(
            course_id=course3.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            content=lesson_data["content"],
            lesson_order=lesson_data["lesson_order"],
            duration=lesson_data["duration"],
            lesson_type=lesson_data["lesson_type"],
            video_url=lesson_data["video_url"],
            is_published=True,
            is_free=lesson_data["is_free"]
        )
        db.add(lesson)
    
    # 更新课程3的课时数量
    course3.total_lessons = len(lessons3)
    
    db.commit()
    
    print(f"✅ 创建课程成功:")
    print(f"  - {course1.title}: {course1.total_lessons} 课时")
    print(f"  - {course2.title}: {course2.total_lessons} 课时") 
    print(f"  - {course3.title}: {course3.total_lessons} 课时")
    
    return [course1, course2, course3], student


def create_test_enrollments(db: Session, courses, student):
    """创建测试注册记录"""
    
    # 学生注册第一个课程
    course1 = courses[0]
    enrollment = CourseEnrollment(
        course_id=course1.id,
        student_id=student.id,
        progress_percentage=60.0,
        completed_lessons=3,
        total_study_time=180,  # 3小时
        is_completed=False,
        enrolled_at=datetime.now() - timedelta(days=7)
    )
    db.add(enrollment)
    
    # 更新课程的注册学生数
    course1.enrolled_students = 1
    
    # 创建课时学习进度
    lessons = db.query(Lesson).filter(Lesson.course_id == course1.id).all()
    for i, lesson in enumerate(lessons[:3]):  # 前3个课时已完成
        progress = LessonProgress(
            lesson_id=lesson.id,
            student_id=student.id,
            progress_percentage=100.0,
            watch_time=lesson.duration * 60,  # 转换为秒
            is_completed=True,
            started_at=datetime.now() - timedelta(days=7-i),
            completed_at=datetime.now() - timedelta(days=6-i),
            last_accessed=datetime.now() - timedelta(days=6-i)
        )
        db.add(progress)
    
    db.commit()
    
    print(f"✅ 创建注册记录成功:")
    print(f"  - 学生 {student.username} 注册了课程 {course1.title}")
    print(f"  - 学习进度: {enrollment.progress_percentage}%")
    print(f"  - 已完成课时: {enrollment.completed_lessons}/{course1.total_lessons}")


def main():
    """主函数"""
    print("🚀 开始创建课程系统测试数据...")
    
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建测试课程
        courses, student = create_test_courses(db)
        
        # 创建测试注册记录
        create_test_enrollments(db, courses, student)
        
        print("\n✅ 课程系统测试数据创建完成！")
        print("\n📋 数据概览:")
        
        # 显示创建的数据统计
        total_courses = db.query(Course).count()
        total_lessons = db.query(Lesson).count()
        total_enrollments = db.query(CourseEnrollment).count()
        
        print(f"  - 课程总数: {total_courses}")
        print(f"  - 课时总数: {total_lessons}")
        print(f"  - 注册记录: {total_enrollments}")
        
        print("\n🔗 测试建议:")
        print("1. 启动后端服务: cd backend && python run.py")
        print("2. 访问课程列表: http://localhost:8000/api/v1/courses/")
        print("3. 测试课程详情: http://localhost:8000/api/v1/courses/1")
        print("4. 运行API测试: python backend/test_course_api.py")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

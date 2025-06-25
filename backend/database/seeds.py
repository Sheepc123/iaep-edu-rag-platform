"""
数据库种子数据管理
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .connection import SessionLocal
from app.models.user import User, StudentProfile, TeacherProfile
from app.models.course import Course, Lesson, CourseEnrollment, CourseCategory
from app.models.exercise import Exercise, Question, ExerciseAttempt, StudentAnswer
from passlib.context import CryptContext

# 创建密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SeedManager:
    """种子数据管理器"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def create_admin_user(self) -> User:
        """创建管理员用户"""
        # 检查是否已存在管理员
        admin = self.db.query(User).filter(User.username == "admin").first()
        if admin:
            print("管理员用户已存在")
            return admin

        # 创建管理员用户
        hashed_password = pwd_context.hash("admin123456")
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            full_name="系统管理员",
            role="admin",
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc)
        )

        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        print(f"管理员用户创建成功: {admin.username}")
        return admin
    
    def create_test_teacher(self) -> User:
        """创建测试教师用户"""
        # 检查是否已存在
        teacher = self.db.query(User).filter(User.username == "teacher123").first()
        if teacher:
            print("测试教师用户已存在")
            return teacher

        # 创建教师用户
        hashed_password = pwd_context.hash("123456")
        teacher = User(
            username="teacher123",
            email="teacher@example.com",
            hashed_password=hashed_password,
            full_name="李教授",
            role="teacher",
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc)
        )

        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        print(f"测试教师用户创建成功: {teacher.username}")
        return teacher
    
    def create_test_student(self) -> User:
        """创建测试学生用户"""
        # 检查是否已存在
        student = self.db.query(User).filter(User.username == "student123").first()
        if student:
            print("测试学生用户已存在")
            return student

        # 创建学生用户
        hashed_password = pwd_context.hash("123456")
        student = User(
            username="student123",
            email="student@example.com",
            hashed_password=hashed_password,
            full_name="张同学",
            role="student",
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc)
        )

        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        print(f"测试学生用户创建成功: {student.username}")
        return student

    def create_multiple_test_students(self) -> list[User]:
        """创建多个测试学生用户"""
        print("开始创建多个测试学生...")

        # 测试学生数据
        students_data = [
            {
                "username": "student001",
                "email": "student001@example.com",
                "password": "123456",
                "full_name": "张三",
                "phone": "13800138001",
                "student_id": "2024001",
                "school": "北京大学",
                "college": "计算机学院",
                "major": "计算机科学与技术",
                "grade": "2024级",
                "class_name": "计科1班"
            },
            {
                "username": "student002",
                "email": "student002@example.com",
                "password": "123456",
                "full_name": "李四",
                "phone": "13800138002",
                "student_id": "2024002",
                "school": "北京大学",
                "college": "数学学院",
                "major": "数学与应用数学",
                "grade": "2024级",
                "class_name": "数学1班"
            },
            {
                "username": "student003",
                "email": "student003@example.com",
                "password": "123456",
                "full_name": "王五",
                "phone": "13800138003",
                "student_id": "2024003",
                "school": "清华大学",
                "college": "电子工程系",
                "major": "电子信息工程",
                "grade": "2024级",
                "class_name": "电子1班"
            },
            {
                "username": "student004",
                "email": "student004@example.com",
                "password": "123456",
                "full_name": "赵六",
                "phone": "13800138004",
                "student_id": "2024004",
                "school": "清华大学",
                "college": "机械工程系",
                "major": "机械工程",
                "grade": "2024级",
                "class_name": "机械1班"
            },
            {
                "username": "student005",
                "email": "student005@example.com",
                "password": "123456",
                "full_name": "孙七",
                "phone": "13800138005",
                "student_id": "2024005",
                "school": "复旦大学",
                "college": "物理学系",
                "major": "应用物理学",
                "grade": "2024级",
                "class_name": "物理1班"
            },
            {
                "username": "student006",
                "email": "student006@example.com",
                "password": "123456",
                "full_name": "周八",
                "phone": "13800138006",
                "student_id": "2024006",
                "school": "上海交通大学",
                "college": "软件学院",
                "major": "软件工程",
                "grade": "2024级",
                "class_name": "软工1班"
            },
            {
                "username": "student007",
                "email": "student007@example.com",
                "password": "123456",
                "full_name": "吴九",
                "phone": "13800138007",
                "student_id": "2024007",
                "school": "华中科技大学",
                "college": "信息学院",
                "major": "信息安全",
                "grade": "2024级",
                "class_name": "信安1班"
            },
            {
                "username": "student008",
                "email": "student008@example.com",
                "password": "123456",
                "full_name": "郑十",
                "phone": "13800138008",
                "student_id": "2024008",
                "school": "西安交通大学",
                "college": "电信学院",
                "major": "通信工程",
                "grade": "2024级",
                "class_name": "通信1班"
            }
        ]

        created_students = []

        for student_data in students_data:
            # 检查用户是否已存在
            existing_user = self.db.query(User).filter(User.username == student_data["username"]).first()
            if existing_user:
                print(f"用户 {student_data['username']} 已存在，跳过创建")
                created_students.append(existing_user)
                continue

            # 创建用户
            user = User(
                username=student_data["username"],
                email=student_data["email"],
                hashed_password=pwd_context.hash(student_data["password"]),
                full_name=student_data["full_name"],
                phone=student_data["phone"],
                role="student",
                is_active=True,
                is_verified=True,
                created_at=datetime.now(timezone.utc)
            )

            self.db.add(user)
            self.db.flush()  # 获取用户ID

            # 创建学生档案
            student_profile = StudentProfile(
                user_id=user.id,
                student_id=student_data["student_id"],
                school=student_data["school"],
                college=student_data["college"],
                major=student_data["major"],
                grade=student_data["grade"],
                class_name=student_data["class_name"],
                total_study_time=0,
                total_exercises=0,
                correct_exercises=0,
                total_courses=0,
                completed_courses=0,
                preferred_subjects=json.dumps(["数学", "计算机科学"]),
                learning_goals="提高专业技能，准备考研",
                created_at=datetime.now(timezone.utc)
            )

            self.db.add(student_profile)
            created_students.append(user)
            print(f"创建学生: {student_data['full_name']} ({student_data['username']})")

        self.db.commit()
        print(f"测试学生数据创建完成！共创建 {len([s for s in created_students if s.username.startswith('student0')])} 个新学生")
        return created_students
    
    def create_sample_course(self, teacher: User) -> Course:
        """创建示例课程"""
        # 检查是否已存在
        course = self.db.query(Course).filter(Course.title == "高等数学(上)").first()
        if course:
            print("示例课程已存在")
            return course

        # 创建课程
        course = Course(
            title="高等数学(上)",
            description="本课程涵盖极限、导数、积分等核心概念，为后续数学课程打下坚实基础。",
            category="数学基础",
            difficulty="medium",
            duration=1440,  # 24小时
            total_lessons=0,
            instructor_id=teacher.id,
            instructor_name=teacher.full_name,
            enrolled_students=0,
            rating=4.8,
            rating_count=0,
            is_active=True,
            is_published=True,
            created_at=datetime.now(timezone.utc)
        )

        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)

        print(f"示例课程创建成功: {course.title}")
        return course

    def create_multiple_courses(self, teacher: User) -> list[Course]:
        """创建多个示例课程"""
        print("开始创建多个课程...")

        # 课程数据 - 扩展版本，包含更多丰富的课程
        courses_data = [
            # 数学基础类
            {
                "title": "高等数学(上)",
                "description": "本课程涵盖极限、导数、积分等核心概念，为后续数学课程打下坚实基础。通过理论学习与实践练习相结合，帮助学生深入理解数学原理。",
                "category": "数学基础",
                "difficulty": "medium",
                "duration": 1440,  # 24小时
                "rating": 4.8,
                "cover_image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=400&fit=crop"
            },
            {
                "title": "高等数学(下)",
                "description": "继续学习多元函数微积分、无穷级数、微分方程等高等数学内容，深化数学思维能力。",
                "category": "数学基础",
                "difficulty": "medium",
                "duration": 1440,  # 24小时
                "rating": 4.7,
                "cover_image": "https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=800&h=400&fit=crop"
            },
            {
                "title": "线性代数",
                "description": "学习矩阵运算、向量空间、线性变换等线性代数基础知识，为机器学习和数据科学打下基础。",
                "category": "数学基础",
                "difficulty": "medium",
                "duration": 1080,  # 18小时
                "rating": 4.6,
                "cover_image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&h=400&fit=crop"
            },
            {
                "title": "概率论与数理统计",
                "description": "学习概率论基础知识和统计分析方法，掌握数据分析的数学基础，为数据科学打下基础。",
                "category": "数学基础",
                "difficulty": "medium",
                "duration": 1320,  # 22小时
                "rating": 4.3,
                "cover_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop"
            },
            {
                "title": "离散数学",
                "description": "学习集合论、图论、数理逻辑等离散数学知识，为计算机科学理论学习奠定基础。",
                "category": "数学基础",
                "difficulty": "medium",
                "duration": 1200,  # 20小时
                "rating": 4.1,
                "cover_image": "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800&h=400&fit=crop"
            },

            # 编程语言类
            {
                "title": "Python程序设计基础",
                "description": "从零开始学习Python编程语言，掌握基础语法、数据结构、函数、面向对象编程等核心概念。适合编程初学者。",
                "category": "编程语言",
                "difficulty": "easy",
                "duration": 1200,  # 20小时
                "rating": 4.7,
                "cover_image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&h=400&fit=crop"
            },
            {
                "title": "Python高级编程",
                "description": "深入学习Python高级特性，包括装饰器、生成器、元类、并发编程等，提升Python编程水平。",
                "category": "编程语言",
                "difficulty": "hard",
                "duration": 1800,  # 30小时
                "rating": 4.8,
                "cover_image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&h=400&fit=crop"
            },
            {
                "title": "Java程序设计",
                "description": "学习Java编程语言，掌握面向对象编程思想、Java核心API、异常处理、集合框架等知识。",
                "category": "编程语言",
                "difficulty": "medium",
                "duration": 1500,  # 25小时
                "rating": 4.5,
                "cover_image": "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=800&h=400&fit=crop"
            },
            {
                "title": "C++程序设计",
                "description": "学习C++编程语言，掌握指针、引用、类与对象、STL标准库等核心概念，培养系统编程能力。",
                "category": "编程语言",
                "difficulty": "hard",
                "duration": 1680,  # 28小时
                "rating": 4.3,
                "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=400&fit=crop"
            },
            {
                "title": "JavaScript现代开发",
                "description": "学习现代JavaScript开发技术，包括ES6+语法、异步编程、模块化开发、前端框架等。",
                "category": "编程语言",
                "difficulty": "medium",
                "duration": 1440,  # 24小时
                "rating": 4.6,
                "cover_image": "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=800&h=400&fit=crop"
            },

            # 计算机科学类
            {
                "title": "数据结构与算法",
                "description": "深入学习常用数据结构（数组、链表、栈、队列、树、图等）和经典算法（排序、搜索、动态规划等），提升编程思维。",
                "category": "计算机科学",
                "difficulty": "hard",
                "duration": 1800,  # 30小时
                "rating": 4.9,
                "cover_image": "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800&h=400&fit=crop"
            },
            {
                "title": "数据库系统原理",
                "description": "学习关系数据库理论、SQL语言、数据库设计和优化技术，掌握数据库管理系统的核心原理。",
                "category": "计算机科学",
                "difficulty": "medium",
                "duration": 1440,  # 24小时
                "rating": 4.5,
                "cover_image": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=800&h=400&fit=crop"
            },
            {
                "title": "操作系统原理",
                "description": "深入理解操作系统的工作原理，包括进程管理、内存管理、文件系统、I/O管理等核心概念。",
                "category": "计算机科学",
                "difficulty": "hard",
                "duration": 1680,  # 28小时
                "rating": 4.4,
                "cover_image": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop"
            },
            {
                "title": "计算机网络",
                "description": "学习计算机网络体系结构、TCP/IP协议栈、网络安全等知识，理解网络通信原理。",
                "category": "计算机科学",
                "difficulty": "medium",
                "duration": 1320,  # 22小时
                "rating": 4.2,
                "cover_image": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=400&fit=crop"
            },
            {
                "title": "软件工程",
                "description": "学习软件开发生命周期、项目管理、软件测试、版本控制等软件工程实践，培养团队协作能力。",
                "category": "计算机科学",
                "difficulty": "medium",
                "duration": 1440,  # 24小时
                "rating": 4.2,
                "cover_image": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=400&fit=crop"
            },

            # Web开发类
            {
                "title": "Web前端开发基础",
                "description": "学习HTML5、CSS3、JavaScript等前端基础技术，掌握响应式设计和现代Web开发技能。",
                "category": "Web开发",
                "difficulty": "easy",
                "duration": 1200,  # 20小时
                "rating": 4.6,
                "cover_image": "https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&h=400&fit=crop"
            },
            {
                "title": "React前端框架",
                "description": "深入学习React框架，掌握组件化开发、状态管理、路由配置等现代前端开发技术。",
                "category": "Web开发",
                "difficulty": "medium",
                "duration": 1800,  # 30小时
                "rating": 4.8,
                "cover_image": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=400&fit=crop"
            },
            {
                "title": "Vue.js全栈开发",
                "description": "学习Vue.js框架及其生态系统，包括Vue Router、Vuex状态管理、Element UI等。",
                "category": "Web开发",
                "difficulty": "medium",
                "duration": 1680,  # 28小时
                "rating": 4.7,
                "cover_image": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=400&fit=crop"
            },
            {
                "title": "Node.js后端开发",
                "description": "学习Node.js服务器端开发，掌握Express框架、数据库操作、API设计等后端技术。",
                "category": "Web开发",
                "difficulty": "medium",
                "duration": 1560,  # 26小时
                "rating": 4.5,
                "cover_image": "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=800&h=400&fit=crop"
            },
            {
                "title": "全栈Web开发项目",
                "description": "通过实际项目学习全栈Web开发，整合前端、后端、数据库技术，完成完整的Web应用。",
                "category": "Web开发",
                "difficulty": "hard",
                "duration": 2400,  # 40小时
                "rating": 4.9,
                "cover_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop"
            },

            # 人工智能与机器学习类
            {
                "title": "机器学习基础",
                "description": "介绍机器学习的基本概念、常用算法（线性回归、决策树、SVM等）和实际应用案例。",
                "category": "人工智能",
                "difficulty": "medium",
                "duration": 1800,  # 30小时
                "rating": 4.8,
                "cover_image": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop"
            },
            {
                "title": "深度学习与神经网络",
                "description": "学习深度学习理论基础，掌握神经网络、卷积神经网络、循环神经网络等核心技术。",
                "category": "人工智能",
                "difficulty": "hard",
                "duration": 2160,  # 36小时
                "rating": 4.9,
                "cover_image": "https://images.unsplash.com/photo-1507146426996-ef05306b995a?w=800&h=400&fit=crop"
            },
            {
                "title": "计算机视觉",
                "description": "学习图像处理、特征提取、目标检测、图像分类等计算机视觉技术及其应用。",
                "category": "人工智能",
                "difficulty": "hard",
                "duration": 1920,  # 32小时
                "rating": 4.7,
                "cover_image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=400&fit=crop"
            },
            {
                "title": "自然语言处理",
                "description": "学习文本预处理、词向量、语言模型、情感分析等自然语言处理技术和应用。",
                "category": "人工智能",
                "difficulty": "hard",
                "duration": 1800,  # 30小时
                "rating": 4.6,
                "cover_image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=400&fit=crop"
            },

            # 数据科学类
            {
                "title": "数据科学入门",
                "description": "学习数据科学基础知识，包括数据收集、清洗、分析、可视化等数据处理全流程。",
                "category": "数据科学",
                "difficulty": "easy",
                "duration": 1320,  # 22小时
                "rating": 4.5,
                "cover_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop"
            },
            {
                "title": "Python数据分析",
                "description": "使用Python进行数据分析，掌握Pandas、NumPy、Matplotlib等数据科学核心库的使用。",
                "category": "数据科学",
                "difficulty": "medium",
                "duration": 1440,  # 24小时
                "rating": 4.7,
                "cover_image": "https://images.unsplash.com/photo-1543286386-713bdd548da4?w=800&h=400&fit=crop"
            },
            {
                "title": "大数据技术",
                "description": "学习Hadoop、Spark等大数据处理技术，掌握分布式计算和大规模数据处理方法。",
                "category": "数据科学",
                "difficulty": "hard",
                "duration": 2040,  # 34小时
                "rating": 4.4,
                "cover_image": "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800&h=400&fit=crop"
            },
            {
                "title": "数据可视化",
                "description": "学习数据可视化理论和实践，掌握D3.js、Tableau、Power BI等可视化工具的使用。",
                "category": "数据科学",
                "difficulty": "medium",
                "duration": 1200,  # 20小时
                "rating": 4.3,
                "cover_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop"
            }
        ]

        created_courses = []

        for course_data in courses_data:
            # 检查课程是否已存在
            existing_course = self.db.query(Course).filter(Course.title == course_data["title"]).first()
            if existing_course:
                print(f"课程 {course_data['title']} 已存在，跳过创建")
                created_courses.append(existing_course)
                continue

            # 创建课程
            course = Course(
                title=course_data["title"],
                description=course_data["description"],
                category=course_data["category"],
                difficulty=course_data["difficulty"],
                duration=course_data["duration"],
                cover_image=course_data.get("cover_image"),  # 添加封面图片
                total_lessons=0,
                instructor_id=teacher.id,
                instructor_name=teacher.full_name,
                enrolled_students=0,
                rating=course_data["rating"],
                rating_count=0,
                is_active=True,
                is_published=True,
                created_at=datetime.now(timezone.utc)
            )

            self.db.add(course)
            created_courses.append(course)
            print(f"创建课程: {course_data['title']}")

        self.db.commit()
        print(f"课程数据创建完成！共创建 {len([c for c in created_courses if c.title in [cd['title'] for cd in courses_data]])} 个新课程")
        return created_courses
    
    def create_sample_lessons(self, course: Course) -> list[Lesson]:
        """创建示例课时"""
        # 检查是否已存在课时
        existing_lessons = self.db.query(Lesson).filter(Lesson.course_id == course.id).count()
        if existing_lessons > 0:
            print("示例课时已存在")
            return []
        
        lessons_data = [
            {
                "title": "函数的概念",
                "description": "学习函数的基本概念和性质",
                "content": "# 函数的概念\n\n函数是数学中的基本概念...",
                "lesson_order": 1,
                "duration": 45,
                "lesson_type": "video",
                "is_published": True,
                "is_free": True
            },
            {
                "title": "函数的性质",
                "description": "深入了解函数的各种性质",
                "content": "# 函数的性质\n\n函数的单调性、奇偶性...",
                "lesson_order": 2,
                "duration": 50,
                "lesson_type": "video",
                "is_published": True,
                "is_free": False
            },
            {
                "title": "极限的定义",
                "description": "学习极限的严格数学定义",
                "content": "# 极限的定义\n\n极限是微积分的基础...",
                "lesson_order": 3,
                "duration": 60,
                "lesson_type": "video",
                "is_published": True,
                "is_free": False
            },
            {
                "title": "极限的计算",
                "description": "掌握各种极限计算方法",
                "content": "# 极限的计算\n\n极限计算的基本方法...",
                "lesson_order": 4,
                "duration": 55,
                "lesson_type": "video",
                "is_published": True,
                "is_free": False
            },
            {
                "title": "导数的概念",
                "description": "理解导数的几何和物理意义",
                "content": "# 导数的概念\n\n导数表示函数的变化率...",
                "lesson_order": 5,
                "duration": 50,
                "lesson_type": "video",
                "is_published": True,
                "is_free": False
            }
        ]
        
        lessons = []
        for lesson_data in lessons_data:
            lesson = Lesson(
                course_id=course.id,
                **lesson_data,
                created_at=datetime.now(timezone.utc)
            )
            self.db.add(lesson)
            lessons.append(lesson)
        
        # 更新课程的总课时数
        course.total_lessons = len(lessons)
        
        self.db.commit()
        print(f"创建了 {len(lessons)} 个示例课时")
        return lessons

    def create_simple_lessons_for_course(self, course: Course) -> list[Lesson]:
        """为课程创建简化的课时数据"""
        # 检查是否已存在课时
        existing_lessons = self.db.query(Lesson).filter(Lesson.course_id == course.id).count()
        if existing_lessons > 0:
            print(f"课程 {course.title} 的课时已存在")
            return []

        # 根据课程类别生成不同的课时
        lessons_templates = {
            "数学基础": [
                "基础概念介绍", "理论基础", "公式推导", "例题讲解", "练习与应用"
            ],
            "编程语言": [
                "环境搭建", "基础语法", "数据类型", "控制结构", "函数与模块", "项目实战"
            ],
            "计算机科学": [
                "课程概述", "基础理论", "核心算法", "实现技术", "应用案例", "综合练习"
            ],
            "Web开发": [
                "开发环境", "基础知识", "核心技术", "框架应用", "项目开发", "部署上线"
            ],
            "人工智能": [
                "AI概述", "理论基础", "算法原理", "模型训练", "实际应用", "项目实战"
            ],
            "数据科学": [
                "数据概述", "数据收集", "数据清洗", "数据分析", "数据可视化", "结果解释"
            ]
        }

        # 获取课程类别对应的课时模板
        lesson_titles = lessons_templates.get(course.category, lessons_templates["计算机科学"])

        lessons = []
        for i, title in enumerate(lesson_titles):
            lesson = Lesson(
                course_id=course.id,
                title=f"{title}",
                description=f"学习{course.title}中{title}的相关知识点",
                content=f"# {title}\n\n这里是{title}的详细内容...\n\n## 学习目标\n- 掌握{title}的基本概念\n- 理解相关理论知识\n- 能够实际应用所学内容",
                lesson_order=i + 1,
                duration=45 + (i * 5),  # 45-70分钟不等
                lesson_type="video",
                is_published=True,
                is_free=(i == 0),  # 第一课时免费
                created_at=datetime.now(timezone.utc)
            )
            self.db.add(lesson)
            lessons.append(lesson)

        # 更新课程的总课时数
        course.total_lessons = len(lessons)

        self.db.commit()
        print(f"为课程 {course.title} 创建了 {len(lessons)} 个课时")
        return lessons
    
    def create_sample_enrollment(self, course: Course, student: User) -> CourseEnrollment:
        """创建示例课程注册"""
        # 检查是否已注册
        enrollment = self.db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course.id,
            CourseEnrollment.student_id == student.id
        ).first()
        
        if enrollment:
            print("学生已注册此课程")
            return enrollment
        
        # 创建注册记录
        enrollment = CourseEnrollment(
            course_id=course.id,
            student_id=student.id,
            progress_percentage=25.0,
            completed_lessons=1,
            total_study_time=45,
            is_completed=False,
            is_active=True,
            enrolled_at=datetime.now(timezone.utc),
            last_accessed=datetime.now(timezone.utc)
        )
        
        self.db.add(enrollment)
        
        # 更新课程注册学生数
        course.enrolled_students += 1
        
        self.db.commit()
        print(f"学生 {student.full_name} 注册课程 {course.title} 成功")
        return enrollment
    
    def seed_all(self):
        """创建所有种子数据"""
        print("开始创建种子数据...")

        # 创建用户
        admin = self.create_admin_user()
        teacher = self.create_test_teacher()
        student = self.create_test_student()

        # 创建课程和课时
        course = self.create_sample_course(teacher)
        lessons = self.create_sample_lessons(course)

        # 创建课程注册
        enrollment = self.create_sample_enrollment(course, student)

        print("种子数据创建完成！")

    def seed_students_only(self):
        """只创建学生测试数据"""
        print("开始创建学生测试数据...")
        students = self.create_multiple_test_students()
        print(f"学生测试数据创建完成！共 {len(students)} 个学生")
        return students

    def seed_complete_data(self):
        """创建完整的测试数据（包括多个学生和丰富的课程）"""
        print("开始创建完整测试数据...")

        # 创建管理员和教师
        admin = self.create_admin_user()
        teacher = self.create_test_teacher()

        # 创建多个学生
        students = self.create_multiple_test_students()

        # 创建多个课程（使用扩展的课程数据）
        print("\n📚 创建丰富的课程数据...")
        courses = self.create_multiple_courses(teacher)

        # 为每个课程创建示例课时（只为前5个课程创建详细课时）
        total_lessons = 0
        for i, course in enumerate(courses[:5]):
            if i == 0:  # 第一个课程使用现有的详细课时
                lessons = self.create_sample_lessons(course)
                total_lessons += len(lessons)
            else:  # 其他课程创建简化的课时
                lessons = self.create_simple_lessons_for_course(course)
                total_lessons += len(lessons)

        # 为学生随机注册一些课程
        import random
        enrolled_count = 0
        for student in students:
            # 每个学生随机注册2-4门课程
            num_courses = random.randint(2, min(4, len(courses)))
            selected_courses = random.sample(courses, num_courses)

            for course in selected_courses:
                try:
                    enrollment = self.create_sample_enrollment(course, student)
                    enrolled_count += 1
                except:
                    # 如果已经注册过，跳过
                    pass

        print("完整测试数据创建完成！")
        print(f"- 管理员: {admin.username}")
        print(f"- 教师: {teacher.username}")
        print(f"- 学生: {len(students)} 个")
        print(f"- 课程: {len(courses)} 门")
        print(f"- 课时: {total_lessons} 个")
        print(f"- 课程注册: {enrolled_count} 个注册记录")


def seed_database():
    """种子数据创建的便捷函数"""
    with SeedManager() as seed_manager:
        seed_manager.seed_all()


def create_test_users():
    """创建测试用户的便捷函数"""
    with SeedManager() as seed_manager:
        seed_manager.create_admin_user()
        seed_manager.create_test_teacher()
        seed_manager.create_test_student()


def create_test_students():
    """创建多个测试学生的便捷函数"""
    with SeedManager() as seed_manager:
        return seed_manager.seed_students_only()


def create_complete_test_data():
    """创建完整测试数据的便捷函数"""
    with SeedManager() as seed_manager:
        seed_manager.seed_complete_data()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "students":
            print("创建学生测试数据...")
            create_test_students()
        elif command == "complete":
            print("创建完整测试数据...")
            create_complete_test_data()
        elif command == "users":
            print("创建基础用户...")
            create_test_users()
        else:
            print("可用命令:")
            print("  python seeds.py students  - 创建学生测试数据")
            print("  python seeds.py complete - 创建完整测试数据")
            print("  python seeds.py users    - 创建基础用户")
            print("  python seeds.py          - 创建默认种子数据")
    else:
        print("创建默认种子数据...")
        seed_database()

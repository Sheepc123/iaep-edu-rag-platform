"""
课程管理功能测试脚本
"""
import requests
import json
from datetime import datetime


class CourseTester:
    """课程功能测试类"""
    
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.teacher_token = None
        self.student_token = None
        self.course_id = None
        self.lesson_id = None
    
    def login_teacher(self):
        """教师登录"""
        print("🔐 教师登录...")
        
        login_data = {
            "username": "teacher123",
            "password": "123456",
            "remember_me": True,
            "device_info": "Test Browser - Teacher"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.teacher_token = data["access_token"]
                print(f"✅ 教师登录成功: {data['user_info']['full_name']}")
                return True
            else:
                print(f"❌ 教师登录失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 教师登录请求失败: {e}")
            return False
    
    def login_student(self):
        """学生登录"""
        print("🔐 学生登录...")
        
        login_data = {
            "username": "student123",
            "password": "123456",
            "remember_me": True,
            "device_info": "Test Browser - Student"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.student_token = data["access_token"]
                print(f"✅ 学生登录成功: {data['user_info']['full_name']}")
                return True
            else:
                print(f"❌ 学生登录失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 学生登录请求失败: {e}")
            return False
    
    def test_create_course(self):
        """测试创建课程"""
        print("\n📚 测试创建课程...")
        
        if not self.teacher_token:
            print("❌ 需要教师登录")
            return False
        
        course_data = {
            "title": "Python编程基础",
            "description": "从零开始学习Python编程语言，掌握基础语法和编程思维。",
            "category": "编程语言",
            "difficulty": "medium",
            "duration": 1200,  # 20小时
            "cover_image": "https://example.com/python-course.jpg",
            "is_published": True
        }
        
        headers = {
            "Authorization": f"Bearer {self.teacher_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/courses/",
                json=course_data,
                headers=headers
            )
            
            if response.status_code == 200:
                course = response.json()
                self.course_id = course["id"]
                print(f"✅ 课程创建成功: {course['title']} (ID: {course['id']})")
                return True
            else:
                print(f"❌ 课程创建失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 创建课程请求失败: {e}")
            return False
    
    def test_create_lesson(self):
        """测试创建课时"""
        print("\n📖 测试创建课时...")
        
        if not self.teacher_token or not self.course_id:
            print("❌ 需要教师登录和课程ID")
            return False
        
        lesson_data = {
            "title": "Python基础语法",
            "description": "学习Python的基本语法，包括变量、数据类型、运算符等。",
            "content": "# Python基础语法\n\n## 变量和数据类型\n\n...",
            "lesson_order": 1,
            "duration": 60,
            "lesson_type": "video",
            "video_url": "https://example.com/lesson1.mp4",
            "is_published": True,
            "is_free": True
        }
        
        headers = {
            "Authorization": f"Bearer {self.teacher_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/courses/{self.course_id}/lessons",
                json=lesson_data,
                headers=headers
            )
            
            if response.status_code == 200:
                lesson = response.json()
                self.lesson_id = lesson["id"]
                print(f"✅ 课时创建成功: {lesson['title']} (ID: {lesson['id']})")
                return True
            else:
                print(f"❌ 课时创建失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 创建课时请求失败: {e}")
            return False
    
    def test_get_courses(self):
        """测试获取课程列表"""
        print("\n📋 测试获取课程列表...")
        
        try:
            response = requests.get(f"{self.api_url}/courses/")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 获取课程列表成功: 共 {data['total']} 门课程")
                if data['courses']:
                    for course in data['courses'][:3]:  # 显示前3门课程
                        print(f"   - {course['title']} (难度: {course['difficulty']})")
                return True
            else:
                print(f"❌ 获取课程列表失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 获取课程列表请求失败: {e}")
            return False
    
    def test_enroll_course(self):
        """测试学生注册课程"""
        print("\n✍️ 测试学生注册课程...")
        
        if not self.student_token or not self.course_id:
            print("❌ 需要学生登录和课程ID")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.student_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/courses/{self.course_id}/enroll",
                headers=headers
            )
            
            if response.status_code == 200:
                enrollment = response.json()
                print(f"✅ 课程注册成功: 课程ID {enrollment['course_id']}")
                return True
            else:
                print(f"❌ 课程注册失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 注册课程请求失败: {e}")
            return False
    
    def test_update_lesson_progress(self):
        """测试更新课时学习进度"""
        print("\n📈 测试更新课时学习进度...")
        
        if not self.student_token or not self.lesson_id:
            print("❌ 需要学生登录和课时ID")
            return False
        
        progress_data = {
            "progress_percentage": 75.0,
            "watch_time": 2700,  # 45分钟
            "is_completed": False,
            "notes": "学习了Python基础语法，需要多练习变量的使用。"
        }
        
        headers = {
            "Authorization": f"Bearer {self.student_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/courses/lessons/{self.lesson_id}/progress",
                json=progress_data,
                headers=headers
            )
            
            if response.status_code == 200:
                progress = response.json()
                print(f"✅ 学习进度更新成功: {progress['progress_percentage']}%")
                return True
            else:
                print(f"❌ 学习进度更新失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 更新学习进度请求失败: {e}")
            return False
    
    def test_get_statistics(self):
        """测试获取课程统计"""
        print("\n📊 测试获取课程统计...")
        
        if not self.teacher_token:
            print("❌ 需要教师登录")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.teacher_token}"
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/courses/statistics",
                headers=headers
            )
            
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ 统计信息获取成功:")
                print(f"   - 总课程数: {stats['total_courses']}")
                print(f"   - 已发布课程: {stats['published_courses']}")
                print(f"   - 总学生数: {stats['total_students']}")
                print(f"   - 平均评分: {stats['average_rating']}")
                return True
            else:
                print(f"❌ 获取统计信息失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 获取统计信息请求失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始课程管理功能测试")
        print("=" * 60)
        
        # 1. 教师和学生登录
        if not self.login_teacher() or not self.login_student():
            print("❌ 登录失败，停止测试")
            return
        
        # 2. 创建课程
        if not self.test_create_course():
            print("❌ 创建课程失败，停止测试")
            return
        
        # 3. 创建课时
        self.test_create_lesson()
        
        # 4. 获取课程列表
        self.test_get_courses()
        
        # 5. 学生注册课程
        self.test_enroll_course()
        
        # 6. 更新学习进度
        self.test_update_lesson_progress()
        
        # 7. 获取统计信息
        self.test_get_statistics()
        
        print("\n" + "=" * 60)
        print("🎉 课程管理功能测试完成")


if __name__ == "__main__":
    tester = CourseTester()
    tester.run_all_tests()

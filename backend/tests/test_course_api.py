"""
课程API测试脚本
"""
import requests
import json
from datetime import datetime


class CourseAPITester:
    """课程API测试类"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.student_token = None
        self.teacher_token = None
    
    def test_server_health(self):
        """测试服务器健康状态"""
        print("=== 测试服务器连接 ===")
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            print(f"服务器状态: {response.status_code}")
            if response.status_code == 200:
                print("✅ 服务器正常运行")
                return True
            else:
                print("❌ 服务器响应异常")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到服务器，请确保后端服务正在运行")
            return False
        except Exception as e:
            print(f"❌ 连接测试失败: {str(e)}")
            return False
    
    def login_user(self, username: str, password: str) -> str:
        """用户登录获取token"""
        url = f"{self.base_url}/api/v1/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            print(f"登录请求状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get("access_token")
                print(f"✅ {username} 登录成功")
                return token
            else:
                print(f"❌ {username} 登录失败: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 登录请求失败: {str(e)}")
            return None
    
    def get_headers(self, token: str) -> dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def test_get_courses(self):
        """测试获取课程列表"""
        print("\n=== 测试获取课程列表 ===")
        
        url = f"{self.base_url}/api/v1/courses/"
        
        # 先尝试不带认证的请求
        try:
            response = requests.get(url, timeout=10)
            print(f"无认证请求状态: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            
            if response.status_code == 200:
                courses_data = response.json()
                print(f"✅ 获取到课程数据: {len(courses_data.get('courses', []))} 个课程")
                return courses_data.get('courses', [])
            else:
                print(f"❌ 获取课程列表失败")
                return []
                
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return []
    
    def test_get_course_detail(self, course_id: int):
        """测试获取课程详情"""
        print(f"\n=== 测试获取课程详情 (ID: {course_id}) ===")
        
        url = f"{self.base_url}/api/v1/courses/{course_id}"
        
        try:
            response = requests.get(url, timeout=10)
            print(f"请求状态: {response.status_code}")
            print(f"响应内容: {response.text[:300]}...")
            
            if response.status_code == 200:
                course = response.json()
                print(f"✅ 获取课程详情成功: {course.get('title', 'Unknown')}")
                return course
            elif response.status_code == 404:
                print(f"❌ 课程不存在 (ID: {course_id})")
                return None
            else:
                print(f"❌ 获取课程详情失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return None
    
    def test_database_connection(self):
        """测试数据库连接"""
        print("\n=== 测试数据库连接 ===")
        
        # 通过API间接测试数据库
        courses = self.test_get_courses()
        
        if courses:
            print(f"✅ 数据库连接正常，找到 {len(courses)} 个课程")
            for course in courses[:3]:  # 只显示前3个
                print(f"  - {course.get('title', 'Unknown')} (ID: {course.get('id', 'Unknown')})")
        else:
            print("❌ 数据库可能为空或连接异常")
    
    def test_create_test_course(self):
        """测试创建测试课程"""
        print("\n=== 测试创建课程 ===")
        
        if not self.teacher_token:
            print("❌ 需要教师token，跳过创建课程测试")
            return None
        
        url = f"{self.base_url}/api/v1/courses/"
        headers = self.get_headers(self.teacher_token)
        data = {
            "title": "API测试课程",
            "description": "这是通过API测试创建的课程",
            "category": "计算机科学",
            "difficulty": "medium",
            "duration": 120,
            "is_published": True
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            print(f"创建课程状态: {response.status_code}")
            
            if response.status_code == 200:
                course = response.json()
                print(f"✅ 创建课程成功: {course.get('title')} (ID: {course.get('id')})")
                return course.get('id')
            else:
                print(f"❌ 创建课程失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 创建课程请求失败: {str(e)}")
            return None
    
    def run_diagnosis(self):
        """运行完整诊断"""
        print("🔍 开始课程系统诊断...")
        
        # 1. 测试服务器连接
        if not self.test_server_health():
            print("\n❌ 诊断结果: 服务器未运行或无法连接")
            print("解决方案:")
            print("1. 确保后端服务正在运行: cd backend && python run.py")
            print("2. 检查端口8000是否被占用")
            print("3. 检查防火墙设置")
            return
        
        # 2. 测试数据库连接
        self.test_database_connection()
        
        # 3. 测试用户登录
        print("\n=== 测试用户登录 ===")
        self.student_token = self.login_user("student", "password")
        self.teacher_token = self.login_user("teacher", "password")
        
        if not self.student_token and not self.teacher_token:
            print("❌ 无法登录任何用户，可能需要创建测试用户")
            print("解决方案: 运行 python backend/database/create_test_data.py")
        
        # 4. 测试课程API
        courses = self.test_get_courses()
        
        if courses:
            # 测试第一个课程的详情
            first_course_id = courses[0].get('id')
            if first_course_id:
                self.test_get_course_detail(first_course_id)
        else:
            print("❌ 没有找到课程数据")
            print("解决方案:")
            print("1. 运行测试数据脚本创建课程")
            print("2. 检查数据库是否正确初始化")
            
            # 尝试创建测试课程
            if self.teacher_token:
                course_id = self.test_create_test_course()
                if course_id:
                    self.test_get_course_detail(course_id)
        
        print("\n✅ 诊断完成!")
    
    def test_specific_course(self, course_id: int):
        """测试特定课程"""
        print(f"🔍 测试课程 ID: {course_id}")
        
        if not self.test_server_health():
            return
        
        course = self.test_get_course_detail(course_id)
        
        if course:
            print(f"✅ 课程详情获取成功:")
            print(f"  标题: {course.get('title')}")
            print(f"  描述: {course.get('description', '无')[:50]}...")
            print(f"  难度: {course.get('difficulty')}")
            print(f"  发布状态: {course.get('is_published')}")
        else:
            print(f"❌ 无法获取课程 {course_id} 的详情")


def main():
    """主函数"""
    import sys
    
    tester = CourseAPITester()
    
    if len(sys.argv) > 1:
        # 测试特定课程
        try:
            course_id = int(sys.argv[1])
            tester.test_specific_course(course_id)
        except ValueError:
            print("请提供有效的课程ID")
    else:
        # 运行完整诊断
        tester.run_diagnosis()


if __name__ == "__main__":
    main()

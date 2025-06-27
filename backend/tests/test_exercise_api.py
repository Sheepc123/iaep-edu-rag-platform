"""
练习系统API测试脚本
"""
import requests
import json
from datetime import datetime


class ExerciseAPITester:
    """练习系统API测试类"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.student_token = None
        self.teacher_token = None
    
    def login_user(self, username: str, password: str) -> str:
        """用户登录获取token"""
        url = f"{self.base_url}/api/v1/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("access_token")
        else:
            print(f"登录失败: {response.text}")
            return None
    
    def get_headers(self, token: str) -> dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def test_get_exercises(self):
        """测试获取练习列表"""
        print("\n=== 测试获取练习列表 ===")
        
        if not self.student_token:
            print("需要先登录学生账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/"
        headers = self.get_headers(self.student_token)
        
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            exercises = response.json()
            print(f"获取到 {len(exercises)} 个练习:")
            for exercise in exercises:
                print(f"- {exercise['title']} ({exercise['subject']}) - {exercise['difficulty']}")
        else:
            print(f"请求失败: {response.text}")
    
    def test_get_exercise_detail(self, exercise_id: int):
        """测试获取练习详情"""
        print(f"\n=== 测试获取练习详情 (ID: {exercise_id}) ===")
        
        if not self.student_token:
            print("需要先登录学生账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/{exercise_id}"
        headers = self.get_headers(self.student_token)
        
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            exercise = response.json()
            print(f"练习标题: {exercise['title']}")
            print(f"题目数量: {exercise['total_questions']}")
            print(f"时间限制: {exercise.get('time_limit', '无限制')} 分钟")
            
            if 'questions' in exercise:
                print("题目列表:")
                for i, question in enumerate(exercise['questions'], 1):
                    print(f"  {i}. {question['title']} ({question['question_type']}) - {question['points']}分")
        else:
            print(f"请求失败: {response.text}")
    
    def test_start_exercise(self, exercise_id: int):
        """测试开始练习"""
        print(f"\n=== 测试开始练习 (ID: {exercise_id}) ===")
        
        if not self.student_token:
            print("需要先登录学生账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/{exercise_id}/start"
        headers = self.get_headers(self.student_token)
        
        response = requests.post(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            attempt = response.json()
            print(f"练习尝试ID: {attempt['id']}")
            print(f"总题目数: {attempt['total_questions']}")
            print(f"最大分数: {attempt['max_score']}")
            print(f"开始时间: {attempt['started_at']}")
            return attempt['id']
        else:
            print(f"请求失败: {response.text}")
            return None
    
    def test_submit_answer(self, attempt_id: int, question_id: int, answer: str):
        """测试提交答案"""
        print(f"\n=== 测试提交答案 (尝试ID: {attempt_id}, 题目ID: {question_id}) ===")
        
        if not self.student_token:
            print("需要先登录学生账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/submit-answer"
        headers = self.get_headers(self.student_token)
        data = {
            "attempt_id": attempt_id,
            "question_id": question_id,
            "answer_content": answer,
            "time_spent": 60  # 假设用时60秒
        }
        
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"答案ID: {result['id']}")
            print(f"是否正确: {result.get('is_correct', '待评分')}")
            print(f"获得分数: {result['points_earned']}")
        else:
            print(f"请求失败: {response.text}")
    
    def test_get_exercise_stats(self):
        """测试获取练习统计"""
        print("\n=== 测试获取练习统计 ===")
        
        if not self.student_token:
            print("需要先登录学生账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/stats"
        headers = self.get_headers(self.student_token)
        
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"总练习数: {stats['total_exercises']}")
            print(f"已完成练习数: {stats['completed_exercises']}")
            print(f"总题目数: {stats['total_questions']}")
            print(f"正确题目数: {stats['correct_questions']}")
            print(f"平均正确率: {stats['average_accuracy']}%")
            print(f"总学习时间: {stats['total_time']} 分钟")
        else:
            print(f"请求失败: {response.text}")
    
    def test_get_wrong_questions(self):
        """测试获取错题本"""
        print("\n=== 测试获取错题本 ===")
        
        if not self.student_token:
            print("需要先登录学生账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/wrong-questions"
        headers = self.get_headers(self.student_token)
        
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            wrong_questions = response.json()
            print(f"错题数量: {len(wrong_questions)}")
            for wq in wrong_questions:
                print(f"- 题目ID: {wq['question_id']}")
                print(f"  错误答案: {wq['wrong_answer']}")
                print(f"  正确答案: {wq['correct_answer']}")
                print(f"  复习次数: {wq['review_count']}")
        else:
            print(f"请求失败: {response.text}")
    
    def test_create_exercise(self):
        """测试创建练习（教师功能）"""
        print("\n=== 测试创建练习 ===")
        
        if not self.teacher_token:
            print("需要先登录教师账号")
            return
        
        url = f"{self.base_url}/api/v1/exercises/"
        headers = self.get_headers(self.teacher_token)
        data = {
            "title": "API测试练习",
            "description": "这是通过API创建的测试练习",
            "category": "自主练习",
            "subject": "计算机科学",
            "difficulty": "medium",
            "time_limit": 30,
            "is_published": True
        }
        
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            exercise = response.json()
            print(f"创建成功! 练习ID: {exercise['id']}")
            print(f"练习标题: {exercise['title']}")
            return exercise['id']
        else:
            print(f"请求失败: {response.text}")
            return None
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始练习系统API测试...")
        
        # 登录用户
        print("\n=== 用户登录 ===")
        self.student_token = self.login_user("student", "password")
        self.teacher_token = self.login_user("teacher", "password")
        
        if not self.student_token:
            print("学生登录失败，跳过学生相关测试")
        
        if not self.teacher_token:
            print("教师登录失败，跳过教师相关测试")
        
        # 测试教师功能
        if self.teacher_token:
            exercise_id = self.test_create_exercise()
        
        # 测试学生功能
        if self.student_token:
            self.test_get_exercises()
            
            # 假设第一个练习ID为1
            self.test_get_exercise_detail(1)
            
            # 开始练习
            attempt_id = self.test_start_exercise(1)
            
            # 提交答案（假设第一个题目ID为1）
            if attempt_id:
                self.test_submit_answer(attempt_id, 1, "B")
            
            # 获取统计
            self.test_get_exercise_stats()
            
            # 获取错题本
            self.test_get_wrong_questions()
        
        print("\n✅ API测试完成！")


def main():
    """主函数"""
    tester = ExerciseAPITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()

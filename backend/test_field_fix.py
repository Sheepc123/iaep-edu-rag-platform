#!/usr/bin/env python3
"""
测试字段修复
"""

import requests
import json
import sys
import os

def test_exercise_fields():
    """测试练习字段是否正确"""
    print("🔍 测试练习字段修复...")
    
    try:
        # 1. 检查数据库中的练习字段
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        
        db = SessionLocal()
        
        # 获取第一个练习
        exercise = db.query(Exercise).first()
        if not exercise:
            print("❌ 数据库中没有练习")
            return False
        
        print(f"📚 检查练习: {exercise.title}")
        
        # 检查字段
        available_fields = []
        for attr in dir(exercise):
            if not attr.startswith('_') and not callable(getattr(exercise, attr)):
                available_fields.append(attr)
        
        print("可用字段:")
        for field in sorted(available_fields):
            value = getattr(exercise, field, 'N/A')
            print(f"  {field}: {value}")
        
        # 检查是否有total_points字段
        has_total_points = hasattr(exercise, 'total_points')
        print(f"\n是否有total_points字段: {has_total_points}")
        
        # 检查题目
        questions = db.query(Question).filter(Question.exercise_id == exercise.id).all()
        print(f"题目数量: {len(questions)}")
        
        total_points_calculated = sum(q.points for q in questions if q.points)
        print(f"计算的总分: {total_points_calculated}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_after_fix():
    """测试修复后的API"""
    print("\n🧪 测试修复后的API...")
    
    try:
        # 1. 健康检查
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code != 200:
            print("❌ 服务器未运行")
            return False
        print("✅ 服务器正常")
        
        # 2. 登录
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False},
            timeout=5
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.status_code}")
            return False
        
        token = login_response.json()["access_token"]
        print("✅ 登录成功")
        
        # 3. 测试课程练习API
        headers = {"Authorization": f"Bearer {token}"}
        
        api_response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers,
            timeout=5
        )
        
        print(f"API状态码: {api_response.status_code}")
        
        if api_response.status_code == 200:
            try:
                data = api_response.json()
                exercises = data.get('exercises', [])
                print(f"✅ 成功获取 {len(exercises)} 个练习")
                
                if exercises:
                    print("\n练习详情:")
                    for i, ex in enumerate(exercises, 1):
                        print(f"  {i}. {ex['title']}")
                        print(f"     分类: {ex['category']}")
                        print(f"     难度: {ex['difficulty']}")
                        print(f"     题目数: {ex['total_questions']}")
                        print(f"     总分: {ex['total_points']}")
                        print(f"     状态: {'已发布' if ex['is_published'] else '草稿'}")
                        print()
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应: {api_response.text}")
                return False
        else:
            print(f"❌ API失败: {api_response.status_code}")
            print(f"错误: {api_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def create_test_data_if_needed():
    """如果需要，创建测试数据"""
    print("\n📝 检查并创建测试数据...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        from app.models.user import User
        from app.core.security import get_password_hash
        
        db = SessionLocal()
        
        # 检查是否有数据
        exercise_count = db.query(Exercise).count()
        if exercise_count > 0:
            print(f"✅ 已有 {exercise_count} 个练习")
            db.close()
            return True
        
        # 检查是否有用户和课程
        teacher = db.query(User).filter(User.role == "teacher").first()
        course = db.query(Course).first()
        
        if not teacher or not course:
            print("❌ 缺少基础数据，请运行: python one_click_fix.py")
            db.close()
            return False
        
        # 创建简单的测试练习
        exercise = Exercise(
            title="测试练习",
            description="用于测试字段修复的练习",
            category="practice",
            subject="测试",
            difficulty="easy",
            time_limit=30,
            course_id=course.id,
            created_by=teacher.id,
            total_questions=2,
            is_published=True,
            is_active=True
        )
        
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        
        # 添加题目
        questions = [
            Question(
                exercise_id=exercise.id,
                content="这是第一道测试题",
                question_type="multiple_choice",
                options={"A": "选项A", "B": "选项B"},
                correct_answer="A",
                explanation="这是解析",
                points=10,
                difficulty="easy",
                subject="测试",
                is_active=True
            ),
            Question(
                exercise_id=exercise.id,
                content="这是第二道测试题",
                question_type="fill_blank",
                options=None,
                correct_answer="答案",
                explanation="这是解析",
                points=15,
                difficulty="easy",
                subject="测试",
                is_active=True
            )
        ]
        
        for q in questions:
            db.add(q)
        
        db.commit()
        db.close()
        
        print("✅ 测试数据创建完成")
        return True
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 测试字段修复")
    print("=" * 40)
    
    # 1. 检查数据库字段
    if not test_exercise_fields():
        print("❌ 数据库字段检查失败")
        return
    
    # 2. 创建测试数据（如果需要）
    if not create_test_data_if_needed():
        print("❌ 测试数据准备失败")
        return
    
    # 3. 测试API
    if test_api_after_fix():
        print("\n🎉 字段修复成功！")
        print("\n💡 现在可以:")
        print("1. 重启前端: npm run dev")
        print("2. 访问: http://localhost:5173/teacher/courses/1")
        print("3. 查看课程练习标签")
    else:
        print("\n❌ API仍有问题")
        print("请检查后端日志")

if __name__ == "__main__":
    main()

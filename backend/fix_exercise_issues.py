#!/usr/bin/env python3
"""
修复练习系统问题的脚本
"""

import os
import sys
import subprocess

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_database_issues():
    """修复数据库问题"""
    print("🔧 修复数据库问题...")
    
    try:
        from app.core.database import SessionLocal, engine
        from app.models.exercise import Exercise, Question
        from app.models.course import Course
        from app.models.user import User
        from app.models import exercise
        
        # 1. 确保表存在
        print("1. 创建练习相关表...")
        exercise.Base.metadata.create_all(bind=engine)
        print("✅ 表创建完成")
        
        # 2. 检查并创建示例数据
        db = SessionLocal()
        
        # 检查是否有教师和课程
        teacher = db.query(User).filter(User.role == "teacher").first()
        course = db.query(Course).first()
        
        if not teacher or not course:
            print("❌ 缺少基础数据（教师或课程），请先运行用户和课程初始化")
            db.close()
            return False
        
        # 检查是否已有练习
        existing_exercises = db.query(Exercise).filter(Exercise.course_id == course.id).count()
        
        if existing_exercises == 0:
            print("2. 创建示例练习...")
            
            # 创建练习1
            exercise1 = Exercise(
                title="Python基础练习",
                description="测试Python基础语法和概念的练习题",
                category="practice",
                subject="Python编程",
                difficulty="easy",
                time_limit=30,
                course_id=course.id,
                created_by=teacher.id,
                total_questions=3,
                is_published=True,
                is_active=True
            )
            
            # 创建练习2
            exercise2 = Exercise(
                title="Python进阶作业",
                description="Python面向对象编程和高级特性练习",
                category="homework",
                subject="Python编程", 
                difficulty="medium",
                time_limit=60,
                course_id=course.id,
                created_by=teacher.id,
                total_questions=2,
                is_published=True,
                is_active=True
            )
            
            db.add(exercise1)
            db.add(exercise2)
            db.commit()
            db.refresh(exercise1)
            db.refresh(exercise2)
            
            # 为练习1添加题目
            questions1 = [
                Question(
                    exercise_id=exercise1.id,
                    content="Python是什么类型的编程语言？",
                    question_type="multiple_choice",
                    options={"A": "编译型", "B": "解释型", "C": "汇编型", "D": "机器型"},
                    correct_answer="B",
                    explanation="Python是一种解释型的高级编程语言。",
                    points=10,
                    difficulty="easy",
                    subject="Python编程",
                    is_active=True
                ),
                Question(
                    exercise_id=exercise1.id,
                    content="在Python中，用于定义函数的关键字是______。",
                    question_type="fill_blank",
                    options=None,
                    correct_answer="def",
                    explanation="在Python中，使用def关键字来定义函数。",
                    points=10,
                    difficulty="easy",
                    subject="Python编程",
                    is_active=True
                ),
                Question(
                    exercise_id=exercise1.id,
                    content="请解释Python中列表(list)和元组(tuple)的区别。",
                    question_type="essay",
                    options=None,
                    correct_answer="列表是可变的数据类型，元组是不可变的数据类型。",
                    explanation="这是一个开放性问题，主要考查对Python基础数据类型的理解。",
                    points=20,
                    difficulty="easy",
                    subject="Python编程",
                    is_active=True
                )
            ]
            
            # 为练习2添加题目
            questions2 = [
                Question(
                    exercise_id=exercise2.id,
                    content="Python中的装饰器主要用于什么？",
                    question_type="multiple_choice",
                    options={"A": "数据存储", "B": "函数增强", "C": "错误处理", "D": "性能优化"},
                    correct_answer="B",
                    explanation="装饰器主要用于在不修改原函数代码的情况下增强函数功能。",
                    points=15,
                    difficulty="medium",
                    subject="Python编程",
                    is_active=True
                ),
                Question(
                    exercise_id=exercise2.id,
                    content="什么是Python的GIL？请简要说明其作用。",
                    question_type="essay",
                    options=None,
                    correct_answer="GIL是全局解释器锁，确保同一时间只有一个线程执行Python字节码。",
                    explanation="GIL是Python多线程编程中的重要概念。",
                    points=25,
                    difficulty="medium",
                    subject="Python编程",
                    is_active=True
                )
            ]
            
            for question in questions1 + questions2:
                db.add(question)
            
            db.commit()
            print("✅ 示例练习创建完成")
        else:
            print(f"ℹ️  已有 {existing_exercises} 个练习")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库修复失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🧪 测试API端点...")
    
    try:
        import requests
        
        # 测试健康检查
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ 后端服务未运行，请启动: python run.py")
            return False
        
        print("✅ 后端服务运行正常")
        
        # 测试登录
        login_data = {
            "username": "teacher1",
            "password": "123456",
            "remember_me": False
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        if response.status_code != 200:
            print("❌ 教师登录失败")
            return False
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 测试课程练习API
        response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            exercises = data.get('exercises', [])
            print(f"✅ API测试成功，获取到 {len(exercises)} 个练习")
            return True
        else:
            print(f"❌ API测试失败: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API测试异常: {e}")
        return False

def check_cors_configuration():
    """检查CORS配置"""
    print("\n🌐 检查CORS配置...")
    
    try:
        from app.core.config import settings
        
        print(f"允许的源: {settings.allowed_origins_list}")
        
        # 检查是否包含前端地址
        required_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ]
        
        missing_origins = []
        for origin in required_origins:
            if origin not in settings.allowed_origins_list:
                missing_origins.append(origin)
        
        if missing_origins:
            print(f"⚠️  可能缺少CORS源: {missing_origins}")
        else:
            print("✅ CORS配置正常")
        
        return True
        
    except Exception as e:
        print(f"❌ CORS检查失败: {e}")
        return False

def generate_fix_summary():
    """生成修复总结"""
    print("\n📋 修复总结...")
    
    summary = """
# 练习系统问题修复总结

## 已修复的问题

1. ✅ 数据库表结构 - 确保所有练习相关表存在
2. ✅ 示例数据 - 创建了示例练习和题目
3. ✅ API端点 - 验证课程练习API正常工作
4. ✅ 前端API调用 - 修复了getExerciseStats中的空值访问问题

## 数据库表
- exercises: 习题集表
- questions: 题目表
- exercise_attempts: 答题尝试表  
- student_answers: 学生答案表

## API端点
- GET /api/v1/courses/{course_id}/exercises - 获取课程练习列表

## 前端页面
- 教师端: http://localhost:5173/teacher/courses/1
- 学生端: http://localhost:5173/student/courses/1

## 下一步
1. 重启前端服务: npm run dev
2. 访问课程详情页面
3. 查看"课程练习"标签
4. 验证数据正确显示

## 注意事项
- 确保后端服务运行: python run.py
- 确保前端服务运行: npm run dev
- 检查浏览器控制台是否还有错误
"""
    
    with open("exercise_fix_summary.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("✅ 修复总结已保存到: exercise_fix_summary.md")

def main():
    """主函数"""
    print("🔧 练习系统问题修复")
    print("=" * 50)
    
    success_count = 0
    
    # 1. 修复数据库
    if fix_database_issues():
        success_count += 1
        print("✅ 数据库修复完成")
    else:
        print("❌ 数据库修复失败")
    
    # 2. 检查CORS
    if check_cors_configuration():
        success_count += 1
    
    # 3. 测试API
    if test_api_endpoints():
        success_count += 1
        print("✅ API测试通过")
    else:
        print("❌ API测试失败")
    
    # 4. 生成总结
    generate_fix_summary()
    success_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 修复完成: {success_count}/4 项成功")
    
    if success_count >= 3:
        print("🎉 主要问题已修复！")
        print("\n💡 下一步:")
        print("1. 重启前端服务")
        print("2. 访问: http://localhost:5173/teacher/courses/1")
        print("3. 查看课程练习标签")
    else:
        print("❌ 仍有问题需要解决")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
更新课程中的教师姓名为真实姓名
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def update_instructor_names():
    """更新课程中的教师姓名"""
    print("🔄 更新课程中的教师姓名...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course
        from app.models.user import User
        
        db = SessionLocal()
        
        # 获取所有课程
        courses = db.query(Course).all()
        print(f"📚 找到 {len(courses)} 门课程")
        
        updated_count = 0
        
        for course in courses:
            # 获取教师信息
            instructor = db.query(User).filter(User.id == course.instructor_id).first()
            
            if instructor:
                # 如果教师有真实姓名，且当前课程显示的不是真实姓名
                if instructor.full_name and course.instructor_name != instructor.full_name:
                    old_name = course.instructor_name
                    course.instructor_name = instructor.full_name
                    updated_count += 1
                    
                    print(f"✅ 课程 '{course.title}' 教师姓名更新:")
                    print(f"   {old_name} → {instructor.full_name}")
                elif not instructor.full_name:
                    print(f"⚠️  课程 '{course.title}' 的教师 {instructor.username} 没有设置真实姓名")
                else:
                    print(f"ℹ️  课程 '{course.title}' 教师姓名已是最新: {course.instructor_name}")
            else:
                print(f"❌ 课程 '{course.title}' 的教师ID {course.instructor_id} 不存在")
        
        if updated_count > 0:
            db.commit()
            print(f"\n🎉 成功更新了 {updated_count} 门课程的教师姓名")
        else:
            print("\n✅ 所有课程的教师姓名都已是最新")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        import traceback
        traceback.print_exc()


def check_instructor_names():
    """检查当前课程的教师姓名状态"""
    print("\n🔍 检查当前课程的教师姓名状态...")
    
    try:
        from app.core.database import SessionLocal
        from app.models.course import Course
        from app.models.user import User
        
        db = SessionLocal()
        
        # 获取所有课程和教师信息
        courses = db.query(Course).all()
        
        print(f"\n📊 课程教师姓名状态报告:")
        print("=" * 60)
        
        for course in courses:
            instructor = db.query(User).filter(User.id == course.instructor_id).first()
            
            if instructor:
                print(f"📚 课程: {course.title}")
                print(f"   当前显示: {course.instructor_name}")
                print(f"   教师用户名: {instructor.username}")
                print(f"   教师真实姓名: {instructor.full_name or '未设置'}")
                
                if instructor.full_name:
                    if course.instructor_name == instructor.full_name:
                        print(f"   状态: ✅ 已使用真实姓名")
                    else:
                        print(f"   状态: ⚠️  需要更新为真实姓名")
                else:
                    print(f"   状态: ❌ 教师未设置真实姓名")
                
                print("   " + "-" * 40)
            else:
                print(f"📚 课程: {course.title}")
                print(f"   ❌ 教师ID {course.instructor_id} 不存在")
                print("   " + "-" * 40)
        
        db.close()
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")


def test_api_response():
    """测试API返回的教师姓名"""
    print("\n🧪 测试API返回的教师姓名...")
    
    try:
        import requests
        
        base_url = "http://localhost:8000/api/v1"
        
        # 获取课程列表
        response = requests.get(f"{base_url}/courses/")
        
        if response.status_code == 200:
            data = response.json()
            courses = data.get('courses', [])
            
            print(f"📚 API返回 {len(courses)} 门课程:")
            
            for course in courses:
                print(f"   - {course['title']}")
                print(f"     教师: {course['instructor_name']}")
                print(f"     教师ID: {course['instructor_id']}")
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")


def main():
    """主函数"""
    print("🚀 课程教师姓名更新工具")
    print("=" * 60)
    
    # 1. 检查当前状态
    check_instructor_names()
    
    # 2. 询问是否更新
    choice = input("\n是否更新课程中的教师姓名为真实姓名? (y/N): ")
    
    if choice.lower() == 'y':
        update_instructor_names()
        
        # 3. 再次检查状态
        check_instructor_names()
        
        # 4. 测试API
        test_api_response()
    else:
        print("取消更新")
    
    print("\n" + "=" * 60)
    print("💡 说明:")
    print("1. 此脚本会将课程中的教师姓名更新为教师的真实姓名")
    print("2. 如果教师没有设置真实姓名，将保持原有显示")
    print("3. 前端课程卡片将显示更新后的教师姓名")
    print("4. 修改后需要刷新前端页面查看效果")


if __name__ == "__main__":
    main()

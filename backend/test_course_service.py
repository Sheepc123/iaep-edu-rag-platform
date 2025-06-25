#!/usr/bin/env python3
"""
直接测试CourseService的脚本
"""
import sys
import os
sys.path.append('.')

from app.core.database import get_db
from app.services.course_service import CourseService
from app.schemas.course import CourseListQuery

def test_course_service():
    """测试CourseService"""
    print("🧪 测试CourseService...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建CourseService实例
        course_service = CourseService(db)
        
        print("1. 测试基本查询...")
        query = CourseListQuery()
        courses, total = course_service.get_courses(query)
        print(f"   总课程数: {total}")
        print(f"   返回课程数: {len(courses)}")
        
        if courses:
            print("   前3门课程:")
            for i, course in enumerate(courses[:3]):
                print(f"     {i+1}. {course.title} - {course.category} - {course.difficulty}")
        
        print("\n2. 测试带参数查询...")
        query_with_params = CourseListQuery(
            is_published=True,
            limit=5
        )
        courses, total = course_service.get_courses(query_with_params)
        print(f"   已发布课程数: {total}")
        print(f"   返回课程数: {len(courses)}")
        
        print("\n✅ CourseService测试成功!")
        
    except Exception as e:
        print(f"❌ CourseService测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_course_service()

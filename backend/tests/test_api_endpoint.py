#!/usr/bin/env python3
"""
测试API端点的脚本
"""
import sys
import os
sys.path.append('.')

from app.core.database import get_db
from app.schemas.course import CourseListQuery, DifficultyLevel
from app.services.course_service import CourseService

def test_api_endpoint_logic():
    """测试API端点逻辑"""
    print("🧪 测试API端点逻辑...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        print("1. 测试无参数调用...")
        # 模拟API端点的参数处理
        category = None
        difficulty = None
        instructor_id = None
        search = None
        is_published = None
        skip = 0
        limit = 20
        sort_by = "created_at"
        sort_order = "desc"
        
        # 处理difficulty参数转换（模拟API端点中的逻辑）
        difficulty_enum = None
        if difficulty:
            try:
                difficulty_enum = DifficultyLevel(difficulty)
            except ValueError:
                difficulty_enum = None
        
        # 构建查询参数
        query = CourseListQuery(
            category=category,
            difficulty=difficulty_enum,
            instructor_id=instructor_id,
            search=search,
            is_published=is_published,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        course_service = CourseService(db)
        courses, total = course_service.get_courses(query)
        
        result = {
            "courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "category": course.category,
                    "difficulty": course.difficulty,
                    "is_published": course.is_published
                } for course in courses
            ],
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }
        
        print(f"   ✅ 成功返回 {len(result['courses'])} 门课程，总共 {result['total']} 门")
        
        print("\n2. 测试带参数调用...")
        # 测试带参数的调用
        difficulty = "medium"
        is_published = True
        limit = 5
        
        difficulty_enum = None
        if difficulty:
            try:
                difficulty_enum = DifficultyLevel(difficulty)
            except ValueError:
                difficulty_enum = None
        
        query = CourseListQuery(
            category=category,
            difficulty=difficulty_enum,
            instructor_id=instructor_id,
            search=search,
            is_published=is_published,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        courses, total = course_service.get_courses(query)
        
        result = {
            "courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "category": course.category,
                    "difficulty": course.difficulty,
                    "is_published": course.is_published
                } for course in courses
            ],
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }
        
        print(f"   ✅ 成功返回 {len(result['courses'])} 门中等难度已发布课程，总共 {result['total']} 门")
        
        if result['courses']:
            print("   前3门课程:")
            for i, course in enumerate(result['courses'][:3]):
                print(f"     {i+1}. {course['title']} - {course['category']} - {course['difficulty']}")
        
        print("\n✅ API端点逻辑测试成功!")
        
    except Exception as e:
        print(f"❌ API端点逻辑测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_api_endpoint_logic()

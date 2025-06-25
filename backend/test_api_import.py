#!/usr/bin/env python3
"""
测试API导入的脚本
"""
import sys
import os
sys.path.append('.')

def test_api_imports():
    """测试API模块导入"""
    print("🧪 测试API模块导入...")
    
    try:
        print("1. 测试基础模块导入...")
        from app.schemas.course import CourseListQuery, DifficultyLevel
        print("   ✅ schemas.course 导入成功")
        
        from app.services.course_service import CourseService
        print("   ✅ services.course_service 导入成功")
        
        print("\n2. 测试API端点导入...")
        from app.api.v1.endpoints import courses
        print("   ✅ endpoints.courses 导入成功")
        
        print("\n3. 测试DifficultyLevel枚举...")
        print(f"   可用难度级别: {[d.value for d in DifficultyLevel]}")
        
        # 测试字符串转换
        test_difficulty = "medium"
        try:
            difficulty_enum = DifficultyLevel(test_difficulty)
            print(f"   字符串 '{test_difficulty}' 转换为枚举: {difficulty_enum}")
        except ValueError as e:
            print(f"   ❌ 字符串转换失败: {e}")
        
        print("\n4. 测试CourseListQuery创建...")
        query = CourseListQuery(
            difficulty=DifficultyLevel.MEDIUM,
            is_published=True,
            limit=5
        )
        print(f"   ✅ CourseListQuery 创建成功: difficulty={query.difficulty}")
        
        print("\n✅ 所有导入测试成功!")
        
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_imports()

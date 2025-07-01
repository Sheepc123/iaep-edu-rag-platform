#!/usr/bin/env python3
"""
简单修复脚本 - 专门解决字段问题
"""

import requests
import json

def test_simple_api():
    """简单测试API"""
    print("🧪 简单API测试...")
    
    try:
        # 登录
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={"username": "teacher1", "password": "123456", "remember_me": False}
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.status_code}")
            return False
        
        token = login_response.json()["access_token"]
        print("✅ 登录成功")
        
        # 测试API
        headers = {"Authorization": f"Bearer {token}"}
        api_response = requests.get(
            "http://localhost:8000/api/v1/courses/1/exercises",
            headers=headers
        )
        
        print(f"API状态: {api_response.status_code}")
        
        if api_response.status_code == 200:
            data = api_response.json()
            exercises = data.get('exercises', [])
            print(f"✅ 获取到 {len(exercises)} 个练习")
            
            for ex in exercises:
                print(f"  - {ex['title']} (总分: {ex['total_points']})")
            
            return True
        else:
            print(f"❌ API失败: {api_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 简单修复测试")
    print("=" * 30)
    
    if test_simple_api():
        print("\n🎉 修复成功！")
    else:
        print("\n❌ 仍有问题")

if __name__ == "__main__":
    main()

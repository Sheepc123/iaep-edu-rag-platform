#!/usr/bin/env python3
"""
测试API登录请求
"""

import requests
import json

def test_api_login():
    """测试API登录"""
    print("🌐 测试API登录...")
    
    url = "http://localhost:8000/api/v1/auth/login"
    
    # 测试数据
    login_data = {
        "username": "teacher1",
        "password": "123456",
        "remember_me": False,
        "device_info": "test_browser"
    }
    
    try:
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(login_data, indent=2)}")
        
        response = requests.post(
            url,
            json=login_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "test_client"
            },
            timeout=10
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 登录成功")
            print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print("❌ 登录失败")
            print(f"错误响应: {response.text}")
            
            # 尝试解析JSON错误
            try:
                error_data = response.json()
                print(f"错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print("无法解析错误响应为JSON")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def test_health_check():
    """测试健康检查"""
    print("\n🔍 测试健康检查...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"健康检查状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"健康检查结果: {json.dumps(data, indent=2)}")
        else:
            print(f"健康检查失败: {response.text}")
            
    except Exception as e:
        print(f"健康检查错误: {e}")


def test_api_docs():
    """测试API文档"""
    print("\n📚 测试API文档...")
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        print(f"API文档状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API文档可访问")
        else:
            print("❌ API文档不可访问")
            
    except Exception as e:
        print(f"API文档错误: {e}")


def main():
    """主函数"""
    print("🚀 API登录测试")
    print("=" * 50)
    
    # 1. 健康检查
    test_health_check()
    
    # 2. API文档检查
    test_api_docs()
    
    # 3. 登录测试
    test_api_login()
    
    print("\n" + "=" * 50)
    print("测试完成")


if __name__ == "__main__":
    main()

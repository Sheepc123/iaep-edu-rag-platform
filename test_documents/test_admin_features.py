#!/usr/bin/env python3
"""
测试管理员功能
"""
import requests
import json

# API配置
BASE_URL = "http://localhost:8000/api/v1"

def test_admin_login():
    """测试管理员登录"""
    print("🔐 测试管理员登录")
    print("=" * 50)
    
    # 尝试使用管理员账户登录
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"登录状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 登录成功")
            print(f"   用户: {data.get('user', {}).get('username')}")
            print(f"   角色: {data.get('user', {}).get('role')}")
            print(f"   令牌: {data.get('access_token', '')[:20]}...")
            return data.get('access_token')
        else:
            print(f"❌ 登录失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return None

def test_admin_apis(token):
    """测试管理员API"""
    if not token:
        print("❌ 没有有效的令牌，跳过API测试")
        return
    
    print("\n🔧 测试管理员API")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试仪表板统计
    print("\n1. 测试仪表板统计...")
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard/stats", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ 获取统计成功")
            print(f"      总用户数: {stats.get('total_users', 0)}")
            print(f"      学生数: {stats.get('total_students', 0)}")
            print(f"      教师数: {stats.get('total_teachers', 0)}")
        else:
            print(f"   ❌ 获取统计失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 测试用户列表
    print("\n2. 测试用户列表...")
    try:
        response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            users_data = response.json()
            print(f"   ✅ 获取用户列表成功")
            print(f"      用户总数: {users_data.get('total', 0)}")
            users = users_data.get('users', [])
            if users:
                print(f"      前3个用户:")
                for i, user in enumerate(users[:3], 1):
                    print(f"        {i}. {user.get('full_name', 'N/A')} ({user.get('role', 'N/A')})")
        else:
            print(f"   ❌ 获取用户列表失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 测试使用统计
    print("\n3. 测试AI使用统计...")
    try:
        response = requests.get(f"{BASE_URL}/admin/usage-stats?days=7", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            stats_data = response.json()
            print(f"   ✅ 获取使用统计成功")
            print(f"      时间范围: {stats_data.get('time_range', 'N/A')}")
            user_stats = stats_data.get('user_stats', [])
            print(f"      活跃用户数: {len(user_stats)}")
        else:
            print(f"   ❌ 获取使用统计失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 测试系统状态
    print("\n4. 测试系统状态...")
    try:
        response = requests.get(f"{BASE_URL}/admin/system/stats", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            system_stats = response.json()
            print(f"   ✅ 获取系统状态成功")
            print(f"      数据库状态: {system_stats.get('database_status', 'N/A')}")
            print(f"      AI服务状态: {system_stats.get('ai_service_status', 'N/A')}")
        else:
            print(f"   ❌ 获取系统状态失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")

def test_frontend_access():
    """测试前端访问"""
    print("\n🌐 测试前端访问")
    print("=" * 50)
    
    frontend_urls = [
        "http://localhost:5173",
        "http://localhost:5173/admin/login",
    ]
    
    for url in frontend_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: {e}")

def main():
    """主函数"""
    print("🚀 管理员功能测试")
    print("=" * 50)
    
    # 测试登录
    token = test_admin_login()
    
    # 测试API
    test_admin_apis(token)
    
    # 测试前端
    test_frontend_access()
    
    print("\n" + "=" * 50)
    print("🎯 测试完成")
    
    if token:
        print("\n💡 下一步:")
        print("1. 访问 http://localhost:5173 查看首页")
        print("2. 点击右上角的'管理员'按钮")
        print("3. 使用 admin/admin123 登录管理员控制台")
        print("4. 探索管理员功能：仪表板、用户管理、使用统计等")
    else:
        print("\n⚠️ 注意:")
        print("1. 确保后端服务正在运行")
        print("2. 确保数据库中有管理员账户")
        print("3. 检查管理员账户的用户名和密码")

if __name__ == "__main__":
    main()

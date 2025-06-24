"""
创建测试用户脚本
"""
import requests
import json

def create_test_user():
    """创建测试用户"""
    base_url = "http://127.0.0.1:8000"
    
    # 测试用户数据
    user_data = {
        "username": "student123",
        "email": "student@example.com",
        "password": "123456",
        "full_name": "测试学生",
        "phone": "13800138000",
        "role": "student"
    }
    
    try:
        print("🔍 检查服务器状态...")
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code != 200:
            print("❌ 服务器未启动")
            return False
        
        print("✅ 服务器运行正常")
        print("\n📝 创建测试用户...")
        
        # 注册用户
        response = requests.post(
            f"{base_url}/api/v1/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 and result.get("success"):
            print("\n🎉 测试用户创建成功！")
            print("=" * 50)
            print("登录信息:")
            print(f"用户名: {user_data['username']}")
            print(f"邮箱: {user_data['email']}")
            print(f"密码: {user_data['password']}")
            print(f"角色: {user_data['role']}")
            print("=" * 50)
            return True
        else:
            print("❌ 用户创建失败")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
        return False
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return False

def test_login():
    """测试登录"""
    base_url = "http://127.0.0.1:8000"
    
    login_data = {
        "username": "student123",
        "password": "123456",
        "remember_me": True,
        "device_info": "Test Browser"
    }
    
    try:
        print("\n🔐 测试登录...")
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 登录成功！")
            print(f"用户信息: {result['user_info']['full_name']} ({result['user_info']['role']})")
            print(f"访问令牌: {result['access_token'][:50]}...")
            return True
        else:
            print(f"❌ 登录失败: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 创建测试用户并验证登录功能")
    print("=" * 50)
    
    # 创建测试用户
    if create_test_user():
        # 测试登录
        test_login()
    
    print("\n" + "=" * 50)
    print("✨ 现在您可以在前端使用以下账号登录:")
    print("用户名: student123")
    print("密码: 123456")
    print("=" * 50)

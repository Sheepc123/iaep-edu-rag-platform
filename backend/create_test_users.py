"""
创建测试用户脚本
"""
import requests
import json

def create_test_users():
    """创建测试用户"""
    base_url = "http://127.0.0.1:8000"
    
    # 测试用户数据
    test_users = [
        {
            "username": "student123",
            "email": "student@example.com",
            "password": "123456",
            "full_name": "张同学",
            "phone": "13800138000",
            "role": "student"
        },
        {
            "username": "teacher123",
            "email": "teacher@example.com",
            "password": "123456",
            "full_name": "李老师",
            "phone": "13800138001",
            "role": "teacher"
        },
        {
            "username": "admin123",
            "email": "admin@example.com",
            "password": "123456",
            "full_name": "王管理员",
            "phone": "13800138002",
            "role": "admin"
        }
    ]
    
    try:
        print("🔍 检查服务器状态...")
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code != 200:
            print("❌ 服务器未启动")
            return False
        
        print("✅ 服务器运行正常")
        print("\n📝 创建测试用户...")
        print("=" * 60)
        
        success_count = 0
        
        for user_data in test_users:
            try:
                response = requests.post(
                    f"{base_url}/api/v1/auth/register",
                    json=user_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        print(f"✅ {user_data['role']} 用户创建成功: {user_data['username']}")
                        success_count += 1
                    else:
                        print(f"❌ {user_data['role']} 用户创建失败: {result.get('message', '未知错误')}")
                else:
                    error_detail = response.json().get('detail', '未知错误')
                    if "已存在" in error_detail:
                        print(f"ℹ️  {user_data['role']} 用户已存在: {user_data['username']}")
                        success_count += 1
                    else:
                        print(f"❌ {user_data['role']} 用户创建失败: {error_detail}")
                        
            except Exception as e:
                print(f"❌ 创建 {user_data['role']} 用户时出错: {e}")
        
        print("=" * 60)
        print(f"创建完成: {success_count}/{len(test_users)} 个用户可用")
        
        if success_count > 0:
            print("\n🎉 测试账号信息:")
            print("=" * 60)
            for user in test_users:
                print(f"【{user['role'].upper()}】")
                print(f"  用户名: {user['username']}")
                print(f"  密码: {user['password']}")
                print(f"  姓名: {user['full_name']}")
                print()
            print("=" * 60)
            print("💡 您现在可以在前端使用这些账号登录测试！")
            return True
        else:
            print("❌ 没有可用的测试账号")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
        print("   启动命令: cd backend && python run.py")
        return False
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return False

def test_login():
    """测试登录功能"""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🔐 测试登录功能...")
    print("=" * 60)
    
    # 测试学生登录
    login_data = {
        "username": "student123",
        "password": "123456",
        "remember_me": True,
        "device_info": "Test Browser"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 学生账号登录测试成功！")
            print(f"   用户: {result['user_info']['full_name']} ({result['user_info']['role']})")
            print(f"   令牌: {result['access_token'][:30]}...")
            return True
        else:
            print(f"❌ 登录测试失败: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 智能教育平台 - 测试用户创建工具")
    print("=" * 60)
    
    # 创建测试用户
    if create_test_users():
        # 测试登录
        test_login()
    
    print("\n" + "=" * 60)
    print("🎯 下一步:")
    print("1. 确保后端服务正在运行: python run.py")
    print("2. 启动前端服务: npm run dev")
    print("3. 在浏览器中访问前端，使用上述账号登录测试")
    print("=" * 60)

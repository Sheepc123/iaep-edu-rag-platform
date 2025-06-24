"""
用户认证功能测试脚本
"""
import requests
import json
from datetime import datetime


class AuthTester:
    """认证功能测试类"""
    
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.access_token = None
        self.refresh_token = None
    
    def test_health_check(self):
        """测试健康检查"""
        print("🔍 测试健康检查...")
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 健康检查失败: {e}")
            return False
    
    def test_register(self):
        """测试用户注册"""
        print("\n📝 测试用户注册...")
        
        # 生成唯一的测试用户
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        user_data = {
            "username": f"testuser_{timestamp}",
            "email": f"test_{timestamp}@example.com",
            "password": "test123456",
            "full_name": "测试用户",
            "phone": "13800138000",
            "role": "student"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/register",
                json=user_data
            )
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            
            if response.status_code == 200:
                print("✅ 用户注册成功")
                return user_data
            else:
                print("❌ 用户注册失败")
                return None
                
        except Exception as e:
            print(f"❌ 注册请求失败: {e}")
            return None
    
    def test_login(self, username, password):
        """测试用户登录"""
        print("\n🔐 测试用户登录...")
        
        login_data = {
            "username": username,
            "password": password,
            "remember_me": True,
            "device_info": "Test Device"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json=login_data
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                print("✅ 用户登录成功")
                print(f"用户信息: {data['user_info']['full_name']} ({data['user_info']['role']})")
                return True
            else:
                print(f"❌ 用户登录失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 登录请求失败: {e}")
            return False
    
    def test_get_user_info(self):
        """测试获取用户信息"""
        print("\n👤 测试获取用户信息...")
        
        if not self.access_token:
            print("❌ 没有访问令牌")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/auth/me",
                headers=headers
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                user_info = response.json()
                print("✅ 获取用户信息成功")
                print(f"用户: {user_info['full_name']} ({user_info['username']})")
                print(f"角色: {user_info['role']}")
                print(f"邮箱: {user_info['email']}")
                return True
            else:
                print(f"❌ 获取用户信息失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    def test_refresh_token(self):
        """测试刷新令牌"""
        print("\n🔄 测试刷新令牌...")
        
        if not self.refresh_token:
            print("❌ 没有刷新令牌")
            return False
        
        refresh_data = {
            "refresh_token": self.refresh_token
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/refresh",
                json=refresh_data
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    new_tokens = data["data"]
                    self.access_token = new_tokens["access_token"]
                    self.refresh_token = new_tokens["refresh_token"]
                    print("✅ 令牌刷新成功")
                    return True
                else:
                    print("❌ 令牌刷新失败")
                    return False
            else:
                print(f"❌ 令牌刷新失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    def test_logout(self):
        """测试用户登出"""
        print("\n👋 测试用户登出...")
        
        if not self.access_token:
            print("❌ 没有访问令牌")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/logout",
                headers=headers
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 用户登出成功")
                self.access_token = None
                self.refresh_token = None
                return True
            else:
                print(f"❌ 用户登出失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始用户认证功能测试")
        print("=" * 50)
        
        # 1. 健康检查
        if not self.test_health_check():
            print("❌ 服务器未启动或不可用")
            return
        
        # 2. 用户注册
        user_data = self.test_register()
        if not user_data:
            print("❌ 用户注册失败，停止测试")
            return
        
        # 3. 用户登录
        if not self.test_login(user_data["username"], user_data["password"]):
            print("❌ 用户登录失败，停止测试")
            return
        
        # 4. 获取用户信息
        self.test_get_user_info()
        
        # 5. 刷新令牌
        self.test_refresh_token()
        
        # 6. 再次获取用户信息（验证新令牌）
        self.test_get_user_info()
        
        # 7. 用户登出
        self.test_logout()
        
        print("\n" + "=" * 50)
        print("🎉 用户认证功能测试完成")


if __name__ == "__main__":
    tester = AuthTester()
    tester.run_all_tests()

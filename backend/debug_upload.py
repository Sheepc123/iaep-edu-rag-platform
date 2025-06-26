"""
调试文档上传功能
"""
import requests
import json

def debug_upload():
    """调试上传功能"""
    
    print("🔍 调试文档上传功能...")
    
    # 1. 检查API是否可访问
    print("\n1. 检查API基础连接...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/teacher-knowledge/categories")
        if response.status_code == 200:
            print("✅ API基础连接正常")
        else:
            print(f"❌ API连接失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API连接异常: {e}")
        return
    
    # 2. 测试登录
    print("\n2. 测试用户登录...")
    login_data = {
        "username": "teacher1",
        "password": "123456"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("✅ 登录成功")
            
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(f"响应: {response.text}")
            return
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return
    
    # 3. 测试文档上传端点（不上传文件，只测试端点）
    print("\n3. 测试上传端点访问...")
    try:
        # 测试没有文件的情况
        response = requests.post("http://127.0.0.1:8000/api/v1/teacher-knowledge/upload", 
                               headers=headers)
        print(f"无文件上传响应状态: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 422:
            print("✅ 端点正常（422是预期的，因为没有提供文件）")
        elif response.status_code == 401:
            print("❌ 认证失败，token可能无效")
        elif response.status_code == 404:
            print("❌ 端点不存在，路由配置可能有问题")
        else:
            print(f"⚠️  意外的状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 上传端点测试异常: {e}")
    
    # 4. 检查文档处理器依赖
    print("\n4. 检查文档处理器依赖...")
    try:
        import PyPDF2
        print("✅ PyPDF2 已安装")
    except ImportError:
        print("❌ PyPDF2 未安装")
    
    try:
        from docx import Document
        print("✅ python-docx 已安装")
    except ImportError:
        print("❌ python-docx 未安装")
    
    try:
        import fitz
        print("✅ PyMuPDF 已安装")
    except ImportError:
        print("❌ PyMuPDF 未安装")
    
    # 5. 检查上传目录
    print("\n5. 检查上传目录...")
    import os
    upload_dir = "uploads/knowledge_base"
    if os.path.exists(upload_dir):
        print(f"✅ 上传目录存在: {upload_dir}")
    else:
        print(f"⚠️  上传目录不存在: {upload_dir}")
        try:
            os.makedirs(upload_dir, exist_ok=True)
            print(f"✅ 已创建上传目录: {upload_dir}")
        except Exception as e:
            print(f"❌ 创建上传目录失败: {e}")
    
    print("\n🎉 调试完成！")
    print("\n💡 如果上传仍然失败，请检查：")
    print("1. 浏览器开发者工具的Network标签中的具体错误")
    print("2. 后端服务器的控制台输出")
    print("3. 确保选择的是PDF或Word文档")
    print("4. 确保文件大小不超过100MB")

if __name__ == "__main__":
    debug_upload()

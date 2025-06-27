"""
测试教师知识库API
"""
import requests
import json
import os
from pathlib import Path

# API基础URL
BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_knowledge_api():
    """测试知识库API"""
    
    print("🧪 开始测试教师知识库API...")
    
    # 1. 首先需要登录获取token
    print("\n1. 用户登录...")
    login_data = {
        "username": "teacher1",  # 假设有这个测试用户
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"✅ 登录成功，获取到token")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print("创建测试教师用户...")
            
            # 创建测试教师用户
            register_data = {
                "username": "teacher1",
                "email": "teacher1@example.com",
                "password": "123456",
                "full_name": "测试教师",
                "role": "teacher"
            }
            
            reg_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
            if reg_response.status_code == 200:
                print("✅ 测试用户创建成功")
                
                # 重新登录
                response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data["access_token"]
                    print(f"✅ 登录成功")
                    
                    headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                else:
                    print(f"❌ 重新登录失败: {response.status_code}")
                    return
            else:
                print(f"❌ 创建测试用户失败: {reg_response.status_code}")
                return
                
    except Exception as e:
        print(f"❌ 登录过程出错: {e}")
        return
    
    # 2. 测试获取文档分类
    print("\n2. 测试获取文档分类...")
    try:
        response = requests.get(f"{BASE_URL}/teacher-knowledge/categories", headers=headers)
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ 获取分类成功: {len(categories['categories'])} 个分类")
            for cat in categories['categories']:
                print(f"   - {cat['label']}: {cat['description']}")
        else:
            print(f"❌ 获取分类失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取分类出错: {e}")
    
    # 3. 测试获取文档列表
    print("\n3. 测试获取文档列表...")
    try:
        response = requests.get(f"{BASE_URL}/teacher-knowledge/documents", headers=headers)
        if response.status_code == 200:
            docs_data = response.json()
            print(f"✅ 获取文档列表成功: 共 {docs_data['total']} 个文档")
            if docs_data['documents']:
                for doc in docs_data['documents'][:3]:  # 只显示前3个
                    print(f"   - {doc['title']} ({doc['category']})")
            else:
                print("   📝 知识库为空，可以上传一些文档进行测试")
        else:
            print(f"❌ 获取文档列表失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
    except Exception as e:
        print(f"❌ 获取文档列表出错: {e}")
    
    # 4. 测试搜索功能
    print("\n4. 测试搜索功能...")
    try:
        search_data = {
            "query": "测试",
            "limit": 5
        }
        response = requests.post(f"{BASE_URL}/teacher-knowledge/search", 
                               headers=headers, json=search_data)
        if response.status_code == 200:
            search_results = response.json()
            print(f"✅ 搜索功能正常: 找到 {len(search_results)} 个结果")
        else:
            print(f"❌ 搜索功能失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 搜索功能出错: {e}")
    
    # 5. 测试统计信息
    print("\n5. 测试统计信息...")
    try:
        response = requests.get(f"{BASE_URL}/teacher-knowledge/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ 获取统计信息成功:")
            print(f"   - 总文档数: {stats['total_documents']}")
            print(f"   - 总大小: {stats['total_size']} 字节")
            print(f"   - 本月上传: {stats['this_month_uploads']}")
            if stats['category_stats']:
                print(f"   - 分类统计:")
                for category, stat in stats['category_stats'].items():
                    print(f"     * {category}: {stat['count']} 个文档")
        else:
            print(f"❌ 获取统计信息失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取统计信息出错: {e}")
    
    # 6. 测试文档上传 (创建一个测试PDF文件)
    print("\n6. 测试文档上传...")
    try:
        # 创建一个简单的PDF文件用于测试
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            test_file_path = "test_document.pdf"
            c = canvas.Canvas(test_file_path, pagesize=letter)
            c.drawString(100, 750, "测试文档")
            c.drawString(100, 720, "这是一个测试文档，用于验证知识库上传功能。")
            c.drawString(100, 690, "内容概述:")
            c.drawString(120, 660, "- 测试文档上传")
            c.drawString(120, 630, "- 测试文本提取")
            c.drawString(120, 600, "- 测试搜索功能")
            c.save()

            print("✅ 创建测试PDF文件成功")

        except ImportError:
            print("⚠️  reportlab未安装，跳过PDF上传测试")
            print("   可以运行: pip install reportlab 来安装")
            return

        # 上传文件
        with open(test_file_path, 'rb') as f:
            files = {
                'file': ('test_document.pdf', f, 'application/pdf')
            }
            data = {
                'category': '测试文档',
                'tags': '测试,API,知识库'
            }

            # 注意：上传文件时不能使用JSON headers
            upload_headers = {
                "Authorization": f"Bearer {access_token}"
            }

            response = requests.post(f"{BASE_URL}/teacher-knowledge/upload",
                                   headers=upload_headers, files=files, data=data)

        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        
        if response.status_code == 200:
            upload_result = response.json()
            print(f"✅ 文档上传成功: 文档ID {upload_result['document_id']}")
            
            # 重新获取文档列表验证
            response = requests.get(f"{BASE_URL}/teacher-knowledge/documents", headers=headers)
            if response.status_code == 200:
                docs_data = response.json()
                print(f"✅ 上传后文档总数: {docs_data['total']}")
        else:
            print(f"❌ 文档上传失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 文档上传出错: {e}")
    
    print("\n🎉 API测试完成！")


if __name__ == "__main__":
    test_knowledge_api()

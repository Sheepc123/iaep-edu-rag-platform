#!/usr/bin/env python3
"""
测试知识库API调用
模拟前端请求，检查API响应
"""
import requests
import json
import sys
import os

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

def get_auth_token():
    """获取认证令牌"""
    # 尝试使用测试教师账户登录
    login_data = {
        "username": "teacher1",  # 假设存在的教师账户
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ 登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return None

def test_get_documents(token):
    """测试获取文档列表API"""
    print("\n=== 测试获取文档列表 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 测试基本请求
        response = requests.get(f"{BASE_URL}/teacher-knowledge/documents", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取文档列表")
            print(f"总文档数: {data.get('total', 0)}")
            print(f"当前页: {data.get('page', 0)}")
            print(f"每页大小: {data.get('size', 0)}")
            print(f"总页数: {data.get('pages', 0)}")
            
            documents = data.get('documents', [])
            print(f"当前页文档数: {len(documents)}")
            
            for i, doc in enumerate(documents[:3]):  # 只显示前3个
                print(f"  文档 {i+1}:")
                print(f"    ID: {doc.get('id')}")
                print(f"    标题: {doc.get('title')}")
                print(f"    文件名: {doc.get('filename')}")
                print(f"    分类: {doc.get('category')}")
                print(f"    状态: {doc.get('status')}")
                print(f"    教师ID: {doc.get('teacher_id')}")
            
            return True
        else:
            print(f"❌ 获取文档列表失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_search_documents(token):
    """测试搜索文档API"""
    print("\n=== 测试搜索文档 ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    test_queries = ["Linux", "Python", "机器学习", "算法", "教程"]
    
    for query in test_queries:
        print(f"\n🔍 搜索: '{query}'")
        
        search_data = {
            "query": query,
            "limit": 5
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/teacher-knowledge/search", 
                headers=headers, 
                json=search_data
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ 搜索成功，结果数: {len(results)}")
                
                for i, result in enumerate(results[:2]):  # 只显示前2个
                    print(f"  结果 {i+1}:")
                    print(f"    ID: {result.get('id')}")
                    print(f"    标题: {result.get('title')}")
                    print(f"    相关度: {result.get('relevance', 'N/A')}")
                    content = result.get('content', '')
                    if content:
                        print(f"    内容预览: {content[:100]}...")
            else:
                print(f"❌ 搜索失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 搜索请求异常: {e}")

def test_semantic_search(token):
    """测试语义搜索API"""
    print("\n=== 测试语义搜索 ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    test_queries = ["机器学习算法", "Python编程基础", "Linux系统管理"]
    
    for query in test_queries:
        print(f"\n🧠 语义搜索: '{query}'")
        
        search_data = {
            "query": query,
            "top_k": 5
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/teacher-knowledge/semantic-search", 
                headers=headers, 
                json=search_data
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ 语义搜索成功，结果数: {len(results)}")
                
                for i, result in enumerate(results[:2]):  # 只显示前2个
                    print(f"  结果 {i+1}:")
                    print(f"    文档ID: {result.get('document_id')}")
                    print(f"    标题: {result.get('title')}")
                    print(f"    相似度: {result.get('similarity', 'N/A')}")
                    print(f"    分类: {result.get('category')}")
                    content = result.get('content', '')
                    if content:
                        print(f"    内容预览: {content[:100]}...")
            else:
                print(f"❌ 语义搜索失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 语义搜索请求异常: {e}")

def test_vector_stats(token):
    """测试向量统计API"""
    print("\n=== 测试向量统计 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/teacher-knowledge/vector-stats", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取向量统计成功")
            print(f"向量服务可用: {data.get('available', False)}")
            
            if data.get('available'):
                stats = data.get('stats', {})
                print(f"向量统计: {json.dumps(stats, indent=2, ensure_ascii=False)}")
            else:
                print(f"向量服务不可用: {data.get('message', '未知原因')}")
        else:
            print(f"❌ 获取向量统计失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 向量统计请求异常: {e}")

def main():
    """主函数"""
    print("🧪 知识库API测试工具")
    print("=" * 50)
    
    # 获取认证令牌
    print("🔐 获取认证令牌...")
    token = get_auth_token()
    
    if not token:
        print("❌ 无法获取认证令牌，请检查:")
        print("  1. 后端服务是否运行 (http://localhost:8000)")
        print("  2. 是否存在测试教师账户 (teacher1/123456)")
        print("  3. 数据库连接是否正常")
        return
    
    print(f"✅ 成功获取令牌: {token[:20]}...")
    
    # 测试各个API
    test_get_documents(token)
    test_search_documents(token)
    test_semantic_search(token)
    test_vector_stats(token)
    
    print("\n" + "=" * 50)
    print("🏁 API测试完成")

if __name__ == "__main__":
    main()

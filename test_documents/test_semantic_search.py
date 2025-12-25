#!/usr/bin/env python3
"""
测试语义搜索功能
"""
import requests
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# API配置
BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "teacher1"
PASSWORD = "123456"

def get_auth_token():
    """获取认证令牌"""
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"登录失败: {response.status_code} - {response.text}")
        return None

def test_semantic_search():
    """测试语义搜索功能"""
    print("🧠 测试语义搜索功能")
    print("=" * 50)
    
    # 1. 获取认证令牌
    print("1. 获取认证令牌...")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证令牌")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. 检查向量统计
    print("\n2. 检查向量数据库状态...")
    try:
        response = requests.get(f"{BASE_URL}/teacher-knowledge/vector-stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ 向量服务状态: {'可用' if stats.get('available') else '不可用'}")
            if stats.get('available') and stats.get('stats'):
                print(f"   - 总向量数: {stats['stats'].get('total_vectors', 0)}")
                print(f"   - 集合名称: {stats['stats'].get('collection_name', 'N/A')}")
                print(f"   - 嵌入模型: {stats['stats'].get('embedding_model', 'N/A')}")
            else:
                print(f"   - 消息: {stats.get('message', 'N/A')}")
        else:
            print(f"❌ 获取向量统计失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 向量统计请求异常: {e}")
    
    # 3. 获取知识库文档列表
    print("\n3. 获取知识库文档...")
    try:
        response = requests.get(f"{BASE_URL}/teacher-knowledge/documents?page=1&page_size=10", headers=headers)
        if response.status_code == 200:
            docs_data = response.json()
            documents = docs_data.get('documents', [])
            print(f"✅ 知识库文档数: {len(documents)}")
            
            if documents:
                print("   文档列表:")
                for i, doc in enumerate(documents[:5]):
                    print(f"     {i+1}. {doc.get('title', 'N/A')} ({doc.get('category', 'N/A')})")
            else:
                print("   ⚠️ 知识库中没有文档")
        else:
            print(f"❌ 获取文档列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 文档列表请求异常: {e}")
    
    # 4. 测试语义搜索
    print("\n4. 测试语义搜索...")
    test_queries = [
        "Python编程",
        "数据结构",
        "算法",
        "机器学习",
        "编程基础"
    ]
    
    for query in test_queries:
        print(f"\n🔍 搜索: '{query}'")
        
        search_data = {
            "query": query,
            "top_k": 5
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/teacher-knowledge/semantic-search", 
                headers=headers, 
                json=search_data,
                timeout=30
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                results = response.json()
                print(f"   ✅ 搜索成功，结果数: {len(results)}")
                
                if results:
                    for i, result in enumerate(results[:3]):  # 只显示前3个
                        print(f"     结果 {i+1}:")
                        print(f"       文档ID: {result.get('document_id')}")
                        print(f"       标题: {result.get('title')}")
                        print(f"       相似度: {result.get('similarity', 'N/A'):.3f}")
                        print(f"       分类: {result.get('category')}")
                        content = result.get('content', '')
                        if content:
                            print(f"       内容预览: {content[:100]}...")
                else:
                    print("     ⚠️ 没有找到相关结果")
            elif response.status_code == 503:
                print(f"   ❌ 服务不可用: {response.text}")
                break
            else:
                print(f"   ❌ 搜索失败: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 搜索请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 测试完成")

if __name__ == "__main__":
    test_semantic_search()

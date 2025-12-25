#!/usr/bin/env python3
"""
测试语义搜索API
"""
import requests
import json

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
    """测试语义搜索"""
    print("🧠 测试语义搜索API")
    print("=" * 50)
    
    # 获取认证令牌
    token = get_auth_token()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试查询
    test_queries = [
        {"query": "Python编程", "top_k": 10},
        {"query": "高等数学", "top_k": 10},
        {"query": "极限理论", "top_k": 10},
        {"query": "编程基础", "top_k": 10},
        {"query": "数学", "top_k": 10},
        {"query": "计算机", "top_k": 10},
        {"query": "测试", "top_k": 10},
        {"query": "文档", "top_k": 10},
        {"query": "内容", "top_k": 10},
        {"query": "教程", "top_k": 10}
    ]
    
    for i, search_data in enumerate(test_queries, 1):
        print(f"\n{i}. 搜索: '{search_data['query']}'")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{BASE_URL}/teacher-knowledge/semantic-search",
                headers=headers,
                json=search_data,
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ 成功，结果数: {len(results)}")
                
                if results:
                    print("搜索结果:")
                    for j, result in enumerate(results, 1):
                        similarity = result.get('similarity', 0)
                        title = result.get('title', 'N/A')
                        content_preview = result.get('content', '')[:100]
                        
                        print(f"  {j}. {title}")
                        print(f"     相似度: {similarity:.4f}")
                        print(f"     内容: {content_preview}...")
                        print()
                else:
                    print("  ⚠️ 没有找到结果")
                    
            else:
                print(f"❌ 失败: {response.status_code}")
                print(f"   错误: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    test_semantic_search()

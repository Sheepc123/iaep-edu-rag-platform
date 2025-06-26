"""
测试知识库全文搜索功能
"""
import requests
import json
from datetime import datetime

def test_search_functionality():
    """测试搜索功能"""
    
    print("🔍 测试知识库全文搜索功能...")
    
    # 1. 登录获取token
    print("\n1. 用户登录...")
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
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return
    
    # 2. 获取当前文档列表
    print("\n2. 获取当前文档列表...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/teacher-knowledge/documents", headers=headers)
        if response.status_code == 200:
            docs_data = response.json()
            total_docs = docs_data['total']
            print(f"✅ 当前知识库有 {total_docs} 个文档")
            
            if total_docs == 0:
                print("⚠️  知识库为空，建议先上传一些文档进行测试")
                return
            
            # 显示前几个文档的信息
            for i, doc in enumerate(docs_data['documents'][:3]):
                print(f"  {i+1}. {doc['title']} ({doc['category']})")
                if doc.get('summary'):
                    print(f"     摘要: {doc['summary'][:50]}...")
                    
        else:
            print(f"❌ 获取文档列表失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 获取文档列表异常: {e}")
        return
    
    # 3. 测试基本搜索功能
    print("\n3. 测试基本搜索功能...")
    
    # 测试用例
    search_tests = [
        {"query": "测试", "description": "搜索'测试'关键词"},
        {"query": "文档", "description": "搜索'文档'关键词"},
        {"query": "教学", "description": "搜索'教学'关键词"},
        {"query": "课程", "description": "搜索'课程'关键词"},
        {"query": "学习", "description": "搜索'学习'关键词"},
    ]
    
    for test in search_tests:
        try:
            search_data = {
                "query": test["query"],
                "limit": 5
            }
            
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/teacher-knowledge/search",
                headers=headers,
                json=search_data
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ {test['description']}: 找到 {len(results)} 个结果")
                
                for i, result in enumerate(results[:2]):  # 只显示前2个结果
                    score = result.get('relevance_score', 'N/A')
                    print(f"   {i+1}. {result['title']} (相关度: {score})")
                    
            else:
                print(f"❌ {test['description']} 失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ {test['description']} 异常: {e}")
    
    # 4. 测试空搜索和特殊字符
    print("\n4. 测试边界情况...")
    
    edge_cases = [
        {"query": "", "description": "空搜索"},
        {"query": "   ", "description": "空白搜索"},
        {"query": "不存在的关键词xyz123", "description": "不存在的关键词"},
        {"query": "a", "description": "单字符搜索"},
        {"query": "测试 AND 文档", "description": "布尔搜索(如果支持)"},
    ]
    
    for test in edge_cases:
        try:
            search_data = {
                "query": test["query"],
                "limit": 3
            }
            
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/teacher-knowledge/search",
                headers=headers,
                json=search_data
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ {test['description']}: 找到 {len(results)} 个结果")
            elif response.status_code == 400:
                print(f"⚠️  {test['description']}: 请求被拒绝 (预期行为)")
            else:
                print(f"❌ {test['description']} 失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {test['description']} 异常: {e}")
    
    # 5. 测试搜索性能
    print("\n5. 测试搜索性能...")
    
    try:
        import time
        
        search_data = {
            "query": "测试",
            "limit": 10
        }
        
        # 执行多次搜索测试性能
        times = []
        for i in range(5):
            start_time = time.time()
            
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/teacher-knowledge/search",
                headers=headers,
                json=search_data
            )
            
            end_time = time.time()
            search_time = (end_time - start_time) * 1000  # 转换为毫秒
            times.append(search_time)
            
            if response.status_code == 200:
                results = response.json()
                print(f"  第{i+1}次搜索: {search_time:.2f}ms, 结果数: {len(results)}")
            else:
                print(f"  第{i+1}次搜索失败: {response.status_code}")
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"✅ 平均搜索时间: {avg_time:.2f}ms")
            
            if avg_time < 100:
                print("🚀 搜索性能优秀 (<100ms)")
            elif avg_time < 500:
                print("👍 搜索性能良好 (<500ms)")
            else:
                print("⚠️  搜索性能需要优化 (>500ms)")
                
    except Exception as e:
        print(f"❌ 性能测试异常: {e}")
    
    # 6. 测试FTS5特性
    print("\n6. 测试FTS5高级特性...")
    
    fts5_tests = [
        {"query": "测试*", "description": "前缀搜索"},
        {"query": '"测试文档"', "description": "短语搜索"},
        {"query": "测试 OR 文档", "description": "OR搜索"},
    ]
    
    for test in fts5_tests:
        try:
            search_data = {
                "query": test["query"],
                "limit": 3
            }
            
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/teacher-knowledge/search",
                headers=headers,
                json=search_data
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ {test['description']}: 找到 {len(results)} 个结果")
            else:
                print(f"⚠️  {test['description']}: {response.status_code} (可能不支持)")
                
        except Exception as e:
            print(f"❌ {test['description']} 异常: {e}")
    
    print("\n🎉 全文搜索功能测试完成!")
    
    print("\n📊 测试总结:")
    print("1. 基本搜索功能是否正常")
    print("2. 边界情况处理是否合理")
    print("3. 搜索性能是否满足要求")
    print("4. FTS5高级特性支持情况")
    
    print("\n💡 优化建议:")
    print("- 如果搜索结果为空，检查FTS5表是否正确同步")
    print("- 如果性能较慢，考虑添加索引优化")
    print("- 可以添加搜索结果高亮显示")
    print("- 考虑添加搜索历史和热门搜索功能")

if __name__ == "__main__":
    test_search_functionality()

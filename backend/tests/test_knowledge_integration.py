"""
测试知识库系统集成
"""
import os
import sys
import requests
import json
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_knowledge_integration():
    """测试知识库系统集成"""
    print("🧪 测试知识库系统集成...")
    
    # API基础URL
    base_url = "http://localhost:8000/api/v1/teacher-knowledge"
    
    # 测试用户登录信息（需要根据实际情况调整）
    login_url = "http://localhost:8000/api/v1/auth/login"
    
    print("\n1. 测试用户登录...")
    
    # 这里需要根据实际的用户系统调整
    login_data = {
        "username": "teacher123",
        "password": "123456"
    }
    
    try:
        # 尝试登录获取token
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ 用户登录成功")
        else:
            print("⚠️  用户登录失败，使用模拟token")
            headers = {"Authorization": "Bearer test_token"}
    except Exception as e:
        print(f"⚠️  登录请求失败: {e}")
        print("使用模拟token进行测试")
        headers = {"Authorization": "Bearer test_token"}
    
    # 2. 测试向量统计API
    print("\n2. 测试向量统计API...")
    try:
        response = requests.get(f"{base_url}/vector-stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("✅ 向量统计API调用成功")
            print(f"   向量服务可用: {stats.get('available', False)}")
            if stats.get('available'):
                vector_stats = stats.get('stats', {})
                print(f"   总向量数: {vector_stats.get('total_vectors', 0)}")
                print(f"   嵌入模型: {vector_stats.get('embedding_model', 'N/A')}")
                print(f"   增强方式: {vector_stats.get('enhancement', 'N/A')}")
        else:
            print(f"❌ 向量统计API调用失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 向量统计API请求异常: {e}")
    
    # 3. 测试语义搜索API
    print("\n3. 测试语义搜索API...")
    
    search_queries = [
        {
            "query": "机器学习",
            "top_k": 3,
            "category": None
        },
        {
            "query": "Python编程",
            "top_k": 2,
            "category": None
        },
        {
            "query": "人工智能算法",
            "top_k": 5,
            "category": None
        }
    ]
    
    for search_request in search_queries:
        try:
            print(f"\n🔍 搜索: '{search_request['query']}'")
            
            response = requests.post(
                f"{base_url}/semantic-search",
                headers=headers,
                json=search_request
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ 搜索成功，找到 {len(results)} 个结果")
                
                for i, result in enumerate(results, 1):
                    print(f"   {i}. {result['title']} (相似度: {result['similarity']:.3f})")
                    print(f"      分类: {result.get('category', 'N/A')}")
                    print(f"      增强: {result.get('enhanced_by', 'N/A')}")
                    print(f"      内容: {result['content'][:50]}...")
                    
            elif response.status_code == 503:
                print("⚠️  语义搜索服务不可用")
                print(f"   错误信息: {response.json().get('detail', 'N/A')}")
            else:
                print(f"❌ 搜索失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ 搜索请求异常: {e}")
    
    # 4. 测试文档列表API
    print("\n4. 测试文档列表API...")
    try:
        response = requests.get(f"{base_url}/documents", headers=headers)
        if response.status_code == 200:
            docs_data = response.json()
            total_docs = docs_data.get('total', 0)
            documents = docs_data.get('documents', [])
            
            print(f"✅ 文档列表获取成功，共 {total_docs} 个文档")
            
            if documents:
                print("   最近的文档:")
                for doc in documents[:3]:  # 显示前3个文档
                    print(f"   - {doc['title']} ({doc.get('category', 'N/A')})")
            else:
                print("   暂无文档")
        else:
            print(f"❌ 文档列表获取失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 文档列表请求异常: {e}")
    
    # 5. 测试知识库统计API
    print("\n5. 测试知识库统计API...")
    try:
        response = requests.get(f"{base_url}/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("✅ 知识库统计获取成功")
            print(f"   总文档数: {stats.get('total_documents', 0)}")
            print(f"   总大小: {stats.get('total_size', 0)} 字节")
            print(f"   本月上传: {stats.get('this_month_uploads', 0)}")
            
            category_stats = stats.get('category_stats', {})
            if category_stats:
                print("   分类统计:")
                for category, stat in category_stats.items():
                    print(f"     {category}: {stat['count']} 个文档")
        else:
            print(f"❌ 知识库统计获取失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 知识库统计请求异常: {e}")

def test_direct_vector_service():
    """直接测试向量服务"""
    print("\n6. 直接测试向量服务...")
    
    try:
        from app.services.vector_service_deepseek import get_deepseek_vector_service
        
        vector_service = get_deepseek_vector_service()
        
        if vector_service.is_available():
            print("✅ 向量服务直接访问成功")
            
            # 获取统计信息
            stats = vector_service.get_collection_stats()
            print(f"   集合名称: {stats.get('collection_name', 'N/A')}")
            print(f"   总向量数: {stats.get('total_vectors', 0)}")
            print(f"   向量维度: {stats.get('embedding_dimension', 'N/A')}")
            
            # 测试搜索
            if stats.get('total_vectors', 0) > 0:
                print("\n   测试直接搜索:")
                results = vector_service.search_similar("测试查询", top_k=2)
                print(f"   搜索结果数: {len(results)}")
                
                for result in results:
                    title = result["metadata"].get("title", "未知")
                    similarity = result["similarity"]
                    print(f"     - {title} (相似度: {similarity:.3f})")
            else:
                print("   向量集合为空，无法测试搜索")
        else:
            print("❌ 向量服务不可用")
            print("   可能的原因:")
            print("   - DeepSeek API Key未设置")
            print("   - 网络连接问题")
            print("   - 依赖包未安装")
            
    except ImportError as e:
        print(f"❌ 向量服务导入失败: {e}")
    except Exception as e:
        print(f"❌ 向量服务测试异常: {e}")

def main():
    """主测试函数"""
    print("🚀 开始知识库系统集成测试...")
    
    print("\n📋 测试说明:")
    print("1. 测试向量统计API")
    print("2. 测试语义搜索API")
    print("3. 测试文档列表API")
    print("4. 测试知识库统计API")
    print("5. 直接测试向量服务")
    
    # 检查服务是否运行
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("\n✅ 后端服务运行正常")
        else:
            print(f"\n⚠️  后端服务状态异常: {response.status_code}")
    except Exception as e:
        print(f"\n❌ 无法连接到后端服务: {e}")
        print("请确保后端服务已启动 (python -m uvicorn app.main:app --reload)")
    
    # 执行API测试
    test_knowledge_integration()
    
    # 执行直接服务测试
    test_direct_vector_service()
    
    print("\n🎯 集成测试总结:")
    print("1. 检查API端点是否正常响应")
    print("2. 验证向量服务是否正确集成")
    print("3. 确认语义搜索功能是否工作")
    print("4. 测试数据访问权限控制")
    
    print("\n🚀 下一步:")
    print("1. 上传测试文档验证向量化")
    print("2. 测试前端集成")
    print("3. 性能优化和监控")

if __name__ == "__main__":
    main()

"""
测试向量数据库服务
"""
import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vector_service():
    """测试向量服务"""
    print("🧪 测试向量数据库服务...")
    
    # 1. 测试依赖导入
    print("\n1. 测试依赖导入...")
    try:
        from app.services.vector_service import get_vector_service
        print("✅ 向量服务导入成功")
    except ImportError as e:
        print(f"❌ 向量服务导入失败: {e}")
        print("💡 请先运行: python install_vector_deps.py")
        return
    
    # 2. 初始化向量服务
    print("\n2. 初始化向量服务...")
    vector_service = get_vector_service()
    
    if not vector_service.is_available():
        print("❌ 向量服务不可用")
        print("💡 可能的原因:")
        print("   - 依赖包未正确安装")
        print("   - 模型下载失败")
        print("   - 配置错误")
        return
    
    print("✅ 向量服务初始化成功")
    
    # 3. 测试文档添加
    print("\n3. 测试文档添加...")
    test_docs = [
        {
            "id": 1,
            "title": "Python编程基础",
            "content": "Python是一种高级编程语言，具有简洁的语法和强大的功能。它广泛应用于Web开发、数据科学、人工智能等领域。Python的设计哲学强调代码的可读性和简洁性。",
            "metadata": {"category": "编程", "language": "中文"}
        },
        {
            "id": 2, 
            "title": "机器学习入门",
            "content": "机器学习是人工智能的一个重要分支，它使计算机能够在没有明确编程的情况下学习和改进。常见的机器学习算法包括线性回归、决策树、神经网络等。",
            "metadata": {"category": "AI", "language": "中文"}
        },
        {
            "id": 3,
            "title": "Database Design",
            "content": "Database design is the process of creating a detailed data model of a database. It involves defining tables, relationships, constraints, and indexes to ensure data integrity and optimal performance.",
            "metadata": {"category": "数据库", "language": "英文"}
        }
    ]
    
    for doc in test_docs:
        success = vector_service.add_document(
            doc_id=doc["id"],
            title=doc["title"], 
            content=doc["content"],
            metadata=doc["metadata"]
        )
        
        if success:
            print(f"✅ 文档 '{doc['title']}' 添加成功")
        else:
            print(f"❌ 文档 '{doc['title']}' 添加失败")
    
    # 4. 测试语义搜索
    print("\n4. 测试语义搜索...")
    
    search_queries = [
        "Python编程",
        "人工智能算法", 
        "数据库设计",
        "machine learning",
        "编程语言"
    ]
    
    for query in search_queries:
        print(f"\n🔍 搜索: '{query}'")
        start_time = time.time()
        
        results = vector_service.search_similar(query, top_k=3)
        
        search_time = (time.time() - start_time) * 1000
        print(f"⏱️  搜索耗时: {search_time:.2f}ms")
        
        if results:
            print(f"📊 找到 {len(results)} 个相关结果:")
            for i, result in enumerate(results, 1):
                similarity = result["similarity"]
                title = result["metadata"].get("title", "未知标题")
                content_preview = result["content"][:50] + "..." if len(result["content"]) > 50 else result["content"]
                
                print(f"   {i}. {title} (相似度: {similarity:.3f})")
                print(f"      内容: {content_preview}")
        else:
            print("❌ 没有找到相关结果")
    
    # 5. 测试元数据过滤
    print("\n5. 测试元数据过滤...")
    
    # 只搜索中文文档
    results = vector_service.search_similar(
        "编程", 
        top_k=5,
        filter_metadata={"language": "中文"}
    )
    
    print(f"🔍 搜索中文文档 '编程': 找到 {len(results)} 个结果")
    for result in results:
        title = result["metadata"].get("title", "未知标题")
        language = result["metadata"].get("language", "未知")
        print(f"   - {title} ({language})")
    
    # 6. 测试统计信息
    print("\n6. 测试统计信息...")
    stats = vector_service.get_collection_stats()
    
    if stats.get("available"):
        print("✅ 向量集合统计:")
        print(f"   - 总向量数: {stats.get('total_vectors', 0)}")
        print(f"   - 集合名称: {stats.get('collection_name', 'N/A')}")
        print(f"   - 嵌入模型: {stats.get('embedding_model', 'N/A')}")
        print(f"   - 向量维度: {stats.get('embedding_dimension', 'N/A')}")
    else:
        print("❌ 无法获取统计信息")
    
    # 7. 测试文档删除
    print("\n7. 测试文档删除...")
    
    # 删除第一个测试文档
    success = vector_service.delete_document(1)
    if success:
        print("✅ 文档删除成功")
        
        # 验证删除效果
        results = vector_service.search_similar("Python编程", top_k=5)
        print(f"🔍 删除后搜索 'Python编程': 找到 {len(results)} 个结果")
    else:
        print("❌ 文档删除失败")
    
    print("\n🎉 向量数据库服务测试完成!")
    
    # 8. 性能建议
    print("\n💡 性能建议:")
    print("1. 首次运行会下载嵌入模型，可能需要较长时间")
    print("2. 建议在生产环境中使用GPU加速")
    print("3. 可以考虑使用更大的嵌入模型提高搜索质量")
    print("4. 定期备份向量数据库")

if __name__ == "__main__":
    test_vector_service()

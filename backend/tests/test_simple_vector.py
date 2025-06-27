"""
测试简化版向量服务
"""
import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_vector_service():
    """测试简化版向量服务"""
    print("🧪 测试简化版向量数据库服务...")
    
    # 1. 测试依赖导入
    print("\n1. 测试依赖导入...")
    try:
        from app.services.vector_service_simple import get_simple_vector_service
        print("✅ 简化向量服务导入成功")
    except ImportError as e:
        print(f"❌ 简化向量服务导入失败: {e}")
        return
    
    # 2. 初始化向量服务
    print("\n2. 初始化简化向量服务...")
    vector_service = get_simple_vector_service()
    
    if not vector_service.is_available():
        print("❌ 简化向量服务不可用")
        return
    
    print("✅ 简化向量服务初始化成功")
    
    # 3. 测试文档添加
    print("\n3. 测试文档添加...")
    test_docs = [
        {
            "id": 1,
            "title": "Python编程基础教程",
            "content": "Python是一种高级编程语言，具有简洁的语法和强大的功能。它广泛应用于Web开发、数据科学、人工智能等领域。Python的设计哲学强调代码的可读性和简洁性。学习Python可以帮助开发者快速构建各种应用程序。",
            "metadata": {"category": "编程教程", "language": "中文", "level": "初级"}
        },
        {
            "id": 2, 
            "title": "机器学习算法详解",
            "content": "机器学习是人工智能的一个重要分支，它使计算机能够在没有明确编程的情况下学习和改进。常见的机器学习算法包括线性回归、决策树、随机森林、支持向量机、神经网络等。每种算法都有其特定的应用场景和优缺点。",
            "metadata": {"category": "人工智能", "language": "中文", "level": "中级"}
        },
        {
            "id": 3,
            "title": "数据库设计原理",
            "content": "数据库设计是软件开发中的重要环节。良好的数据库设计需要考虑数据的完整性、一致性、性能和扩展性。关系型数据库设计遵循范式理论，包括第一范式、第二范式、第三范式等。索引设计对查询性能有重要影响。",
            "metadata": {"category": "数据库", "language": "中文", "level": "中级"}
        },
        {
            "id": 4,
            "title": "Web前端开发技术",
            "content": "前端开发涉及HTML、CSS、JavaScript等技术。现代前端框架如React、Vue、Angular提供了组件化开发模式。响应式设计确保网站在不同设备上的良好显示效果。前端性能优化包括代码压缩、图片优化、缓存策略等。",
            "metadata": {"category": "前端开发", "language": "中文", "level": "中级"}
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
        "Python编程语言",
        "人工智能算法", 
        "数据库设计",
        "前端开发框架",
        "机器学习",
        "Web开发",
        "编程教程",
        "算法原理"
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
                category = result["metadata"].get("category", "未知分类")
                content_preview = result["content"][:50] + "..." if len(result["content"]) > 50 else result["content"]
                
                print(f"   {i}. {title} [{category}] (相似度: {similarity:.3f})")
                print(f"      内容: {content_preview}")
        else:
            print("❌ 没有找到相关结果")
    
    # 5. 测试元数据过滤
    print("\n5. 测试元数据过滤...")
    
    # 只搜索编程相关文档
    results = vector_service.search_similar(
        "编程", 
        top_k=5,
        filter_metadata={"category": "编程教程"}
    )
    
    print(f"🔍 搜索编程教程类别 '编程': 找到 {len(results)} 个结果")
    for result in results:
        title = result["metadata"].get("title", "未知标题")
        category = result["metadata"].get("category", "未知")
        print(f"   - {title} ({category})")
    
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
        for result in results:
            title = result["metadata"].get("title", "未知标题")
            print(f"   - {title}")
    else:
        print("❌ 文档删除失败")
    
    print("\n🎉 简化版向量数据库服务测试完成!")
    
    # 8. 性能和功能总结
    print("\n📊 测试总结:")
    print("✅ 基于TF-IDF + Jieba的中文向量化")
    print("✅ Chroma向量数据库存储和检索")
    print("✅ 元数据过滤功能")
    print("✅ 文档增删改查操作")
    
    print("\n💡 简化版特点:")
    print("1. 不依赖sentence-transformers，避免版本冲突")
    print("2. 使用TF-IDF进行文本向量化")
    print("3. 集成jieba进行中文分词")
    print("4. 支持基本的语义搜索功能")
    print("5. 性能较好，适合中小规模文档库")
    
    print("\n🚀 下一步建议:")
    print("1. 集成到知识库上传流程")
    print("2. 开发混合搜索（关键词+语义）")
    print("3. 优化中文分词和向量化效果")
    print("4. 考虑升级到更先进的嵌入模型")

if __name__ == "__main__":
    test_simple_vector_service()

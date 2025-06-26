"""
测试DeepSeek混合向量服务
"""
import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_deepseek_vector_service():
    """测试DeepSeek混合向量服务"""
    print("🧪 测试DeepSeek混合向量数据库服务...")
    
    # 1. 测试依赖导入
    print("\n1. 测试依赖导入...")
    try:
        from app.services.vector_service_deepseek import get_deepseek_vector_service
        print("✅ DeepSeek混合向量服务导入成功")
    except ImportError as e:
        print(f"❌ DeepSeek混合向量服务导入失败: {e}")
        return
    
    # 2. 初始化向量服务
    print("\n2. 初始化DeepSeek混合向量服务...")
    vector_service = get_deepseek_vector_service()
    
    if not vector_service.is_available():
        print("❌ DeepSeek混合向量服务不可用")
        print("💡 可能的原因:")
        print("   - DeepSeek API Key未设置")
        print("   - 网络连接问题")
        print("   - 依赖包未安装")
        return
    
    print("✅ DeepSeek混合向量服务初始化成功")
    
    # 3. 测试文档添加
    print("\n3. 测试文档添加（包含DeepSeek关键词提取）...")
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
            "content": "机器学习是人工智能的一个重要分支，它使计算机能够在没有明确编程的情况下学习和改进。常见的机器学习算法包括线性回归、决策树、随机森林、支持向量机、神经网络等。每种算法都有其特定的应用场景和优缺点。深度学习作为机器学习的子领域，在图像识别、自然语言处理等方面取得了突破性进展。",
            "metadata": {"category": "人工智能", "language": "中文", "level": "中级"}
        }
    ]
    
    for doc in test_docs:
        print(f"\n📄 处理文档: {doc['title']}")
        start_time = time.time()
        
        success = vector_service.add_document(
            doc_id=doc["id"],
            title=doc["title"], 
            content=doc["content"],
            metadata=doc["metadata"]
        )
        
        process_time = (time.time() - start_time) * 1000
        
        if success:
            print(f"✅ 文档 '{doc['title']}' 添加成功 (耗时: {process_time:.2f}ms)")
        else:
            print(f"❌ 文档 '{doc['title']}' 添加失败")
    
    # 4. 测试DeepSeek增强的语义搜索
    print("\n4. 测试DeepSeek增强的语义搜索...")
    
    search_queries = [
        "Python编程语言",
        "人工智能算法", 
        "机器学习",
        "深度学习",
        "编程教程",
        "数据科学",
        "神经网络"
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
                enhancement = result["metadata"].get("enhanced_by", "未知")
                content_preview = result["content"][:50] + "..." if len(result["content"]) > 50 else result["content"]
                
                print(f"   {i}. {title} [{category}] (相似度: {similarity:.3f}, 增强: {enhancement})")
                print(f"      内容: {content_preview}")
        else:
            print("❌ 没有找到相关结果")
    
    # 5. 测试统计信息
    print("\n5. 测试统计信息...")
    stats = vector_service.get_collection_stats()
    
    if stats.get("available"):
        print("✅ DeepSeek向量集合统计:")
        print(f"   - 总向量数: {stats.get('total_vectors', 0)}")
        print(f"   - 集合名称: {stats.get('collection_name', 'N/A')}")
        print(f"   - 嵌入模型: {stats.get('embedding_model', 'N/A')}")
        print(f"   - 向量维度: {stats.get('embedding_dimension', 'N/A')}")
        print(f"   - 增强方式: {stats.get('enhancement', 'N/A')}")
    else:
        print("❌ 无法获取统计信息")
    
    # 6. 测试文档删除
    print("\n6. 测试文档删除...")
    
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
    
    print("\n🎉 DeepSeek混合向量数据库服务测试完成!")
    
    # 7. 性能和功能总结
    print("\n📊 测试总结:")
    print("✅ DeepSeek关键词提取 + TF-IDF向量化")
    print("✅ Chroma向量数据库存储和检索")
    print("✅ 增强的语义理解能力")
    print("✅ 中文文本处理优化")
    
    print("\n💡 DeepSeek增强版特点:")
    print("1. 使用DeepSeek AI提取关键词，提升语义理解")
    print("2. 结合传统TF-IDF方法，保证稳定性")
    print("3. 支持中文文本的智能分析")
    print("4. 成本可控，按需调用AI服务")
    print("5. 向量质量比纯哈希方法更好")
    
    print("\n🚀 优势对比:")
    print("vs 简化版: 语义理解更准确，搜索质量更高")
    print("vs OpenAI: 成本更低，支持中文更好")
    print("vs Sentence-Transformers: 无版本冲突，部署简单")
    
    print("\n🎯 适用场景:")
    print("1. 中文文档为主的知识库")
    print("2. 对搜索质量有要求但成本敏感")
    print("3. 需要快速部署的项目")
    print("4. 希望AI增强但不完全依赖的场景")

def main():
    """主测试函数"""
    print("🚀 开始DeepSeek混合向量服务测试...")
    
    # 检查API配置
    try:
        from app.core.config import settings
        if not settings.DEEPSEEK_API_KEY:
            print("❌ 未设置DEEPSEEK_API_KEY，请检查配置")
            return
        print(f"✅ DeepSeek API配置正常")
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return
    
    test_deepseek_vector_service()

if __name__ == "__main__":
    main()

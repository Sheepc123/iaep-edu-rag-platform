"""
测试向量修复
"""
import os
import sys
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vector_fix():
    """测试向量修复"""
    print("🔧 测试向量修复...")
    
    try:
        from app.services.vector_service_deepseek import get_deepseek_vector_service
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return
    
    vector_service = get_deepseek_vector_service()
    
    if not vector_service.is_available():
        print("❌ 向量服务不可用")
        return
    
    print("✅ 向量服务可用")
    
    # 1. 测试哈希向量归一化
    print("\n1. 测试哈希向量归一化...")
    
    test_texts = ["机器学习", "Python编程", "人工智能"]
    
    for text in test_texts:
        hash_vector = vector_service._get_hash_embedding(text)
        norm = np.linalg.norm(hash_vector)
        print(f"文本: '{text}'")
        print(f"  向量维度: {len(hash_vector)}")
        print(f"  向量模长: {norm:.6f}")
        print(f"  向量范围: [{min(hash_vector):.3f}, {max(hash_vector):.3f}]")
        print(f"  是否归一化: {'✅' if abs(norm - 1.0) < 0.001 else '❌'}")
    
    # 2. 重新添加一个测试文档
    print("\n2. 重新添加测试文档...")
    
    # 先清空集合
    try:
        vector_service.collection.delete(where={})
        print("✅ 清空现有数据")
    except:
        print("⚠️  清空数据失败或集合为空")
    
    # 添加测试文档
    test_doc = {
        "id": 100,
        "title": "测试文档",
        "content": "这是一个关于机器学习和人工智能的测试文档。它包含了深度学习、神经网络等关键词。",
        "metadata": {"category": "测试", "language": "中文"}
    }
    
    success = vector_service.add_document(
        doc_id=test_doc["id"],
        title=test_doc["title"],
        content=test_doc["content"],
        metadata=test_doc["metadata"]
    )
    
    if success:
        print("✅ 测试文档添加成功")
    else:
        print("❌ 测试文档添加失败")
        return
    
    # 3. 检查存储的向量
    print("\n3. 检查存储的向量...")
    
    try:
        all_data = vector_service.collection.get(include=['embeddings', 'documents', 'metadatas'])
        
        if len(all_data['ids']) > 0:
            embedding = all_data['embeddings'][0] if all_data['embeddings'] else None
            
            if embedding:
                norm = np.linalg.norm(embedding)
                print(f"存储的向量维度: {len(embedding)}")
                print(f"存储的向量模长: {norm:.6f}")
                print(f"存储的向量范围: [{min(embedding):.3f}, {max(embedding):.3f}]")
                print(f"存储向量是否归一化: {'✅' if abs(norm - 1.0) < 0.001 else '❌'}")
            else:
                print("❌ 没有获取到存储的向量")
        else:
            print("❌ 集合中没有文档")
    
    except Exception as e:
        print(f"❌ 检查存储向量失败: {e}")
    
    # 4. 测试搜索
    print("\n4. 测试搜索...")
    
    test_queries = ["机器学习", "人工智能", "深度学习"]
    
    for query in test_queries:
        print(f"\n🔍 搜索: '{query}'")
        
        # 生成查询向量
        query_embedding = vector_service._get_hash_embedding(query)
        query_norm = np.linalg.norm(query_embedding)
        
        print(f"  查询向量模长: {query_norm:.6f}")
        print(f"  查询向量是否归一化: {'✅' if abs(query_norm - 1.0) < 0.001 else '❌'}")
        
        # 执行搜索
        try:
            results = vector_service.collection.query(
                query_embeddings=[query_embedding],
                n_results=1
            )
            
            if results['documents'] and results['documents'][0]:
                distance = results['distances'][0][0]
                similarity = 1 - distance
                
                print(f"  距离: {distance:.6f}")
                print(f"  相似度: {similarity:.6f}")
                print(f"  是否合理: {'✅' if 0 <= distance <= 2 else '❌'}")
                
                # 使用我们的搜索方法
                formatted_results = vector_service.search_similar(query, top_k=1)
                print(f"  格式化结果数: {len(formatted_results)}")
                
                if formatted_results:
                    result = formatted_results[0]
                    print(f"  最终相似度: {result['similarity']:.6f}")
                    print(f"  内容: {result['content'][:30]}...")
            else:
                print("  ❌ 没有搜索结果")
                
        except Exception as e:
            print(f"  ❌ 搜索失败: {e}")
    
    print("\n🎯 修复测试总结:")
    print("1. 哈希向量归一化是否正确")
    print("2. 存储向量是否正确")
    print("3. 搜索距离是否合理")
    print("4. 相似度计算是否正确")

if __name__ == "__main__":
    test_vector_fix()

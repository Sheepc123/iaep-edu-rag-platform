"""
调试向量搜索问题
"""
import os
import sys
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_vector_search():
    """调试向量搜索问题"""
    print("🔍 调试向量搜索问题...")
    
    try:
        from app.services.vector_service_deepseek import get_deepseek_vector_service
        import chromadb
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return
    
    vector_service = get_deepseek_vector_service()
    
    if not vector_service.is_available():
        print("❌ 向量服务不可用")
        return
    
    print("✅ 向量服务可用")
    
    # 1. 检查集合中的数据
    print("\n1. 检查集合中的数据...")
    try:
        collection = vector_service.collection
        
        # 获取所有数据
        all_data = collection.get()
        
        print(f"集合中的文档数: {len(all_data['ids'])}")
        
        for i, doc_id in enumerate(all_data['ids']):
            metadata = all_data['metadatas'][i]
            document = all_data['documents'][i]
            embedding = all_data['embeddings'][i] if all_data['embeddings'] else None
            
            print(f"\n文档 {i+1}:")
            print(f"  ID: {doc_id}")
            print(f"  标题: {metadata.get('title', 'N/A')}")
            print(f"  内容: {document[:50]}...")
            print(f"  向量维度: {len(embedding) if embedding else 'N/A'}")
            if embedding:
                print(f"  向量范围: [{min(embedding):.3f}, {max(embedding):.3f}]")
                print(f"  向量模长: {np.linalg.norm(embedding):.3f}")
                print(f"  向量前5个值: {embedding[:5]}")
        
    except Exception as e:
        print(f"❌ 检查集合数据失败: {e}")
        return
    
    # 2. 测试查询向量生成
    print("\n2. 测试查询向量生成...")
    
    test_queries = ["机器学习", "Python", "编程"]
    
    for query in test_queries:
        try:
            print(f"\n查询: '{query}'")
            
            # 生成查询向量
            if len(query) <= 10:
                print("  使用短查询优化路径")
                if hasattr(vector_service.tfidf_vectorizer, 'vocabulary_'):
                    vector = vector_service.tfidf_vectorizer.transform([query])
                    dense_vector = vector.toarray()[0]
                    print(f"  TF-IDF向量维度: {len(dense_vector)}")
                    print(f"  TF-IDF向量非零元素: {np.count_nonzero(dense_vector)}")
                    
                    if len(dense_vector) == 384 and np.sum(dense_vector) > 0:
                        norm = np.linalg.norm(dense_vector)
                        if norm > 0:
                            dense_vector = dense_vector / norm
                        query_embedding = dense_vector.tolist()
                        print(f"  使用TF-IDF向量，模长: {np.linalg.norm(query_embedding):.3f}")
                    else:
                        query_embedding = vector_service._get_hash_embedding(query)
                        print(f"  使用哈希向量，模长: {np.linalg.norm(query_embedding):.3f}")
                else:
                    query_embedding = vector_service._get_hash_embedding(query)
                    print(f"  TF-IDF未训练，使用哈希向量")
            else:
                print("  使用DeepSeek增强路径")
                query_embedding = vector_service._get_enhanced_embedding(query)
            
            print(f"  查询向量维度: {len(query_embedding)}")
            print(f"  查询向量范围: [{min(query_embedding):.3f}, {max(query_embedding):.3f}]")
            print(f"  查询向量模长: {np.linalg.norm(query_embedding):.3f}")
            
        except Exception as e:
            print(f"  ❌ 查询向量生成失败: {e}")
    
    # 3. 手动计算相似度
    print("\n3. 手动计算相似度...")
    
    try:
        # 获取第一个文档的向量
        all_data = collection.get()
        if len(all_data['embeddings']) > 0:
            doc_embedding = all_data['embeddings'][0]
            doc_title = all_data['metadatas'][0].get('title', 'Unknown')
            
            print(f"文档: {doc_title}")
            print(f"文档向量维度: {len(doc_embedding)}")
            
            # 测试查询
            query = "机器学习"
            
            # 生成查询向量（简化版）
            query_embedding = vector_service._get_hash_embedding(query)
            
            print(f"查询: {query}")
            print(f"查询向量维度: {len(query_embedding)}")
            
            # 计算余弦相似度
            doc_vec = np.array(doc_embedding)
            query_vec = np.array(query_embedding)
            
            # 归一化
            doc_norm = np.linalg.norm(doc_vec)
            query_norm = np.linalg.norm(query_vec)
            
            if doc_norm > 0 and query_norm > 0:
                doc_vec_normalized = doc_vec / doc_norm
                query_vec_normalized = query_vec / query_norm
                
                # 余弦相似度
                cosine_similarity = np.dot(doc_vec_normalized, query_vec_normalized)
                
                print(f"余弦相似度: {cosine_similarity:.6f}")
                print(f"距离 (1-相似度): {1-cosine_similarity:.6f}")
                
                # 检查阈值
                threshold = 0.001
                print(f"阈值: {threshold}")
                print(f"是否通过阈值: {cosine_similarity >= threshold}")
                
            else:
                print("❌ 向量模长为0，无法计算相似度")
        
    except Exception as e:
        print(f"❌ 手动相似度计算失败: {e}")
    
    # 4. 直接测试Chroma查询
    print("\n4. 直接测试Chroma查询...")
    
    try:
        query = "机器学习"
        query_embedding = vector_service._get_hash_embedding(query)
        
        print(f"查询: {query}")
        print(f"查询向量维度: {len(query_embedding)}")
        
        # 直接调用Chroma查询
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        print(f"Chroma原始结果:")
        print(f"  文档数: {len(results['documents'][0]) if results['documents'] else 0}")
        
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                distance = results['distances'][0][i]
                similarity = 1 - distance
                doc_content = results['documents'][0][i][:50]
                
                print(f"  结果 {i+1}:")
                print(f"    距离: {distance:.6f}")
                print(f"    相似度: {similarity:.6f}")
                print(f"    内容: {doc_content}...")
                print(f"    是否通过阈值(0.001): {similarity >= 0.001}")
        
    except Exception as e:
        print(f"❌ 直接Chroma查询失败: {e}")
    
    print("\n🎯 调试总结:")
    print("1. 检查向量是否正确存储")
    print("2. 检查查询向量是否正确生成")
    print("3. 检查相似度计算是否正确")
    print("4. 检查阈值设置是否合理")

if __name__ == "__main__":
    debug_vector_search()

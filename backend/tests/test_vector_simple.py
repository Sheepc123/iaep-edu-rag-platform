"""
简化的向量数据库测试
"""
import os
import sys

def test_dependencies():
    """测试依赖导入"""
    print("🧪 测试向量数据库依赖...")
    
    dependencies = [
        ("chromadb", "Chroma向量数据库"),
        ("sentence_transformers", "Sentence Transformers"),
        ("numpy", "NumPy"),
        ("sklearn", "Scikit-learn"),
        ("jieba", "Jieba中文分词")
    ]
    
    success_count = 0
    failed_deps = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
            failed_deps.append((module, name, str(e)))
    
    print(f"\n📊 依赖测试结果: {success_count}/{len(dependencies)} 成功")
    
    if failed_deps:
        print(f"\n❌ 失败的依赖:")
        for module, name, error in failed_deps:
            print(f"   - {name} ({module}): {error}")
        
        print(f"\n💡 解决建议:")
        print(f"1. 运行安装脚本: python install_vector_deps.py")
        print(f"2. 手动安装失败的包:")
        for module, name, error in failed_deps:
            if "huggingface_hub" in error:
                print(f"   pip install huggingface-hub==0.17.3")
            else:
                print(f"   pip install {module}")
        
        return False
    
    return True

def test_basic_vector_operations():
    """测试基本向量操作"""
    print("\n🔧 测试基本向量操作...")
    
    try:
        import chromadb
        from chromadb.config import Settings
        import numpy as np
        
        # 创建临时客户端
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=None,
            anonymized_telemetry=False
        ))
        
        # 创建集合
        collection = client.create_collection(
            name="test_collection",
            metadata={"description": "测试集合"}
        )
        
        print("✅ Chroma客户端和集合创建成功")
        
        # 测试添加文档
        test_docs = [
            "这是一个关于Python编程的文档",
            "机器学习是人工智能的重要分支",
            "数据库设计需要考虑性能和扩展性"
        ]
        
        # 生成简单的向量（随机向量用于测试）
        embeddings = [np.random.rand(384).tolist() for _ in test_docs]
        
        collection.add(
            embeddings=embeddings,
            documents=test_docs,
            ids=[f"doc_{i}" for i in range(len(test_docs))]
        )
        
        print(f"✅ 添加 {len(test_docs)} 个测试文档成功")
        
        # 测试查询
        query_embedding = np.random.rand(384).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        print(f"✅ 查询测试成功，返回 {len(results['documents'][0])} 个结果")
        
        # 测试统计
        count = collection.count()
        print(f"✅ 集合统计成功，共 {count} 个文档")
        
        return True
        
    except Exception as e:
        print(f"❌ 向量操作测试失败: {e}")
        return False

def test_sentence_transformers():
    """测试Sentence Transformers"""
    print("\n🤖 测试Sentence Transformers...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # 使用较小的模型进行测试
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        print(f"📥 加载模型: {model_name}")
        print("⚠️  首次运行会下载模型，请耐心等待...")
        
        model = SentenceTransformer(model_name)
        print("✅ 模型加载成功")
        
        # 测试编码
        test_texts = [
            "这是一个测试句子",
            "Python是一种编程语言",
            "机器学习很有趣"
        ]
        
        embeddings = model.encode(test_texts)
        print(f"✅ 文本编码成功，向量维度: {embeddings.shape}")
        
        # 测试相似度计算
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarity_matrix = cosine_similarity(embeddings)
        print(f"✅ 相似度计算成功，矩阵形状: {similarity_matrix.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sentence Transformers测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始向量数据库简化测试...")
    
    # 1. 测试依赖
    if not test_dependencies():
        print("\n❌ 依赖测试失败，请先安装所需依赖")
        return
    
    # 2. 测试基本向量操作
    if not test_basic_vector_operations():
        print("\n❌ 基本向量操作测试失败")
        return
    
    # 3. 测试Sentence Transformers
    if not test_sentence_transformers():
        print("\n❌ Sentence Transformers测试失败")
        return
    
    print("\n🎉 所有测试通过!")
    print("\n📋 测试总结:")
    print("✅ 依赖导入正常")
    print("✅ Chroma向量数据库工作正常")
    print("✅ Sentence Transformers模型工作正常")
    print("✅ 向量操作功能正常")
    
    print("\n🚀 下一步:")
    print("1. 可以运行完整的向量服务测试")
    print("2. 集成向量化到知识库系统")
    print("3. 开发语义搜索API")

if __name__ == "__main__":
    main()

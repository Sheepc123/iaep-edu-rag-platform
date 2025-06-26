"""
重置向量数据库
"""
import os
import shutil

def reset_vector_db():
    """重置向量数据库"""
    print("🔄 重置向量数据库...")
    
    # 向量数据库目录
    chroma_dir = "data/chroma_db"
    
    if os.path.exists(chroma_dir):
        try:
            shutil.rmtree(chroma_dir)
            print(f"✅ 删除向量数据库目录: {chroma_dir}")
        except Exception as e:
            print(f"❌ 删除向量数据库目录失败: {e}")
            return False
    
    # 重新创建目录
    try:
        os.makedirs(chroma_dir, exist_ok=True)
        print(f"✅ 重新创建向量数据库目录: {chroma_dir}")
    except Exception as e:
        print(f"❌ 创建向量数据库目录失败: {e}")
        return False
    
    print("🎉 向量数据库重置完成!")
    return True

if __name__ == "__main__":
    reset_vector_db()

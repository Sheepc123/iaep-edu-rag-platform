#!/usr/bin/env python3
"""
简单检查向量数据库状态
"""
import os
import sqlite3

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    print("=" * 50)
    
    # 检查环境变量
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    print(f"DEEPSEEK_API_KEY: {'✅ 已设置' if deepseek_key else '❌ 未设置'}")
    
    if deepseek_key:
        print(f"  密钥长度: {len(deepseek_key)} 字符")
        print(f"  密钥前缀: {deepseek_key[:10]}...")
    
    print(f"DEEPSEEK_BASE_URL: {os.getenv('DEEPSEEK_BASE_URL', '未设置')}")
    print(f"DEEPSEEK_MODEL: {os.getenv('DEEPSEEK_MODEL', '未设置')}")

def check_database():
    """检查数据库中的文档"""
    print("\n📄 检查数据库文档...")
    print("=" * 50)
    
    db_path = 'data/database/education_platform.db'
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查文档数量
        cursor.execute("SELECT COUNT(*) FROM teacher_knowledge_docs WHERE status = 'active'")
        doc_count = cursor.fetchone()[0]
        print(f"活跃文档数量: {doc_count}")
        
        if doc_count > 0:
            # 检查文档详情
            cursor.execute("""
                SELECT id, title, category, file_type, 
                       LENGTH(text_content) as content_length,
                       upload_time
                FROM teacher_knowledge_docs 
                WHERE status = 'active'
                ORDER BY upload_time DESC
            """)
            docs = cursor.fetchall()
            
            print("\n文档详情:")
            for doc in docs:
                print(f"  ID: {doc[0]}")
                print(f"  标题: {doc[1]}")
                print(f"  分类: {doc[2]}")
                print(f"  类型: {doc[3]}")
                print(f"  内容长度: {doc[4]} 字符")
                print(f"  上传时间: {doc[5]}")
                print("  ---")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")

def check_vector_db():
    """检查向量数据库文件"""
    print("\n🗂️ 检查向量数据库文件...")
    print("=" * 50)
    
    vector_dirs = ['data/vector_db', 'data/chroma_db']
    
    for vector_dir in vector_dirs:
        if os.path.exists(vector_dir):
            print(f"📁 {vector_dir}:")
            files = os.listdir(vector_dir)
            if files:
                for file in files:
                    file_path = os.path.join(vector_dir, file)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        print(f"  - {file}: {size} bytes")
                    elif os.path.isdir(file_path):
                        sub_files = os.listdir(file_path)
                        print(f"  - {file}/ ({len(sub_files)} 文件)")
            else:
                print("  (空目录)")
        else:
            print(f"❌ {vector_dir} 不存在")

def check_dependencies():
    """检查Python依赖"""
    print("\n📦 检查Python依赖...")
    print("=" * 50)
    
    required_packages = [
        'chromadb',
        'sentence_transformers', 
        'sklearn',
        'jieba',
        'numpy',
        'requests'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (未安装)")

def main():
    """主函数"""
    print("🚀 向量数据库状态检查")
    print("=" * 50)
    
    check_environment()
    check_database()
    check_vector_db()
    check_dependencies()
    
    print("\n💡 解决建议:")
    print("=" * 50)
    
    # 检查是否有DeepSeek API密钥
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("1. 配置DeepSeek API密钥:")
        print("   export DEEPSEEK_API_KEY='your-api-key'")
        print("   或在.env文件中添加: DEEPSEEK_API_KEY=your-api-key")
    
    print("2. 如果有文档但没有向量数据，需要重新向量化:")
    print("   - 重新上传文档")
    print("   - 或运行向量化脚本")
    
    print("3. 检查网络连接和API服务状态")

if __name__ == "__main__":
    main()

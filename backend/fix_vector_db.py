#!/usr/bin/env python3
"""
修复向量数据库 - 手动向量化现有文档
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.knowledge_base import TeacherKnowledgeDoc
from app.services.vector_service_deepseek import get_deepseek_vector_service
from app.core.config import settings

def check_vector_service():
    """检查向量服务状态"""
    print("🔍 检查向量服务状态...")
    print("=" * 50)
    
    vector_service = get_deepseek_vector_service()
    
    # 1. 检查服务可用性
    is_available = vector_service.is_available()
    print(f"向量服务可用性: {'✅ 可用' if is_available else '❌ 不可用'}")
    
    # 2. 检查配置
    print(f"DeepSeek API Key: {'✅ 已配置' if settings.DEEPSEEK_API_KEY else '❌ 未配置'}")
    print(f"DeepSeek Base URL: {settings.DEEPSEEK_BASE_URL}")
    print(f"DeepSeek Model: {settings.DEEPSEEK_MODEL}")
    
    # 3. 检查向量统计
    if is_available:
        try:
            stats = vector_service.get_collection_stats()
            if stats.get("available"):
                print(f"向量集合统计:")
                print(f"  - 总向量数: {stats.get('total_vectors', 0)}")
                print(f"  - 集合名称: {stats.get('collection_name', 'N/A')}")
                print(f"  - 嵌入模型: {stats.get('embedding_model', 'N/A')}")
                print(f"  - 向量维度: {stats.get('embedding_dimension', 'N/A')}")
            else:
                print(f"❌ 无法获取向量统计: {stats.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ 获取向量统计失败: {e}")
    
    return vector_service, is_available

def get_unvectorized_documents(db: Session):
    """获取未向量化的文档"""
    print("\n📄 检查数据库中的文档...")
    
    # 获取所有活跃文档
    docs = db.query(TeacherKnowledgeDoc).filter(
        TeacherKnowledgeDoc.status == 'active'
    ).all()
    
    print(f"数据库中的文档总数: {len(docs)}")
    
    if docs:
        print("文档列表:")
        for doc in docs:
            print(f"  ID: {doc.id}")
            print(f"  标题: {doc.title}")
            print(f"  分类: {doc.category}")
            print(f"  文件类型: {doc.file_type}")
            print(f"  文件大小: {doc.file_size} bytes")
            print(f"  有文本内容: {'是' if doc.text_content else '否'}")
            print(f"  上传时间: {doc.upload_time}")
            print("  ---")
    
    return docs

def vectorize_document(vector_service, doc):
    """向量化单个文档"""
    print(f"\n🔄 向量化文档: {doc.title} (ID: {doc.id})")
    
    if not doc.text_content:
        print("  ⚠️ 文档没有文本内容，跳过向量化")
        return False
    
    try:
        # 准备元数据
        metadata = {
            "category": doc.category,
            "tags": doc.tags,
            "file_type": doc.file_type,
            "teacher_id": doc.teacher_id,
            "upload_time": doc.upload_time.isoformat() if doc.upload_time else None,
            "enhanced_by": "deepseek"
        }
        
        # 向量化
        success = vector_service.add_document(
            doc_id=doc.id,
            title=doc.title,
            content=doc.text_content,
            metadata=metadata
        )
        
        if success:
            print(f"  ✅ 向量化成功")
            return True
        else:
            print(f"  ❌ 向量化失败")
            return False
            
    except Exception as e:
        print(f"  ❌ 向量化异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 修复向量数据库")
    print("=" * 50)
    
    # 1. 检查向量服务
    vector_service, is_available = check_vector_service()
    
    if not is_available:
        print("\n❌ 向量服务不可用，无法继续")
        print("请检查:")
        print("1. DeepSeek API密钥是否正确配置")
        print("2. 网络连接是否正常")
        print("3. 依赖包是否正确安装")
        return
    
    # 2. 获取数据库会话
    db = next(get_db())
    
    try:
        # 3. 获取文档列表
        docs = get_unvectorized_documents(db)
        
        if not docs:
            print("\n✅ 没有需要向量化的文档")
            return
        
        # 4. 向量化文档
        print(f"\n🔄 开始向量化 {len(docs)} 个文档...")
        
        success_count = 0
        for doc in docs:
            if vectorize_document(vector_service, doc):
                success_count += 1
        
        print(f"\n📊 向量化完成:")
        print(f"  - 成功: {success_count}")
        print(f"  - 失败: {len(docs) - success_count}")
        print(f"  - 总计: {len(docs)}")
        
        # 5. 检查最终状态
        final_stats = vector_service.get_collection_stats()
        if final_stats.get("available"):
            print(f"\n✅ 最终向量数量: {final_stats.get('total_vectors', 0)}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()

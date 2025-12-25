#!/usr/bin/env python3
"""
重建向量数据库 - 使用改进的分块策略
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.knowledge_base import TeacherKnowledgeDoc
from app.services.vector_service_deepseek import get_deepseek_vector_service

def clear_vector_database():
    """清空向量数据库"""
    print("🗑️ 清空向量数据库...")
    
    vector_service = get_deepseek_vector_service()
    
    if not vector_service.is_available():
        print("❌ 向量服务不可用")
        return False
    
    try:
        # 删除现有集合
        if vector_service.collection:
            vector_service.client.delete_collection(vector_service.collection.name)
            print("✅ 已删除现有向量集合")
        
        # 重新初始化
        vector_service._initialize()
        print("✅ 重新初始化向量服务")
        return True
        
    except Exception as e:
        print(f"❌ 清空向量数据库失败: {e}")
        return False

def rebuild_document_vectors():
    """重建文档向量"""
    print("🔄 重建文档向量...")
    print("=" * 50)
    
    # 1. 清空向量数据库
    if not clear_vector_database():
        return
    
    # 2. 获取向量服务
    vector_service = get_deepseek_vector_service()
    
    # 3. 获取数据库会话
    db = next(get_db())
    
    try:
        # 4. 获取所有活跃文档
        docs = db.query(TeacherKnowledgeDoc).filter(
            TeacherKnowledgeDoc.status == 'active'
        ).all()
        
        print(f"📄 找到 {len(docs)} 个文档需要重新向量化")
        
        if not docs:
            print("⚠️ 没有文档需要处理")
            return
        
        # 5. 逐个处理文档
        success_count = 0
        for i, doc in enumerate(docs, 1):
            print(f"\n{i}/{len(docs)} 处理文档: {doc.title}")
            print("-" * 30)
            
            if not doc.text_content:
                print("  ⚠️ 文档没有文本内容，跳过")
                continue
            
            try:
                # 准备元数据
                metadata = {
                    "category": doc.category,
                    "tags": doc.tags or "",
                    "file_type": doc.file_type,
                    "teacher_id": doc.teacher_id,
                    "upload_time": doc.upload_time.isoformat() if doc.upload_time else None,
                    "enhanced_by": "deepseek_v2"
                }
                
                # 向量化文档
                success = vector_service.add_document(
                    doc_id=doc.id,
                    title=doc.title,
                    content=doc.text_content,
                    metadata=metadata
                )
                
                if success:
                    print(f"  ✅ 向量化成功")
                    success_count += 1
                else:
                    print(f"  ❌ 向量化失败")
                    
            except Exception as e:
                print(f"  ❌ 处理异常: {e}")
        
        # 6. 显示最终统计
        print(f"\n📊 重建完成:")
        print(f"  - 成功: {success_count}")
        print(f"  - 失败: {len(docs) - success_count}")
        print(f"  - 总计: {len(docs)}")
        
        # 7. 检查最终状态
        final_stats = vector_service.get_collection_stats()
        if final_stats.get("available"):
            print(f"\n✅ 最终向量数量: {final_stats.get('total_vectors', 0)}")
            print(f"   集合名称: {final_stats.get('collection_name', 'N/A')}")
            print(f"   嵌入模型: {final_stats.get('embedding_model', 'N/A')}")
        
        # 8. 测试搜索
        print(f"\n🧪 测试搜索功能...")
        test_queries = ["Python", "数学", "编程", "计算机", "云计算"]
        
        for query in test_queries:
            try:
                results = vector_service.search_similar(query, top_k=3)
                print(f"  '{query}': {len(results)} 个结果")
                if results:
                    for j, result in enumerate(results[:2], 1):
                        similarity = result.get('similarity', 0)
                        title = result.get('metadata', {}).get('title', 'N/A')
                        print(f"    {j}. {title} (相似度: {similarity:.3f})")
            except Exception as e:
                print(f"  '{query}': 搜索失败 - {e}")
        
    finally:
        db.close()

def main():
    """主函数"""
    print("🚀 重建向量数据库")
    print("=" * 50)
    
    # 检查向量服务
    vector_service = get_deepseek_vector_service()
    if not vector_service.is_available():
        print("❌ 向量服务不可用，请检查配置")
        return
    
    print("✅ 向量服务可用")
    
    # 显示当前配置
    config = vector_service.config
    print(f"📋 当前配置:")
    print(f"  - 分块大小: {config.CHUNK_SIZE} 字符")
    print(f"  - 分块重叠: {config.CHUNK_OVERLAP} 字符")
    print(f"  - 相似度阈值: {config.SIMILARITY_THRESHOLD}")
    print(f"  - 搜索结果数: {config.VECTOR_SEARCH_TOP_K}")
    
    # 确认操作
    confirm = input("\n⚠️ 这将删除现有的向量数据并重新构建，确定继续吗？(y/N): ")
    if confirm.lower() != 'y':
        print("❌ 操作已取消")
        return
    
    # 执行重建
    rebuild_document_vectors()
    
    print("\n🎉 重建完成！")
    print("现在可以测试语义搜索功能了。")

if __name__ == "__main__":
    main()

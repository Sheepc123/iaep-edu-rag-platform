#!/usr/bin/env python3
"""
检查数据库中的知识库文档
"""
import sqlite3
import os

def check_database():
    """检查数据库中的知识库文档"""
    db_path = 'data/database/education_platform.db'
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return
    
    print(f"📊 检查数据库: {db_path}")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 查看所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("数据库中的表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # 2. 检查知识库相关表
        knowledge_tables = [t[0] for t in tables if 'knowledge' in t[0].lower()]
        if knowledge_tables:
            print(f"\n📚 知识库相关表: {knowledge_tables}")
            
            for table_name in knowledge_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {table_name}: {count} 条记录")
                
                if count > 0:
                    # 显示表结构
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    print(f"    字段: {[col[1] for col in columns]}")
                    
                    # 显示前几条记录
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    records = cursor.fetchall()
                    print(f"    前3条记录:")
                    for i, record in enumerate(records):
                        print(f"      {i+1}. {record[:5]}...")  # 只显示前5个字段
        else:
            print("\n❌ 没有找到知识库相关表")
        
        # 3. 检查teacher_knowledge_documents表（如果存在）
        try:
            cursor.execute("SELECT COUNT(*) FROM teacher_knowledge_documents")
            doc_count = cursor.fetchone()[0]
            print(f"\n📄 知识库文档总数: {doc_count}")
            
            if doc_count > 0:
                cursor.execute("""
                    SELECT id, title, category, file_type, file_size, upload_time 
                    FROM teacher_knowledge_documents 
                    ORDER BY upload_time DESC 
                    LIMIT 5
                """)
                docs = cursor.fetchall()
                print("最近上传的文档:")
                for doc in docs:
                    print(f"  ID: {doc[0]}")
                    print(f"  标题: {doc[1]}")
                    print(f"  分类: {doc[2]}")
                    print(f"  类型: {doc[3]}")
                    print(f"  大小: {doc[4]} bytes")
                    print(f"  上传时间: {doc[5]}")
                    print("  ---")
        except sqlite3.OperationalError as e:
            print(f"\n⚠️ teacher_knowledge_documents表不存在或查询失败: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")

if __name__ == "__main__":
    check_database()

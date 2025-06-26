"""
检查FTS5表状态
"""
import sqlite3
import os

def check_fts5_status():
    """检查FTS5表状态"""
    
    print("🔍 检查FTS5表状态...")
    
    # 数据库文件路径
    db_path = "database/data/education_platform.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 检查主表
        print("\n1. 检查主表 teacher_knowledge_docs...")
        cursor.execute("SELECT COUNT(*) FROM teacher_knowledge_docs")
        main_count = cursor.fetchone()[0]
        print(f"✅ 主表记录数: {main_count}")
        
        if main_count > 0:
            cursor.execute("SELECT id, title, text_content FROM teacher_knowledge_docs LIMIT 3")
            docs = cursor.fetchall()
            for doc in docs:
                content_preview = doc[2][:50] if doc[2] else "无内容"
                print(f"   - ID: {doc[0]}, 标题: {doc[1]}, 内容: {content_preview}...")
        
        # 2. 检查FTS5表是否存在
        print("\n2. 检查FTS5表...")
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='teacher_knowledge_docs_fts'
        """)
        fts_table = cursor.fetchone()
        
        if fts_table:
            print("✅ FTS5表存在")
            
            # 检查FTS5表记录数
            try:
                cursor.execute("SELECT COUNT(*) FROM teacher_knowledge_docs_fts")
                fts_count = cursor.fetchone()[0]
                print(f"✅ FTS5表记录数: {fts_count}")
                
                if fts_count != main_count:
                    print(f"⚠️  FTS5表记录数({fts_count})与主表({main_count})不一致!")
                
            except Exception as e:
                print(f"❌ 查询FTS5表失败: {e}")
        else:
            print("❌ FTS5表不存在")
        
        # 3. 检查FTS5表结构
        print("\n3. 检查FTS5表结构...")
        try:
            cursor.execute("PRAGMA table_info(teacher_knowledge_docs_fts)")
            fts_columns = cursor.fetchall()
            if fts_columns:
                print("✅ FTS5表结构:")
                for col in fts_columns:
                    print(f"   - {col[1]} ({col[2]})")
            else:
                print("❌ 无法获取FTS5表结构")
        except Exception as e:
            print(f"❌ 检查FTS5表结构失败: {e}")
        
        # 4. 测试FTS5搜索
        print("\n4. 测试FTS5搜索...")
        try:
            # 简单搜索测试
            cursor.execute("""
                SELECT rowid, title FROM teacher_knowledge_docs_fts 
                WHERE teacher_knowledge_docs_fts MATCH '测试'
                LIMIT 3
            """)
            search_results = cursor.fetchall()
            print(f"✅ FTS5搜索'测试': 找到 {len(search_results)} 个结果")
            
            for result in search_results:
                print(f"   - ID: {result[0]}, 标题: {result[1]}")
                
        except Exception as e:
            print(f"❌ FTS5搜索测试失败: {e}")
        
        # 5. 检查触发器
        print("\n5. 检查触发器...")
        cursor.execute("""
            SELECT name, sql FROM sqlite_master 
            WHERE type='trigger' AND tbl_name='teacher_knowledge_docs'
        """)
        triggers = cursor.fetchall()
        
        if triggers:
            print(f"✅ 找到 {len(triggers)} 个触发器:")
            for trigger in triggers:
                print(f"   - {trigger[0]}")
        else:
            print("⚠️  没有找到触发器，FTS5表可能不会自动同步")
        
        # 6. 手动同步FTS5表（如果需要）
        if main_count > 0 and fts_count == 0:
            print("\n6. 尝试手动同步FTS5表...")
            try:
                cursor.execute("""
                    INSERT INTO teacher_knowledge_docs_fts(rowid, title, text_content, summary)
                    SELECT id, title, text_content, summary 
                    FROM teacher_knowledge_docs 
                    WHERE status = 'active'
                """)
                conn.commit()
                
                cursor.execute("SELECT COUNT(*) FROM teacher_knowledge_docs_fts")
                new_fts_count = cursor.fetchone()[0]
                print(f"✅ 手动同步完成，FTS5表现在有 {new_fts_count} 条记录")
                
            except Exception as e:
                print(f"❌ 手动同步失败: {e}")
        
        # 7. 测试BM25评分
        print("\n7. 测试BM25评分...")
        try:
            cursor.execute("""
                SELECT d.title, bm25(fts) as score
                FROM teacher_knowledge_docs d
                JOIN teacher_knowledge_docs_fts fts ON d.id = fts.rowid
                WHERE teacher_knowledge_docs_fts MATCH '测试'
                ORDER BY score
                LIMIT 3
            """)
            scored_results = cursor.fetchall()
            
            if scored_results:
                print(f"✅ BM25评分测试成功:")
                for result in scored_results:
                    print(f"   - {result[0]}: {result[1]:.4f}")
            else:
                print("⚠️  BM25评分测试无结果")
                
        except Exception as e:
            print(f"❌ BM25评分测试失败: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
    
    print("\n🎉 FTS5状态检查完成!")

if __name__ == "__main__":
    check_fts5_status()

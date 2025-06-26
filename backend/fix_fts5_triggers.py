"""
修复FTS5触发器和中文搜索问题
"""
import sqlite3
import os

def fix_fts5_triggers():
    """修复FTS5触发器"""
    
    print("🔧 修复FTS5触发器和中文搜索...")
    
    db_path = "database/data/education_platform.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 删除现有的FTS5表和触发器
        print("\n1. 清理现有FTS5表和触发器...")
        
        # 删除可能存在的触发器
        trigger_names = [
            'teacher_knowledge_docs_ai',
            'teacher_knowledge_docs_ad', 
            'teacher_knowledge_docs_au'
        ]
        
        for trigger_name in trigger_names:
            try:
                cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
                print(f"✅ 删除触发器: {trigger_name}")
            except Exception as e:
                print(f"⚠️  删除触发器 {trigger_name} 失败: {e}")
        
        # 删除FTS5表
        try:
            cursor.execute("DROP TABLE IF EXISTS teacher_knowledge_docs_fts")
            print("✅ 删除旧的FTS5表")
        except Exception as e:
            print(f"⚠️  删除FTS5表失败: {e}")
        
        # 2. 重新创建FTS5表
        print("\n2. 重新创建FTS5表...")
        
        # 创建FTS5表，使用默认分词器
        cursor.execute("""
            CREATE VIRTUAL TABLE teacher_knowledge_docs_fts USING fts5(
                title,
                text_content,
                summary,
                content='teacher_knowledge_docs',
                content_rowid='id'
            )
        """)
        print("✅ 创建新的FTS5表")
        
        # 3. 创建触发器
        print("\n3. 创建触发器...")
        
        # INSERT触发器
        cursor.execute("""
            CREATE TRIGGER teacher_knowledge_docs_ai AFTER INSERT ON teacher_knowledge_docs 
            BEGIN
                INSERT INTO teacher_knowledge_docs_fts(rowid, title, text_content, summary)
                VALUES (new.id, new.title, new.text_content, new.summary);
            END
        """)
        print("✅ 创建INSERT触发器")
        
        # DELETE触发器
        cursor.execute("""
            CREATE TRIGGER teacher_knowledge_docs_ad AFTER DELETE ON teacher_knowledge_docs 
            BEGIN
                INSERT INTO teacher_knowledge_docs_fts(teacher_knowledge_docs_fts, rowid, title, text_content, summary)
                VALUES('delete', old.id, old.title, old.text_content, old.summary);
            END
        """)
        print("✅ 创建DELETE触发器")
        
        # UPDATE触发器
        cursor.execute("""
            CREATE TRIGGER teacher_knowledge_docs_au AFTER UPDATE ON teacher_knowledge_docs 
            BEGIN
                INSERT INTO teacher_knowledge_docs_fts(teacher_knowledge_docs_fts, rowid, title, text_content, summary)
                VALUES('delete', old.id, old.title, old.text_content, old.summary);
                INSERT INTO teacher_knowledge_docs_fts(rowid, title, text_content, summary)
                VALUES (new.id, new.title, new.text_content, new.summary);
            END
        """)
        print("✅ 创建UPDATE触发器")
        
        # 4. 重新填充FTS5表
        print("\n4. 重新填充FTS5表...")
        
        cursor.execute("""
            INSERT INTO teacher_knowledge_docs_fts(rowid, title, text_content, summary)
            SELECT id, title, text_content, summary 
            FROM teacher_knowledge_docs 
            WHERE status = 'active'
        """)
        
        cursor.execute("SELECT COUNT(*) FROM teacher_knowledge_docs_fts")
        fts_count = cursor.fetchone()[0]
        print(f"✅ FTS5表重新填充完成，共 {fts_count} 条记录")
        
        # 5. 测试中文搜索
        print("\n5. 测试中文搜索...")
        
        test_queries = ["测试", "文档", "中国", "Linux", "课程"]
        
        for query in test_queries:
            try:
                cursor.execute("""
                    SELECT rowid, title FROM teacher_knowledge_docs_fts 
                    WHERE teacher_knowledge_docs_fts MATCH ?
                    LIMIT 3
                """, (query,))
                
                results = cursor.fetchall()
                print(f"✅ 搜索'{query}': 找到 {len(results)} 个结果")
                
                for result in results:
                    print(f"   - ID: {result[0]}, 标题: {result[1][:30]}...")
                    
            except Exception as e:
                print(f"❌ 搜索'{query}'失败: {e}")
        
        # 6. 测试BM25评分（修复SQL）
        print("\n6. 测试BM25评分...")
        try:
            cursor.execute("""
                SELECT d.title, bm25(teacher_knowledge_docs_fts) as score
                FROM teacher_knowledge_docs d
                JOIN teacher_knowledge_docs_fts ON d.id = teacher_knowledge_docs_fts.rowid
                WHERE teacher_knowledge_docs_fts MATCH '测试'
                ORDER BY score
                LIMIT 3
            """)
            
            scored_results = cursor.fetchall()
            
            if scored_results:
                print(f"✅ BM25评分测试成功:")
                for result in scored_results:
                    print(f"   - {result[0][:30]}...: {result[1]:.4f}")
            else:
                print("⚠️  BM25评分测试无结果")
                
        except Exception as e:
            print(f"❌ BM25评分测试失败: {e}")
        
        # 7. 提交更改
        conn.commit()
        conn.close()
        
        print("\n🎉 FTS5修复完成!")
        
        print("\n💡 中文搜索优化建议:")
        print("1. SQLite FTS5对中文分词支持有限")
        print("2. 可以考虑使用jieba分词预处理文本")
        print("3. 或者使用专门的中文搜索引擎如Elasticsearch")
        print("4. 当前使用simple分词器，按字符分割")
        
    except Exception as e:
        print(f"❌ 修复过程失败: {e}")

if __name__ == "__main__":
    fix_fts5_triggers()

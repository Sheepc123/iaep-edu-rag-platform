#!/usr/bin/env python3
"""
完整的知识库功能测试
测试数据库、搜索、向量化、API等所有功能
"""
import requests
import json
import sqlite3
import sys
import os
import traceback

# 配置
API_BASE_URL = "http://localhost:8000/api/v1"
DB_PATH = "./database/data/education_platform.db"

def test_database_status():
    """测试数据库状态"""
    try:
        print('=== 测试数据库状态 ===')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查活跃文档
        cursor.execute('SELECT COUNT(*) FROM teacher_knowledge_docs WHERE status = "active"')
        active_docs = cursor.fetchone()[0]
        print(f'✅ 活跃文档数: {active_docs}')
        
        # 检查教师档案
        cursor.execute('SELECT COUNT(*) FROM teacher_profiles')
        profiles = cursor.fetchone()[0]
        print(f'✅ 教师档案数: {profiles}')
        
        # 检查FTS5索引
        cursor.execute('SELECT COUNT(*) FROM teacher_knowledge_docs_fts')
        fts_docs = cursor.fetchone()[0]
        print(f'✅ FTS5索引数: {fts_docs}')
        
        # 检查各教师的文档分布
        cursor.execute('''
            SELECT d.teacher_id, u.username, COUNT(*) as doc_count
            FROM teacher_knowledge_docs d
            LEFT JOIN users u ON d.teacher_id = u.id
            WHERE d.status = 'active'
            GROUP BY d.teacher_id, u.username
        ''')
        
        teacher_docs = cursor.fetchall()
        print('\n📚 教师文档分布:')
        for teacher_id, username, doc_count in teacher_docs:
            print(f'   {username or "未知"} (ID: {teacher_id}): {doc_count} 个文档')
        
        conn.close()
        return active_docs > 0
        
    except Exception as e:
        print(f'❌ 数据库状态检查失败: {e}')
        return False

def test_fts_search():
    """测试FTS5搜索"""
    try:
        print('\n=== 测试FTS5搜索 ===')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        test_queries = ['Python', '测试', '文档', 'Linux']
        
        for query in test_queries:
            print(f'\n🔍 FTS5搜索: "{query}"')
            
            try:
                # 基本FTS5搜索
                cursor.execute('''
                    SELECT COUNT(*) FROM teacher_knowledge_docs_fts 
                    WHERE teacher_knowledge_docs_fts MATCH ?
                ''', (query,))
                
                count = cursor.fetchone()[0]
                print(f'   结果数: {count}')
                
                if count > 0:
                    # 获取具体结果
                    cursor.execute('''
                        SELECT d.id, d.title, d.teacher_id
                        FROM teacher_knowledge_docs d
                        JOIN teacher_knowledge_docs_fts fts ON d.id = fts.rowid
                        WHERE fts.teacher_knowledge_docs_fts MATCH ?
                        AND d.status = 'active'
                        LIMIT 3
                    ''', (query,))
                    
                    results = cursor.fetchall()
                    for doc_id, title, teacher_id in results:
                        print(f'     - ID: {doc_id}, 标题: {title}, 教师: {teacher_id}')
                
            except Exception as e:
                print(f'   ❌ FTS5搜索失败: {e}')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ FTS5搜索测试失败: {e}')
        return False

def test_vector_search():
    """测试向量搜索"""
    try:
        print('\n=== 测试向量搜索 ===')
        
        sys.path.append('.')
        from app.services.vector_service_simple import get_simple_vector_service
        from app.services.vector_service_deepseek import get_deepseek_vector_service
        
        # 选择可用的向量服务
        deepseek_service = get_deepseek_vector_service()
        simple_service = get_simple_vector_service()
        
        if deepseek_service.is_available():
            vector_service = deepseek_service
            service_name = "DeepSeek"
        else:
            vector_service = simple_service
            service_name = "Simple"
        
        print(f'使用 {service_name} 向量服务')
        
        # 获取统计信息
        stats = vector_service.get_collection_stats()
        total_vectors = stats.get('total_vectors', 0)
        print(f'向量数据库中共有 {total_vectors} 个向量')
        
        if total_vectors == 0:
            print('⚠️ 向量数据库为空')
            return False
        
        # 测试搜索
        test_queries = ['Python编程', '测试文档', 'Linux']
        
        for query in test_queries:
            print(f'\n🧠 向量搜索: "{query}"')
            
            try:
                results = vector_service.search_similar(query, top_k=3)
                print(f'   结果数: {len(results)}')
                
                for i, result in enumerate(results, 1):
                    metadata = result.get('metadata', {})
                    similarity = result.get('similarity', 0)
                    title = metadata.get('title', '未知')
                    teacher_id = metadata.get('teacher_id', '未知')
                    
                    print(f'     {i}. {title} (教师: {teacher_id}, 相似度: {similarity:.3f})')
                
            except Exception as e:
                print(f'   ❌ 向量搜索失败: {e}')
        
        return True
        
    except Exception as e:
        print(f'❌ 向量搜索测试失败: {e}')
        return False

def get_auth_token():
    """获取认证令牌"""
    try:
        # 尝试不同的教师账户
        test_accounts = [
            {"username": "teacher123", "password": "123456"},
            {"username": "teacher1", "password": "123456"},
            {"username": "admin", "password": "admin123"}
        ]
        
        for account in test_accounts:
            try:
                response = requests.post(f"{API_BASE_URL}/auth/login", json=account, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("access_token")
                    if token:
                        print(f'✅ 成功登录: {account["username"]}')
                        return token, account["username"]
            except:
                continue
        
        print('❌ 所有测试账户登录失败')
        return None, None
        
    except Exception as e:
        print(f'❌ 获取认证令牌失败: {e}')
        return None, None

def test_api_endpoints(token, username):
    """测试API端点"""
    try:
        print(f'\n=== 测试API端点 (用户: {username}) ===')
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. 测试获取文档列表
        print('\n📄 测试获取文档列表...')
        try:
            response = requests.get(f"{API_BASE_URL}/teacher-knowledge/documents", headers=headers, timeout=10)
            print(f'   状态码: {response.status_code}')
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', 0)
                documents = data.get('documents', [])
                print(f'   ✅ 成功获取文档列表，总数: {total}，当前页: {len(documents)}')
                
                # 显示文档信息
                for i, doc in enumerate(documents[:3]):
                    print(f'     {i+1}. {doc.get("title", "无标题")} (ID: {doc.get("id")})')
            else:
                print(f'   ❌ 获取文档列表失败: {response.text}')
                
        except Exception as e:
            print(f'   ❌ 请求异常: {e}')
        
        # 2. 测试搜索API
        print('\n🔍 测试搜索API...')
        search_data = {"query": "Python", "limit": 5}
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/teacher-knowledge/search", 
                headers={**headers, "Content-Type": "application/json"}, 
                json=search_data,
                timeout=10
            )
            print(f'   状态码: {response.status_code}')
            
            if response.status_code == 200:
                results = response.json()
                print(f'   ✅ 搜索成功，结果数: {len(results)}')
                
                for i, result in enumerate(results[:2]):
                    print(f'     {i+1}. {result.get("title", "无标题")} (ID: {result.get("id")})')
            else:
                print(f'   ❌ 搜索失败: {response.text}')
                
        except Exception as e:
            print(f'   ❌ 搜索请求异常: {e}')
        
        # 3. 测试语义搜索API
        print('\n🧠 测试语义搜索API...')
        semantic_data = {"query": "Python编程", "top_k": 3}
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/teacher-knowledge/semantic-search", 
                headers={**headers, "Content-Type": "application/json"}, 
                json=semantic_data,
                timeout=30
            )
            print(f'   状态码: {response.status_code}')
            
            if response.status_code == 200:
                results = response.json()
                print(f'   ✅ 语义搜索成功，结果数: {len(results)}')
                
                for i, result in enumerate(results[:2]):
                    title = result.get("title", "无标题")
                    similarity = result.get("similarity", 0)
                    print(f'     {i+1}. {title} (相似度: {similarity:.3f})')
            else:
                print(f'   ❌ 语义搜索失败: {response.text}')
                
        except Exception as e:
            print(f'   ❌ 语义搜索请求异常: {e}')
        
        # 4. 测试向量统计API
        print('\n📊 测试向量统计API...')
        try:
            response = requests.get(f"{API_BASE_URL}/teacher-knowledge/vector-stats", headers=headers, timeout=10)
            print(f'   状态码: {response.status_code}')
            
            if response.status_code == 200:
                data = response.json()
                available = data.get('available', False)
                print(f'   ✅ 向量服务可用: {available}')
                
                if available:
                    stats = data.get('stats', {})
                    print(f'   向量统计: {stats}')
                else:
                    print(f'   原因: {data.get("message", "未知")}')
            else:
                print(f'   ❌ 获取向量统计失败: {response.text}')
                
        except Exception as e:
            print(f'   ❌ 向量统计请求异常: {e}')
        
        return True
        
    except Exception as e:
        print(f'❌ API端点测试失败: {e}')
        return False

def main():
    """主函数"""
    print('🧪 知识库完整功能测试')
    print('=' * 60)
    
    # 1. 测试数据库状态
    db_ok = test_database_status()
    
    # 2. 测试FTS5搜索
    fts_ok = test_fts_search()
    
    # 3. 测试向量搜索
    vector_ok = test_vector_search()
    
    # 4. 测试API端点
    print('\n🌐 测试后端服务连接...')
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        if response.status_code == 200:
            print('✅ 后端服务运行正常')
            
            # 获取认证令牌并测试API
            token, username = get_auth_token()
            if token:
                api_ok = test_api_endpoints(token, username)
            else:
                api_ok = False
                print('❌ 无法获取认证令牌，跳过API测试')
        else:
            print('❌ 后端服务响应异常')
            api_ok = False
    except Exception as e:
        print(f'❌ 后端服务连接失败: {e}')
        print('请确保后端服务正在运行 (python run.py)')
        api_ok = False
    
    # 总结
    print('\n' + '=' * 60)
    print('📋 测试结果总结:')
    print(f'   数据库状态: {"✅" if db_ok else "❌"}')
    print(f'   FTS5搜索: {"✅" if fts_ok else "❌"}')
    print(f'   向量搜索: {"✅" if vector_ok else "❌"}')
    print(f'   API接口: {"✅" if api_ok else "❌"}')
    
    all_ok = db_ok and fts_ok and vector_ok and api_ok
    
    if all_ok:
        print('\n🎉 所有功能测试通过！')
        print('\n建议接下来:')
        print('1. 测试前端知识库页面')
        print('2. 验证不同教师的文档隔离')
        print('3. 测试文档上传功能')
    else:
        print('\n⚠️ 部分功能存在问题，请检查上述错误信息')
        
        if not db_ok:
            print('- 运行 fix_database_integrity.py 修复数据库')
        if not vector_ok:
            print('- 运行 rebuild_vector_database.py 重建向量数据库')
        if not api_ok:
            print('- 检查后端服务是否正常运行')

if __name__ == '__main__':
    main()

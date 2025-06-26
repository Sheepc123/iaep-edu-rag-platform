-- Migration: add_teacher_knowledge_docs
-- Description: 添加教师知识库文档表
-- Created: 2025-06-26T10:57:54.484162

-- 创建教师知识库文档表
CREATE TABLE IF NOT EXISTS teacher_knowledge_docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    file_size INTEGER NOT NULL,
    text_content TEXT,
    summary TEXT,
    category VARCHAR(100),
    tags VARCHAR(500),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_teacher_knowledge_docs_teacher_id ON teacher_knowledge_docs(teacher_id);
CREATE INDEX IF NOT EXISTS idx_teacher_knowledge_docs_category ON teacher_knowledge_docs(category);
CREATE INDEX IF NOT EXISTS idx_teacher_knowledge_docs_status ON teacher_knowledge_docs(status);
CREATE INDEX IF NOT EXISTS idx_teacher_knowledge_docs_upload_time ON teacher_knowledge_docs(upload_time);

-- 创建全文搜索虚拟表 (SQLite FTS5)
CREATE VIRTUAL TABLE IF NOT EXISTS teacher_knowledge_docs_fts USING fts5(
    title,
    text_content,
    summary,
    content='teacher_knowledge_docs',
    content_rowid='id'
);

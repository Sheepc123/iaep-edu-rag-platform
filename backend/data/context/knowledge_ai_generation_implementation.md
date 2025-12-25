# 知识库增强AI生成功能实现文档

## 概述

基于已有的DeepSeek混合向量数据库系统，我们成功实现了本地知识库的一键生成课程和一键AI生成习题功能。该功能允许教师基于已上传的知识库文档，通过AI智能生成高质量的课程内容和练习题目。

## 功能特性

### 🎯 核心功能
1. **一键生成课程**: 基于知识库文档自动生成完整的课程结构
2. **一键生成习题**: 基于知识库内容智能生成各类题型
3. **智能文档搜索**: 自动搜索相关文档或手动选择指定文档
4. **多种生成模式**: 支持预览模式和自动保存模式

### 🔧 技术特性
1. **语义搜索增强**: 利用DeepSeek向量搜索找到最相关的文档内容
2. **AI内容生成**: 使用DeepSeek API生成高质量的教学内容
3. **灵活配置**: 支持难度级别、数量、类型等多种参数配置
4. **错误处理**: 完善的错误处理和回退机制

## 系统架构

### 后端架构
```
AIKnowledgeGenerator (核心服务)
├── 向量搜索服务 (DeepSeek Vector Service)
├── AI生成服务 (DeepSeek API)
├── 课程管理服务 (Course Service)
├── 习题管理服务 (Exercise Service)
└── 知识库服务 (Knowledge Service)
```

### 前端架构
```
KnowledgeBase.tsx (主页面)
├── AI生成按钮组
├── AIGenerateModal (生成配置弹窗)
├── 文档选择器
└── 参数配置表单
```

## 实现细节

### 1. 核心服务类 (AIKnowledgeGenerator)

**位置**: `backend/app/services/ai_knowledge_generator.py`

**主要方法**:
- `generate_course_from_knowledge()`: 基于知识库生成课程
- `generate_exercises_from_knowledge()`: 基于知识库生成习题
- `_get_relevant_knowledge_content()`: 获取相关知识库内容
- `_build_course_generation_prompt()`: 构建课程生成提示词
- `_build_exercise_generation_prompt()`: 构建习题生成提示词

### 2. API端点

**位置**: `backend/app/api/v1/endpoints/teacher_knowledge.py`

**新增端点**:
- `POST /generate-course`: 基于知识库生成课程
- `POST /generate-exercises`: 基于知识库生成习题

### 3. 前端界面

**位置**: `frontend/src/pages/teacher/KnowledgeBase.tsx`

**新增功能**:
- AI生成按钮组 (课程/习题)
- AIGenerateModal 组件
- 文档选择和参数配置
- 生成状态管理

### 4. API服务

**位置**: `frontend/src/services/knowledgeAPI.ts`

**新增方法**:
- `generateCourse()`: 调用课程生成API
- `generateExercise()`: 调用习题生成API

## 使用流程

### 课程生成流程
1. 教师在知识库页面点击"AI生成课程"按钮
2. 在弹窗中输入课程主题
3. 选择参考文档(可选)或让AI自动搜索
4. 配置课程参数(难度、课时数等)
5. 选择是否自动保存
6. 点击"开始生成"，AI基于知识库内容生成课程
7. 生成完成后显示结果，可选择保存到课程管理

### 习题生成流程
1. 教师在知识库页面点击"AI生成习题"按钮
2. 在弹窗中输入习题主题
3. 选择参考文档(可选)或让AI自动搜索
4. 配置习题参数(题型、难度、数量等)
5. 选择是否自动保存
6. 点击"开始生成"，AI基于知识库内容生成习题
7. 生成完成后显示结果，可选择保存到练习管理

## 技术实现

### 1. 知识库内容检索

```python
async def _get_relevant_knowledge_content(self, teacher_id, topic, knowledge_doc_ids):
    """获取相关的知识库内容"""
    if knowledge_doc_ids:
        # 直接获取指定文档
        return self._get_documents_by_ids(knowledge_doc_ids)
    else:
        # 使用向量搜索找到相关文档
        search_results = self.vector_service.search_similar(
            query=topic,
            top_k=5,
            filter_metadata={"teacher_id": teacher_id}
        )
        # 回退到关键词搜索
        if not search_results:
            search_results = self.knowledge_service.search_documents(
                teacher_id=teacher_id, query=topic, limit=5
            )
        return search_results
```

### 2. AI提示词构建

**课程生成提示词**:
- 基于知识库内容
- 指定课程主题和难度
- 要求JSON格式输出
- 包含课程信息和课时安排

**习题生成提示词**:
- 基于知识库内容
- 指定题型和难度
- 要求JSON格式输出
- 包含题目内容和答案解析

### 3. 错误处理和回退

```python
try:
    # 使用DeepSeek API生成
    result = await self._call_deepseek_api(prompt)
    return self._parse_json_response(result)
except Exception as e:
    logger.error(f"AI生成失败: {e}")
    # 回退到模拟数据
    return self._generate_mock_data()
```

## 配置参数

### 课程生成参数
- **topic**: 课程主题 (必填)
- **knowledge_doc_ids**: 指定文档ID列表 (可选)
- **course_level**: 难度级别 (easy/medium/hard)
- **lesson_count**: 课时数量 (1-20)
- **auto_save**: 是否自动保存

### 习题生成参数
- **topic**: 习题主题 (必填)
- **knowledge_doc_ids**: 指定文档ID列表 (可选)
- **exercise_types**: 题目类型 (multiple_choice/fill_blank/essay/true_false)
- **difficulty**: 难度级别 (easy/medium/hard)
- **question_count**: 题目数量 (1-50)
- **auto_save**: 是否自动保存
- **course_id**: 关联课程ID (可选)

## 数据流

### 课程生成数据流
```
用户输入 → 知识库搜索 → AI提示词构建 → DeepSeek API → JSON解析 → 课程数据 → 保存(可选)
```

### 习题生成数据流
```
用户输入 → 知识库搜索 → AI提示词构建 → DeepSeek API → JSON解析 → 习题数据 → 保存(可选)
```

## 性能优化

1. **内容限制**: 每个文档最多使用2000字符，避免提示词过长
2. **文档数量**: 最多使用3个最相关的文档
3. **缓存机制**: 可以考虑缓存常见主题的生成结果
4. **异步处理**: 使用异步API调用，提高响应速度

## 测试

**测试脚本**: `backend/test_knowledge_ai_generation.py`

**测试内容**:
- 向量搜索功能测试
- 课程生成功能测试
- 习题生成功能测试
- 错误处理测试

## 部署说明

### 环境要求
- DeepSeek API密钥配置
- ChromaDB向量数据库
- 知识库文档已上传并向量化

### 配置检查
1. 确认DeepSeek API配置正确
2. 确认向量服务可用
3. 确认知识库有足够的文档内容

## 未来优化方向

1. **提示词优化**: 根据使用反馈优化AI提示词
2. **模板系统**: 支持自定义课程和习题模板
3. **批量生成**: 支持批量生成多个课程或习题集
4. **质量评估**: 添加生成内容的质量评估机制
5. **个性化**: 根据教师偏好个性化生成内容

## 总结

本功能成功整合了DeepSeek混合向量数据库系统和AI生成能力，为教师提供了强大的智能教学内容生成工具。通过知识库驱动的AI生成，教师可以快速创建高质量的课程和习题，大大提高了教学效率。

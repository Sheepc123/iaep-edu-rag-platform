# 教师端本地知识库功能方案

## 需求分析

### 核心功能需求
1. **知识库管理**: 教师可以查看已上传的书籍/文档列表
2. **智能课程创建**: 基于本地知识库 + DeepSeek AI 生成课程
3. **智能习题生成**: 基于本地知识库 + DeepSeek AI 生成练习题
4. **知识库检索**: 快速查找和引用已上传的教学资料

### 技术可行性
✅ **完全可行** - 您的现有架构已经具备所有必要条件：
- 文档处理能力 (PDF/Word解析)
- DeepSeek AI集成
- 用户权限管理 (教师角色)
- 文件上传和存储
- 前端交互界面

## 1. 精简架构设计

### 1.1 教师端知识库架构
```
┌─────────────────────────────────────────────────────────────┐
│                    教师端知识库系统                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│   文档管理      │   知识检索      │      AI内容生成         │
│                 │                 │                         │
│ • 上传书籍      │ • 文本搜索      │ • 基于知识库生成课程    │
│ • 查看列表      │ • 内容预览      │ • 基于知识库生成习题    │
│ • 分类管理      │ • 相关推荐      │ • DeepSeek AI增强       │
│ • 删除文档      │ • 快速定位      │ • 智能内容优化          │
└─────────────────┴─────────────────┴─────────────────────────┘
         │                 │                         │
         ▼                 ▼                         ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   文件存储      │ │   文本索引      │ │    DeepSeek API     │
│                 │ │                 │ │                     │
│ • 本地文件      │ │ • 全文检索      │ │ • 课程生成          │
│ • 元数据存储    │ │ • 关键词匹配    │ │ • 习题生成          │
│ • SQLite数据库  │ │ • 内容摘要      │ │ • 内容优化          │
└─────────────────┘ └─────────────────┘ └─────────────────────┘
```

### 1.2 技术选型 (精简版)

#### 存储方案
- **文件存储**: 本地文件系统 (现有uploads目录)
- **元数据存储**: SQLite数据库 (现有数据库)
- **文本索引**: 简单的全文检索 (SQLite FTS)

#### AI集成
- **主要AI**: DeepSeek API (已集成)
- **辅助功能**: 本地文本处理和检索
- **无需向量数据库**: 使用传统文本检索即可满足需求

## 2. 数据库设计 (精简版)

### 2.1 新增数据表

#### 教师知识库文档表
```sql
-- 教师知识库文档表 (简化版)
CREATE TABLE teacher_knowledge_docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,           -- 书籍/文档标题
    filename VARCHAR(255) NOT NULL,        -- 原始文件名
    file_path VARCHAR(500) NOT NULL,       -- 文件存储路径
    file_type VARCHAR(10) NOT NULL,        -- 文件类型 (.pdf, .docx)
    file_size INTEGER NOT NULL,            -- 文件大小
    text_content TEXT,                     -- 提取的文本内容
    summary TEXT,                          -- 文档摘要
    category VARCHAR(100),                 -- 分类 (教材、参考书、论文等)
    tags VARCHAR(500),                     -- 标签 (逗号分隔)
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',   -- active, deleted
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- 创建全文搜索索引 (SQLite FTS5)
CREATE VIRTUAL TABLE teacher_knowledge_docs_fts USING fts5(
    title,
    text_content,
    summary,
    content='teacher_knowledge_docs',
    content_rowid='id'
);
```

### 2.2 核心服务实现

#### 教师知识库服务
```python
class TeacherKnowledgeService:
    """教师知识库服务 (精简版)"""

    def __init__(self, db: Session):
        self.db = db
        self.document_processor = DocumentProcessor()

    async def upload_document(self, file: UploadFile, teacher_id: int,
                            category: str = None, tags: str = None) -> dict:
        """上传文档到教师知识库"""
        try:
            # 1. 验证文件
            self.document_processor.validate_file(file)

            # 2. 保存文件
            file_path = await self._save_file(file, teacher_id)

            # 3. 提取文本内容
            document_info = await self.document_processor.extract_text(file)

            # 4. 生成摘要 (可选)
            summary = self._generate_summary(document_info["text_content"])

            # 5. 保存到数据库
            doc_record = TeacherKnowledgeDoc(
                teacher_id=teacher_id,
                title=self._extract_title(file.filename, document_info["text_content"]),
                filename=file.filename,
                file_path=file_path,
                file_type=document_info["file_type"],
                file_size=document_info.get("file_size", 0),
                text_content=document_info["text_content"],
                summary=summary,
                category=category,
                tags=tags
            )

            self.db.add(doc_record)
            self.db.commit()
            self.db.refresh(doc_record)

            return {
                "success": True,
                "document_id": doc_record.id,
                "message": "文档上传成功"
            }

        except Exception as e:
            self.db.rollback()
            raise Exception(f"文档上传失败: {str(e)}")

    def get_teacher_documents(self, teacher_id: int, category: str = None,
                            page: int = 1, size: int = 20) -> dict:
        """获取教师的知识库文档列表"""
        query = self.db.query(TeacherKnowledgeDoc).filter(
            TeacherKnowledgeDoc.teacher_id == teacher_id,
            TeacherKnowledgeDoc.status == 'active'
        )

        if category:
            query = query.filter(TeacherKnowledgeDoc.category == category)

        # 分页
        total = query.count()
        documents = query.offset((page - 1) * size).limit(size).all()

        return {
            "documents": [self._format_document(doc) for doc in documents],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }

    def search_documents(self, teacher_id: int, query: str, limit: int = 10) -> List[dict]:
        """搜索教师知识库文档"""
        # 使用SQLite FTS5全文搜索
        sql = """
        SELECT d.*, rank
        FROM teacher_knowledge_docs d
        JOIN teacher_knowledge_docs_fts fts ON d.id = fts.rowid
        WHERE d.teacher_id = :teacher_id
        AND d.status = 'active'
        AND teacher_knowledge_docs_fts MATCH :query
        ORDER BY rank
        LIMIT :limit
        """

        results = self.db.execute(sql, {
            "teacher_id": teacher_id,
            "query": query,
            "limit": limit
        }).fetchall()

        return [self._format_document_with_rank(result) for result in results]

    def delete_document(self, document_id: int, teacher_id: int) -> bool:
        """删除文档 (软删除)"""
        doc = self.db.query(TeacherKnowledgeDoc).filter(
            TeacherKnowledgeDoc.id == document_id,
            TeacherKnowledgeDoc.teacher_id == teacher_id
        ).first()

        if doc:
            doc.status = 'deleted'
            self.db.commit()
            return True
        return False
```

## 3. AI增强服务

### 3.1 基于知识库的内容生成服务

#### 智能课程生成服务
```python
class KnowledgeBasedCourseGenerator:
    """基于知识库的课程生成器"""

    def __init__(self, knowledge_service: TeacherKnowledgeService,
                 ai_service: AIService):
        self.knowledge_service = knowledge_service
        self.ai_service = ai_service

    async def generate_course_with_knowledge(self, teacher_id: int,
                                           topic: str,
                                           knowledge_doc_ids: List[int],
                                           course_level: str = "medium",
                                           lesson_count: int = 8) -> dict:
        """基于知识库文档生成课程"""

        # 1. 获取相关知识库内容
        knowledge_content = await self._get_knowledge_content(
            teacher_id, knowledge_doc_ids, topic
        )

        # 2. 构建课程生成提示词
        course_prompt = self._build_course_generation_prompt(
            topic, knowledge_content, course_level, lesson_count
        )

        # 3. 调用DeepSeek API生成课程
        generated_course = await self.ai_service._call_deepseek_api(
            course_prompt, conversation_id=0, user_role="teacher"
        )

        # 4. 解析和格式化结果
        course_data = self._parse_course_response(generated_course["content"])

        # 5. 添加知识库引用信息
        course_data["knowledge_sources"] = knowledge_doc_ids
        course_data["generated_from_knowledge"] = True

        return course_data

    def _build_course_generation_prompt(self, topic: str, knowledge_content: str,
                                      level: str, lesson_count: int) -> str:
        """构建课程生成提示词"""
        return f"""
你是一位专业的教学设计专家。请基于以下教学资料为"{topic}"主题设计一门完整的课程。

**教学资料内容：**
{knowledge_content}

**课程要求：**
- 课程主题：{topic}
- 难度级别：{level}
- 课时数量：{lesson_count}个课时
- 每课时时长：30-45分钟

**请生成以下内容：**
1. 课程标题和描述
2. 学习目标
3. 详细的课时安排
4. 每个课时的具体内容大纲
5. 推荐的教学方法

**输出格式要求：**
请以JSON格式输出，包含以下字段：
- title: 课程标题
- description: 课程描述
- objectives: 学习目标列表
- lessons: 课时列表，每个课时包含标题、描述、内容大纲、时长

请确保课程内容与提供的教学资料高度相关，并充分利用资料中的知识点。
"""
```

#### 智能习题生成服务
```python
class KnowledgeBasedExerciseGenerator:
    """基于知识库的习题生成器"""

    def __init__(self, knowledge_service: TeacherKnowledgeService,
                 ai_service: AIService):
        self.knowledge_service = knowledge_service
        self.ai_service = ai_service

    async def generate_exercises_with_knowledge(self, teacher_id: int,
                                              topic: str,
                                              knowledge_doc_ids: List[int],
                                              exercise_types: List[str],
                                              difficulty: str = "medium",
                                              count: int = 10) -> dict:
        """基于知识库生成习题"""

        # 1. 获取相关知识内容
        knowledge_content = await self._get_relevant_knowledge(
            teacher_id, knowledge_doc_ids, topic
        )

        # 2. 构建习题生成提示词
        exercise_prompt = self._build_exercise_generation_prompt(
            topic, knowledge_content, exercise_types, difficulty, count
        )

        # 3. 调用DeepSeek API生成习题
        generated_exercises = await self.ai_service._call_deepseek_api(
            exercise_prompt, conversation_id=0, user_role="teacher"
        )

        # 4. 解析习题结果
        exercises_data = self._parse_exercises_response(generated_exercises["content"])

        return {
            "exercises": exercises_data,
            "knowledge_sources": knowledge_doc_ids,
            "topic": topic,
            "generated_at": datetime.utcnow().isoformat()
        }

    def _build_exercise_generation_prompt(self, topic: str, knowledge_content: str,
                                        exercise_types: List[str], difficulty: str,
                                        count: int) -> str:
        """构建习题生成提示词"""
        types_str = "、".join(exercise_types)

        return f"""
你是一位专业的教育测评专家。请基于以下教学资料为"{topic}"主题生成高质量的练习题。

**教学资料内容：**
{knowledge_content}

**习题要求：**
- 主题：{topic}
- 题目类型：{types_str}
- 难度级别：{difficulty}
- 题目数量：{count}道

**生成规则：**
1. 题目必须基于提供的教学资料内容
2. 确保题目覆盖资料中的重要知识点
3. 题目难度要与要求匹配
4. 每道题都要有标准答案和详细解析
5. 选择题需要4个选项，只有1个正确答案

**输出格式：**
请以JSON格式输出，包含exercises数组，每个习题包含：
- question_text: 题目内容
- question_type: 题目类型
- options: 选项列表（选择题）
- correct_answer: 正确答案
- explanation: 详细解析
- knowledge_point: 对应的知识点
- difficulty: 难度级别

请确保所有题目都与教学资料密切相关。
"""
```

### 3.2 API接口设计

#### 知识库管理接口
```python
# backend/app/api/v1/endpoints/teacher_knowledge.py

@router.post("/teacher-knowledge/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("教材"),
    tags: str = Form(""),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """上传文档到教师知识库"""
    knowledge_service = TeacherKnowledgeService(db)
    result = await knowledge_service.upload_document(
        file, current_user.id, category, tags
    )
    return result

@router.get("/teacher-knowledge/documents")
async def get_documents(
    category: str = None,
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """获取教师知识库文档列表"""
    knowledge_service = TeacherKnowledgeService(db)
    return knowledge_service.get_teacher_documents(
        current_user.id, category, page, size
    )

@router.post("/teacher-knowledge/search")
async def search_documents(
    query: str = Body(...),
    limit: int = Body(10),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """搜索知识库文档"""
    knowledge_service = TeacherKnowledgeService(db)
    return knowledge_service.search_documents(current_user.id, query, limit)
```

#### AI内容生成接口
```python
@router.post("/ai-course/generate-from-knowledge")
async def generate_course_from_knowledge(
    topic: str = Body(...),
    knowledge_doc_ids: List[int] = Body(...),
    course_level: str = Body("medium"),
    lesson_count: int = Body(8),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """基于知识库生成课程"""
    knowledge_service = TeacherKnowledgeService(db)
    ai_service = AIService(db)
    course_generator = KnowledgeBasedCourseGenerator(knowledge_service, ai_service)

    result = await course_generator.generate_course_with_knowledge(
        current_user.id, topic, knowledge_doc_ids, course_level, lesson_count
    )
    return {"success": True, "course": result}

@router.post("/ai-exercise/generate-from-knowledge")
async def generate_exercises_from_knowledge(
    topic: str = Body(...),
    knowledge_doc_ids: List[int] = Body(...),
    exercise_types: List[str] = Body(["multiple_choice", "fill_blank"]),
    difficulty: str = Body("medium"),
    count: int = Body(10),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """基于知识库生成习题"""
    knowledge_service = TeacherKnowledgeService(db)
    ai_service = AIService(db)
    exercise_generator = KnowledgeBasedExerciseGenerator(knowledge_service, ai_service)

    result = await exercise_generator.generate_exercises_with_knowledge(
        current_user.id, topic, knowledge_doc_ids, exercise_types, difficulty, count
    )
    return {"success": True, "exercises": result}
```

## 4. 前端界面设计

### 4.1 教师知识库管理页面

#### 主界面布局
```typescript
// frontend/src/pages/teacher/KnowledgeBase.tsx
export const TeacherKnowledgeBase: React.FC = () => {
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [categories] = useState(['教材', '参考书', '论文', '课件', '其他']);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  return (
    <TeacherLayout>
      <div className="knowledge-base-container p-6">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <BookOpen className="w-8 h-8 mr-3 text-blue-600" />
            我的知识库
          </h1>
          <p className="text-gray-600 mt-2">管理您的教学资料，让AI更好地为您服务</p>
        </div>

        {/* 操作区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* 文档上传 */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Upload className="w-5 h-5 mr-2" />
                上传文档
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocumentUpload
                onFileSelect={handleFileUpload}
                acceptedTypes={['.pdf', '.docx', '.doc']}
                maxSize={10 * 1024 * 1024}
              />
            </CardContent>
          </Card>

          {/* 统计信息 */}
          <Card>
            <CardHeader>
              <CardTitle>知识库统计</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span>总文档数</span>
                  <span className="font-semibold">{documents.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>总大小</span>
                  <span className="font-semibold">{formatFileSize(totalSize)}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 快速操作 */}
          <Card>
            <CardHeader>
              <CardTitle>快速操作</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button
                className="w-full"
                onClick={() => navigate('/teacher/ai-course-create')}
              >
                <Sparkles className="w-4 h-4 mr-2" />
                AI生成课程
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={() => navigate('/teacher/ai-exercise-create')}
              >
                <FileText className="w-4 h-4 mr-2" />
                AI生成习题
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* 搜索和筛选 */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1">
            <Input
              placeholder="搜索文档内容..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full"
            />
          </div>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="选择分类" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">全部分类</SelectItem>
              {categories.map(cat => (
                <SelectItem key={cat} value={cat}>{cat}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* 文档列表 */}
        <DocumentList
          documents={documents}
          onDelete={handleDeleteDocument}
          onPreview={handlePreviewDocument}
        />
      </div>
    </TeacherLayout>
  );
};
```

### 4.2 增强的AI课程创建页面

#### 集成知识库选择
```typescript
// 在现有的CourseCreate.tsx中添加知识库选择功能
const [useKnowledgeBase, setUseKnowledgeBase] = useState(false);
const [selectedDocuments, setSelectedDocuments] = useState<number[]>([]);
const [knowledgeDocuments, setKnowledgeDocuments] = useState<KnowledgeDocument[]>([]);

// 在AI生成器模态框中添加知识库选择
{showAIGenerator && (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      {/* 现有的文档上传区域 */}

      {/* 新增：知识库选择区域 */}
      <div className="mt-6 border-t pt-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">使用知识库资料</h3>
          <Switch
            checked={useKnowledgeBase}
            onCheckedChange={setUseKnowledgeBase}
          />
        </div>

        {useKnowledgeBase && (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              选择您知识库中的相关资料，AI将基于这些内容生成更精准的课程
            </p>

            <KnowledgeDocumentSelector
              documents={knowledgeDocuments}
              selected={selectedDocuments}
              onChange={setSelectedDocuments}
            />
          </div>
        )}
      </div>

      {/* 生成按钮 */}
      <div className="flex justify-end mt-6">
        <Button
          onClick={handleGenerateCourseWithKnowledge}
          disabled={!uploadedFile && selectedDocuments.length === 0}
        >
          开始生成课程
        </Button>
      </div>
    </div>
  </div>
)}
```

### 4.3 知识库文档选择组件

```typescript
// frontend/src/components/teacher/KnowledgeDocumentSelector.tsx
interface KnowledgeDocumentSelectorProps {
  documents: KnowledgeDocument[];
  selected: number[];
  onChange: (selected: number[]) => void;
}

export const KnowledgeDocumentSelector: React.FC<KnowledgeDocumentSelectorProps> = ({
  documents,
  selected,
  onChange
}) => {
  const handleToggleDocument = (docId: number) => {
    if (selected.includes(docId)) {
      onChange(selected.filter(id => id !== docId));
    } else {
      onChange([...selected, docId]);
    }
  };

  return (
    <div className="max-h-60 overflow-y-auto border rounded-lg">
      {documents.map(doc => (
        <div
          key={doc.id}
          className={`p-3 border-b cursor-pointer hover:bg-gray-50 ${
            selected.includes(doc.id) ? 'bg-blue-50 border-blue-200' : ''
          }`}
          onClick={() => handleToggleDocument(doc.id)}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Checkbox
                checked={selected.includes(doc.id)}
                onChange={() => {}} // 由父级点击处理
              />
              <div>
                <h4 className="font-medium text-gray-900">{doc.title}</h4>
                <p className="text-sm text-gray-500">
                  {doc.category} • {formatFileSize(doc.file_size)}
                </p>
              </div>
            </div>
            <Badge variant="outline">{doc.category}</Badge>
          </div>
        </div>
      ))}
    </div>
  );
};
```

## 5. 实施计划 (精简版)

### 5.1 第一阶段：数据库和基础服务 (1周)

#### 任务清单
1. **数据库设计**
   - 创建 `teacher_knowledge_docs` 表
   - 设置 SQLite FTS5 全文搜索索引
   - 数据库迁移脚本

2. **后端服务开发**
   - `TeacherKnowledgeService` 基础功能
   - 文档上传、列表、搜索、删除
   - API接口实现

3. **测试验证**
   - 文档上传功能测试
   - 全文搜索功能测试

### 5.2 第二阶段：AI增强功能 (1-2周)

#### 任务清单
1. **AI服务增强**
   - `KnowledgeBasedCourseGenerator` 实现
   - `KnowledgeBasedExerciseGenerator` 实现
   - 提示词工程优化

2. **API接口完善**
   - 基于知识库的课程生成接口
   - 基于知识库的习题生成接口

3. **集成测试**
   - 端到端功能测试
   - AI生成质量验证

### 5.3 第三阶段：前端界面开发 (1-2周)

#### 任务清单
1. **知识库管理页面**
   - 文档列表展示
   - 上传和删除功能
   - 搜索和筛选功能

2. **AI生成界面增强**
   - 知识库文档选择组件
   - 课程创建页面集成
   - 习题生成页面集成

3. **用户体验优化**
   - 加载状态处理
   - 错误提示优化
   - 响应式设计

## 6. 技术优势

### 6.1 实现简单
- **无需复杂向量数据库**: 使用SQLite FTS5即可满足搜索需求
- **基于现有架构**: 充分利用已有的文档处理和AI服务
- **渐进式开发**: 可以分阶段实施，风险可控

### 6.2 功能实用
- **教师友好**: 简单的文档管理界面
- **AI增强**: 基于个人资料的智能生成
- **即时可用**: 上传文档后立即可用于AI生成

### 6.3 扩展性好
- **数据结构清晰**: 便于后续功能扩展
- **接口标准化**: 易于集成更多AI功能
- **性能可优化**: 后续可升级为向量检索

## 7. 总结

### ✅ 方案完全可行
您的需求非常明确且技术上完全可行：

1. **教师知识库管理**: 上传、查看、搜索个人教学资料
2. **AI内容生成增强**: 基于知识库 + DeepSeek API 生成课程和习题
3. **简单实用**: 无需复杂的向量数据库，使用传统搜索即可

### 🚀 实施建议
1. **优先开发**: 数据库设计 → 后端服务 → 前端界面
2. **分阶段验证**: 每个阶段完成后进行功能测试
3. **用户反馈**: 及时收集使用反馈，持续优化

这个方案既满足您的具体需求，又充分利用了现有的技术基础，实施难度适中，预期效果显著！
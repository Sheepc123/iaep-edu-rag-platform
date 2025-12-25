"""
知识库相关的Pydantic模式
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class KnowledgeDocumentBase(BaseModel):
    """知识库文档基础模式"""
    title: str = Field(..., description="文档标题")
    category: str = Field(..., description="文档分类")
    tags: Optional[str] = Field(None, description="标签，逗号分隔")


class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    """创建知识库文档模式"""
    filename: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    file_type: str = Field(..., description="文件类型")
    file_size: int = Field(..., description="文件大小")
    text_content: Optional[str] = Field(None, description="文本内容")
    summary: Optional[str] = Field(None, description="文档摘要")


class KnowledgeDocumentUpdate(BaseModel):
    """更新知识库文档模式"""
    title: Optional[str] = Field(None, description="文档标题")
    category: Optional[str] = Field(None, description="文档分类")
    tags: Optional[str] = Field(None, description="标签")
    summary: Optional[str] = Field(None, description="文档摘要")


class KnowledgeDocument(KnowledgeDocumentBase):
    """知识库文档响应模式"""
    id: int
    teacher_id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    text_content: Optional[str] = None
    summary: Optional[str] = None
    upload_time: datetime
    status: str

    class Config:
        from_attributes = True


class KnowledgeDocumentList(BaseModel):
    """知识库文档列表响应模式"""
    documents: List[KnowledgeDocument]
    total: int
    page: int
    size: int
    pages: int


class KnowledgeSearchResult(BaseModel):
    """知识库搜索结果模式"""
    id: int
    title: str
    filename: str
    category: str
    file_size: int
    upload_time: datetime
    relevance_score: Optional[float] = None
    matched_content: Optional[str] = None

    class Config:
        from_attributes = True


class UploadDocumentResponse(BaseModel):
    """文档上传响应模式"""
    success: bool
    document_id: int
    message: str


class KnowledgeSearchRequest(BaseModel):
    """知识库搜索请求模式"""
    query: str = Field(..., description="搜索关键词")
    limit: int = Field(10, description="返回结果数量限制")


class DeleteDocumentResponse(BaseModel):
    """删除文档响应模式"""
    success: bool
    message: str


class SemanticSearchRequest(BaseModel):
    """语义搜索请求模式"""
    query: str = Field(..., description="搜索查询")
    top_k: int = Field(5, description="返回结果数量")
    category: Optional[str] = Field(None, description="分类过滤")
    tags: Optional[List[str]] = Field(None, description="标签过滤")


class SemanticSearchResult(BaseModel):
    """语义搜索结果模式"""
    document_id: int = Field(..., description="文档ID")
    title: str = Field(..., description="文档标题")
    content: str = Field(..., description="文档内容片段")
    similarity: float = Field(..., description="相似度分数")
    category: Optional[str] = Field(None, description="文档分类")
    tags: Optional[List[str]] = Field(None, description="文档标签")
    file_type: Optional[str] = Field(None, description="文件类型")
    enhanced_by: Optional[str] = Field(None, description="增强方式")


# ==================== AI生成相关模式 ====================

class KnowledgeCourseGenerationRequest(BaseModel):
    """基于知识库生成课程请求模式"""
    topic: str = Field(..., min_length=1, max_length=100, description="课程主题")
    knowledge_doc_ids: Optional[List[int]] = Field(None, description="指定的知识库文档ID列表")
    course_level: str = Field("medium", description="课程难度级别")
    lesson_count: int = Field(8, ge=1, le=20, description="课时数量")
    auto_save: bool = Field(False, description="是否自动保存课程")

    class Config:
        schema_extra = {
            "example": {
                "topic": "Python编程基础",
                "knowledge_doc_ids": [1, 2, 3],
                "course_level": "medium",
                "lesson_count": 8,
                "auto_save": True
            }
        }


class KnowledgeExerciseGenerationRequest(BaseModel):
    """基于知识库生成习题请求模式"""
    topic: str = Field(..., min_length=1, max_length=100, description="习题主题")
    knowledge_doc_ids: Optional[List[int]] = Field(None, description="指定的知识库文档ID列表")
    exercise_types: List[str] = Field(["multiple_choice", "fill_blank", "essay"], description="题目类型列表")
    difficulty: str = Field("medium", description="难度级别")
    question_count: int = Field(10, ge=1, le=50, description="题目数量")
    auto_save: bool = Field(False, description="是否自动保存习题")
    course_id: Optional[int] = Field(None, description="关联的课程ID")

    class Config:
        schema_extra = {
            "example": {
                "topic": "Python编程基础",
                "knowledge_doc_ids": [1, 2],
                "exercise_types": ["multiple_choice", "fill_blank"],
                "difficulty": "medium",
                "question_count": 10,
                "auto_save": True,
                "course_id": 1
            }
        }


class KnowledgeSource(BaseModel):
    """知识来源信息模式"""
    doc_id: int = Field(..., description="文档ID")
    title: str = Field(..., description="文档标题")
    relevance_score: float = Field(..., description="相关度分数")


class GenerationInfo(BaseModel):
    """生成信息模式"""
    topic: str = Field(..., description="主题")
    difficulty: str = Field(..., description="难度级别")
    knowledge_docs_used: int = Field(..., description="使用的知识库文档数量")
    generated_at: str = Field(..., description="生成时间")


class CourseGenerationInfo(GenerationInfo):
    """课程生成信息模式"""
    lesson_count: int = Field(..., description="课时数量")


class ExerciseGenerationInfo(GenerationInfo):
    """习题生成信息模式"""
    question_count: int = Field(..., description="题目数量")
    exercise_types: List[str] = Field(..., description="题目类型列表")


class SavedCourseInfo(BaseModel):
    """保存的课程信息模式"""
    course_id: int = Field(..., description="课程ID")
    course_title: str = Field(..., description="课程标题")
    lessons_count: int = Field(..., description="课时数量")
    lessons: List[Dict[str, Any]] = Field(..., description="课时列表")


class SavedExerciseInfo(BaseModel):
    """保存的习题信息模式"""
    exercise_id: int = Field(..., description="习题集ID")
    exercise_title: str = Field(..., description="习题集标题")
    questions_count: int = Field(..., description="题目数量")
    questions: List[Dict[str, Any]] = Field(..., description="题目列表")


class KnowledgeCourseGenerationResponse(BaseModel):
    """基于知识库生成课程响应模式"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    course_data: Dict[str, Any] = Field(..., description="生成的课程数据")
    saved_course: Optional[SavedCourseInfo] = Field(None, description="保存的课程信息")
    knowledge_sources: List[KnowledgeSource] = Field(..., description="知识来源列表")
    generation_info: CourseGenerationInfo = Field(..., description="生成信息")


class KnowledgeExerciseGenerationResponse(BaseModel):
    """基于知识库生成习题响应模式"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    exercise_data: Dict[str, Any] = Field(..., description="生成的习题数据")
    saved_exercise: Optional[SavedExerciseInfo] = Field(None, description="保存的习题信息")
    knowledge_sources: List[KnowledgeSource] = Field(..., description="知识来源列表")
    generation_info: ExerciseGenerationInfo = Field(..., description="生成信息")

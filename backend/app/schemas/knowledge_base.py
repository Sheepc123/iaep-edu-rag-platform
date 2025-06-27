"""
知识库相关的Pydantic模式
"""
from datetime import datetime
from typing import Optional, List
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

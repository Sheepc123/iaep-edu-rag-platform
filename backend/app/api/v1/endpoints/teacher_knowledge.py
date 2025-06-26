"""
教师知识库API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_teacher
from app.models.user import User
from app.services.teacher_knowledge_service import TeacherKnowledgeService
from app.schemas.knowledge_base import (
    KnowledgeDocumentList, KnowledgeSearchResult, UploadDocumentResponse,
    KnowledgeSearchRequest, DeleteDocumentResponse
)
from app.services.vector_service_simple import get_simple_vector_service

router = APIRouter()


@router.post("/upload", response_model=UploadDocumentResponse, summary="上传文档到知识库")
async def upload_document(
    file: UploadFile = File(..., description="PDF或Word文档"),
    category: str = Form("教材", description="文档分类"),
    tags: str = Form("", description="标签，逗号分隔"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    上传文档到教师个人知识库
    
    - **file**: 支持PDF (.pdf) 和Word (.docx, .doc) 格式
    - **category**: 文档分类（教材、参考书、论文、课件、习题集、其他）
    - **tags**: 标签，用逗号分隔，有助于搜索和组织
    - 文件大小限制: 100MB
    
    返回上传结果和文档ID
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请选择要上传的文件"
        )
    
    knowledge_service = TeacherKnowledgeService(db)
    result = await knowledge_service.upload_document(
        file=file,
        teacher_id=current_user.id,
        category=category,
        tags=tags if tags else None
    )
    
    return result


@router.get("/documents", response_model=KnowledgeDocumentList, summary="获取知识库文档列表")
async def get_documents(
    category: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    获取教师知识库文档列表
    
    - **category**: 可选，按分类筛选
    - **page**: 页码，从1开始
    - **size**: 每页数量，默认20
    
    返回分页的文档列表
    """
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 20
    
    knowledge_service = TeacherKnowledgeService(db)
    return knowledge_service.get_teacher_documents(
        teacher_id=current_user.id,
        category=category,
        page=page,
        size=size
    )


@router.post("/search", response_model=List[KnowledgeSearchResult], summary="搜索知识库文档")
async def search_documents(
    search_request: KnowledgeSearchRequest,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    搜索教师知识库文档
    
    - **query**: 搜索关键词，支持全文搜索
    - **limit**: 返回结果数量限制，默认10
    
    使用SQLite FTS5全文搜索，支持标题、内容、摘要搜索
    """
    if not search_request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="搜索关键词不能为空"
        )
    
    knowledge_service = TeacherKnowledgeService(db)
    return knowledge_service.search_documents(
        teacher_id=current_user.id,
        query=search_request.query,
        limit=search_request.limit
    )


@router.delete("/documents/{document_id}", response_model=DeleteDocumentResponse, summary="删除知识库文档")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    删除知识库文档（软删除）
    
    - **document_id**: 文档ID
    
    只能删除自己上传的文档
    """
    knowledge_service = TeacherKnowledgeService(db)
    success = knowledge_service.delete_document(
        document_id=document_id,
        teacher_id=current_user.id
    )
    
    return DeleteDocumentResponse(
        success=success,
        message="文档删除成功" if success else "文档删除失败"
    )


@router.get("/documents/{document_id}/content", summary="获取文档内容")
async def get_document_content(
    document_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    获取文档的文本内容
    
    - **document_id**: 文档ID
    
    返回文档的提取文本内容，用于AI处理
    """
    knowledge_service = TeacherKnowledgeService(db)
    content = knowledge_service.get_document_content(
        document_id=document_id,
        teacher_id=current_user.id
    )
    
    return {
        "document_id": document_id,
        "content": content
    }


@router.get("/categories", summary="获取文档分类列表")
async def get_categories():
    """
    获取支持的文档分类列表
    """
    categories = [
        {"value": "教材", "label": "教材", "description": "教学用书、课本"},
        {"value": "参考书", "label": "参考书", "description": "参考资料、辅导书"},
        {"value": "论文", "label": "论文", "description": "学术论文、研究报告"},
        {"value": "课件", "label": "课件", "description": "PPT、讲义"},
        {"value": "习题集", "label": "习题集", "description": "练习题、试卷"},
        {"value": "其他", "label": "其他", "description": "其他类型文档"}
    ]
    
    return {
        "categories": categories
    }


@router.get("/stats", summary="获取知识库统计信息")
async def get_knowledge_stats(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    获取教师知识库统计信息
    
    返回文档数量、总大小、分类统计等信息
    """
    knowledge_service = TeacherKnowledgeService(db)
    
    # 获取所有文档
    all_docs = knowledge_service.get_teacher_documents(
        teacher_id=current_user.id,
        page=1,
        size=1000  # 获取所有文档用于统计
    )
    
    # 计算统计信息
    total_docs = all_docs.total
    total_size = sum(doc.file_size for doc in all_docs.documents)
    
    # 按分类统计
    category_stats = {}
    for doc in all_docs.documents:
        category = doc.category or "其他"
        if category not in category_stats:
            category_stats[category] = {"count": 0, "size": 0}
        category_stats[category]["count"] += 1
        category_stats[category]["size"] += doc.file_size
    
    # 本月上传统计
    from datetime import datetime, timedelta
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month_docs = [
        doc for doc in all_docs.documents 
        if doc.upload_time >= month_start
    ]
    
    return {
        "total_documents": total_docs,
        "total_size": total_size,
        "this_month_uploads": len(this_month_docs),
        "category_stats": category_stats,
        "avg_document_size": total_size // total_docs if total_docs > 0 else 0
    }

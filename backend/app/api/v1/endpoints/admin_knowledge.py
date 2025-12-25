"""
管理员知识库API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.database import get_db
from app.api.dependencies import get_current_admin
from app.models.user import User
from app.models.knowledge_base import TeacherKnowledgeDoc
from app.schemas.knowledge_base import KnowledgeDocument

router = APIRouter()


@router.get("/all", summary="获取所有教师的知识库文档")
async def get_all_teachers_knowledge_base(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(50, ge=1, le=1000, description="每页数量"),
    teacher_id: Optional[int] = Query(None, description="筛选特定教师"),
    category: Optional[str] = Query(None, description="筛选分类"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取所有教师的知识库文档（管理员权限）
    
    - **page**: 页码，从1开始
    - **size**: 每页数量，最大1000
    - **teacher_id**: 可选，筛选特定教师的文档
    - **category**: 可选，筛选特定分类
    - **search**: 可选，搜索标题、内容或标签
    
    返回按教师分组的知识库文档列表
    """
    try:
        # 构建查询
        query = db.query(TeacherKnowledgeDoc).join(User, TeacherKnowledgeDoc.teacher_id == User.id)
        
        # 筛选条件
        if teacher_id:
            query = query.filter(TeacherKnowledgeDoc.teacher_id == teacher_id)
        
        if category:
            query = query.filter(TeacherKnowledgeDoc.category == category)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    TeacherKnowledgeDoc.title.ilike(search_term),
                    TeacherKnowledgeDoc.text_content.ilike(search_term),
                    TeacherKnowledgeDoc.summary.ilike(search_term),
                    TeacherKnowledgeDoc.tags.ilike(search_term)
                )
            )
        
        # 只获取活跃状态的文档
        query = query.filter(TeacherKnowledgeDoc.status == "active")
        
        # 排序
        query = query.order_by(desc(TeacherKnowledgeDoc.upload_time))
        
        # 分页
        offset = (page - 1) * size
        documents = query.offset(offset).limit(size).all()
        
        # 获取总数
        total = query.count()
        
        # 转换为响应格式，包含教师信息
        documents_with_teacher = []
        for doc in documents:
            doc_dict = {
                "id": doc.id,
                "title": doc.title,
                "filename": doc.filename,
                "file_path": doc.file_path,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "text_content": doc.text_content,
                "summary": doc.summary,
                "category": doc.category,
                "tags": doc.tags,
                "upload_time": doc.upload_time.isoformat() if doc.upload_time else None,
                "status": doc.status,
                "teacher_id": doc.teacher_id,
                "teacher": {
                    "id": doc.teacher.id,
                    "username": doc.teacher.username,
                    "full_name": doc.teacher.full_name,
                    "email": doc.teacher.email
                } if doc.teacher else None
            }
            documents_with_teacher.append(doc_dict)
        
        return {
            "documents": documents_with_teacher,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取知识库数据失败: {str(e)}"
        )


@router.get("/stats", summary="获取知识库统计信息")
async def get_knowledge_base_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取知识库统计信息（管理员权限）
    
    返回知识库的总体统计数据
    """
    try:
        # 总文档数
        total_documents = db.query(TeacherKnowledgeDoc).filter(
            TeacherKnowledgeDoc.status == "active"
        ).count()
        
        # 总教师数（有知识库文档的）
        total_teachers = db.query(TeacherKnowledgeDoc.teacher_id).filter(
            TeacherKnowledgeDoc.status == "active"
        ).distinct().count()
        
        # 总文件大小
        total_size_result = db.query(func.sum(TeacherKnowledgeDoc.file_size)).filter(
            TeacherKnowledgeDoc.status == "active"
        ).scalar()
        total_size = total_size_result or 0
        
        # 所有分类
        categories_result = db.query(TeacherKnowledgeDoc.category).filter(
            TeacherKnowledgeDoc.status == "active",
            TeacherKnowledgeDoc.category.isnot(None)
        ).distinct().all()
        categories = [cat[0] for cat in categories_result if cat[0]]
        
        # 按教师统计
        teacher_stats = db.query(
            User.id,
            User.username,
            User.full_name,
            func.count(TeacherKnowledgeDoc.id).label('doc_count'),
            func.sum(TeacherKnowledgeDoc.file_size).label('total_size')
        ).join(
            TeacherKnowledgeDoc, User.id == TeacherKnowledgeDoc.teacher_id
        ).filter(
            TeacherKnowledgeDoc.status == "active"
        ).group_by(User.id).all()
        
        teacher_statistics = []
        for stat in teacher_stats:
            teacher_statistics.append({
                "teacher_id": stat.id,
                "teacher_username": stat.username,
                "teacher_name": stat.full_name,
                "document_count": stat.doc_count,
                "total_size": stat.total_size or 0
            })
        
        return {
            "total_documents": total_documents,
            "total_teachers": total_teachers,
            "total_size": total_size,
            "categories": categories,
            "teacher_statistics": teacher_statistics
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}"
        )


@router.get("/{doc_id}", summary="获取知识库文档详情")
async def get_knowledge_document_detail(
    doc_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取知识库文档详情（管理员权限）
    """
    try:
        document = db.query(TeacherKnowledgeDoc).join(
            User, TeacherKnowledgeDoc.teacher_id == User.id
        ).filter(TeacherKnowledgeDoc.id == doc_id).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文档不存在"
            )
        
        return {
            "id": document.id,
            "title": document.title,
            "filename": document.filename,
            "file_path": document.file_path,
            "file_type": document.file_type,
            "file_size": document.file_size,
            "text_content": document.text_content,
            "summary": document.summary,
            "category": document.category,
            "tags": document.tags,
            "upload_time": document.upload_time.isoformat() if document.upload_time else None,
            "status": document.status,
            "teacher_id": document.teacher_id,
            "teacher": {
                "id": document.teacher.id,
                "username": document.teacher.username,
                "full_name": document.teacher.full_name,
                "email": document.teacher.email
            } if document.teacher else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文档详情失败: {str(e)}"
        )


@router.delete("/{doc_id}", summary="删除知识库文档")
async def delete_knowledge_document(
    doc_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    删除知识库文档（管理员权限）
    """
    try:
        document = db.query(TeacherKnowledgeDoc).filter(
            TeacherKnowledgeDoc.id == doc_id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文档不存在"
            )
        
        # 软删除：设置状态为deleted
        document.status = "deleted"
        db.commit()
        
        return {"message": "文档删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除文档失败: {str(e)}"
        )

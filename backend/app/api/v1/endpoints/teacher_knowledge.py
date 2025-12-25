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
    KnowledgeSearchRequest, DeleteDocumentResponse, SemanticSearchRequest, SemanticSearchResult
)
from app.services.vector_service_deepseek import get_deepseek_vector_service
from app.services.vector_service_simple import get_simple_vector_service
from app.services.ai_knowledge_generator import AIKnowledgeGenerator

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


@router.post("/semantic-search", response_model=List[SemanticSearchResult], summary="DeepSeek语义搜索")
async def semantic_search(
    request: SemanticSearchRequest,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    DeepSeek增强的语义搜索

    - **query**: 搜索查询文本
    - **top_k**: 返回结果数量（默认5）
    - **category**: 分类过滤（可选）
    - **tags**: 标签过滤（可选）

    使用DeepSeek AI进行关键词提取，结合TF-IDF向量化实现高质量语义搜索
    """
    vector_service = get_deepseek_vector_service()

    if not vector_service.is_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="DeepSeek语义搜索服务不可用，请检查API配置"
        )

    # 构建元数据过滤条件
    filter_metadata = {}

    # 临时注释掉教师ID过滤用于调试
    # filter_metadata = {"teacher_id": current_user.id}

    if request.category:
        filter_metadata["category"] = request.category

    # 执行语义搜索
    try:
        results = vector_service.search_similar(
            query=request.query,
            top_k=request.top_k,
            filter_metadata=filter_metadata
        )

        # 转换为响应格式
        search_results = []
        for result in results:
            metadata = result["metadata"]

            # 解析标签
            tags = None
            if metadata.get("tags"):
                if isinstance(metadata["tags"], str):
                    tags = [tag.strip() for tag in metadata["tags"].split(",") if tag.strip()]
                elif isinstance(metadata["tags"], list):
                    tags = metadata["tags"]

            search_results.append(SemanticSearchResult(
                document_id=metadata["doc_id"],
                title=metadata.get("title", "未知标题"),
                content=result["content"],
                similarity=result["similarity"],
                category=metadata.get("category"),
                tags=tags,
                file_type=metadata.get("file_type"),
                enhanced_by=metadata.get("enhanced_by", "deepseek")
            ))

        return search_results

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"语义搜索失败: {str(e)}"
        )


@router.get("/vector-stats", summary="获取向量数据库统计")
async def get_vector_stats(
    current_user: User = Depends(get_current_teacher)
):
    """
    获取向量数据库统计信息

    返回向量集合的统计数据，包括总向量数、模型信息等
    """
    vector_service = get_deepseek_vector_service()

    if not vector_service.is_available():
        return {
            "available": False,
            "message": "DeepSeek向量服务不可用"
        }

    try:
        stats = vector_service.get_collection_stats()
        return {
            "available": True,
            "stats": stats
        }
    except Exception as e:
        return {
            "available": False,
            "message": f"获取统计信息失败: {str(e)}"
        }


@router.post("/generate-course", summary="基于知识库生成课程")
async def generate_course_from_knowledge(
    topic: str = Form(..., description="课程主题"),
    knowledge_doc_ids: Optional[str] = Form(None, description="知识库文档ID列表，逗号分隔"),
    course_level: str = Form("medium", description="课程难度级别"),
    lesson_count: int = Form(8, description="课时数量"),
    auto_save: bool = Form(False, description="是否自动保存课程"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    基于知识库文档生成课程

    - **topic**: 课程主题
    - **knowledge_doc_ids**: 指定的知识库文档ID列表（可选，逗号分隔）
    - **course_level**: 课程难度级别 (easy/medium/hard)
    - **lesson_count**: 课时数量
    - **auto_save**: 是否自动保存生成的课程

    如果不指定knowledge_doc_ids，系统会自动搜索相关文档
    """
    try:
        # 解析文档ID列表
        doc_ids = None
        if knowledge_doc_ids:
            try:
                doc_ids = [int(id.strip()) for id in knowledge_doc_ids.split(',') if id.strip()]
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="文档ID格式错误，请使用逗号分隔的数字"
                )

        # 创建AI知识库生成器
        ai_generator = AIKnowledgeGenerator(db)

        # 生成课程
        result = await ai_generator.generate_course_from_knowledge(
            teacher_id=current_user.id,
            topic=topic,
            knowledge_doc_ids=doc_ids,
            course_level=course_level,
            lesson_count=lesson_count,
            auto_save=auto_save
        )

        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"课程生成失败: {str(e)}"
        )


@router.post("/generate-exercises", summary="基于知识库生成习题")
async def generate_exercises_from_knowledge(
    topic: str = Form(..., description="习题主题"),
    knowledge_doc_ids: Optional[str] = Form(None, description="知识库文档ID列表，逗号分隔"),
    exercise_types: str = Form("multiple_choice,fill_blank,essay", description="题目类型，逗号分隔"),
    difficulty: str = Form("medium", description="难度级别"),
    question_count: int = Form(10, description="题目数量"),
    auto_save: bool = Form(False, description="是否自动保存习题"),
    course_id: Optional[int] = Form(None, description="关联的课程ID"),
    exercise_category: str = Form("自主练习", description="习题分类"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    基于知识库文档生成习题

    - **topic**: 习题主题
    - **knowledge_doc_ids**: 指定的知识库文档ID列表（可选，逗号分隔）
    - **exercise_types**: 题目类型列表，逗号分隔 (multiple_choice/fill_blank/essay/true_false)
    - **difficulty**: 难度级别 (easy/medium/hard)
    - **question_count**: 题目数量
    - **auto_save**: 是否自动保存生成的习题
    - **course_id**: 关联的课程ID（可选）

    如果不指定knowledge_doc_ids，系统会自动搜索相关文档
    """
    try:
        # 解析文档ID列表
        doc_ids = None
        if knowledge_doc_ids:
            try:
                doc_ids = [int(id.strip()) for id in knowledge_doc_ids.split(',') if id.strip()]
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="文档ID格式错误，请使用逗号分隔的数字"
                )

        # 解析题目类型列表
        types_list = [t.strip() for t in exercise_types.split(',') if t.strip()]
        if not types_list:
            types_list = ["multiple_choice", "fill_blank", "essay"]

        # 验证题目类型
        valid_types = ["multiple_choice", "fill_blank", "essay", "true_false"]
        for t in types_list:
            if t not in valid_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"不支持的题目类型: {t}，支持的类型: {', '.join(valid_types)}"
                )

        # 创建AI知识库生成器
        ai_generator = AIKnowledgeGenerator(db)

        # 生成习题
        result = await ai_generator.generate_exercises_from_knowledge(
            teacher_id=current_user.id,
            topic=topic,
            knowledge_doc_ids=doc_ids,
            exercise_types=types_list,
            difficulty=difficulty,
            question_count=question_count,
            auto_save=auto_save,
            course_id=course_id,
            exercise_category=exercise_category
        )

        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"习题生成失败: {str(e)}"
        )

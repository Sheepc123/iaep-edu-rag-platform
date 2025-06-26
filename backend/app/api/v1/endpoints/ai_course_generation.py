"""
AI课程生成API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Any, Optional
from loguru import logger

from ....core.database import get_db
from ....api.dependencies import get_current_teacher
from ....models.user import User
from ....services.document_processor import DocumentProcessor
from ....services.ai_course_generator import AICourseGenerator
from ....services.course_service import CourseService
from ....schemas.course import CourseCreate, CourseResponse

router = APIRouter()


@router.post("/upload-document", summary="上传文档并提取内容")
async def upload_document(
    file: UploadFile = File(..., description="PDF或Word文档"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    上传PDF或Word文档并提取文本内容
    
    - **file**: 支持PDF (.pdf) 和Word (.docx, .doc) 格式
    - 文件大小限制: 10MB
    
    返回提取的文本内容和文档信息
    """
    try:
        # 验证文件
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请选择要上传的文件"
            )
        
        logger.info(f"教师 {current_user.id} 上传文档: {file.filename}")
        
        # 处理文档
        document_processor = DocumentProcessor()
        document_info = await document_processor.extract_text(file)
        
        # 获取文档摘要
        summary = document_processor.get_document_summary(document_info["text_content"])
        
        return {
            "success": True,
            "message": "文档上传成功",
            "document_info": {
                **document_info,
                "summary": summary
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"文档上传失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="文档上传失败"
        )


@router.post("/generate-course", summary="根据文档内容生成课程")
async def generate_course_from_document(
    file: UploadFile = File(..., description="PDF或Word文档"),
    auto_save: bool = Form(False, description="是否自动保存生成的课程"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    根据上传的文档内容智能生成课程结构
    
    - **file**: 支持PDF (.pdf) 和Word (.docx, .doc) 格式
    - **auto_save**: 是否自动保存生成的课程到数据库
    
    返回生成的课程结构，包括课程信息和课时安排
    """
    try:
        # 验证文件
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请选择要上传的文件"
            )
        
        logger.info(f"教师 {current_user.id} 请求AI生成课程: {file.filename}")
        
        # 1. 提取文档内容
        document_processor = DocumentProcessor()
        document_info = await document_processor.extract_text(file)
        
        # 2. 使用AI生成课程结构
        ai_generator = AICourseGenerator()
        generated_course = ai_generator.generate_course_from_text(
            document_info["text_content"],
            document_info["filename"]
        )
        
        # 3. 如果需要自动保存，保存到数据库
        saved_course = None
        if auto_save:
            try:
                # 转换为CourseCreate格式
                course_data = CourseCreate(
                    title=generated_course["title"],
                    description=generated_course["description"],
                    category=generated_course["category"],
                    difficulty=generated_course["difficulty"],
                    duration=generated_course["duration"],
                    cover_image=generated_course.get("cover_image", ""),
                    is_published=False  # 默认不发布
                )
                
                # 保存课程
                course_service = CourseService(db)
                saved_course = course_service.create_course(course_data, current_user.id)
                
                logger.info(f"AI生成的课程已保存: {saved_course.id}")
                
            except Exception as save_error:
                logger.warning(f"自动保存课程失败: {str(save_error)}")
                # 不抛出异常，继续返回生成的课程数据
        
        return {
            "success": True,
            "message": "课程生成成功",
            "generated_course": generated_course,
            "saved_course_id": saved_course.id if saved_course else None,
            "document_info": {
                "filename": document_info["filename"],
                "word_count": document_info["word_count"],
                "char_count": document_info["char_count"]
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"AI课程生成失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI课程生成失败: {str(e)}"
        )


@router.post("/generate-course-preview", summary="预览AI生成的课程结构")
async def preview_generated_course(
    file: UploadFile = File(..., description="PDF或Word文档"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    预览AI生成的课程结构，不保存到数据库
    
    - **file**: 支持PDF (.pdf) 和Word (.docx, .doc) 格式
    
    返回生成的课程预览信息
    """
    try:
        # 验证文件
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请选择要上传的文件"
            )
        
        logger.info(f"教师 {current_user.id} 请求预览AI生成课程: {file.filename}")
        
        # 1. 提取文档内容
        document_processor = DocumentProcessor()
        document_info = await document_processor.extract_text(file)
        
        # 2. 使用AI生成课程结构
        ai_generator = AICourseGenerator()
        generated_course = ai_generator.generate_course_from_text(
            document_info["text_content"],
            document_info["filename"]
        )
        
        # 3. 生成预览摘要
        preview_summary = {
            "course_title": generated_course["title"],
            "course_description": generated_course["description"],
            "category": generated_course["category"],
            "difficulty": generated_course["difficulty"],
            "total_duration": generated_course["duration"],
            "total_lessons": len(generated_course["lessons"]),
            "lesson_titles": [lesson["title"] for lesson in generated_course["lessons"]],
            "estimated_complexity": generated_course["difficulty"],
            "source_document": {
                "filename": document_info["filename"],
                "word_count": document_info["word_count"],
                "estimated_reading_time": document_info["word_count"] // 200
            }
        }
        
        return {
            "success": True,
            "message": "课程预览生成成功",
            "preview": preview_summary,
            "full_course_data": generated_course
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"课程预览生成失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"课程预览生成失败: {str(e)}"
        )


@router.get("/supported-formats", summary="获取支持的文档格式")
async def get_supported_formats() -> Any:
    """
    获取支持的文档格式和限制信息
    """
    return {
        "supported_formats": [
            {
                "extension": ".pdf",
                "description": "PDF文档",
                "mime_types": ["application/pdf"]
            },
            {
                "extension": ".docx", 
                "description": "Word文档 (新版)",
                "mime_types": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
            },
            {
                "extension": ".doc",
                "description": "Word文档 (旧版)",
                "mime_types": ["application/msword"]
            }
        ],
        "limitations": {
            "max_file_size": "10MB",
            "max_file_size_bytes": 10 * 1024 * 1024,
            "processing_timeout": "60秒"
        },
        "features": [
            "智能提取文档内容",
            "自动生成课程标题和描述",
            "智能划分课程章节",
            "估算课程难度和时长",
            "支持课程预览和编辑"
        ]
    }

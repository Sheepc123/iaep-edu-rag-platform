"""
课程管理API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from loguru import logger

from ....core.database import get_db
from ....schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse, CourseListQuery,
    LessonCreate, LessonUpdate, LessonResponse,
    CourseEnrollRequest, CourseEnrollResponse,
    LessonProgressUpdate, LessonProgressResponse,
    CourseRatingCreate, CourseStatistics
)
from ....services.course_service import CourseService
from ....services.course_service import LessonService
from ....models.user import User
from ...dependencies import (
    get_current_active_user, get_current_student, get_current_teacher,
    get_pagination_params, get_optional_user
)


router = APIRouter()


# 课程管理端点
@router.post("/", response_model=CourseResponse, summary="创建课程")
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    创建新课程（教师功能）

    - **title**: 课程标题
    - **description**: 课程描述
    - **category**: 课程分类
    - **difficulty**: 难度级别 (easy/medium/hard)
    - **duration**: 课程总时长(分钟)
    - **cover_image**: 封面图片URL
    - **is_published**: 是否发布
    """
    try:
        course_service = CourseService(db)
        course = course_service.create_course(course_data, current_user.id)
        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建课程失败"
        )


@router.get("/", response_model=dict, summary="获取课程列表")
async def get_courses(
    category: Optional[str] = Query(None, description="课程分类"),
    difficulty: Optional[str] = Query(None, description="难度级别"),
    instructor_id: Optional[int] = Query(None, description="教师ID"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_published: Optional[bool] = Query(None, description="是否发布"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取课程列表

    支持分类、难度、教师、关键词搜索和分页
    """
    try:
        # 处理difficulty参数转换
        difficulty_enum = None
        if difficulty:
            try:
                from ....schemas.course import DifficultyLevel
                difficulty_enum = DifficultyLevel(difficulty)
            except ValueError:
                # 如果传入的difficulty值无效，忽略该参数
                difficulty_enum = None

        # 构建查询参数
        query = CourseListQuery(
            category=category,
            difficulty=difficulty_enum,
            instructor_id=instructor_id,
            search=search,
            is_published=is_published,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )

        course_service = CourseService(db)
        user_id = current_user.id if current_user else None
        courses, total = course_service.get_courses(query, user_id)

        # 将Course模型转换为CourseResponse格式
        course_responses = []
        for course in courses:
            course_responses.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "cover_image": course.cover_image,
                "category": course.category,
                "difficulty": course.difficulty,
                "duration": course.duration,
                "total_lessons": course.total_lessons,
                "instructor_id": course.instructor_id,
                "instructor_name": course.instructor_name,
                "enrolled_students": course.enrolled_students,
                "rating": course.rating,
                "rating_count": course.rating_count,
                "is_active": course.is_active,
                "is_published": course.is_published,
                "created_at": course.created_at,
                "updated_at": course.updated_at,
                "is_enrolled": getattr(course, 'is_enrolled', False),
                "enrollment_id": getattr(course, 'enrollment_id', None)
            })

        return {
            "courses": course_responses,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }

    except Exception as e:
        # 添加详细的错误日志
        logger.error(f"获取课程列表失败: {str(e)}")
        logger.error(f"请求参数: category={category}, difficulty={difficulty}, instructor_id={instructor_id}, search={search}, is_published={is_published}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取课程列表失败: {str(e)}"
        )


@router.get("/{course_id}", response_model=CourseResponse, summary="获取课程详情")
async def get_course(
    course_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """获取指定课程的详细信息"""
    try:
        course_service = CourseService(db)
        course = course_service.get_course_by_id(course_id)

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课程不存在"
            )

        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课程详情失败"
        )


@router.put("/{course_id}", response_model=CourseResponse, summary="更新课程")
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新课程信息（教师功能）

    只有课程创建者可以修改课程
    """
    try:
        course_service = CourseService(db)
        course = course_service.update_course(course_id, course_data, current_user.id)
        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新课程失败"
        )


@router.delete("/{course_id}", response_model=dict, summary="删除课程")
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    删除课程（教师功能）

    只有课程创建者可以删除课程，且课程不能有学生注册
    """
    try:
        course_service = CourseService(db)
        success = course_service.delete_course(course_id, current_user.id)

        return {
            "success": success,
            "message": "课程删除成功"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除课程失败"
        )


# 课程注册端点
@router.post("/{course_id}/enroll", response_model=CourseEnrollResponse, summary="注册课程")
async def enroll_course(
    course_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    学生注册课程

    - **course_id**: 课程ID
    """
    try:
        course_service = CourseService(db)
        enrollment = course_service.enroll_course(course_id, current_user.id)
        return enrollment

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册课程失败"
        )


@router.get("/my-courses", response_model=List[CourseEnrollResponse], summary="获取我的课程")
async def get_my_courses(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前学生注册的所有课程"""
    try:
        course_service = CourseService(db)
        enrollments = course_service.get_student_enrollments(current_user.id)
        return enrollments

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取我的课程失败"
        )


@router.get("/{course_id}/enrollment", response_model=CourseEnrollResponse, summary="获取课程注册信息")
async def get_course_enrollment(
    course_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取学生在指定课程的注册信息"""
    try:
        course_service = CourseService(db)
        enrollment = course_service.get_course_enrollment(course_id, current_user.id)

        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到课程注册信息"
            )

        return enrollment

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课程注册信息失败"
        )


@router.post("/{course_id}/rate", response_model=dict, summary="课程评分")
async def rate_course(
    course_id: int,
    rating_data: CourseRatingCreate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    学生对课程进行评分

    - **rating**: 评分 (1-5)
    - **review**: 评价内容
    """
    try:
        course_service = CourseService(db)
        course_service.rate_course(course_id, current_user.id, rating_data)

        return {
            "success": True,
            "message": "评分成功"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="课程评分失败"
        )


# 课时管理端点
@router.post("/{course_id}/lessons", response_model=LessonResponse, summary="创建课时")
async def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    在指定课程中创建课时（教师功能）

    - **title**: 课时标题
    - **description**: 课时描述
    - **content**: 课时内容
    - **lesson_order**: 课时顺序
    - **duration**: 课时时长(分钟)
    - **lesson_type**: 课时类型 (video/text/interactive/quiz)
    - **video_url**: 视频URL
    - **materials**: 学习材料
    - **is_published**: 是否发布
    - **is_free**: 是否免费
    """
    try:
        lesson_service = LessonService(db)
        lesson = lesson_service.create_lesson(course_id, lesson_data, current_user.id)
        return lesson

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建课时失败"
        )


@router.get("/{course_id}/lessons", response_model=List[LessonResponse], summary="获取课程课时列表")
async def get_course_lessons(
    course_id: int,
    include_unpublished: bool = Query(False, description="是否包含未发布的课时"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取指定课程的所有课时"""
    try:
        lesson_service = LessonService(db)

        # 检查权限：教师可以看到未发布的课时，学生只能看到已发布的
        if include_unpublished and current_user.role not in ["teacher", "admin"]:
            include_unpublished = False

        lessons = lesson_service.get_course_lessons(course_id, include_unpublished)
        return lessons

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课时列表失败"
        )


@router.get("/lessons/{lesson_id}", response_model=LessonResponse, summary="获取课时详情")
async def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """获取指定课时的详细信息"""
    try:
        lesson_service = LessonService(db)
        lesson = lesson_service.get_lesson_by_id(lesson_id)

        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课时不存在"
            )

        return lesson

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课时详情失败"
        )


@router.put("/lessons/{lesson_id}", response_model=LessonResponse, summary="更新课时")
async def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新课时信息（教师功能）

    只有课程创建者可以修改课时
    """
    try:
        lesson_service = LessonService(db)
        lesson = lesson_service.update_lesson(lesson_id, lesson_data, current_user.id)
        return lesson

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新课时失败"
        )


@router.delete("/lessons/{lesson_id}", response_model=dict, summary="删除课时")
async def delete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    删除课时（教师功能）

    只有课程创建者可以删除课时
    """
    try:
        lesson_service = LessonService(db)
        success = lesson_service.delete_lesson(lesson_id, current_user.id)

        return {
            "success": success,
            "message": "课时删除成功"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除课时失败"
        )


# 学习进度管理端点
@router.post("/lessons/{lesson_id}/progress", response_model=LessonProgressResponse, summary="更新课时学习进度")
async def update_lesson_progress(
    lesson_id: int,
    progress_data: LessonProgressUpdate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新课时学习进度（学生功能）

    - **progress_percentage**: 进度百分比 (0-100)
    - **watch_time**: 观看时间(秒)
    - **is_completed**: 是否完成
    - **notes**: 学习笔记
    """
    try:
        lesson_service = LessonService(db)
        progress = lesson_service.update_lesson_progress(
            lesson_id, current_user.id, progress_data
        )
        return progress

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新学习进度失败"
        )


@router.get("/lessons/{lesson_id}/progress", response_model=LessonProgressResponse, summary="获取课时学习进度")
async def get_lesson_progress(
    lesson_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前学生在指定课时的学习进度"""
    try:
        lesson_service = LessonService(db)
        progress = lesson_service.get_lesson_progress(lesson_id, current_user.id)

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到学习进度记录"
            )

        return progress

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学习进度失败"
        )


@router.get("/{course_id}/progress", response_model=List[LessonProgressResponse], summary="获取课程学习进度")
async def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前学生在指定课程中所有课时的学习进度"""
    try:
        lesson_service = LessonService(db)
        progresses = lesson_service.get_student_lesson_progresses(course_id, current_user.id)
        return progresses

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课程学习进度失败"
        )


# 统计信息端点
@router.get("/statistics", response_model=CourseStatistics, summary="获取课程统计信息")
async def get_course_statistics(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """获取课程统计信息（教师功能）"""
    try:
        course_service = CourseService(db)

        # 教师只能看到自己的课程统计，管理员可以看到全部
        instructor_id = None if current_user.role == "admin" else current_user.id

        statistics = course_service.get_course_statistics(instructor_id)
        return statistics

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计信息失败"
        )


# ==================== 教师端API端点 ====================

@router.get("/teacher/courses", response_model=List[CourseResponse], summary="获取教师课程列表")
async def get_teacher_courses(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    category: Optional[str] = Query(None, description="课程分类"),
    is_published: Optional[bool] = Query(None, description="发布状态"),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """获取教师的课程列表"""
    try:
        course_service = CourseService(db)
        courses, total = course_service.get_teacher_courses(
            teacher_id=current_user.id,
            skip=skip,
            limit=limit,
            search=search,
            category=category,
            is_published=is_published
        )

        return courses

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取教师课程列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课程列表失败"
        )


@router.post("/teacher/courses", response_model=CourseResponse, summary="创建课程")
async def create_teacher_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """创建新课程（教师功能）"""
    try:
        course_service = CourseService(db)
        course = course_service.create_course(course_data, current_user.id)

        logger.info(f"教师 {current_user.id} 创建了课程: {course.title}")
        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"创建课程失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建课程失败"
        )


@router.get("/teacher/courses/{course_id}", response_model=CourseResponse, summary="获取教师课程详情")
async def get_teacher_course_detail(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """获取教师课程详情"""
    try:
        course_service = CourseService(db)
        course = course_service.get_teacher_course_detail(course_id, current_user.id)

        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取教师课程详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取课程详情失败"
        )


@router.put("/teacher/courses/{course_id}", response_model=CourseResponse, summary="更新课程")
async def update_teacher_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """更新课程信息（教师功能）"""
    try:
        course_service = CourseService(db)
        course = course_service.update_teacher_course(course_id, current_user.id, course_data)

        logger.info(f"教师 {current_user.id} 更新了课程 {course_id}")
        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"更新课程失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新课程失败"
        )


@router.delete("/teacher/courses/{course_id}", response_model=dict, summary="删除课程")
async def delete_teacher_course(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """删除课程（教师功能）"""
    try:
        course_service = CourseService(db)
        success = course_service.delete_teacher_course(course_id, current_user.id)

        if success:
            logger.info(f"教师 {current_user.id} 删除了课程 {course_id}")
            return {"message": "课程删除成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="删除课程失败"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"删除课程失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除课程失败"
        )


@router.post("/teacher/courses/{course_id}/toggle-publish", response_model=CourseResponse, summary="切换课程发布状态")
async def toggle_course_publish(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """切换课程发布状态（教师功能）"""
    try:
        course_service = CourseService(db)
        course = course_service.toggle_course_publish(course_id, current_user.id)

        status_text = "发布" if course.is_published else "取消发布"
        logger.info(f"教师 {current_user.id} {status_text}了课程 {course_id}")

        return course

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"切换课程发布状态失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="操作失败"
        )


@router.get("/teacher/statistics", response_model=dict, summary="获取教师课程统计")
async def get_teacher_course_statistics(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """获取教师课程统计信息"""
    try:
        course_service = CourseService(db)
        statistics = course_service.get_teacher_course_statistics(current_user.id)

        return statistics

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取教师课程统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计信息失败"
        )

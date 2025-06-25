"""
练习系统API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from loguru import logger

from ....core.database import get_db
from ....schemas.exercise import (
    ExerciseCreate, ExerciseUpdate, ExerciseResponse, ExerciseDetailResponse,
    QuestionCreate, QuestionUpdate, QuestionResponse,
    ExerciseAttemptCreate, ExerciseAttemptResponse, ExerciseAttemptDetailResponse,
    StudentAnswerResponse, SubmitAnswerRequest, SubmitExerciseRequest, SubmitExerciseResponse,
    WrongQuestionResponse, ExerciseStatsResponse, DailyStatsResponse, ExerciseCategoryStatsResponse,
    ExerciseListQuery, QuestionListQuery, ExerciseCategory, DifficultyLevel
)
from ....services.exercise_service import ExerciseService
from ....models.user import User
from ...dependencies import (
    get_current_active_user, get_current_student, get_current_teacher,
    get_pagination_params
)

router = APIRouter()


# ==================== 练习管理端点 ====================

@router.post("/", response_model=ExerciseResponse, summary="创建练习")
async def create_exercise(
    exercise_data: ExerciseCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    创建新练习（教师功能）

    - **title**: 练习标题
    - **description**: 练习描述
    - **category**: 练习分类
    - **subject**: 科目
    - **difficulty**: 难度级别
    - **time_limit**: 时间限制(分钟)
    - **is_published**: 是否发布
    """
    try:
        exercise_service = ExerciseService(db)
        exercise = exercise_service.create_exercise(exercise_data, current_user.id)
        return exercise

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"创建练习失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建练习失败"
        )


@router.get("/", response_model=List[ExerciseResponse], summary="获取练习列表")
async def get_exercises(
    category: Optional[ExerciseCategory] = Query(None, description="练习分类"),
    subject: Optional[str] = Query(None, description="科目"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="难度级别"),
    is_published: Optional[bool] = Query(None, description="是否已发布"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取练习列表

    支持按分类、科目、难度等筛选
    """
    try:
        exercise_service = ExerciseService(db)

        query_params = ExerciseListQuery(
            category=category,
            subject=subject,
            difficulty=difficulty,
            is_published=is_published,
            page=page,
            page_size=page_size
        )

        exercises, total = exercise_service.get_exercises(query_params, current_user.id)

        return exercises

    except Exception as e:
        logger.error(f"获取练习列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取练习列表失败"
        )


@router.get("/{exercise_id}", response_model=ExerciseDetailResponse, summary="获取练习详情")
async def get_exercise_detail(
    exercise_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取练习详情，包含所有题目
    """
    try:
        exercise_service = ExerciseService(db)
        exercise = exercise_service.get_exercise_by_id(exercise_id, include_questions=True)

        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )

        # 检查访问权限
        if not exercise.is_published and exercise.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )

        return exercise

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取练习详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取练习详情失败"
        )


@router.put("/{exercise_id}", response_model=ExerciseResponse, summary="更新练习")
async def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新练习信息（教师功能）
    """
    try:
        exercise_service = ExerciseService(db)
        exercise = exercise_service.update_exercise(exercise_id, exercise_data, current_user.id)
        return exercise

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"更新练习失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新练习失败"
        )


@router.delete("/{exercise_id}", summary="删除练习")
async def delete_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    删除练习（软删除，教师功能）
    """
    try:
        exercise_service = ExerciseService(db)
        success = exercise_service.delete_exercise(exercise_id, current_user.id)

        if success:
            return {"message": "练习删除成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="删除练习失败"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"删除练习失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除练习失败"
        )


# ==================== 题目管理端点 ====================

@router.post("/{exercise_id}/questions", response_model=QuestionResponse, summary="添加题目")
async def create_question(
    exercise_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    向练习中添加题目（教师功能）
    """
    try:
        exercise_service = ExerciseService(db)

        # 设置练习ID
        question_data.exercise_id = exercise_id

        question = exercise_service.create_question(question_data, current_user.id)
        return question

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"创建题目失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建题目失败"
        )


@router.get("/{exercise_id}/questions", response_model=List[QuestionResponse], summary="获取练习题目")
async def get_exercise_questions(
    exercise_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取练习的所有题目
    """
    try:
        exercise_service = ExerciseService(db)

        # 验证练习存在和权限
        exercise = exercise_service.get_exercise_by_id(exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )

        if not exercise.is_published and exercise.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )

        query_params = QuestionListQuery(exercise_id=exercise_id, page=1, page_size=1000)
        questions, _ = exercise_service.get_questions(query_params)

        return questions

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取练习题目失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取练习题目失败"
        )


@router.put("/questions/{question_id}", response_model=QuestionResponse, summary="更新题目")
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新题目信息（教师功能）
    """
    try:
        exercise_service = ExerciseService(db)
        question = exercise_service.update_question(question_id, question_data, current_user.id)
        return question

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"更新题目失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新题目失败"
        )


@router.delete("/questions/{question_id}", summary="删除题目")
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    删除题目（软删除，教师功能）
    """
    try:
        exercise_service = ExerciseService(db)
        success = exercise_service.delete_question(question_id, current_user.id)

        if success:
            return {"message": "题目删除成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="删除题目失败"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"删除题目失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除题目失败"
        )


# ==================== 练习尝试端点 ====================

@router.post("/{exercise_id}/start", response_model=ExerciseAttemptResponse, summary="开始练习")
async def start_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    开始练习（学生功能）
    """
    try:
        exercise_service = ExerciseService(db)
        attempt = exercise_service.start_exercise_attempt(exercise_id, current_user.id)
        return attempt

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"开始练习失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="开始练习失败"
        )


@router.get("/attempts/{attempt_id}", response_model=ExerciseAttemptDetailResponse, summary="获取练习尝试详情")
async def get_exercise_attempt(
    attempt_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取练习尝试详情（学生功能）
    """
    try:
        exercise_service = ExerciseService(db)
        attempt = exercise_service.get_exercise_attempt(attempt_id, current_user.id)

        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习尝试不存在"
            )

        return attempt

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取练习尝试失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取练习尝试失败"
        )


# ==================== 答题提交端点 ====================

@router.post("/submit-answer", response_model=StudentAnswerResponse, summary="提交单个答案")
async def submit_answer(
    answer_data: SubmitAnswerRequest,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    提交单个题目的答案（学生功能）
    """
    try:
        exercise_service = ExerciseService(db)
        answer = exercise_service.submit_answer(answer_data, current_user.id)
        return answer

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"提交答案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="提交答案失败"
        )


@router.post("/submit-exercise", response_model=SubmitExerciseResponse, summary="提交整个练习")
async def submit_exercise(
    submit_data: SubmitExerciseRequest,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    提交整个练习（学生功能）
    """
    try:
        exercise_service = ExerciseService(db)
        attempt = exercise_service.submit_exercise(submit_data, current_user.id)

        # 构建响应数据
        response = SubmitExerciseResponse(
            attempt_id=attempt.id,
            total_questions=attempt.total_questions,
            answered_questions=attempt.answered_questions,
            correct_answers=attempt.correct_answers,
            score=attempt.score,
            max_score=attempt.max_score,
            accuracy_rate=attempt.accuracy_rate,
            time_spent=attempt.time_spent,
            submitted_at=attempt.submitted_at
        )

        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"提交练习失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="提交练习失败"
        )


# ==================== 学生练习记录端点 ====================

@router.get("/my-attempts", response_model=List[ExerciseAttemptResponse], summary="获取我的练习记录")
async def get_my_attempts(
    exercise_id: Optional[int] = Query(None, description="练习ID"),
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取当前学生的练习记录
    """
    try:
        exercise_service = ExerciseService(db)
        attempts = exercise_service.get_student_attempts(current_user.id, exercise_id)
        return attempts

    except Exception as e:
        logger.error(f"获取练习记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取练习记录失败"
        )


# ==================== 错题本端点 ====================

@router.get("/wrong-questions", response_model=List[WrongQuestionResponse], summary="获取错题本")
async def get_wrong_questions(
    subject: Optional[str] = Query(None, description="科目筛选"),
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取学生错题本
    """
    try:
        exercise_service = ExerciseService(db)
        wrong_questions = exercise_service.get_wrong_questions(current_user.id, subject)
        return wrong_questions

    except Exception as e:
        logger.error(f"获取错题本失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取错题本失败"
        )


@router.post("/wrong-questions/{question_id}/master", summary="标记题目已掌握")
async def mark_question_mastered(
    question_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    标记错题已掌握
    """
    try:
        exercise_service = ExerciseService(db)
        success = exercise_service.mark_question_mastered(current_user.id, question_id)

        if success:
            return {"message": "标记成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="错题记录不存在"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"标记题目掌握失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="标记失败"
        )


@router.post("/wrong-questions/{question_id}/review", summary="复习错题")
async def review_wrong_question(
    question_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    记录错题复习
    """
    try:
        exercise_service = ExerciseService(db)
        success = exercise_service.review_wrong_question(current_user.id, question_id)

        if success:
            return {"message": "复习记录成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="错题记录不存在"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"记录错题复习失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="记录复习失败"
        )


# ==================== 统计分析端点 ====================

@router.get("/stats", response_model=ExerciseStatsResponse, summary="获取练习统计")
async def get_exercise_stats(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取学生练习统计数据
    """
    try:
        exercise_service = ExerciseService(db)
        stats = exercise_service.get_exercise_stats(current_user.id)
        return ExerciseStatsResponse(**stats)

    except Exception as e:
        logger.error(f"获取练习统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取练习统计失败"
        )


@router.get("/stats/daily", response_model=DailyStatsResponse, summary="获取每日统计")
async def get_daily_stats(
    date: Optional[str] = Query(None, description="日期(YYYY-MM-DD)，默认今天"),
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取指定日期的练习统计
    """
    try:
        from datetime import datetime

        if date:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        else:
            target_date = datetime.now()

        exercise_service = ExerciseService(db)
        stats = exercise_service.get_daily_stats(current_user.id, target_date)
        return DailyStatsResponse(**stats)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="日期格式错误，请使用YYYY-MM-DD格式"
        )
    except Exception as e:
        logger.error(f"获取每日统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取每日统计失败"
        )


@router.get("/stats/categories", response_model=List[ExerciseCategoryStatsResponse], summary="获取分类统计")
async def get_category_stats(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取按练习分类的统计数据
    """
    try:
        exercise_service = ExerciseService(db)
        stats = exercise_service.get_category_stats(current_user.id)
        return [ExerciseCategoryStatsResponse(**stat) for stat in stats]

    except Exception as e:
        logger.error(f"获取分类统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取分类统计失败"
        )


@router.get("/stats/progress", summary="获取学习进度")
async def get_learning_progress(
    days: int = Query(30, ge=1, le=365, description="统计天数"),
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取学习进度趋势数据
    """
    try:
        exercise_service = ExerciseService(db)
        progress = exercise_service.get_learning_progress(current_user.id, days)
        return {"progress": progress}

    except Exception as e:
        logger.error(f"获取学习进度失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学习进度失败"
        )

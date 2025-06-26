"""
成绩分析API端点
"""
from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
import io

from ....core.database import get_db
from ....api.dependencies import get_current_teacher
from ....models.user import User
from ....models.exercise import Exercise
from ....services.grade_analysis_service import GradeAnalysisService
from ....services.grade_export_service import GradeExportService
from ....schemas.grade_analysis import (
    GradeAnalysisResponse,
    TeacherGradeOverviewResponse,
    ClassReportResponse,
    StudentPerformanceResponse
)

router = APIRouter()


@router.get("/exercise/{exercise_id}/analysis", response_model=GradeAnalysisResponse, summary="分析练习成绩")
async def analyze_exercise_grades(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    分析指定练习的成绩情况
    
    - **exercise_id**: 练习ID
    
    返回详细的成绩分析结果，包括：
    - 基础统计信息
    - 分数分布
    - 题目分析
    - 时间分析
    - 学生表现
    """
    try:
        # 验证练习是否存在且属于当前教师
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )
        
        if exercise.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )
        
        # 执行成绩分析
        grade_service = GradeAnalysisService(db)
        analysis_result = grade_service.analyze_exercise_grades(exercise_id, current_user.id)
        
        return analysis_result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="分析成绩时发生错误"
        )


@router.get("/overview", response_model=TeacherGradeOverviewResponse, summary="获取教师成绩概览")
async def get_teacher_grade_overview(
    days: int = Query(30, description="统计天数", ge=1, le=365),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取教师的成绩概览信息
    
    - **days**: 统计最近多少天的数据（默认30天）
    
    返回：
    - 成绩统计
    - 趋势数据
    - 科目分析
    - 最近活动
    """
    try:
        grade_service = GradeAnalysisService(db)
        overview_data = grade_service.get_teacher_grade_overview(current_user.id, days)
        
        return overview_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取概览数据时发生错误"
        )


@router.post("/exercise/{exercise_id}/report", response_model=ClassReportResponse, summary="生成班级成绩报告")
async def generate_class_report(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    生成指定练习的班级成绩报告
    
    - **exercise_id**: 练习ID
    
    返回完整的班级成绩分析报告
    """
    try:
        # 验证练习权限
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )
        
        if exercise.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )
        
        # 生成报告
        grade_service = GradeAnalysisService(db)
        report_data = grade_service.generate_class_report(exercise_id, current_user.id)
        
        return report_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="生成报告时发生错误"
        )


@router.get("/exercise/{exercise_id}/students", response_model=List[StudentPerformanceResponse], summary="获取学生表现详情")
async def get_student_performance(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取指定练习中所有学生的详细表现
    
    - **exercise_id**: 练习ID
    
    返回学生表现列表，按成绩排序
    """
    try:
        # 验证练习权限
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )
        
        if exercise.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )
        
        # 获取学生表现数据
        grade_service = GradeAnalysisService(db)
        analysis_result = grade_service.analyze_exercise_grades(exercise_id, current_user.id)
        
        return analysis_result["student_performance"]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学生表现数据时发生错误"
        )


@router.get("/statistics/summary", summary="获取成绩统计摘要")
async def get_grade_statistics_summary(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取教师的成绩统计摘要信息
    
    返回：
    - 总体统计
    - 最新动态
    - 需要关注的问题
    """
    try:
        grade_service = GradeAnalysisService(db)
        
        # 获取最近30天的概览数据
        overview_data = grade_service.get_teacher_grade_overview(current_user.id, 30)
        
        # 提取关键统计信息
        grade_stats = overview_data["grade_stats"]
        
        # 计算一些额外的统计指标
        summary = {
            "total_students": grade_stats["total_students"],
            "total_exercises": grade_stats["total_exercises"],
            "total_attempts": grade_stats["total_attempts"],
            "average_score": round(grade_stats["average_score"], 2),
            "average_percentage": round(grade_stats["average_percentage"], 2),
            "recent_activities_count": len(overview_data["recent_activities"]),
            "subject_count": len(overview_data["subject_analysis"]),
            "trend_days": len(overview_data["trend_data"])
        }
        
        # 添加表现等级
        avg_percentage = summary["average_percentage"]
        if avg_percentage >= 90:
            summary["performance_level"] = "优秀"
            summary["performance_color"] = "green"
        elif avg_percentage >= 80:
            summary["performance_level"] = "良好"
            summary["performance_color"] = "blue"
        elif avg_percentage >= 70:
            summary["performance_level"] = "中等"
            summary["performance_color"] = "yellow"
        elif avg_percentage >= 60:
            summary["performance_level"] = "及格"
            summary["performance_color"] = "orange"
        else:
            summary["performance_level"] = "需改进"
            summary["performance_color"] = "red"
        
        return {
            "summary": summary,
            "recent_activities": overview_data["recent_activities"][:5],  # 只返回最近5条
            "top_subjects": overview_data["subject_analysis"][:3]  # 只返回前3个科目
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计摘要时发生错误"
        )


@router.get("/trends", summary="获取成绩趋势数据")
async def get_grade_trends(
    days: int = Query(30, description="统计天数", ge=7, le=365),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取成绩趋势数据，用于图表展示
    
    - **days**: 统计天数
    
    返回按日期的成绩趋势数据
    """
    try:
        grade_service = GradeAnalysisService(db)
        overview_data = grade_service.get_teacher_grade_overview(current_user.id, days)
        
        return {
            "trend_data": overview_data["trend_data"],
            "period": f"最近{days}天",
            "data_points": len(overview_data["trend_data"])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取趋势数据时发生错误"
        )


@router.get("/exercise/{exercise_id}/export", summary="导出练习成绩Excel")
async def export_exercise_grades(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    导出指定练习的成绩数据到Excel文件

    - **exercise_id**: 练习ID

    返回Excel文件流
    """
    try:
        # 验证练习权限
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )

        if exercise.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )

        # 导出Excel
        export_service = GradeExportService(db)
        excel_data = export_service.export_exercise_grades_to_excel(exercise_id, current_user.id)

        # 创建文件名
        filename = f"{exercise.title}_成绩分析_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # 返回文件流
        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="导出文件时发生错误"
        )


@router.get("/overview/export", summary="导出教师概览Excel")
async def export_teacher_overview(
    days: int = Query(30, description="统计天数", ge=1, le=365),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    导出教师概览数据到Excel文件

    - **days**: 统计天数

    返回Excel文件流
    """
    try:
        # 导出Excel
        export_service = GradeExportService(db)
        excel_data = export_service.export_teacher_overview_to_excel(current_user.id, days)

        # 创建文件名
        filename = f"教师概览_{current_user.full_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # 返回文件流
        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="导出文件时发生错误"
        )


@router.get("/exercise/{exercise_id}/report/export", summary="导出班级报告Excel")
async def export_class_report(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    导出班级成绩报告到Excel文件

    - **exercise_id**: 练习ID

    返回Excel文件流
    """
    try:
        # 验证练习权限
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )

        if exercise.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )

        # 导出Excel
        export_service = GradeExportService(db)
        excel_data = export_service.export_class_report_to_excel(exercise_id, current_user.id)

        # 创建文件名
        filename = f"{exercise.title}_班级报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # 返回文件流
        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="导出文件时发生错误"
        )


@router.get("/exercise/{exercise_id}/answers/export", summary="导出学生答题详情Excel")
async def export_student_answers(
    exercise_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    导出学生答题详情到Excel文件

    - **exercise_id**: 练习ID

    返回包含每个学生详细答题情况的Excel文件
    """
    try:
        # 验证练习权限
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习不存在"
            )

        if exercise.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此练习"
            )

        # 导出Excel
        export_service = GradeExportService(db)
        excel_data = export_service.export_student_answers_to_excel(exercise_id, current_user.id)

        # 创建文件名
        filename = f"{exercise.title}_答题详情_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # 返回文件流
        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="导出文件时发生错误"
        )

"""
API v1 路由汇总
"""
from fastapi import APIRouter

from .endpoints import auth, users, courses, exercises, chat, ai, grade_analysis, ai_course_generation, teacher_knowledge

# 创建API路由器
api_router = APIRouter()

# 注册各模块路由
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"]
)

api_router.include_router(
    users.router,
    prefix="/users", 
    tags=["用户管理"]
)

api_router.include_router(
    courses.router,
    prefix="/courses",
    tags=["课程管理"]
)

api_router.include_router(
    exercises.router,
    prefix="/exercises",
    tags=["练习系统"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["聊天通信"]
)

api_router.include_router(
    ai.router,
    prefix="/ai",
    tags=["AI助手"]
)

api_router.include_router(
    grade_analysis.router,
    prefix="/grade-analysis",
    tags=["成绩分析"]
)

api_router.include_router(
    ai_course_generation.router,
    prefix="/ai-course",
    tags=["AI课程生成"]
)

api_router.include_router(
    teacher_knowledge.router,
    prefix="/teacher-knowledge",
    tags=["教师知识库"]
)

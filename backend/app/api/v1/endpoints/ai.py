"""
AI助手API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....core.database import get_db
from ....schemas.ai import (
    AIMessageCreate, AIMessageResponse, AIConversationCreate,
    AIConversationResponse, AIFeedbackCreate, AIUsageStats
)
from ....services.ai_service import AIService
from ....models.user import User
from ...dependencies import get_current_active_user

router = APIRouter()


def get_ai_service(db: Session = Depends(get_db)) -> AIService:
    """获取AI服务实例"""
    return AIService(db)


@router.post("/conversations", response_model=AIConversationResponse, summary="创建新对话")
async def create_conversation(
    conversation_data: AIConversationCreate,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    创建新的AI对话会话

    - **title**: 对话标题（可选）
    - **context**: 对话上下文（可选）
    """
    try:
        return await ai_service.create_conversation(current_user.id, conversation_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/conversations", response_model=List[AIConversationResponse], summary="获取对话列表")
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    获取当前用户的所有AI对话列表
    """
    try:
        return await ai_service.get_conversations(current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[AIMessageResponse], summary="获取对话消息")
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    获取指定对话的所有消息

    - **conversation_id**: 对话ID
    """
    try:
        return await ai_service.get_conversation_messages(current_user.id, conversation_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "不存在" in str(e) else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/messages", response_model=AIMessageResponse, summary="发送消息")
async def send_message(
    message_data: AIMessageCreate,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    发送消息给AI助手并获取回复

    - **content**: 消息内容
    - **conversation_id**: 对话ID（可选，不提供则创建新对话）
    - **message_type**: 消息类型
    - **context**: 额外上下文信息（可选）
    """
    try:
        return await ai_service.send_message(current_user.id, message_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/conversations/{conversation_id}", summary="删除对话")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    删除指定的对话

    - **conversation_id**: 对话ID
    """
    try:
        success = await ai_service.delete_conversation(current_user.id, conversation_id)
        if success:
            return {"message": "对话删除成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="删除对话失败"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "不存在" in str(e) else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/quick-actions", summary="获取快速操作")
async def get_quick_actions():
    """
    获取AI助手的快速操作列表
    """
    quick_actions = [
        {
            "id": "study_guidance",
            "title": "学习指导",
            "description": "获得个性化学习建议",
            "prompt": "请为我制定一个学习计划，我想提高数学成绩",
            "icon": "📚",
            "category": "学习"
        },
        {
            "id": "problem_solving",
            "title": "解题帮助",
            "description": "解答学习中的疑难问题",
            "prompt": "我在学习高等数学时遇到了困难，请帮我解答",
            "icon": "🤔",
            "category": "答疑"
        },
        {
            "id": "study_plan",
            "title": "制定计划",
            "description": "制定个性化学习计划",
            "prompt": "请帮我制定一个详细的学习计划",
            "icon": "📅",
            "category": "规划"
        },
        {
            "id": "exercise_recommend",
            "title": "练习推荐",
            "description": "推荐适合的练习题目",
            "prompt": "请为我推荐一些适合的练习题",
            "icon": "💪",
            "category": "练习"
        }
    ]

    return {"quick_actions": quick_actions}


@router.get("/health", summary="AI服务健康检查")
async def ai_health_check():
    """
    检查AI服务的健康状态
    """
    return {
        "status": "healthy",
        "service": "AI Assistant",
        "model": "deepseek-chat",
        "version": "1.0.0",
        "timestamp": "2024-06-25T00:00:00Z"
    }

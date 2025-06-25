"""
AI助手相关的Pydantic模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageSender(str, Enum):
    """消息发送者类型"""
    USER = "user"
    AI = "ai"


class MessageType(str, Enum):
    """消息类型"""
    TEXT = "text"
    IMAGE = "image"
    CODE = "code"
    SUGGESTION = "suggestion"


class AIMessageCreate(BaseModel):
    """创建AI消息的请求模型"""
    content: str = Field(..., min_length=1, max_length=2000, description="消息内容")
    conversation_id: Optional[int] = Field(None, description="对话ID，不提供则创建新对话")
    message_type: MessageType = Field(MessageType.TEXT, description="消息类型")
    context: Optional[Dict[str, Any]] = Field(None, description="额外上下文信息")


class AIMessageResponse(BaseModel):
    """AI消息响应模型"""
    id: int = Field(..., description="消息ID")
    conversation_id: int = Field(..., description="对话ID")
    content: str = Field(..., description="消息内容")
    sender: MessageSender = Field(..., description="发送者")
    message_type: MessageType = Field(..., description="消息类型")
    model_used: Optional[str] = Field(None, description="使用的AI模型")
    tokens_used: Optional[int] = Field(None, description="使用的token数量")
    response_time: Optional[float] = Field(None, description="响应时间(秒)")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True


class AIConversationCreate(BaseModel):
    """创建AI对话的请求模型"""
    title: Optional[str] = Field(None, max_length=200, description="对话标题")
    context: Optional[str] = Field(None, description="对话上下文")


class AIConversationUpdate(BaseModel):
    """更新AI对话的请求模型"""
    title: Optional[str] = Field(None, max_length=200, description="对话标题")
    context: Optional[str] = Field(None, description="对话上下文")


class AIConversationResponse(BaseModel):
    """AI对话响应模型"""
    id: int = Field(..., description="对话ID")
    title: str = Field(..., description="对话标题")
    context: Optional[str] = Field(None, description="对话上下文")
    message_count: int = Field(..., description="消息数量")
    total_tokens: int = Field(..., description="总token数量")
    is_active: bool = Field(..., description="是否活跃")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    last_message_at: Optional[datetime] = Field(None, description="最后消息时间")
    
    class Config:
        from_attributes = True


class AIConversationWithMessages(AIConversationResponse):
    """包含消息的AI对话响应模型"""
    messages: List[AIMessageResponse] = Field([], description="对话消息列表")


class AIStreamResponse(BaseModel):
    """AI流式响应模型"""
    conversation_id: int = Field(..., description="对话ID")
    message_id: int = Field(..., description="消息ID")
    content: str = Field(..., description="消息内容片段")
    is_complete: bool = Field(False, description="是否完成")
    tokens_used: Optional[int] = Field(None, description="使用的token数量")


class AIRecommendationType(str, Enum):
    """AI推荐类型"""
    COURSE = "course"
    EXERCISE = "exercise"
    STUDY_PLAN = "study_plan"
    LEARNING_PATH = "learning_path"


class AIRecommendationCreate(BaseModel):
    """创建AI推荐的请求模型"""
    recommendation_type: AIRecommendationType = Field(..., description="推荐类型")
    content: Dict[str, Any] = Field(..., description="推荐内容")
    reason: Optional[str] = Field(None, description="推荐理由")


class AIRecommendationResponse(BaseModel):
    """AI推荐响应模型"""
    id: int = Field(..., description="推荐ID")
    recommendation_type: AIRecommendationType = Field(..., description="推荐类型")
    content: Dict[str, Any] = Field(..., description="推荐内容")
    reason: Optional[str] = Field(None, description="推荐理由")
    is_accepted: Optional[bool] = Field(None, description="是否接受")
    is_helpful: Optional[bool] = Field(None, description="是否有帮助")
    feedback: Optional[str] = Field(None, description="用户反馈")
    is_active: bool = Field(..., description="是否活跃")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True


class AIFeedbackCreate(BaseModel):
    """AI反馈创建模型"""
    message_id: int = Field(..., description="消息ID")
    rating: Optional[int] = Field(None, ge=1, le=5, description="评分(1-5)")
    feedback: Optional[str] = Field(None, max_length=500, description="反馈内容")
    is_helpful: Optional[bool] = Field(None, description="是否有帮助")


class AIUsageStats(BaseModel):
    """AI使用统计模型"""
    total_conversations: int = Field(..., description="总对话数")
    total_messages: int = Field(..., description="总消息数")
    total_tokens: int = Field(..., description="总token数")
    avg_response_time: float = Field(..., description="平均响应时间")
    today_conversations: int = Field(..., description="今日对话数")
    today_messages: int = Field(..., description="今日消息数")
    today_tokens: int = Field(..., description="今日token数")


class QuickAction(BaseModel):
    """快速操作模型"""
    id: str = Field(..., description="操作ID")
    title: str = Field(..., description="操作标题")
    description: str = Field(..., description="操作描述")
    prompt: str = Field(..., description="操作提示词")
    icon: Optional[str] = Field(None, description="图标")
    category: Optional[str] = Field(None, description="分类")


class AISystemPrompt(BaseModel):
    """AI系统提示词模型"""
    role: str = Field(..., description="角色定义")
    context: str = Field(..., description="上下文信息")
    instructions: List[str] = Field(..., description="指令列表")
    examples: Optional[List[Dict[str, str]]] = Field(None, description="示例对话")


class AIErrorResponse(BaseModel):
    """AI错误响应模型"""
    error_code: str = Field(..., description="错误代码")
    error_message: str = Field(..., description="错误信息")
    suggestion: Optional[str] = Field(None, description="建议")
    retry_after: Optional[int] = Field(None, description="重试间隔(秒)")

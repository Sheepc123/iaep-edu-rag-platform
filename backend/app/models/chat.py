"""
聊天和AI助手相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class ChatRoom(Base):
    """聊天室模型"""
    __tablename__ = "chat_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 聊天室信息
    name = Column(String(100), nullable=True)
    room_type = Column(String(20), nullable=False)  # private, group, class
    description = Column(Text, nullable=True)
    
    # 创建者
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 统计信息
    member_count = Column(Integer, default=0)
    message_count = Column(Integer, default=0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    members = relationship("ChatMember", back_populates="room")
    messages = relationship("ChatMessage", back_populates="room")


class ChatMember(Base):
    """聊天室成员模型"""
    __tablename__ = "chat_members"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 成员角色
    role = Column(String(20), default="member")  # admin, member
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_muted = Column(Boolean, default=False)
    
    # 消息状态
    last_read_message_id = Column(Integer, nullable=True)
    unread_count = Column(Integer, default=0)
    
    # 时间戳
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    room = relationship("ChatRoom", back_populates="members")


class ChatMessage(Base):
    """聊天消息模型"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 消息内容
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, image, file, system
    
    # 文件信息 (如果是文件消息)
    file_url = Column(String(255), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    
    # 回复信息
    reply_to_id = Column(Integer, ForeignKey("chat_messages.id"), nullable=True)
    
    # 状态
    is_deleted = Column(Boolean, default=False)
    is_edited = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    room = relationship("ChatRoom", back_populates="messages")


class UserContact(Base):
    """用户联系人模型"""
    __tablename__ = "user_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 联系人信息
    nickname = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # 状态
    status = Column(String(20), default="active")  # active, blocked, pending
    is_favorite = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AIConversation(Base):
    """AI对话会话模型"""
    __tablename__ = "ai_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 会话信息
    title = Column(String(200), nullable=False)
    context = Column(Text, nullable=True)  # 会话上下文
    
    # 统计信息
    message_count = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    messages = relationship("AIMessage", back_populates="conversation")


class AIMessage(Base):
    """AI对话消息模型"""
    __tablename__ = "ai_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id"), nullable=False)
    
    # 消息内容
    content = Column(Text, nullable=False)
    sender = Column(String(10), nullable=False)  # user, ai
    message_type = Column(String(20), default="text")  # text, image, code
    
    # AI相关信息
    model_used = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    response_time = Column(Float, nullable=True)  # 响应时间(秒)
    
    # 用户反馈
    rating = Column(Integer, nullable=True)  # 1-5星评分
    feedback = Column(Text, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    conversation = relationship("AIConversation", back_populates="messages")


class AIRecommendation(Base):
    """AI推荐记录模型"""
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 推荐内容
    recommendation_type = Column(String(50), nullable=False)  # course, exercise, study_plan
    content = Column(JSON, nullable=False)  # 推荐内容详情
    reason = Column(Text, nullable=True)  # 推荐理由
    
    # 用户反馈
    is_accepted = Column(Boolean, nullable=True)
    is_helpful = Column(Boolean, nullable=True)
    feedback = Column(Text, nullable=True)
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserOnlineStatus(Base):
    """用户在线状态模型"""
    __tablename__ = "user_online_status"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # 状态信息
    status = Column(String(20), default="offline")  # online, offline, busy, away
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    
    # 设备信息
    device_type = Column(String(20), nullable=True)  # web, mobile, desktop
    ip_address = Column(String(45), nullable=True)
    
    # 时间戳
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

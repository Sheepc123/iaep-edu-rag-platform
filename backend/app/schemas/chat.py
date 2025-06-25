"""
聊天相关数据模式
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """消息类型枚举"""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"


class UserStatus(str, Enum):
    """用户状态枚举"""
    ONLINE = "online"
    BUSY = "busy"
    AWAY = "away"
    OFFLINE = "offline"


class RoomType(str, Enum):
    """聊天室类型枚举"""
    PRIVATE = "private"
    GROUP = "group"
    CLASS = "class"


# ==================== 基础模式 ====================

class ContactBase(BaseModel):
    """联系人基础模式"""
    user_id: int
    full_name: str
    avatar_url: Optional[str] = None
    role: str  # teacher, student
    status: UserStatus = UserStatus.OFFLINE
    last_seen: Optional[datetime] = None


class ContactResponse(ContactBase):
    """联系人响应模式"""
    id: int
    unread_count: int = 0
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    """消息基础模式"""
    content: str = Field(..., min_length=1, max_length=2000)
    message_type: MessageType = MessageType.TEXT
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    reply_to_id: Optional[int] = None


class MessageCreate(MessageBase):
    """创建消息请求"""
    receiver_id: Optional[int] = None  # 私聊时指定接收者
    room_id: Optional[int] = None      # 群聊时指定房间


class MessageResponse(MessageBase):
    """消息响应模式"""
    id: int
    room_id: int
    sender_id: int
    sender_name: str
    sender_avatar: Optional[str] = None
    is_deleted: bool = False
    is_edited: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # 消息状态（对于私聊）
    is_read: bool = False
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RoomBase(BaseModel):
    """聊天室基础模式"""
    name: Optional[str] = None
    room_type: RoomType = RoomType.PRIVATE
    description: Optional[str] = None


class RoomCreate(RoomBase):
    """创建聊天室请求"""
    member_ids: List[int] = []


class RoomResponse(RoomBase):
    """聊天室响应模式"""
    id: int
    created_by: int
    member_count: int = 0
    message_count: int = 0
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
    
    # 当前用户在此房间的信息
    unread_count: int = 0
    last_read_message_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    """成员基础模式"""
    user_id: int
    role: str = "member"  # admin, member


class MemberResponse(MemberBase):
    """成员响应模式"""
    id: int
    room_id: int
    user_name: str
    user_avatar: Optional[str] = None
    user_role: str  # teacher, student
    is_active: bool = True
    is_muted: bool = False
    joined_at: datetime
    last_active_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== WebSocket相关模式 ====================

class WSMessageType(str, Enum):
    """WebSocket消息类型"""
    MESSAGE = "message"
    TYPING = "typing"
    USER_STATUS = "user_status"
    MESSAGE_READ = "message_read"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    ERROR = "error"


class WSMessage(BaseModel):
    """WebSocket消息格式"""
    type: WSMessageType
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


class TypingIndicator(BaseModel):
    """正在输入指示器"""
    room_id: int
    user_id: int
    user_name: str
    is_typing: bool


class UserStatusUpdate(BaseModel):
    """用户状态更新"""
    user_id: int
    status: UserStatus
    last_seen: Optional[datetime] = None


class MessageReadUpdate(BaseModel):
    """消息已读更新"""
    message_id: int
    room_id: int
    user_id: int
    read_at: datetime


# ==================== 查询参数模式 ====================

class ContactListQuery(BaseModel):
    """联系人列表查询参数"""
    search: Optional[str] = None
    role: Optional[str] = None  # teacher, student, all
    status: Optional[UserStatus] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class MessageListQuery(BaseModel):
    """消息列表查询参数"""
    room_id: Optional[int] = None
    contact_id: Optional[int] = None  # 用于私聊
    before_id: Optional[int] = None   # 分页：获取此ID之前的消息
    limit: int = Field(50, ge=1, le=100)


class RoomListQuery(BaseModel):
    """聊天室列表查询参数"""
    room_type: Optional[RoomType] = None
    search: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


# ==================== 统计和状态模式 ====================

class ChatStatistics(BaseModel):
    """聊天统计信息"""
    total_messages: int = 0
    total_rooms: int = 0
    total_contacts: int = 0
    unread_messages: int = 0
    active_conversations: int = 0


class OnlineUsersResponse(BaseModel):
    """在线用户响应"""
    online_users: List[ContactResponse]
    total_count: int


# ==================== 批量操作模式 ====================

class BatchMessageRead(BaseModel):
    """批量标记消息已读"""
    message_ids: List[int]
    room_id: int


class BatchDeleteMessages(BaseModel):
    """批量删除消息"""
    message_ids: List[int]
    room_id: int


# ==================== 响应包装模式 ====================

class ContactListResponse(BaseModel):
    """联系人列表响应"""
    contacts: List[ContactResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


class MessageListResponse(BaseModel):
    """消息列表响应"""
    messages: List[MessageResponse]
    total: int
    has_more: bool


class RoomListResponse(BaseModel):
    """聊天室列表响应"""
    rooms: List[RoomResponse]
    total: int
    page: int
    page_size: int
    has_next: bool

"""
聊天服务层
"""
import logging
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, func

from ..models.user import User
from ..models.chat import (
    ChatRoom, ChatMember, ChatMessage, UserContact, UserOnlineStatus
)
from ..schemas.chat import (
    ContactListQuery, MessageListQuery, RoomListQuery,
    MessageCreate, RoomCreate, ContactResponse, MessageResponse,
    RoomResponse, MemberResponse, ChatStatistics, UserStatus
)

logger = logging.getLogger(__name__)


class ChatService:
    """聊天服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ==================== 联系人管理 ====================
    
    async def get_contacts(self, user_id: int, query: ContactListQuery) -> Tuple[List[ContactResponse], int]:
        """获取联系人列表"""
        try:
            # 构建基础查询
            base_query = self.db.query(User).join(
                UserContact, 
                or_(
                    and_(UserContact.user_id == user_id, UserContact.contact_id == User.id),
                    and_(UserContact.contact_id == user_id, UserContact.user_id == User.id)
                )
            ).filter(
                User.id != user_id,
                User.is_active == True
            )
            
            # 应用筛选条件
            if query.role and query.role != "all":
                base_query = base_query.filter(User.role == query.role)
            
            if query.search:
                search_term = f"%{query.search}%"
                base_query = base_query.filter(
                    or_(
                        User.full_name.ilike(search_term),
                        User.email.ilike(search_term)
                    )
                )
            
            # 获取总数
            total = base_query.count()
            
            # 应用分页
            users = base_query.offset(
                (query.page - 1) * query.page_size
            ).limit(query.page_size).all()
            
            # 转换为响应格式
            contacts = []
            for user in users:
                # 获取用户状态
                status_record = self.db.query(UserOnlineStatus).filter(
                    UserOnlineStatus.user_id == user.id
                ).first()
                
                # 获取未读消息数
                unread_count = await self._get_unread_count(user_id, user.id)
                
                # 获取最后一条消息
                last_message_info = await self._get_last_message_info(user_id, user.id)
                
                contact = ContactResponse(
                    id=user.id,
                    user_id=user.id,
                    full_name=user.full_name,
                    avatar_url=getattr(user, 'avatar_url', None),
                    role=user.role,
                    status=UserStatus(status_record.status) if status_record else UserStatus.OFFLINE,
                    last_seen=status_record.last_seen if status_record else None,
                    unread_count=unread_count,
                    last_message=last_message_info.get('content'),
                    last_message_at=last_message_info.get('created_at')
                )
                contacts.append(contact)
            
            return contacts, total
            
        except Exception as e:
            logger.error(f"获取联系人列表失败: {e}")
            raise Exception("获取联系人列表失败")
    
    async def add_contact(self, user_id: int, contact_id: int) -> bool:
        """添加联系人"""
        try:
            # 检查是否已经是联系人
            existing = self.db.query(UserContact).filter(
                or_(
                    and_(UserContact.user_id == user_id, UserContact.contact_id == contact_id),
                    and_(UserContact.user_id == contact_id, UserContact.contact_id == user_id)
                )
            ).first()
            
            if existing:
                return True
            
            # 创建联系人关系
            contact = UserContact(
                user_id=user_id,
                contact_id=contact_id
            )
            self.db.add(contact)
            self.db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"添加联系人失败: {e}")
            self.db.rollback()
            raise Exception("添加联系人失败")
    
    # ==================== 聊天室管理 ====================
    
    async def get_or_create_private_room(self, user1_id: int, user2_id: int) -> ChatRoom:
        """获取或创建私聊房间"""
        try:
            # 查找现有的私聊房间
            room = self.db.query(ChatRoom).join(ChatMember).filter(
                ChatRoom.room_type == "private",
                ChatRoom.is_active == True
            ).group_by(ChatRoom.id).having(
                func.count(ChatMember.user_id) == 2
            ).filter(
                ChatRoom.id.in_(
                    self.db.query(ChatMember.room_id).filter(
                        ChatMember.user_id.in_([user1_id, user2_id]),
                        ChatMember.is_active == True
                    ).group_by(ChatMember.room_id).having(
                        func.count(ChatMember.user_id) == 2
                    )
                )
            ).first()
            
            if room:
                return room
            
            # 创建新的私聊房间
            room = ChatRoom(
                room_type="private",
                created_by=user1_id,
                member_count=2
            )
            self.db.add(room)
            self.db.flush()
            
            # 添加成员
            member1 = ChatMember(room_id=room.id, user_id=user1_id)
            member2 = ChatMember(room_id=room.id, user_id=user2_id)
            self.db.add_all([member1, member2])
            
            self.db.commit()
            return room
            
        except Exception as e:
            logger.error(f"创建私聊房间失败: {e}")
            self.db.rollback()
            raise Exception("创建私聊房间失败")
    
    async def get_user_rooms(self, user_id: int, query: RoomListQuery) -> Tuple[List[RoomResponse], int]:
        """获取用户的聊天室列表"""
        try:
            # 构建查询
            base_query = self.db.query(ChatRoom).join(ChatMember).filter(
                ChatMember.user_id == user_id,
                ChatMember.is_active == True,
                ChatRoom.is_active == True
            )
            
            # 应用筛选条件
            if query.room_type:
                base_query = base_query.filter(ChatRoom.room_type == query.room_type.value)
            
            if query.search:
                search_term = f"%{query.search}%"
                base_query = base_query.filter(
                    or_(
                        ChatRoom.name.ilike(search_term),
                        ChatRoom.description.ilike(search_term)
                    )
                )
            
            # 获取总数
            total = base_query.count()
            
            # 应用分页和排序
            rooms = base_query.order_by(
                desc(ChatRoom.last_message_at)
            ).offset(
                (query.page - 1) * query.page_size
            ).limit(query.page_size).all()
            
            # 转换为响应格式
            room_responses = []
            for room in rooms:
                # 获取用户在此房间的成员信息
                member = self.db.query(ChatMember).filter(
                    ChatMember.room_id == room.id,
                    ChatMember.user_id == user_id
                ).first()
                
                room_response = RoomResponse(
                    id=room.id,
                    name=room.name,
                    room_type=room.room_type,
                    description=room.description,
                    created_by=room.created_by,
                    member_count=room.member_count,
                    message_count=room.message_count,
                    is_active=room.is_active,
                    created_at=room.created_at,
                    updated_at=room.updated_at,
                    last_message_at=room.last_message_at,
                    unread_count=member.unread_count if member else 0,
                    last_read_message_id=member.last_read_message_id if member else None
                )
                room_responses.append(room_response)
            
            return room_responses, total
            
        except Exception as e:
            logger.error(f"获取聊天室列表失败: {e}")
            raise Exception("获取聊天室列表失败")
    
    # ==================== 消息管理 ====================
    
    async def send_message(self, sender_id: int, message_data: MessageCreate) -> MessageResponse:
        """发送消息"""
        try:
            # 确定聊天室
            room = None
            if message_data.room_id:
                room = self.db.query(ChatRoom).filter(
                    ChatRoom.id == message_data.room_id,
                    ChatRoom.is_active == True
                ).first()
            elif message_data.receiver_id:
                room = await self.get_or_create_private_room(sender_id, message_data.receiver_id)
                # 确保双方都是联系人
                await self.add_contact(sender_id, message_data.receiver_id)
            
            if not room:
                raise Exception("无效的聊天室或接收者")
            
            # 检查用户是否是房间成员
            member = self.db.query(ChatMember).filter(
                ChatMember.room_id == room.id,
                ChatMember.user_id == sender_id,
                ChatMember.is_active == True
            ).first()
            
            if not member:
                raise Exception("您不是此聊天室的成员")
            
            # 创建消息
            message = ChatMessage(
                room_id=room.id,
                sender_id=sender_id,
                content=message_data.content,
                message_type=message_data.message_type.value,
                file_url=message_data.file_url,
                file_name=message_data.file_name,
                file_size=message_data.file_size,
                reply_to_id=message_data.reply_to_id
            )
            self.db.add(message)
            self.db.flush()
            
            # 更新房间统计
            room.message_count += 1
            room.last_message_at = datetime.now()
            
            # 更新其他成员的未读计数
            self.db.query(ChatMember).filter(
                ChatMember.room_id == room.id,
                ChatMember.user_id != sender_id,
                ChatMember.is_active == True
            ).update({
                ChatMember.unread_count: ChatMember.unread_count + 1
            })
            
            self.db.commit()
            
            # 获取发送者信息
            sender = self.db.query(User).filter(User.id == sender_id).first()
            
            # 构建响应
            response = MessageResponse(
                id=message.id,
                room_id=message.room_id,
                sender_id=message.sender_id,
                sender_name=sender.full_name,
                sender_avatar=getattr(sender, 'avatar_url', None),
                content=message.content,
                message_type=message.message_type,
                file_url=message.file_url,
                file_name=message.file_name,
                file_size=message.file_size,
                reply_to_id=message.reply_to_id,
                is_deleted=message.is_deleted,
                is_edited=message.is_edited,
                created_at=message.created_at,
                updated_at=message.updated_at
            )
            
            return response
            
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            self.db.rollback()
            raise Exception(f"发送消息失败: {str(e)}")
    
    async def get_messages(self, user_id: int, query: MessageListQuery) -> Tuple[List[MessageResponse], bool]:
        """获取消息列表"""
        try:
            # 确定聊天室
            room_id = None
            if query.room_id:
                room_id = query.room_id
            elif query.contact_id:
                room = await self.get_or_create_private_room(user_id, query.contact_id)
                room_id = room.id
            
            if not room_id:
                return [], False
            
            # 检查用户权限
            member = self.db.query(ChatMember).filter(
                ChatMember.room_id == room_id,
                ChatMember.user_id == user_id,
                ChatMember.is_active == True
            ).first()
            
            if not member:
                raise Exception("您不是此聊天室的成员")
            
            # 构建查询
            message_query = self.db.query(ChatMessage).options(
                joinedload(ChatMessage.sender)
            ).filter(
                ChatMessage.room_id == room_id,
                ChatMessage.is_deleted == False
            )
            
            # 分页处理
            if query.before_id:
                message_query = message_query.filter(ChatMessage.id < query.before_id)
            
            messages = message_query.order_by(
                desc(ChatMessage.created_at)
            ).limit(query.limit + 1).all()
            
            has_more = len(messages) > query.limit
            if has_more:
                messages = messages[:-1]
            
            # 转换为响应格式
            message_responses = []
            for message in reversed(messages):  # 反转以获得正确的时间顺序
                sender = self.db.query(User).filter(User.id == message.sender_id).first()
                
                response = MessageResponse(
                    id=message.id,
                    room_id=message.room_id,
                    sender_id=message.sender_id,
                    sender_name=sender.full_name if sender else "未知用户",
                    sender_avatar=getattr(sender, 'avatar_url', None) if sender else None,
                    content=message.content,
                    message_type=message.message_type,
                    file_url=message.file_url,
                    file_name=message.file_name,
                    file_size=message.file_size,
                    reply_to_id=message.reply_to_id,
                    is_deleted=message.is_deleted,
                    is_edited=message.is_edited,
                    created_at=message.created_at,
                    updated_at=message.updated_at
                )
                message_responses.append(response)
            
            return message_responses, has_more
            
        except Exception as e:
            logger.error(f"获取消息列表失败: {e}")
            raise Exception("获取消息列表失败")
    
    # ==================== 辅助方法 ====================
    
    async def _get_unread_count(self, user_id: int, contact_id: int) -> int:
        """获取与指定联系人的未读消息数"""
        try:
            room = await self.get_or_create_private_room(user_id, contact_id)
            member = self.db.query(ChatMember).filter(
                ChatMember.room_id == room.id,
                ChatMember.user_id == user_id
            ).first()
            return member.unread_count if member else 0
        except:
            return 0
    
    async def _get_last_message_info(self, user_id: int, contact_id: int) -> Dict[str, Any]:
        """获取与指定联系人的最后一条消息信息"""
        try:
            room = await self.get_or_create_private_room(user_id, contact_id)
            message = self.db.query(ChatMessage).filter(
                ChatMessage.room_id == room.id,
                ChatMessage.is_deleted == False
            ).order_by(desc(ChatMessage.created_at)).first()
            
            if message:
                return {
                    'content': message.content,
                    'created_at': message.created_at
                }
            return {}
        except:
            return {}

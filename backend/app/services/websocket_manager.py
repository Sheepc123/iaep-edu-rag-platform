"""
WebSocket连接管理器
"""
import json
import logging
from typing import Dict, List, Set, Optional
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from ..models.user import User
from ..models.chat import UserOnlineStatus
from ..schemas.chat import WSMessage, WSMessageType, UserStatus
from ..core.database import SessionLocal

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储活跃连接: {user_id: {connection_id: websocket}}
        self.active_connections: Dict[int, Dict[str, WebSocket]] = {}
        # 存储用户房间映射: {user_id: set(room_ids)}
        self.user_rooms: Dict[int, Set[int]] = {}
        # 存储房间用户映射: {room_id: set(user_ids)}
        self.room_users: Dict[int, Set[int]] = {}
        # 存储正在输入状态: {room_id: {user_id: timestamp}}
        self.typing_users: Dict[int, Dict[int, datetime]] = {}
        
    async def connect(self, websocket: WebSocket, user_id: int, connection_id: str):
        """建立WebSocket连接"""
        await websocket.accept()
        
        # 添加连接
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        self.active_connections[user_id][connection_id] = websocket
        
        # 更新用户在线状态
        await self._update_user_status(user_id, UserStatus.ONLINE)
        
        # 通知其他用户该用户上线
        await self._broadcast_user_status(user_id, UserStatus.ONLINE)
        
        logger.info(f"用户 {user_id} 建立WebSocket连接: {connection_id}")
        
    async def disconnect(self, user_id: int, connection_id: str):
        """断开WebSocket连接"""
        if user_id in self.active_connections:
            if connection_id in self.active_connections[user_id]:
                del self.active_connections[user_id][connection_id]
                
            # 如果用户没有其他连接，标记为离线
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                await self._update_user_status(user_id, UserStatus.OFFLINE)
                await self._broadcast_user_status(user_id, UserStatus.OFFLINE)
                
                # 清理用户房间映射
                if user_id in self.user_rooms:
                    for room_id in self.user_rooms[user_id]:
                        if room_id in self.room_users:
                            self.room_users[room_id].discard(user_id)
                    del self.user_rooms[user_id]
        
        logger.info(f"用户 {user_id} 断开WebSocket连接: {connection_id}")
    
    async def join_room(self, user_id: int, room_id: int):
        """用户加入聊天室"""
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = set()
        self.user_rooms[user_id].add(room_id)
        
        if room_id not in self.room_users:
            self.room_users[room_id] = set()
        self.room_users[room_id].add(user_id)
        
        # 通知房间内其他用户
        await self._broadcast_to_room(room_id, WSMessage(
            type=WSMessageType.USER_JOINED,
            data={"user_id": user_id, "room_id": room_id}
        ), exclude_user=user_id)
        
        logger.info(f"用户 {user_id} 加入聊天室 {room_id}")
    
    async def leave_room(self, user_id: int, room_id: int):
        """用户离开聊天室"""
        if user_id in self.user_rooms:
            self.user_rooms[user_id].discard(room_id)
            
        if room_id in self.room_users:
            self.room_users[room_id].discard(user_id)
            
        # 清理正在输入状态
        if room_id in self.typing_users:
            self.typing_users[room_id].pop(user_id, None)
        
        # 通知房间内其他用户
        await self._broadcast_to_room(room_id, WSMessage(
            type=WSMessageType.USER_LEFT,
            data={"user_id": user_id, "room_id": room_id}
        ), exclude_user=user_id)
        
        logger.info(f"用户 {user_id} 离开聊天室 {room_id}")
    
    async def send_personal_message(self, user_id: int, message: WSMessage):
        """发送个人消息"""
        if user_id in self.active_connections:
            disconnected_connections = []
            for connection_id, websocket in self.active_connections[user_id].items():
                try:
                    await websocket.send_text(message.model_dump_json())
                except Exception as e:
                    logger.error(f"发送消息失败 {user_id}:{connection_id}: {e}")
                    disconnected_connections.append(connection_id)
            
            # 清理断开的连接
            for connection_id in disconnected_connections:
                await self.disconnect(user_id, connection_id)
    
    async def broadcast_to_room(self, room_id: int, message: WSMessage, exclude_user: Optional[int] = None):
        """向聊天室广播消息"""
        await self._broadcast_to_room(room_id, message, exclude_user)
    
    async def set_typing_status(self, user_id: int, room_id: int, is_typing: bool):
        """设置正在输入状态"""
        if room_id not in self.typing_users:
            self.typing_users[room_id] = {}
            
        if is_typing:
            self.typing_users[room_id][user_id] = datetime.now()
        else:
            self.typing_users[room_id].pop(user_id, None)
        
        # 广播输入状态
        await self._broadcast_to_room(room_id, WSMessage(
            type=WSMessageType.TYPING,
            data={
                "user_id": user_id,
                "room_id": room_id,
                "is_typing": is_typing
            }
        ), exclude_user=user_id)
    
    def get_online_users(self) -> List[int]:
        """获取在线用户列表"""
        return list(self.active_connections.keys())
    
    def is_user_online(self, user_id: int) -> bool:
        """检查用户是否在线"""
        return user_id in self.active_connections
    
    def get_room_users(self, room_id: int) -> Set[int]:
        """获取聊天室内的用户"""
        return self.room_users.get(room_id, set())
    
    async def _broadcast_to_room(self, room_id: int, message: WSMessage, exclude_user: Optional[int] = None):
        """向聊天室内所有用户广播消息"""
        if room_id not in self.room_users:
            return
            
        for user_id in self.room_users[room_id]:
            if exclude_user and user_id == exclude_user:
                continue
            await self.send_personal_message(user_id, message)
    
    async def _broadcast_user_status(self, user_id: int, status: UserStatus):
        """广播用户状态变化"""
        # 获取用户的所有聊天室
        user_rooms = self.user_rooms.get(user_id, set())
        notified_users = set()
        
        for room_id in user_rooms:
            for room_user_id in self.room_users.get(room_id, set()):
                if room_user_id != user_id and room_user_id not in notified_users:
                    await self.send_personal_message(room_user_id, WSMessage(
                        type=WSMessageType.USER_STATUS,
                        data={
                            "user_id": user_id,
                            "status": status.value,
                            "timestamp": datetime.now().isoformat()
                        }
                    ))
                    notified_users.add(room_user_id)
    
    async def _update_user_status(self, user_id: int, status: UserStatus):
        """更新数据库中的用户在线状态"""
        try:
            db = SessionLocal()
            try:
                # 查找或创建用户状态记录
                user_status = db.query(UserOnlineStatus).filter(
                    UserOnlineStatus.user_id == user_id
                ).first()
                
                if not user_status:
                    user_status = UserOnlineStatus(
                        user_id=user_id,
                        status=status.value,
                        last_seen=datetime.now()
                    )
                    db.add(user_status)
                else:
                    user_status.status = status.value
                    user_status.last_seen = datetime.now()
                
                db.commit()
            finally:
                db.close()
        except Exception as e:
            logger.error(f"更新用户状态失败 {user_id}: {e}")


# 全局连接管理器实例
connection_manager = ConnectionManager()

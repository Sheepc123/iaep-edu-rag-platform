"""
聊天通信API端点
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from ....core.database import get_db
from ....models.user import User
from ....schemas.chat import (
    ContactListQuery, MessageListQuery, RoomListQuery,
    MessageCreate, MessageResponse, ContactResponse,
    ContactListResponse, MessageListResponse, WSMessage, WSMessageType
)
from ....services.chat_service import ChatService
from ....services.websocket_manager import connection_manager
from ...dependencies import get_current_active_user, get_optional_user

router = APIRouter()
logger = logging.getLogger(__name__)


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    """获取聊天服务实例"""
    return ChatService(db)


# ==================== REST API端点 ====================

@router.get("/contacts", response_model=ContactListResponse, summary="获取联系人列表")
async def get_contacts(
    search: Optional[str] = Query(None, description="搜索关键词"),
    role: Optional[str] = Query("all", description="角色筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    获取联系人列表

    - **search**: 搜索关键词（姓名、邮箱）
    - **role**: 角色筛选（all/teacher/student）
    - **page**: 页码
    - **page_size**: 每页数量
    """
    try:
        query = ContactListQuery(
            search=search,
            role=role,
            page=page,
            page_size=page_size
        )

        contacts, total = await chat_service.get_contacts(current_user.id, query)

        return ContactListResponse(
            contacts=contacts,
            total=total,
            page=page,
            page_size=page_size,
            has_next=total > page * page_size
        )

    except Exception as e:
        logger.error(f"获取联系人列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取联系人列表失败"
        )


@router.post("/contacts/{contact_id}", summary="添加联系人")
async def add_contact(
    contact_id: int,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    添加联系人

    - **contact_id**: 要添加的联系人ID
    """
    try:
        if contact_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能添加自己为联系人"
            )

        success = await chat_service.add_contact(current_user.id, contact_id)

        if success:
            return {"message": "联系人添加成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="添加联系人失败"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"添加联系人失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="添加联系人失败"
        )


@router.get("/messages", response_model=MessageListResponse, summary="获取消息列表")
async def get_messages(
    room_id: Optional[int] = Query(None, description="聊天室ID"),
    contact_id: Optional[int] = Query(None, description="联系人ID（私聊）"),
    before_id: Optional[int] = Query(None, description="获取此ID之前的消息"),
    limit: int = Query(50, ge=1, le=100, description="消息数量限制"),
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    获取消息列表

    - **room_id**: 聊天室ID（群聊）
    - **contact_id**: 联系人ID（私聊）
    - **before_id**: 分页参数，获取此ID之前的消息
    - **limit**: 消息数量限制
    """
    try:
        if not room_id and not contact_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="必须指定room_id或contact_id"
            )

        query = MessageListQuery(
            room_id=room_id,
            contact_id=contact_id,
            before_id=before_id,
            limit=limit
        )

        messages, has_more = await chat_service.get_messages(current_user.id, query)

        return MessageListResponse(
            messages=messages,
            total=len(messages),
            has_more=has_more
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取消息列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取消息列表失败"
        )


@router.post("/messages", response_model=MessageResponse, summary="发送消息")
async def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    发送消息

    - **receiver_id**: 接收者ID（私聊时使用）
    - **room_id**: 聊天室ID（群聊时使用）
    - **content**: 消息内容
    - **message_type**: 消息类型（text/image/file）
    """
    try:
        if not message_data.receiver_id and not message_data.room_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="必须指定receiver_id或room_id"
            )

        # 发送消息
        message = await chat_service.send_message(current_user.id, message_data)

        # 通过WebSocket广播消息
        await connection_manager.broadcast_to_room(
            message.room_id,
            WSMessage(
                type=WSMessageType.MESSAGE,
                data=message.model_dump()
            ),
            exclude_user=current_user.id
        )

        return message

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"发送消息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送消息失败: {str(e)}"
        )


# ==================== WebSocket端点 ====================

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    WebSocket聊天连接

    - **token**: JWT认证令牌
    """
    # 验证用户身份
    current_user = None
    if token:
        try:
            # 这里需要实现JWT token验证逻辑
            # 暂时跳过验证，实际使用时需要添加
            pass
        except Exception as e:
            logger.error(f"WebSocket认证失败: {e}")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

    if not current_user:
        # 临时处理：如果没有认证，拒绝连接
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 生成连接ID
    connection_id = str(uuid.uuid4())

    try:
        # 建立连接
        await connection_manager.connect(websocket, current_user.id, connection_id)

        while True:
            try:
                # 接收消息
                data = await websocket.receive_text()
                message_data = WSMessage.model_validate_json(data)

                # 处理不同类型的消息
                if message_data.type == WSMessageType.MESSAGE:
                    # 处理聊天消息
                    await handle_chat_message(current_user.id, message_data.data, db)

                elif message_data.type == WSMessageType.TYPING:
                    # 处理正在输入状态
                    await handle_typing_status(current_user.id, message_data.data)

                elif message_data.type == WSMessageType.MESSAGE_READ:
                    # 处理消息已读状态
                    await handle_message_read(current_user.id, message_data.data, db)

            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"处理WebSocket消息失败: {e}")
                await connection_manager.send_personal_message(
                    current_user.id,
                    WSMessage(
                        type=WSMessageType.ERROR,
                        data={"message": "消息处理失败"}
                    )
                )

    except Exception as e:
        logger.error(f"WebSocket连接异常: {e}")
    finally:
        # 断开连接
        await connection_manager.disconnect(current_user.id, connection_id)


# ==================== WebSocket消息处理函数 ====================

async def handle_chat_message(user_id: int, data: dict, db: Session):
    """处理聊天消息"""
    try:
        chat_service = ChatService(db)

        # 创建消息数据
        message_create = MessageCreate(
            content=data.get("content", ""),
            message_type=data.get("message_type", "text"),
            receiver_id=data.get("receiver_id"),
            room_id=data.get("room_id"),
            file_url=data.get("file_url"),
            file_name=data.get("file_name"),
            file_size=data.get("file_size")
        )

        # 发送消息
        message = await chat_service.send_message(user_id, message_create)

        # 广播消息
        await connection_manager.broadcast_to_room(
            message.room_id,
            WSMessage(
                type=WSMessageType.MESSAGE,
                data=message.model_dump()
            ),
            exclude_user=user_id
        )

    except Exception as e:
        logger.error(f"处理聊天消息失败: {e}")


async def handle_typing_status(user_id: int, data: dict):
    """处理正在输入状态"""
    try:
        room_id = data.get("room_id")
        is_typing = data.get("is_typing", False)

        if room_id:
            await connection_manager.set_typing_status(user_id, room_id, is_typing)

    except Exception as e:
        logger.error(f"处理输入状态失败: {e}")


async def handle_message_read(user_id: int, data: dict, db: Session):
    """处理消息已读状态"""
    try:
        message_id = data.get("message_id")
        room_id = data.get("room_id")

        if message_id and room_id:
            # 这里可以添加标记消息已读的逻辑
            # 暂时只广播已读状态
            await connection_manager.broadcast_to_room(
                room_id,
                WSMessage(
                    type=WSMessageType.MESSAGE_READ,
                    data={
                        "message_id": message_id,
                        "user_id": user_id,
                        "room_id": room_id
                    }
                ),
                exclude_user=user_id
            )

    except Exception as e:
        logger.error(f"处理消息已读失败: {e}")


# ==================== 状态查询端点 ====================

@router.get("/online-users", summary="获取在线用户列表")
async def get_online_users(
    current_user: User = Depends(get_current_active_user)
):
    """获取在线用户列表"""
    try:
        online_user_ids = connection_manager.get_online_users()
        return {
            "online_users": online_user_ids,
            "total_count": len(online_user_ids)
        }

    except Exception as e:
        logger.error(f"获取在线用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取在线用户失败"
        )


@router.get("/rooms/{room_id}/members", summary="获取聊天室成员")
async def get_room_members(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    """获取聊天室成员列表"""
    try:
        # 这里可以添加获取聊天室成员的逻辑
        # 暂时返回在线成员
        online_members = connection_manager.get_room_users(room_id)
        return {
            "room_id": room_id,
            "online_members": list(online_members),
            "online_count": len(online_members)
        }

    except Exception as e:
        logger.error(f"获取聊天室成员失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取聊天室成员失败"
        )

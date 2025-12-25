# 聊天室后端实现文档

## 实现概述
完整实现了聊天室的后端功能，包括REST API、WebSocket实时通信、数据库模型和业务逻辑。

## 实现时间
2025-06-25

## 核心组件

### 1. 数据模式 (schemas/chat.py)

#### 核心数据结构
- **ContactResponse**: 联系人信息响应
- **MessageResponse**: 消息响应格式
- **RoomResponse**: 聊天室信息响应
- **WSMessage**: WebSocket消息格式

#### 枚举类型
- **MessageType**: 消息类型（text/image/file/system）
- **UserStatus**: 用户状态（online/busy/away/offline）
- **RoomType**: 聊天室类型（private/group/class）
- **WSMessageType**: WebSocket消息类型

#### 查询参数
- **ContactListQuery**: 联系人列表查询
- **MessageListQuery**: 消息列表查询
- **RoomListQuery**: 聊天室列表查询

### 2. WebSocket管理器 (services/websocket_manager.py)

#### 核心功能
- **连接管理**: 管理用户的WebSocket连接
- **房间管理**: 用户加入/离开聊天室
- **消息广播**: 向房间内用户广播消息
- **状态同步**: 用户在线状态、正在输入状态

#### 关键特性
```python
class ConnectionManager:
    # 存储活跃连接: {user_id: {connection_id: websocket}}
    active_connections: Dict[int, Dict[str, WebSocket]]
    
    # 存储用户房间映射: {user_id: set(room_ids)}
    user_rooms: Dict[int, Set[int]]
    
    # 存储房间用户映射: {room_id: set(user_ids)}
    room_users: Dict[int, Set[int]]
```

#### 主要方法
- `connect()`: 建立WebSocket连接
- `disconnect()`: 断开连接并清理状态
- `join_room()`: 用户加入聊天室
- `leave_room()`: 用户离开聊天室
- `broadcast_to_room()`: 向房间广播消息
- `set_typing_status()`: 设置正在输入状态

### 3. 聊天服务层 (services/chat_service.py)

#### 联系人管理
- `get_contacts()`: 获取联系人列表（支持搜索、筛选、分页）
- `add_contact()`: 添加联系人关系

#### 聊天室管理
- `get_or_create_private_room()`: 获取或创建私聊房间
- `get_user_rooms()`: 获取用户的聊天室列表

#### 消息管理
- `send_message()`: 发送消息（支持私聊和群聊）
- `get_messages()`: 获取消息列表（支持分页）

#### 业务逻辑特性
- **自动创建私聊房间**: 首次对话时自动创建
- **联系人关系维护**: 发送消息时自动建立联系人关系
- **未读消息计数**: 自动维护未读消息数量
- **权限检查**: 确保用户只能访问有权限的聊天室

### 4. API端点 (api/v1/endpoints/chat.py)

#### REST API端点

##### 联系人相关
- `GET /chat/contacts`: 获取联系人列表
- `POST /chat/contacts/{contact_id}`: 添加联系人

##### 消息相关
- `GET /chat/messages`: 获取消息列表
- `POST /chat/messages`: 发送消息

##### 状态查询
- `GET /chat/online-users`: 获取在线用户列表
- `GET /chat/rooms/{room_id}/members`: 获取聊天室成员

#### WebSocket端点
- `WS /chat/ws`: WebSocket连接端点

#### 消息处理函数
- `handle_chat_message()`: 处理聊天消息
- `handle_typing_status()`: 处理正在输入状态
- `handle_message_read()`: 处理消息已读状态

## 数据库模型集成

### 使用现有模型
- **ChatRoom**: 聊天室信息
- **ChatMember**: 聊天室成员关系
- **ChatMessage**: 聊天消息记录
- **UserContact**: 用户联系人关系
- **UserOnlineStatus**: 用户在线状态

### 模型关系
```
User ←→ UserContact ←→ User (多对多联系人关系)
User → ChatRoom (一对多，创建者关系)
User ←→ ChatMember ←→ ChatRoom (多对多成员关系)
User → ChatMessage (一对多，发送者关系)
ChatRoom → ChatMessage (一对多，消息归属)
User → UserOnlineStatus (一对一状态记录)
```

## API使用示例

### 1. 获取联系人列表
```http
GET /api/v1/chat/contacts?search=王老师&role=teacher&page=1&page_size=20
Authorization: Bearer {token}
```

### 2. 发送私聊消息
```http
POST /api/v1/chat/messages
Authorization: Bearer {token}
Content-Type: application/json

{
  "receiver_id": 123,
  "content": "老师您好，我有个问题想请教",
  "message_type": "text"
}
```

### 3. 获取聊天记录
```http
GET /api/v1/chat/messages?contact_id=123&limit=50
Authorization: Bearer {token}
```

### 4. WebSocket连接
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/chat/ws?token=your_jwt_token');

// 发送消息
ws.send(JSON.stringify({
  type: "message",
  data: {
    receiver_id: 123,
    content: "Hello",
    message_type: "text"
  }
}));

// 接收消息
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('收到消息:', message);
};
```

## 安全特性

### 1. 用户认证
- 所有API端点都需要JWT认证
- WebSocket连接需要token验证

### 2. 权限控制
- 用户只能访问自己的联系人和聊天室
- 消息发送前检查房间成员权限
- 数据库查询都包含用户ID过滤

### 3. 数据隔离
- 每个用户只能看到自己的数据
- 聊天室成员权限严格控制
- 消息访问权限验证

## 性能优化

### 1. 数据库优化
- 使用索引优化查询性能
- 分页查询避免大量数据加载
- 使用joinedload预加载关联数据

### 2. WebSocket优化
- 连接池管理，支持多连接
- 消息广播优化，避免重复发送
- 自动清理断开的连接

### 3. 缓存策略
- 在线用户状态内存缓存
- 房间成员关系缓存
- 正在输入状态临时存储

## 错误处理

### 1. API错误处理
- 统一的HTTP状态码返回
- 详细的错误信息描述
- 日志记录便于调试

### 2. WebSocket错误处理
- 连接异常自动重连机制
- 消息发送失败处理
- 错误消息通知客户端

### 3. 数据库错误处理
- 事务回滚保证数据一致性
- 连接池异常处理
- 查询超时处理

## 扩展功能建议

### 1. 消息功能增强
- 消息撤回功能
- 消息编辑功能
- 消息转发功能
- 文件上传支持

### 2. 聊天室功能
- 群聊创建和管理
- 聊天室权限管理
- 聊天室公告功能
- 成员邀请功能

### 3. 用户体验
- 消息搜索功能
- 聊天记录导出
- 消息提醒设置
- 免打扰模式

### 4. 管理功能
- 聊天记录审核
- 敏感词过滤
- 用户行为统计
- 系统消息推送

## 部署注意事项

### 1. 环境配置
- 确保WebSocket支持
- 配置CORS策略
- 设置合适的连接超时

### 2. 监控指标
- WebSocket连接数
- 消息发送成功率
- API响应时间
- 错误率统计

### 3. 扩展性考虑
- 支持水平扩展
- 消息队列集成
- 分布式WebSocket管理
- 数据库读写分离

## 测试建议

### 1. 单元测试
- 服务层业务逻辑测试
- 数据模型验证测试
- WebSocket管理器测试

### 2. 集成测试
- API端点完整流程测试
- WebSocket连接和消息测试
- 数据库操作测试

### 3. 性能测试
- 并发连接压力测试
- 消息发送性能测试
- 数据库查询性能测试

## 维护指南

### 1. 日志监控
- 关键操作日志记录
- 错误日志分析
- 性能指标监控

### 2. 数据备份
- 聊天记录定期备份
- 用户关系数据备份
- 配置文件版本管理

### 3. 版本升级
- 数据库迁移脚本
- API版本兼容性
- WebSocket协议升级

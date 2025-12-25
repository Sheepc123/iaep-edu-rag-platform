# 聊天室功能实现文档

## 功能概述
实现了学生与老师、学生与学生之间的聊天功能，包含完整的UI界面和基础交互逻辑。

## 已实现功能

### 1. 导航栏集成
- ✅ 在左侧导航栏添加了"聊天室"选项
- ✅ 使用 MessageCircle 图标
- ✅ 路由路径：`/student/chatroom`

### 2. 聊天界面布局
- ✅ 左侧联系人列表（宽度320px）
- ✅ 右侧聊天对话区域
- ✅ 响应式设计，适配不同屏幕尺寸

### 3. 联系人管理
- ✅ 支持老师和学生两种角色
- ✅ 显示在线状态（在线/忙碌/离线）
- ✅ 未读消息数量提示
- ✅ 联系人搜索功能
- ✅ 按角色筛选（全部/老师/同学）

### 4. 聊天功能
- ✅ 消息发送和接收
- ✅ 消息状态显示（已发送/已送达/已读）
- ✅ 正在输入指示器
- ✅ 消息时间戳
- ✅ 自动滚动到最新消息
- ✅ 支持 Shift+Enter 换行

### 5. 视觉设计
- ✅ 现代化UI设计
- ✅ 渐变色头像区分角色
- ✅ 平滑动画效果
- ✅ 消息气泡样式
- ✅ 状态指示器

## 当前限制（需要后端支持）

### 1. 数据持久化
- ❌ 消息记录无法持久化存储
- ❌ 联系人列表为静态数据
- ❌ 用户状态无法实时同步

### 2. 实时通信
- ❌ 缺少 WebSocket 连接
- ❌ 无法实现真实的实时消息推送
- ❌ 消息状态更新需要手动模拟

### 3. 用户认证
- ❌ 无法获取真实的用户信息
- ❌ 无法验证用户权限
- ❌ 无法区分当前登录用户

## 技术实现细节

### 文件结构
```
frontend/src/pages/student/ChatRoom.tsx  # 主要聊天室组件
frontend/src/components/layouts/StudentLayout.tsx  # 导航栏更新
frontend/src/App.tsx  # 路由配置
```

### 主要组件
- `ChatRoom`: 主聊天室组件
- `Contact`: 联系人接口定义
- `ChatMessage`: 消息接口定义

### 状态管理
- `contacts`: 联系人列表
- `selectedContact`: 当前选中的联系人
- `messages`: 当前对话的消息列表
- `inputValue`: 输入框内容
- `isTyping`: 正在输入状态
- `searchQuery`: 搜索关键词
- `activeTab`: 当前选中的标签页

### 模拟数据
当前使用模拟数据来展示功能：
- 4个联系人（2个老师，2个学生）
- 每个联系人有独立的聊天记录
- 模拟的在线状态和未读消息数

## 后端API需求

### 1. 联系人相关API
```typescript
GET /api/contacts - 获取联系人列表
GET /api/contacts/search?q={query} - 搜索联系人
GET /api/contacts/{id}/status - 获取联系人状态
```

### 2. 消息相关API
```typescript
GET /api/messages/{contactId} - 获取与指定联系人的聊天记录
POST /api/messages - 发送消息
PUT /api/messages/{id}/read - 标记消息为已读
```

### 3. WebSocket事件
```typescript
// 接收消息
socket.on('message', (message: ChatMessage) => {})

// 用户状态变化
socket.on('user_status', (userId: string, status: string) => {})

// 正在输入
socket.on('typing', (userId: string, isTyping: boolean) => {})

// 消息状态更新
socket.on('message_status', (messageId: string, status: string) => {})
```

## 数据库设计建议

### 用户表 (users)
- id, name, email, role (teacher/student), avatar_url, status, last_seen

### 消息表 (messages)
- id, sender_id, receiver_id, content, type, status, created_at, updated_at

### 联系人关系表 (contacts)
- id, user_id, contact_id, created_at

## 下一步开发计划

### 短期目标
1. 集成用户认证系统
2. 连接真实的联系人API
3. 实现消息发送API调用

### 中期目标
1. 集成WebSocket实时通信
2. 实现消息状态同步
3. 添加文件上传功能

### 长期目标
1. 群聊功能
2. 消息搜索
3. 聊天记录导出
4. 消息加密

## 使用说明

### 访问聊天室
1. 登录学生账户
2. 点击左侧导航栏的"聊天室"
3. 选择联系人开始聊天

### 发送消息
1. 在输入框中输入消息
2. 按 Enter 发送，Shift+Enter 换行
3. 点击发送按钮

### 搜索联系人
1. 在搜索框中输入姓名或科目
2. 使用标签页筛选角色类型

## 注意事项
- 当前为前端模拟实现，所有数据在页面刷新后会丢失
- 消息发送后会有模拟的自动回复
- 用户状态和未读消息数为静态数据
- 建议在后端API准备就绪后进行完整的功能集成

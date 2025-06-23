# AI助手API接口设计文档

## 接口概述

本文档定义了AI助手功能所需的后端API接口，为前后端分离开发提供标准规范。

## 基础配置

### 接口基础信息
- **Base URL**: `/api/v1/ai`
- **认证方式**: Bearer Token (JWT)
- **数据格式**: JSON
- **字符编码**: UTF-8

### 通用响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-06-23T10:30:00Z"
}
```

### 错误响应格式
```json
{
  "code": 400,
  "message": "参数错误",
  "error": "详细错误信息",
  "timestamp": "2024-06-23T10:30:00Z"
}
```

## 数据模型

### Message 消息模型
```json
{
  "id": "string",
  "conversationId": "string",
  "content": "string",
  "sender": "user|ai",
  "type": "text|image|file|suggestion",
  "metadata": {
    "tokens": 150,
    "model": "deepseek-chat",
    "confidence": 0.95
  },
  "createdAt": "2024-06-23T10:30:00Z",
  "updatedAt": "2024-06-23T10:30:00Z"
}
```

### Conversation 对话模型
```json
{
  "id": "string",
  "userId": "string",
  "title": "string",
  "status": "active|archived|deleted",
  "messageCount": 10,
  "lastMessageAt": "2024-06-23T10:30:00Z",
  "createdAt": "2024-06-23T10:30:00Z",
  "updatedAt": "2024-06-23T10:30:00Z"
}
```

## API接口详情

### 1. 对话管理

#### 1.1 获取对话列表
```http
GET /api/v1/ai/conversations
```

**请求参数**
```json
{
  "page": 1,
  "pageSize": 20,
  "status": "active"
}
```

**响应数据**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "conversations": [
      {
        "id": "conv_123",
        "title": "数学学习计划",
        "messageCount": 15,
        "lastMessageAt": "2024-06-23T10:30:00Z",
        "createdAt": "2024-06-23T09:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 5,
      "totalPages": 1
    }
  }
}
```

#### 1.2 创建新对话
```http
POST /api/v1/ai/conversations
```

**请求体**
```json
{
  "title": "新的学习讨论"
}
```

**响应数据**
```json
{
  "code": 201,
  "message": "对话创建成功",
  "data": {
    "conversation": {
      "id": "conv_124",
      "title": "新的学习讨论",
      "messageCount": 1,
      "lastMessageAt": "2024-06-23T10:30:00Z",
      "createdAt": "2024-06-23T10:30:00Z"
    }
  }
}
```

#### 1.3 更新对话信息
```http
PUT /api/v1/ai/conversations/{conversationId}
```

**请求体**
```json
{
  "title": "更新后的标题"
}
```

#### 1.4 删除对话
```http
DELETE /api/v1/ai/conversations/{conversationId}
```

### 2. 消息管理

#### 2.1 获取对话消息
```http
GET /api/v1/ai/conversations/{conversationId}/messages
```

**请求参数**
```json
{
  "page": 1,
  "pageSize": 50,
  "order": "asc"
}
```

**响应数据**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "messages": [
      {
        "id": "msg_001",
        "conversationId": "conv_123",
        "content": "你好，我需要学习建议",
        "sender": "user",
        "type": "text",
        "createdAt": "2024-06-23T10:25:00Z"
      },
      {
        "id": "msg_002",
        "conversationId": "conv_123",
        "content": "你好！我很乐意为你提供学习建议...",
        "sender": "ai",
        "type": "text",
        "metadata": {
          "tokens": 120,
          "model": "deepseek-chat",
          "confidence": 0.95
        },
        "createdAt": "2024-06-23T10:25:30Z"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 50,
      "total": 15,
      "totalPages": 1
    }
  }
}
```

#### 2.2 发送消息
```http
POST /api/v1/ai/conversations/{conversationId}/messages
```

**请求体**
```json
{
  "content": "请帮我制定一个数学学习计划",
  "type": "text",
  "context": {
    "userProfile": {
      "grade": "大一",
      "major": "计算机科学",
      "weakPoints": ["微积分", "线性代数"]
    }
  }
}
```

**响应数据**
```json
{
  "code": 201,
  "message": "消息发送成功",
  "data": {
    "userMessage": {
      "id": "msg_003",
      "conversationId": "conv_123",
      "content": "请帮我制定一个数学学习计划",
      "sender": "user",
      "type": "text",
      "createdAt": "2024-06-23T10:30:00Z"
    },
    "aiMessage": {
      "id": "msg_004",
      "conversationId": "conv_123",
      "content": "根据你的情况，我为你制定以下学习计划...",
      "sender": "ai",
      "type": "text",
      "metadata": {
        "tokens": 200,
        "model": "deepseek-chat",
        "confidence": 0.92,
        "processingTime": 1.5
      },
      "createdAt": "2024-06-23T10:30:02Z"
    }
  }
}
```

### 3. 流式对话接口

#### 3.1 流式消息发送
```http
POST /api/v1/ai/conversations/{conversationId}/messages/stream
```

**请求体**
```json
{
  "content": "解释一下导数的概念",
  "type": "text",
  "stream": true
}
```

**响应格式** (Server-Sent Events)
```
data: {"type": "start", "messageId": "msg_005"}

data: {"type": "content", "content": "导数是"}

data: {"type": "content", "content": "微积分中的"}

data: {"type": "content", "content": "重要概念..."}

data: {"type": "end", "messageId": "msg_005", "metadata": {"tokens": 150}}
```

### 4. 智能功能

#### 4.1 获取学习建议
```http
POST /api/v1/ai/suggestions
```

**请求体**
```json
{
  "type": "learning_plan",
  "context": {
    "subject": "数学",
    "currentLevel": "初级",
    "timeAvailable": "2小时/天",
    "goals": ["提高计算能力", "理解基础概念"]
  }
}
```

**响应数据**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "suggestions": [
      {
        "type": "daily_plan",
        "title": "每日学习计划",
        "content": "建议每天安排2小时学习时间...",
        "priority": "high"
      },
      {
        "type": "resource",
        "title": "推荐资源",
        "content": "以下是适合你的学习资源...",
        "priority": "medium"
      }
    ]
  }
}
```

#### 4.2 题目生成
```http
POST /api/v1/ai/exercises/generate
```

**请求体**
```json
{
  "subject": "数学",
  "topic": "导数",
  "difficulty": "medium",
  "count": 5,
  "type": "multiple_choice"
}
```

**响应数据**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "exercises": [
      {
        "id": "ex_001",
        "question": "求函数 f(x) = x² + 2x 的导数",
        "options": ["2x + 2", "x + 2", "2x", "x²"],
        "answer": "2x + 2",
        "explanation": "根据导数公式...",
        "difficulty": "medium"
      }
    ]
  }
}
```

### 5. 用户偏好

#### 5.1 获取用户AI设置
```http
GET /api/v1/ai/user/preferences
```

**响应数据**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "preferences": {
      "language": "zh-CN",
      "responseStyle": "detailed",
      "subjects": ["数学", "物理"],
      "difficulty": "medium",
      "enableVoice": false,
      "autoSave": true
    }
  }
}
```

#### 5.2 更新用户AI设置
```http
PUT /api/v1/ai/user/preferences
```

**请求体**
```json
{
  "responseStyle": "concise",
  "enableVoice": true,
  "subjects": ["数学", "物理", "化学"]
}
```

## 错误码定义

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权访问 | 重新登录获取token |
| 403 | 权限不足 | 联系管理员 |
| 404 | 资源不存在 | 检查资源ID |
| 429 | 请求频率过高 | 降低请求频率 |
| 500 | 服务器内部错误 | 稍后重试 |
| 503 | AI服务不可用 | 稍后重试 |

## 安全考虑

### 1. 认证授权
- 所有接口需要JWT认证
- 用户只能访问自己的对话数据
- 管理员可以访问所有数据

### 2. 数据验证
- 输入内容长度限制（最大1000字符）
- 敏感词过滤
- SQL注入防护
- XSS攻击防护

### 3. 频率限制
- 每用户每分钟最多30次请求
- 每用户每天最多1000次AI对话
- 流式接口特殊限制

## 性能优化

### 1. 缓存策略
- 对话列表缓存5分钟
- 用户偏好缓存30分钟
- AI回复缓存1小时（相同问题）

### 2. 数据库优化
- 消息表按对话ID分区
- 创建适当索引
- 定期清理过期数据

### 3. AI服务优化
- 连接池管理
- 请求队列
- 超时处理
- 降级策略

---

**文档版本**：v1.0  
**最后更新**：2024-06-23  
**维护者**：后端开发团队

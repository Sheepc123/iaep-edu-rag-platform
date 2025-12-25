# 智能教育实训平台API接口设计规范

## 📋 设计概述

基于RESTful API设计原则，为智能教育实训平台提供完整的后端API接口规范，支持前端所有功能模块的数据交互需求。

## 🎯 设计原则

1. **RESTful规范**：遵循REST架构风格
2. **统一响应格式**：标准化的数据返回格式
3. **版本控制**：支持API版本管理
4. **安全认证**：JWT token认证机制
5. **错误处理**：完善的错误码和错误信息
6. **文档自动生成**：基于OpenAPI 3.0规范

## 🔧 基础配置

### API基础信息
- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token (JWT)
- **数据格式**: JSON
- **字符编码**: UTF-8
- **API版本**: v1

### 通用请求头
```http
Content-Type: application/json
Authorization: Bearer {jwt_token}
Accept: application/json
```

### 统一响应格式
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": "2024-06-24T10:30:00Z",
  "request_id": "req_123456789"
}
```

### 错误响应格式
```json
{
  "success": false,
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "type": "ValidationError",
    "details": "用户名不能为空",
    "field": "username"
  },
  "timestamp": "2024-06-24T10:30:00Z",
  "request_id": "req_123456789"
}
```

## 🔐 认证授权模块

### 1. 用户注册
```http
POST /api/v1/auth/register
```

**请求体**
```json
{
  "username": "student001",
  "email": "student@example.com",
  "password": "password123",
  "full_name": "张同学",
  "role": "student",
  "school": "清华大学",
  "college": "计算机学院"
}
```

**响应数据**
```json
{
  "success": true,
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": "user_123",
      "username": "student001",
      "email": "student@example.com",
      "full_name": "张同学",
      "role": "student",
      "created_at": "2024-06-24T10:30:00Z"
    },
    "tokens": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "token_type": "bearer",
      "expires_in": 1800
    }
  }
}
```

### 2. 用户登录
```http
POST /api/v1/auth/login
```

**请求体**
```json
{
  "username": "student001",
  "password": "password123"
}
```

### 3. 刷新Token
```http
POST /api/v1/auth/refresh
```

**请求体**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. 用户登出
```http
POST /api/v1/auth/logout
Authorization: Bearer {access_token}
```

## 👤 用户管理模块

### 1. 获取用户信息
```http
GET /api/v1/users/profile
Authorization: Bearer {access_token}
```

**响应数据**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "user": {
      "id": "user_123",
      "username": "student001",
      "email": "student@example.com",
      "full_name": "张同学",
      "avatar_url": "https://example.com/avatar.jpg",
      "phone": "138****8888",
      "school": "清华大学",
      "college": "计算机学院",
      "student_id": "2021012345",
      "role": "student",
      "status": "active",
      "created_at": "2024-06-24T10:30:00Z",
      "last_login_at": "2024-06-24T10:30:00Z"
    },
    "preferences": {
      "ai_language": "zh-CN",
      "ai_response_style": "detailed",
      "theme": "light",
      "email_notifications": true
    }
  }
}
```

### 2. 更新用户信息
```http
PUT /api/v1/users/profile
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "full_name": "张同学",
  "email": "newemail@example.com",
  "phone": "13800138000",
  "school": "清华大学",
  "college": "计算机科学与技术学院"
}
```

### 3. 修改密码
```http
POST /api/v1/users/change-password
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

### 4. 上传头像
```http
POST /api/v1/users/avatar
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**请求体**
```
avatar: [file]
```

## 🤖 AI助手模块

### 1. 获取对话列表
```http
GET /api/v1/ai/conversations?page=1&page_size=20&status=active
Authorization: Bearer {access_token}
```

**响应数据**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "conversations": [
      {
        "id": "conv_123",
        "title": "数学学习计划",
        "message_count": 15,
        "last_message_at": "2024-06-24T10:30:00Z",
        "created_at": "2024-06-24T09:00:00Z",
        "status": "active"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 5,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 2. 创建新对话
```http
POST /api/v1/ai/conversations
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "title": "新的学习讨论"
}
```

### 3. 获取对话消息
```http
GET /api/v1/ai/conversations/{conversation_id}/messages?page=1&page_size=50
Authorization: Bearer {access_token}
```

**响应数据**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "messages": [
      {
        "id": "msg_001",
        "conversation_id": "conv_123",
        "content": "你好，我需要学习建议",
        "sender": "user",
        "message_type": "text",
        "created_at": "2024-06-24T10:25:00Z"
      },
      {
        "id": "msg_002",
        "conversation_id": "conv_123",
        "content": "你好！我很乐意为你提供学习建议...",
        "sender": "ai",
        "message_type": "text",
        "metadata": {
          "tokens": 120,
          "model": "deepseek-chat",
          "confidence": 0.95,
          "processing_time": 1.2
        },
        "created_at": "2024-06-24T10:25:30Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 50,
      "total": 15,
      "total_pages": 1
    }
  }
}
```

### 4. 发送消息
```http
POST /api/v1/ai/conversations/{conversation_id}/messages
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "content": "请帮我制定一个数学学习计划",
  "message_type": "text",
  "context": {
    "user_profile": {
      "grade": "大一",
      "major": "计算机科学",
      "weak_points": ["微积分", "线性代数"]
    },
    "current_course": "高等数学",
    "learning_goal": "期末考试准备"
  }
}
```

**响应数据**
```json
{
  "success": true,
  "code": 201,
  "data": {
    "user_message": {
      "id": "msg_003",
      "conversation_id": "conv_123",
      "content": "请帮我制定一个数学学习计划",
      "sender": "user",
      "message_type": "text",
      "created_at": "2024-06-24T10:30:00Z"
    },
    "ai_message": {
      "id": "msg_004",
      "conversation_id": "conv_123",
      "content": "根据你的情况，我为你制定以下学习计划...",
      "sender": "ai",
      "message_type": "text",
      "metadata": {
        "tokens": 200,
        "model": "deepseek-chat",
        "confidence": 0.92,
        "processing_time": 1.5
      },
      "created_at": "2024-06-24T10:30:02Z"
    }
  }
}
```

### 5. 流式消息发送
```http
POST /api/v1/ai/conversations/{conversation_id}/messages/stream
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "content": "解释一下导数的概念",
  "message_type": "text",
  "stream": true
}
```

**响应格式** (Server-Sent Events)
```
data: {"type": "start", "message_id": "msg_005"}

data: {"type": "content", "content": "导数是"}

data: {"type": "content", "content": "微积分中的"}

data: {"type": "content", "content": "重要概念..."}

data: {"type": "end", "message_id": "msg_005", "metadata": {"tokens": 150}}
```

### 6. 删除对话
```http
DELETE /api/v1/ai/conversations/{conversation_id}
Authorization: Bearer {access_token}
```

### 7. 获取学习建议
```http
POST /api/v1/ai/suggestions
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "type": "learning_plan",
  "context": {
    "subject": "数学",
    "current_level": "初级",
    "time_available": "2小时/天",
    "goals": ["提高计算能力", "理解基础概念"]
  }
}
```

### 8. 生成练习题
```http
POST /api/v1/ai/exercises/generate
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "subject": "数学",
  "topic": "导数",
  "difficulty": "medium",
  "count": 5,
  "question_type": "multiple_choice"
}
```

## 📚 课程管理模块

### 1. 获取课程列表
```http
GET /api/v1/courses?page=1&page_size=20&category=数学&difficulty=medium&status=published
Authorization: Bearer {access_token}
```

**响应数据**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "courses": [
      {
        "id": "course_123",
        "title": "高等数学基础",
        "description": "适合大一学生的高等数学入门课程",
        "cover_image_url": "https://example.com/course-cover.jpg",
        "teacher": {
          "id": "teacher_001",
          "full_name": "李教授",
          "avatar_url": "https://example.com/teacher-avatar.jpg"
        },
        "category": "数学",
        "difficulty": "intermediate",
        "duration_hours": 40,
        "enrolled_count": 1250,
        "rating": 4.8,
        "rating_count": 320,
        "is_enrolled": false,
        "created_at": "2024-06-24T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 45,
      "total_pages": 3
    }
  }
}
```

### 2. 获取课程详情
```http
GET /api/v1/courses/{course_id}
Authorization: Bearer {access_token}
```

### 3. 注册课程
```http
POST /api/v1/courses/{course_id}/enroll
Authorization: Bearer {access_token}
```

### 4. 获取我的课程
```http
GET /api/v1/courses/my-courses?status=active
Authorization: Bearer {access_token}
```

### 5. 更新学习进度
```http
PUT /api/v1/courses/{course_id}/progress
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "lesson_id": "lesson_001",
  "progress": 75.5,
  "completed_lessons": 8,
  "study_time": 120
}
```

## 💬 聊天室模块

### 1. 获取联系人列表
```http
GET /api/v1/chat/contacts?search=&role=all
Authorization: Bearer {access_token}
```

**响应数据**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "contacts": [
      {
        "id": "user_456",
        "full_name": "王老师",
        "avatar_url": "https://example.com/avatar.jpg",
        "role": "teacher",
        "status": "online",
        "last_seen": "2024-06-24T10:30:00Z",
        "unread_count": 3
      }
    ]
  }
}
```

### 2. 获取聊天记录
```http
GET /api/v1/chat/messages/{contact_id}?page=1&page_size=50
Authorization: Bearer {access_token}
```

### 3. 发送消息
```http
POST /api/v1/chat/messages
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "receiver_id": "user_456",
  "content": "老师您好，我有个问题想请教",
  "message_type": "text"
}
```

### 4. WebSocket连接
```
ws://localhost:8000/ws/chat
Authorization: Bearer {access_token}
```

**消息格式**
```json
{
  "type": "message",
  "data": {
    "receiver_id": "user_456",
    "content": "Hello",
    "message_type": "text"
  }
}
```

## 📝 练习系统模块

### 1. 获取练习列表
```http
GET /api/v1/exercises?subject=数学&difficulty=medium&page=1&page_size=20
Authorization: Bearer {access_token}
```

### 2. 获取练习详情
```http
GET /api/v1/exercises/{exercise_id}
Authorization: Bearer {access_token}
```

### 3. 提交答案
```http
POST /api/v1/exercises/{exercise_id}/submit
Authorization: Bearer {access_token}
```

**请求体**
```json
{
  "answer": {
    "choice": "A",
    "explanation": "根据导数定义..."
  }
}
```

### 4. 获取练习记录
```http
GET /api/v1/exercises/attempts?page=1&page_size=20
Authorization: Bearer {access_token}
```

## 📊 统计分析模块

### 1. 获取学习统计
```http
GET /api/v1/stats/learning
Authorization: Bearer {access_token}
```

### 2. 获取AI使用统计
```http
GET /api/v1/stats/ai-usage
Authorization: Bearer {access_token}
```

## 🔧 系统管理模块

### 1. 健康检查
```http
GET /api/v1/health
```

### 2. 系统信息
```http
GET /api/v1/system/info
Authorization: Bearer {access_token}
```

## 📋 错误码定义

| 错误码 | HTTP状态码 | 说明 | 处理建议 |
|--------|------------|------|----------|
| 200 | 200 | 请求成功 | - |
| 400 | 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 401 | 未授权访问 | 重新登录获取token |
| 403 | 403 | 权限不足 | 联系管理员 |
| 404 | 404 | 资源不存在 | 检查资源ID |
| 409 | 409 | 资源冲突 | 检查数据唯一性 |
| 422 | 422 | 数据验证失败 | 检查数据格式 |
| 429 | 429 | 请求频率过高 | 降低请求频率 |
| 500 | 500 | 服务器内部错误 | 稍后重试 |
| 503 | 503 | 服务不可用 | 稍后重试 |

---

**文档版本**：v1.0  
**创建日期**：2024-06-24  
**维护者**：后端开发团队

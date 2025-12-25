# 前端API需求文档

## 📋 概述

本文档定义了前端页面所需的API接口，为后端开发提供明确的需求规范。

## 🔐 认证系统

### 用户登录
```typescript
POST /api/auth/login
Content-Type: application/json

Request:
{
  "username": "string",
  "password": "string",
  "role": "student" | "teacher" | "admin"
}

Response:
{
  "success": boolean,
  "data": {
    "token": "string",
    "user": {
      "id": "string",
      "name": "string",
      "role": "student" | "teacher" | "admin",
      "avatar": "string",
      "email": "string"
    }
  },
  "message": "string"
}
```

### 用户信息获取
```typescript
GET /api/auth/profile
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": {
    "id": "string",
    "name": "string",
    "role": "string",
    "avatar": "string",
    "email": "string",
    "createdAt": "string",
    "lastLoginAt": "string"
  }
}
```

## 📊 学生仪表盘API

### 仪表盘数据
```typescript
GET /api/student/dashboard
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": {
    "stats": {
      "todayStudyTime": number,      // 今日学习时长(分钟)
      "completedTasks": number,      // 完成任务数
      "averageScore": number,        // 平均得分
      "studyProgress": number        // 学习进度百分比
    },
    "todos": [
      {
        "id": "string",
        "title": "string",
        "completed": boolean,
        "priority": "high" | "medium" | "low",
        "dueDate": "string"
      }
    ],
    "courses": [
      {
        "id": "string",
        "title": "string",
        "instructor": "string",
        "progress": number,
        "totalLessons": number,
        "completedLessons": number,
        "nextClass": "string"
      }
    ],
    "aiSuggestion": {
      "title": "string",
      "content": "string",
      "type": "focus" | "plan" | "exercise"
    }
  }
}
```

### 能力评估数据
```typescript
GET /api/student/abilities
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": {
    "overall": number,             // 综合评分
    "abilities": [
      {
        "name": "string",          // 能力名称
        "score": number,           // 得分(0-100)
        "category": "string"       // 分类
      }
    ],
    "radarData": [
      {
        "subject": "string",       // 科目
        "A": number,              // 当前值
        "fullMark": number        // 满分
      }
    ],
    "suggestion": "string"        // 提升建议
  }
}
```

## 📚 课程中心API

### 课程列表
```typescript
GET /api/student/courses
Authorization: Bearer {token}
Query Parameters:
  - page: number (default: 1)
  - limit: number (default: 10)
  - category: string (optional)
  - difficulty: string (optional)
  - search: string (optional)

Response:
{
  "success": boolean,
  "data": {
    "courses": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "instructor": "string",
        "category": "string",
        "difficulty": "初级" | "中级" | "高级",
        "duration": "string",
        "rating": number,
        "students": number,
        "progress": number,
        "totalLessons": number,
        "completedLessons": number,
        "nextClass": "string",
        "thumbnail": "string",
        "enrolled": boolean
      }
    ],
    "total": number,
    "page": number,
    "limit": number
  }
}
```

### 课程详情
```typescript
GET /api/student/courses/{courseId}
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "instructor": {
      "id": "string",
      "name": "string",
      "avatar": "string",
      "bio": "string"
    },
    "syllabus": [
      {
        "id": "string",
        "title": "string",
        "duration": "string",
        "completed": boolean,
        "locked": boolean
      }
    ],
    "progress": number,
    "enrollment": {
      "enrolledAt": "string",
      "lastAccessAt": "string"
    }
  }
}
```

## 📝 练习系统API

### 练习分类统计
```typescript
GET /api/student/exercises/stats
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": {
    "categories": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "icon": "string",
        "count": number,
        "completed": number,
        "accuracy": number
      }
    ],
    "dailyStats": {
      "todayExercises": number,
      "accuracy": number,
      "studyTime": number,
      "streak": number
    }
  }
}
```

### 练习列表
```typescript
GET /api/student/exercises
Authorization: Bearer {token}
Query Parameters:
  - category: string (optional)
  - status: "completed" | "in-progress" | "pending" (optional)
  - difficulty: string (optional)

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "title": "string",
      "subject": "string",
      "difficulty": "初级" | "中级" | "高级",
      "questions": number,
      "completed": number,
      "score": number | null,
      "timeSpent": "string",
      "status": "completed" | "in-progress" | "pending",
      "dueDate": "string",
      "type": "practice" | "homework" | "exam"
    }
  ]
}
```

### 错题本
```typescript
GET /api/student/exercises/wrong-questions
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "question": "string",
      "subject": "string",
      "difficulty": "string",
      "wrongAnswer": "string",
      "correctAnswer": "string",
      "explanation": "string",
      "wrongAt": "string",
      "reviewedAt": "string | null"
    }
  ]
}
```

## 🎯 学习中心API

### 学习计划
```typescript
GET /api/student/learning/plan
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": {
    "currentWeek": number,
    "totalWeeks": number,
    "completedTasks": number,
    "totalTasks": number,
    "weeklyGoal": "string",
    "progress": number,
    "tasks": [
      {
        "id": "string",
        "title": "string",
        "completed": boolean,
        "priority": "high" | "medium" | "low",
        "dueDate": "string"
      }
    ]
  }
}
```

### 学习资源
```typescript
GET /api/student/learning/resources
Authorization: Bearer {token}
Query Parameters:
  - type: "video" | "document" | "interactive" (optional)
  - category: string (optional)

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "type": "video" | "document" | "interactive",
      "category": "string",
      "thumbnail": "string",
      "rating": number,
      "duration": "string",      // for video
      "pages": number,           // for document
      "exercises": number,       // for interactive
      "views": number,
      "downloads": number,
      "completions": number
    }
  ]
}
```

### 收藏夹
```typescript
GET /api/student/learning/favorites
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "resourceId": "string",
      "title": "string",
      "type": "video" | "document" | "interactive",
      "category": "string",
      "addedAt": "string"
    }
  ]
}

POST /api/student/learning/favorites
Authorization: Bearer {token}
{
  "resourceId": "string"
}

DELETE /api/student/learning/favorites/{id}
Authorization: Bearer {token}
```

### 学习历史
```typescript
GET /api/student/learning/history
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "resourceId": "string",
      "title": "string",
      "type": "video" | "document" | "interactive",
      "category": "string",
      "progress": number,
      "lastAccessAt": "string",
      "totalTime": number
    }
  ]
}
```

## 🤖 AI助手API

### 发送消息
```typescript
POST /api/ai/chat
Authorization: Bearer {token}
{
  "message": "string",
  "sessionId": "string | null",
  "context": {
    "currentPage": "string",
    "userProgress": object
  }
}

Response:
{
  "success": boolean,
  "data": {
    "messageId": "string",
    "response": "string",
    "sessionId": "string",
    "suggestions": ["string"],
    "timestamp": "string"
  }
}
```

### 会话历史
```typescript
GET /api/ai/sessions
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "title": "string",
      "lastMessage": "string",
      "messageCount": number,
      "createdAt": "string",
      "updatedAt": "string"
    }
  ]
}

GET /api/ai/sessions/{sessionId}/messages
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "data": [
    {
      "id": "string",
      "content": "string",
      "sender": "user" | "ai",
      "timestamp": "string",
      "type": "text" | "suggestion" | "exercise"
    }
  ]
}
```

### 创建新会话
```typescript
POST /api/ai/sessions
Authorization: Bearer {token}
{
  "title": "string"
}

Response:
{
  "success": boolean,
  "data": {
    "sessionId": "string",
    "title": "string",
    "createdAt": "string"
  }
}
```

### 删除会话
```typescript
DELETE /api/ai/sessions/{sessionId}
Authorization: Bearer {token}

Response:
{
  "success": boolean,
  "message": "string"
}
```

## 📈 通用响应格式

### 成功响应
```typescript
{
  "success": true,
  "data": any,
  "message": "string (optional)"
}
```

### 错误响应
```typescript
{
  "success": false,
  "error": {
    "code": "string",
    "message": "string",
    "details": "string (optional)"
  }
}
```

### 分页响应
```typescript
{
  "success": true,
  "data": {
    "items": any[],
    "pagination": {
      "page": number,
      "limit": number,
      "total": number,
      "totalPages": number,
      "hasNext": boolean,
      "hasPrev": boolean
    }
  }
}
```

## 🔧 技术要求

### HTTP状态码
- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `403` - 禁止访问
- `404` - 资源不存在
- `500` - 服务器错误

### 请求头
```
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
```

### 数据格式
- 时间格式: ISO 8601 (`2024-03-15T10:30:00Z`)
- 数字精度: 小数点后2位
- 字符编码: UTF-8

---

**API版本**: v1.0  
**文档更新**: 2024年3月15日  
**联系人**: 前端开发团队

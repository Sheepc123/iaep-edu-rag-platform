# 课程编辑模块数据库文档

## 概述
课程编辑模块是教师端的核心功能，允许教师对已创建的课程进行全面管理，包括基本信息编辑、学生管理、文件管理等功能。该模块基于现有的课程管理数据库结构，提供了丰富的编辑和管理功能。

## 功能特性
- **课程信息编辑**: 修改课程标题、描述、分类、难度等基本信息
- **学生管理**: 查看课程注册学生列表、移除学生、查看学习进度
- **文件管理**: 上传、下载、删除课程相关文件
- **权限控制**: 只有课程创建者可以编辑课程
- **实时数据**: 实时显示学生学习进度和统计信息

## 数据库表结构

### 主要使用的表

#### 1. courses 表
课程编辑模块主要操作此表进行课程基本信息的更新。

**编辑字段**:
- `title`: 课程标题
- `description`: 课程描述  
- `category`: 课程分类
- `difficulty`: 难度级别
- `duration`: 课程时长
- `cover_image`: 封面图片
- `is_published`: 发布状态
- `updated_at`: 更新时间

**权限验证**:
- 通过 `instructor_id` 字段验证编辑权限
- 只有课程创建者可以编辑课程信息

#### 2. course_enrollments 表
用于学生管理功能，查看和管理课程注册学生。

**查询字段**:
- `student_id`: 学生ID（关联users表）
- `progress_percentage`: 学习进度百分比
- `completed_lessons`: 已完成课时数
- `total_study_time`: 总学习时间
- `is_completed`: 是否完成课程
- `enrolled_at`: 注册时间
- `last_accessed_at`: 最后访问时间
- `is_active`: 注册状态（用于软删除）

**学生移除操作**:
- 设置 `is_active = FALSE` 实现软删除
- 同时更新courses表的 `enrolled_students` 计数

#### 3. users 表
关联查询获取学生详细信息。

**关联字段**:
- `id`: 用户ID
- `username`: 用户名
- `full_name`: 真实姓名
- `email`: 邮箱
- `avatar_url`: 头像URL

## API接口设计

### 课程编辑相关接口

#### 1. 获取课程学生列表
```http
GET /api/v1/courses/teacher/courses/{course_id}/students
Authorization: Bearer <teacher_token>
```

**响应数据**:
```json
[
  {
    "id": 1,
    "username": "student1",
    "full_name": "张三",
    "email": "student1@example.com",
    "avatar_url": "https://example.com/avatar.jpg",
    "enrolled_at": "2024-01-01T00:00:00Z",
    "progress_percentage": 75.5,
    "completed_lessons": 8,
    "total_study_time": 480,
    "is_completed": false,
    "last_accessed_at": "2024-01-15T10:30:00Z"
  }
]
```

#### 2. 移除课程学生
```http
DELETE /api/v1/courses/teacher/courses/{course_id}/students/{student_id}
Authorization: Bearer <teacher_token>
```

**响应数据**:
```json
{
  "message": "学生已成功移除",
  "success": true
}
```

#### 3. 获取课程文件列表
```http
GET /api/v1/courses/teacher/courses/{course_id}/files
Authorization: Bearer <teacher_token>
```

**响应数据**:
```json
[
  {
    "id": "file_uuid",
    "name": "课程资料.pdf",
    "size": 1024000,
    "type": "application/pdf",
    "url": "https://example.com/files/course_material.pdf",
    "uploaded_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 4. 上传课程文件
```http
POST /api/v1/courses/teacher/courses/{course_id}/files
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "name": "新文件.pdf",
  "size": 2048000,
  "type": "application/pdf",
  "url": "https://example.com/files/new_file.pdf"
}
```

#### 5. 删除课程文件
```http
DELETE /api/v1/courses/teacher/courses/{course_id}/files/{file_id}
Authorization: Bearer <teacher_token>
```

**响应数据**:
```json
{
  "message": "文件已成功删除",
  "success": true
}
```

## 业务逻辑说明

### 课程信息编辑流程
1. 验证教师身份和课程编辑权限
2. 验证输入数据的有效性
3. 更新课程基本信息
4. 记录更新时间
5. 返回更新后的课程信息

### 学生管理流程
1. **查看学生列表**:
   - 验证教师权限
   - 关联查询课程注册表和用户表
   - 返回学生详细信息和学习进度

2. **移除学生**:
   - 验证教师权限和学生注册状态
   - 设置注册记录为非活跃状态（软删除）
   - 更新课程注册人数统计
   - 记录操作日志

### 文件管理流程
1. **文件列表查询**:
   - 验证教师权限
   - 从文件存储系统获取课程相关文件
   - 返回文件基本信息和下载链接

2. **文件上传**:
   - 验证教师权限和文件格式
   - 保存文件到指定存储位置
   - 记录文件元数据
   - 返回文件访问信息

3. **文件删除**:
   - 验证教师权限和文件所有权
   - 从存储系统删除文件
   - 清理文件元数据记录

## 权限控制

### 教师权限验证
```sql
-- 验证课程编辑权限
SELECT id FROM courses 
WHERE id = ? AND instructor_id = ?
```

### 操作权限矩阵
| 操作 | 课程创建者 | 其他教师 | 学生 | 管理员 |
|------|-----------|----------|------|--------|
| 编辑课程信息 | ✅ | ❌ | ❌ | ✅ |
| 查看学生列表 | ✅ | ❌ | ❌ | ✅ |
| 移除学生 | ✅ | ❌ | ❌ | ✅ |
| 管理文件 | ✅ | ❌ | ❌ | ✅ |

## 数据统计

### 学生学习统计
- **进度计算**: `progress_percentage = (completed_lessons / total_lessons) * 100`
- **学习时间**: 累计所有课时的学习时间
- **完成状态**: 基于进度百分比和课时完成情况判断

### 课程统计更新
- **注册人数**: 移除学生时自动更新 `enrolled_students` 字段
- **评分统计**: 学生移除后重新计算平均评分
- **活跃度**: 基于学生最后访问时间统计活跃学生数

## 性能优化

### 数据库优化
```sql
-- 课程学生查询优化索引
CREATE INDEX idx_course_enrollments_course_active 
ON course_enrollments(course_id, is_active);

-- 学生进度查询优化
CREATE INDEX idx_course_enrollments_student_progress 
ON course_enrollments(student_id, progress_percentage);
```

### 查询优化策略
- 使用JOIN查询减少数据库往返次数
- 对大量学生的课程使用分页查询
- 缓存课程基本信息减少重复查询
- 异步更新统计数据避免阻塞主流程

## 安全考虑

### 数据安全
- 所有操作都需要验证教师身份和权限
- 学生移除采用软删除，保留历史记录
- 文件操作需要验证文件所有权
- 敏感信息（如学生邮箱）需要权限控制

### 操作审计
- 记录所有编辑操作的时间和操作者
- 学生移除操作需要记录详细日志
- 文件操作需要记录访问和修改历史

## 扩展功能

### 高级学生管理
- 批量移除学生功能
- 学生学习报告生成
- 学习进度预警机制
- 学生分组管理功能

### 文件管理增强
- 文件版本控制
- 文件分享权限设置
- 文件预览功能
- 批量文件操作

### 数据分析
- 学生学习行为分析
- 课程质量评估指标
- 教学效果统计报告
- 学习路径优化建议

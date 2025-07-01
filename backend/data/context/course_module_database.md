# 课程管理模块数据库文档

## 概述
课程管理模块是智能教育平台的核心功能模块，负责课程的创建、管理、发布和学习进度跟踪。该模块支持教师创建和管理课程内容，学生注册学习课程，以及完整的学习进度跟踪系统。

## 功能特性
- **课程管理**: 支持课程的创建、编辑、发布和删除
- **课时管理**: 多种类型课时内容管理(视频、文本、互动、测验)
- **学习跟踪**: 完整的学习进度跟踪和统计
- **课程注册**: 学生课程注册和退课管理
- **评价系统**: 课程评分和评价功能
- **分类筛选**: 课程分类、难度级别筛选
- **搜索功能**: 支持课程标题、描述的全文搜索

## 数据库表结构

### 1. courses 表 - 课程基础信息
**用途**: 存储课程的基本信息、属性和统计数据

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 课程唯一标识 |
| title | VARCHAR(200) | NOT NULL, INDEX | 课程标题 |
| description | TEXT | NULL | 课程详细描述 |
| cover_image | VARCHAR(255) | NULL | 课程封面图片URL |
| category | VARCHAR(50) | NULL | 课程分类 |
| difficulty | VARCHAR(20) | DEFAULT 'medium' | 难度级别(easy/medium/hard) |
| duration | INTEGER | NULL | 课程总时长(分钟) |
| total_lessons | INTEGER | DEFAULT 0 | 总课时数 |
| instructor_id | INTEGER | FOREIGN KEY, NOT NULL | 教师用户ID |
| instructor_name | VARCHAR(100) | NOT NULL | 教师姓名 |
| enrolled_students | INTEGER | DEFAULT 0 | 注册学生数 |
| rating | FLOAT | DEFAULT 0.0 | 课程平均评分 |
| rating_count | INTEGER | DEFAULT 0 | 评分人数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| is_published | BOOLEAN | DEFAULT FALSE | 是否发布 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_courses_instructor_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_courses_title` ON title
- `idx_courses_category` ON category
- `idx_courses_difficulty` ON difficulty
- `idx_courses_instructor_id` ON instructor_id
- `idx_courses_is_published` ON is_published

**默认数据**:
```sql
-- 示例课程
INSERT INTO courses (title, description, category, difficulty, duration, total_lessons, instructor_id, instructor_name, is_published)
VALUES ('Python编程基础', '学习Python编程语言的基础知识，适合初学者入门', '编程语言', 'easy', 1200, 3, 1, 'teacher1', 1);
```

**业务规则**:
- 课程标题不能为空且长度不超过200字符
- 难度级别只能是 easy、medium、hard 之一
- 只有发布的课程才能被学生搜索和注册
- 教师只能管理自己创建的课程
- 删除课程时会级联删除相关的课时和注册记录

### 2. lessons 表 - 课时内容管理
**用途**: 存储课程中的具体课时内容和学习资源

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 课时唯一标识 |
| course_id | INTEGER | FOREIGN KEY, NOT NULL | 所属课程ID |
| title | VARCHAR(200) | NOT NULL | 课时标题 |
| description | TEXT | NULL | 课时描述 |
| content | TEXT | NULL | 课时内容 |
| lesson_order | INTEGER | NOT NULL | 课时顺序 |
| duration | INTEGER | NULL | 课时时长(分钟) |
| lesson_type | VARCHAR(20) | DEFAULT 'video' | 课时类型 |
| video_url | VARCHAR(255) | NULL | 视频资源URL |
| materials | TEXT | NULL | 学习材料(JSON格式) |
| is_published | BOOLEAN | DEFAULT FALSE | 是否发布 |
| is_free | BOOLEAN | DEFAULT FALSE | 是否免费 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_lessons_course_id` REFERENCES courses(id) ON DELETE CASCADE

**索引**:
- `idx_lessons_course_id` ON course_id
- `idx_lessons_order` ON (course_id, lesson_order)
- `idx_lessons_type` ON lesson_type

**课时类型说明**:
- `video`: 视频课时
- `text`: 文本课时
- `interactive`: 互动课时
- `quiz`: 测验课时

**默认数据**:
```sql
-- 示例课时
INSERT INTO lessons (course_id, title, description, content, lesson_order, duration, lesson_type, is_published, is_free)
VALUES 
(1, 'Python环境搭建', '学习如何安装和配置Python开发环境', '本课时将介绍Python的安装过程...', 1, 30, 'video', 1, 1),
(1, 'Python基础语法', '学习Python的基本语法规则', 'Python语法简洁明了...', 2, 45, 'video', 1, 0),
(1, '变量和数据类型', '了解Python中的变量定义和数据类型', 'Python支持多种数据类型...', 3, 40, 'interactive', 1, 0);
```

### 3. course_enrollments 表 - 课程注册管理
**用途**: 管理学生的课程注册信息和学习进度

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 注册记录唯一标识 |
| course_id | INTEGER | FOREIGN KEY, NOT NULL | 课程ID |
| student_id | INTEGER | FOREIGN KEY, NOT NULL | 学生用户ID |
| progress_percentage | FLOAT | DEFAULT 0.0 | 学习进度百分比 |
| completed_lessons | INTEGER | DEFAULT 0 | 已完成课时数 |
| total_study_time | INTEGER | DEFAULT 0 | 总学习时间(分钟) |
| rating | FLOAT | NULL | 学生评分 |
| review | TEXT | NULL | 学生评价 |
| is_completed | BOOLEAN | DEFAULT FALSE | 是否完成课程 |
| is_active | BOOLEAN | DEFAULT TRUE | 注册是否有效 |
| enrolled_at | DATETIME | NOT NULL | 注册时间 |
| completed_at | DATETIME | NULL | 完成时间 |
| last_accessed_at | DATETIME | NULL | 最后访问时间 |

**外键约束**:
- `fk_course_enrollments_course_id` REFERENCES courses(id) ON DELETE CASCADE
- `fk_course_enrollments_student_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_course_enrollments_course_student` ON (course_id, student_id) UNIQUE
- `idx_course_enrollments_student_id` ON student_id
- `idx_course_enrollments_progress` ON progress_percentage

**业务规则**:
- 同一学生不能重复注册同一课程
- 进度百分比范围为0-100
- 完成课程时自动设置完成时间
- 评分范围为1-5分

### 4. lesson_progress 表 - 课时学习进度
**用途**: 详细记录学生对每个课时的学习进度

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 进度记录唯一标识 |
| enrollment_id | INTEGER | FOREIGN KEY, NOT NULL | 课程注册ID |
| lesson_id | INTEGER | FOREIGN KEY, NOT NULL | 课时ID |
| student_id | INTEGER | FOREIGN KEY, NOT NULL | 学生用户ID |
| progress_percentage | FLOAT | DEFAULT 0.0 | 课时完成百分比 |
| study_time | INTEGER | DEFAULT 0 | 学习时间(分钟) |
| is_completed | BOOLEAN | DEFAULT FALSE | 是否完成 |
| notes | TEXT | NULL | 学习笔记 |
| last_position | INTEGER | DEFAULT 0 | 最后学习位置(秒) |
| started_at | DATETIME | NULL | 开始学习时间 |
| completed_at | DATETIME | NULL | 完成时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_lesson_progress_enrollment_id` REFERENCES course_enrollments(id) ON DELETE CASCADE
- `fk_lesson_progress_lesson_id` REFERENCES lessons(id) ON DELETE CASCADE
- `fk_lesson_progress_student_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_lesson_progress_enrollment_lesson` ON (enrollment_id, lesson_id) UNIQUE
- `idx_lesson_progress_student_id` ON student_id
- `idx_lesson_progress_lesson_id` ON lesson_id

## 数据关系图

```
users (1) ←→ (n) courses (instructor_id)
users (1) ←→ (n) course_enrollments (student_id)
courses (1) ←→ (n) lessons
courses (1) ←→ (n) course_enrollments
course_enrollments (1) ←→ (n) lesson_progress
lessons (1) ←→ (n) lesson_progress
```

## 业务逻辑说明

### 课程创建流程
1. 教师创建课程基本信息
2. 添加课时内容和资源
3. 设置课程发布状态
4. 系统自动计算总时长和课时数

### 学生注册流程
1. 学生浏览课程列表
2. 查看课程详情和课时安排
3. 点击注册课程
4. 系统创建注册记录
5. 更新课程注册人数统计

### 学习进度跟踪
1. 学生开始学习课时
2. 系统记录学习时间和进度
3. 自动更新课时完成状态
4. 计算整体课程进度
5. 记录学习笔记和位置

### 课程评价流程
1. 学生完成课程学习
2. 提交课程评分和评价
3. 系统更新课程平均评分
4. 更新评分人数统计

## API接口设计

### 课程管理接口
```http
GET    /api/v1/courses                    # 获取课程列表
POST   /api/v1/courses                    # 创建课程
GET    /api/v1/courses/{id}               # 获取课程详情
PUT    /api/v1/courses/{id}               # 更新课程
DELETE /api/v1/courses/{id}               # 删除课程
```

### 课时管理接口
```http
GET    /api/v1/courses/{id}/lessons       # 获取课程课时列表
POST   /api/v1/courses/{id}/lessons       # 创建课时
PUT    /api/v1/lessons/{id}               # 更新课时
DELETE /api/v1/lessons/{id}               # 删除课时
```

### 学习管理接口
```http
POST   /api/v1/courses/{id}/enroll        # 注册课程
GET    /api/v1/courses/my-courses         # 获取我的课程
POST   /api/v1/lessons/{id}/progress      # 更新学习进度
GET    /api/v1/courses/{id}/progress      # 获取课程进度
```

## 前端页面对应

### 学生端页面
- **课程列表页** (`/student/courses`): 显示所有可注册课程
- **课程详情页** (`/student/courses/{id}`): 课程详细信息和注册
- **我的课程页** (`/student/learning`): 已注册课程和学习进度
- **课时学习页** (`/student/lessons/{id}`): 具体课时内容学习

### 教师端页面
- **课程管理页** (`/teacher/courses`): 管理所有创建的课程
- **课程创建页** (`/teacher/courses/create`): 创建新课程
- **课程编辑页** (`/teacher/courses/{id}/edit`): 编辑课程信息
- **课程详情页** (`/teacher/courses/{id}`): 查看课程统计和学生情况

## 性能优化

### 数据库优化
```sql
-- 关键索引
CREATE INDEX idx_courses_search ON courses(title, category, difficulty);
CREATE INDEX idx_lessons_course_order ON lessons(course_id, lesson_order);
CREATE INDEX idx_enrollments_student_active ON course_enrollments(student_id, is_active);
CREATE INDEX idx_progress_completion ON lesson_progress(student_id, is_completed);
```

### 查询优化
- 课程列表使用分页查询，避免一次加载过多数据
- 学习进度使用增量更新，减少数据库写入频率
- 课程统计信息使用缓存，定期更新
- 搜索功能使用全文索引提高性能

### 缓存策略
- **课程列表**: Redis缓存热门课程，TTL 30分钟
- **课程详情**: 缓存课程基本信息，TTL 1小时
- **学习进度**: 内存缓存当前学习状态，定期同步数据库
- **统计数据**: 缓存课程统计信息，每小时更新

## 扩展功能

### 高级功能
- **课程推荐**: 基于学习历史的智能推荐
- **学习路径**: 多课程组合的学习路径规划
- **证书系统**: 课程完成证书生成
- **直播课程**: 实时直播课程支持
- **作业系统**: 课程作业提交和批改

### 数据分析
- **学习分析**: 学习行为数据分析
- **课程质量**: 课程质量评估指标
- **教学效果**: 教学效果统计分析
- **用户画像**: 学生学习偏好分析

# 课程管理模块开发文档 v1.0

## 📋 模块概述

### 基本信息
- **模块名称**: 课程管理模块 (Course Management Module)
- **开发状态**: ✅ 完成开发
- **技术栈**: FastAPI + SQLAlchemy + Pydantic
- **文档版本**: v1.0
- **最后更新**: 2024-06-24

### 功能定位
提供完整的课程管理功能，包括课程创建、课时管理、学习进度跟踪、课程评价等核心功能，为教师和学生提供完整的教学和学习体验。

## 🎯 功能特性

### 1. 课程基础管理
- ✅ **课程CRUD**: 创建、查询、更新、删除课程
- ✅ **课程分类**: 支持课程分类和难度级别
- ✅ **课程发布**: 发布状态控制，支持草稿模式
- ✅ **课程搜索**: 多条件搜索和排序功能
- ✅ **权限控制**: 教师只能管理自己的课程

### 2. 课时内容管理
- ✅ **课时CRUD**: 完整的课时管理功能
- ✅ **多种类型**: 支持视频、文本、互动、测验等类型
- ✅ **顺序管理**: 课时顺序控制和调整
- ✅ **资源管理**: 视频URL、学习材料管理
- ✅ **发布控制**: 课时级别的发布状态

### 3. 学习进度跟踪
- ✅ **课程注册**: 学生课程注册管理
- ✅ **进度记录**: 详细的学习进度跟踪
- ✅ **完成统计**: 课时完成度和课程完成率
- ✅ **学习时间**: 学习时间统计和分析
- ✅ **学习笔记**: 支持学习笔记记录

### 4. 课程评价系统
- ✅ **课程评分**: 1-5星评分系统
- ✅ **评价内容**: 文字评价和反馈
- ✅ **评分统计**: 平均评分和评分人数
- ✅ **权限验证**: 只有注册学生可以评价

### 5. 统计分析功能
- ✅ **课程统计**: 课程数量、发布状态统计
- ✅ **学生统计**: 注册学生数、完成率统计
- ✅ **评分分析**: 平均评分、评价趋势分析
- ✅ **教师视图**: 教师个人课程统计

## 🏗️ 技术架构

### 模块结构
```
course_module/
├── schemas/course.py        # 数据验证模式
├── services/
│   └── course_service.py    # 课程业务逻辑
├── models/course.py         # 课程数据模型
├── api/endpoints/
│   └── courses.py          # 课程API端点
└── test_courses.py         # 功能测试脚本
```

### 数据模型设计

#### 1. 课程模型 (Course)
```python
- id: 课程ID (主键)
- title: 课程标题
- description: 课程描述
- cover_image: 封面图片URL
- category: 课程分类
- difficulty: 难度级别 (easy/medium/hard)
- duration: 课程总时长(分钟)
- total_lessons: 总课时数
- instructor_id: 教师ID (外键)
- instructor_name: 教师姓名
- enrolled_students: 注册学生数
- rating: 课程评分
- rating_count: 评分人数
- is_active: 是否激活
- is_published: 是否发布
- created_at: 创建时间
- updated_at: 更新时间
```

#### 2. 课时模型 (Lesson)
```python
- id: 课时ID (主键)
- course_id: 课程ID (外键)
- title: 课时标题
- description: 课时描述
- content: 课时内容
- lesson_order: 课时顺序
- duration: 课时时长(分钟)
- lesson_type: 课时类型 (video/text/interactive/quiz)
- video_url: 视频URL
- materials: 学习材料 (JSON格式)
- is_published: 是否发布
- is_free: 是否免费
- created_at: 创建时间
- updated_at: 更新时间
```

#### 3. 课程注册模型 (CourseEnrollment)
```python
- id: 注册ID (主键)
- course_id: 课程ID (外键)
- student_id: 学生ID (外键)
- progress_percentage: 学习进度百分比
- completed_lessons: 已完成课时数
- total_study_time: 总学习时间(分钟)
- rating: 学生评分
- review: 评价内容
- is_completed: 是否完成
- is_active: 是否激活
- enrolled_at: 注册时间
- completed_at: 完成时间
- last_accessed: 最后访问时间
```

#### 4. 课时进度模型 (LessonProgress)
```python
- id: 进度ID (主键)
- lesson_id: 课时ID (外键)
- student_id: 学生ID (外键)
- progress_percentage: 进度百分比
- watch_time: 观看时间(秒)
- is_completed: 是否完成
- notes: 学习笔记
- bookmarks: 书签 (JSON格式)
- started_at: 开始时间
- completed_at: 完成时间
- last_accessed: 最后访问时间
```

## 🔧 API接口设计

### 课程管理接口

#### 1. 创建课程
```http
POST /api/v1/courses/
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "title": "Python编程基础",
  "description": "从零开始学习Python编程",
  "category": "编程语言",
  "difficulty": "medium",
  "duration": 1200,
  "cover_image": "https://example.com/cover.jpg",
  "is_published": true
}
```

#### 2. 获取课程列表
```http
GET /api/v1/courses/?category=编程语言&difficulty=medium&search=Python&skip=0&limit=20
```

#### 3. 获取课程详情
```http
GET /api/v1/courses/{course_id}
```

#### 4. 更新课程
```http
PUT /api/v1/courses/{course_id}
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "title": "Python编程进阶",
  "difficulty": "hard"
}
```

#### 5. 删除课程
```http
DELETE /api/v1/courses/{course_id}
Authorization: Bearer <teacher_token>
```

### 课程注册接口

#### 1. 注册课程
```http
POST /api/v1/courses/{course_id}/enroll
Authorization: Bearer <student_token>
```

#### 2. 获取我的课程
```http
GET /api/v1/courses/my-courses
Authorization: Bearer <student_token>
```

#### 3. 课程评分
```http
POST /api/v1/courses/{course_id}/rate
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "rating": 4.5,
  "review": "课程内容很好，讲解清晰"
}
```

### 课时管理接口

#### 1. 创建课时
```http
POST /api/v1/courses/{course_id}/lessons
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "title": "Python基础语法",
  "description": "学习Python基本语法",
  "content": "# Python基础语法\n\n...",
  "lesson_order": 1,
  "duration": 60,
  "lesson_type": "video",
  "video_url": "https://example.com/lesson1.mp4",
  "is_published": true,
  "is_free": true
}
```

#### 2. 获取课程课时列表
```http
GET /api/v1/courses/{course_id}/lessons?include_unpublished=false
Authorization: Bearer <token>
```

#### 3. 更新课时学习进度
```http
POST /api/v1/courses/lessons/{lesson_id}/progress
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "progress_percentage": 75.0,
  "watch_time": 2700,
  "is_completed": false,
  "notes": "学习笔记内容"
}
```

### 统计分析接口

#### 1. 获取课程统计
```http
GET /api/v1/courses/statistics
Authorization: Bearer <teacher_token>
```

## 🔒 权限控制

### 1. 教师权限
- **课程管理**: 只能管理自己创建的课程
- **课时管理**: 只能管理自己课程的课时
- **统计查看**: 只能查看自己课程的统计信息
- **学生管理**: 可以查看注册自己课程的学生

### 2. 学生权限
- **课程浏览**: 可以浏览所有已发布的课程
- **课程注册**: 可以注册已发布的课程
- **学习进度**: 只能管理自己的学习进度
- **课程评价**: 只能评价已注册的课程

### 3. 管理员权限
- **全局管理**: 可以管理所有课程和课时
- **统计查看**: 可以查看全局统计信息
- **用户管理**: 可以管理所有用户的课程数据

## 🧪 测试验证

### 测试脚本功能
提供了完整的测试脚本 `test_courses.py`，包含：

1. **教师登录**: 测试教师身份认证
2. **学生登录**: 测试学生身份认证
3. **创建课程**: 测试课程创建功能
4. **创建课时**: 测试课时创建功能
5. **获取课程列表**: 测试课程查询功能
6. **课程注册**: 测试学生注册课程
7. **学习进度**: 测试学习进度更新
8. **统计信息**: 测试统计数据获取

### 运行测试
```bash
# 确保后端服务运行
python run.py

# 运行课程测试
python test_courses.py
```

## 📊 业务流程

### 教师创建课程流程
```
1. 教师登录系统
2. 创建课程基本信息
3. 添加课时内容
4. 设置课时顺序和类型
5. 上传学习资源
6. 发布课程
7. 查看学生注册情况
8. 分析课程统计数据
```

### 学生学习流程
```
1. 学生登录系统
2. 浏览课程列表
3. 查看课程详情
4. 注册感兴趣的课程
5. 按顺序学习课时
6. 记录学习进度和笔记
7. 完成课程学习
8. 对课程进行评价
```

### 学习进度跟踪流程
```
1. 学生开始学习课时
2. 系统记录学习时间
3. 更新课时进度百分比
4. 标记课时完成状态
5. 计算课程整体进度
6. 更新课程注册信息
7. 生成学习统计报告
```

## 🚀 部署说明

### 数据库迁移
```bash
# 生成迁移文件
alembic revision --autogenerate -m "Add course management tables"

# 执行迁移
alembic upgrade head
```

### API文档
启动服务后访问 http://127.0.0.1:8000/docs 查看完整的课程管理API文档

## 📈 性能优化

### 1. 数据库优化
- 课程标题和分类字段建立索引
- 课时顺序字段建立索引
- 学习进度按学生和课程建立复合索引
- 定期清理无效的学习记录

### 2. 查询优化
- 课程列表查询支持分页
- 使用预加载减少N+1查询问题
- 统计信息使用聚合查询
- 热门课程数据缓存

### 3. 业务优化
- 课程发布状态控制访问权限
- 学习进度批量更新
- 评分计算异步处理
- 统计数据定时更新

## 🔄 后续扩展

### 短期计划
- [ ] 课程分类管理功能
- [ ] 学习计划制定功能
- [ ] 课程推荐算法
- [ ] 学习报告生成

### 中期计划
- [ ] 直播课程支持
- [ ] 作业提交系统
- [ ] 讨论区功能
- [ ] 证书颁发系统

### 长期计划
- [ ] AI智能推荐
- [ ] 个性化学习路径
- [ ] 学习效果分析
- [ ] 多媒体内容支持

---

**文档维护**: 后端开发团队  
**版本**: v1.0  
**日期**: 2024-06-24

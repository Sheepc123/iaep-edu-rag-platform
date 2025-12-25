# 习题系统模块数据库文档

## 概述
习题系统模块是智能教育平台的重要功能模块，负责习题的创建、管理、发布和学生答题跟踪。该模块支持教师创建多种类型的习题（自主练习、课后作业、模拟考试等），学生完成答题，以及完整的答题记录和统计分析。

## 功能特性
- **习题管理**: 支持习题的创建、编辑、发布和删除
- **多种题型**: 支持选择题、填空题、问答题等多种题型
- **分类管理**: 自主练习、课后作业、模拟考试、错题本等分类
- **课程绑定**: 习题与课程紧密关联，支持课程专属习题
- **答题跟踪**: 完整的学生答题记录和进度跟踪
- **统计分析**: 习题完成率、正确率、平均分等统计
- **时间控制**: 支持限时答题和答题时长统计
- **自动评分**: 客观题自动评分，主观题支持手动评分

## 数据库表结构

### 1. exercises 表 - 习题集基础信息
**用途**: 存储习题集的基本信息、属性和统计数据

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 习题集唯一标识 |
| title | VARCHAR(200) | NOT NULL, INDEX | 习题集标题 |
| description | TEXT | NULL | 习题集详细描述 |
| category | VARCHAR(50) | NOT NULL | 习题分类(practice/homework/exam/review) |
| subject | VARCHAR(50) | NOT NULL | 科目分类 |
| difficulty | VARCHAR(20) | DEFAULT 'medium' | 难度级别(easy/medium/hard) |
| time_limit | INTEGER | NULL | 时间限制(分钟) |
| created_by | INTEGER | FOREIGN KEY, NOT NULL | 创建者用户ID |
| course_id | INTEGER | FOREIGN KEY, NULL | 关联课程ID |
| total_questions | INTEGER | DEFAULT 0 | 题目总数 |
| total_attempts | INTEGER | DEFAULT 0 | 总尝试次数 |
| average_score | FLOAT | DEFAULT 0.0 | 平均分数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| is_published | BOOLEAN | DEFAULT FALSE | 是否发布 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_exercises_created_by` REFERENCES users(id) ON DELETE CASCADE
- `fk_exercises_course_id` REFERENCES courses(id) ON DELETE CASCADE

**索引**:
- `idx_exercises_title` ON title
- `idx_exercises_category` ON category
- `idx_exercises_subject` ON subject
- `idx_exercises_course_id` ON course_id
- `idx_exercises_created_by` ON created_by
- `idx_exercises_is_published` ON is_published

**习题分类说明**:
- `practice`: 自主练习 - 学生自由练习，不计入成绩
- `homework`: 课后作业 - 教师布置的作业，计入平时成绩
- `exam`: 模拟考试 - 模拟考试环境，严格计时
- `review`: 复习练习 - 复习巩固用练习

**默认数据**:
```sql
-- 示例习题集
INSERT INTO exercises (title, description, category, subject, difficulty, time_limit, created_by, course_id, is_published)
VALUES ('Python基础练习', '测试Python基础语法和概念的练习题', 'practice', 'Python编程', 'easy', 30, 1, 1, 1);
```

### 2. questions 表 - 题目内容管理
**用途**: 存储具体的题目内容、选项和答案

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 题目唯一标识 |
| exercise_id | INTEGER | FOREIGN KEY, NULL | 所属习题集ID |
| title | VARCHAR(200) | NULL | 题目标题 |
| content | TEXT | NOT NULL | 题目内容 |
| question_type | VARCHAR(20) | NOT NULL | 题目类型 |
| options | JSON | NULL | 选择题选项(JSON格式) |
| correct_answer | TEXT | NOT NULL | 正确答案 |
| explanation | TEXT | NULL | 答案解析 |
| difficulty | VARCHAR(20) | DEFAULT 'medium' | 难度级别 |
| points | INTEGER | DEFAULT 10 | 题目分值 |
| subject | VARCHAR(50) | NULL | 科目分类 |
| tags | TEXT | NULL | 题目标签(JSON格式) |
| total_attempts | INTEGER | DEFAULT 0 | 总答题次数 |
| correct_attempts | INTEGER | DEFAULT 0 | 正确答题次数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_questions_exercise_id` REFERENCES exercises(id) ON DELETE CASCADE

**索引**:
- `idx_questions_exercise_id` ON exercise_id
- `idx_questions_type` ON question_type
- `idx_questions_difficulty` ON difficulty
- `idx_questions_subject` ON subject

**题目类型说明**:
- `multiple_choice`: 选择题 - 单选或多选
- `fill_blank`: 填空题 - 填入正确答案
- `essay`: 问答题 - 主观题，需要文字回答

**选项格式示例**:
```json
{
  "A": "选项A内容",
  "B": "选项B内容", 
  "C": "选项C内容",
  "D": "选项D内容"
}
```

### 3. exercise_attempts 表 - 答题尝试记录
**用途**: 记录学生的答题尝试和完成情况

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 尝试记录唯一标识 |
| exercise_id | INTEGER | FOREIGN KEY, NOT NULL | 习题集ID |
| student_id | INTEGER | FOREIGN KEY, NOT NULL | 学生用户ID |
| total_questions | INTEGER | NOT NULL | 题目总数 |
| answered_questions | INTEGER | DEFAULT 0 | 已答题目数 |
| correct_answers | INTEGER | DEFAULT 0 | 正确答案数 |
| score | FLOAT | DEFAULT 0.0 | 得分 |
| max_score | FLOAT | NOT NULL | 满分 |
| time_spent | INTEGER | DEFAULT 0 | 用时(秒) |
| is_completed | BOOLEAN | DEFAULT FALSE | 是否完成 |
| is_submitted | BOOLEAN | DEFAULT FALSE | 是否提交 |
| started_at | DATETIME | NOT NULL | 开始时间 |
| completed_at | DATETIME | NULL | 完成时间 |
| submitted_at | DATETIME | NULL | 提交时间 |

**外键约束**:
- `fk_exercise_attempts_exercise_id` REFERENCES exercises(id) ON DELETE CASCADE
- `fk_exercise_attempts_student_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_exercise_attempts_exercise_student` ON (exercise_id, student_id)
- `idx_exercise_attempts_student_id` ON student_id
- `idx_exercise_attempts_completed` ON is_completed

### 4. student_answers 表 - 学生答案记录
**用途**: 详细记录学生对每道题的答案

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 答案记录唯一标识 |
| attempt_id | INTEGER | FOREIGN KEY, NOT NULL | 尝试记录ID |
| question_id | INTEGER | FOREIGN KEY, NOT NULL | 题目ID |
| student_id | INTEGER | FOREIGN KEY, NOT NULL | 学生用户ID |
| answer_content | TEXT | NOT NULL | 学生答案内容 |
| is_correct | BOOLEAN | NULL | 是否正确 |
| points_earned | FLOAT | DEFAULT 0.0 | 获得分数 |
| time_spent | INTEGER | DEFAULT 0 | 答题用时(秒) |
| answered_at | DATETIME | NOT NULL | 答题时间 |

**外键约束**:
- `fk_student_answers_attempt_id` REFERENCES exercise_attempts(id) ON DELETE CASCADE
- `fk_student_answers_question_id` REFERENCES questions(id) ON DELETE CASCADE
- `fk_student_answers_student_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_student_answers_attempt_question` ON (attempt_id, question_id) UNIQUE
- `idx_student_answers_student_id` ON student_id
- `idx_student_answers_question_id` ON question_id

## 数据关系图

```
users (1) ←→ (n) exercises (created_by)
users (1) ←→ (n) exercise_attempts (student_id)
users (1) ←→ (n) student_answers (student_id)
courses (1) ←→ (n) exercises (course_id)
exercises (1) ←→ (n) questions
exercises (1) ←→ (n) exercise_attempts
exercise_attempts (1) ←→ (n) student_answers
questions (1) ←→ (n) student_answers
```

## 业务逻辑说明

### 习题创建流程
1. 教师创建习题集基本信息
2. 添加具体题目和答案
3. 设置发布状态和时间限制
4. 系统自动计算总题数和满分

### 学生答题流程
1. 学生选择习题开始答题
2. 系统创建答题尝试记录
3. 学生逐题作答，系统记录答案
4. 完成后提交，系统自动评分
5. 更新统计数据和答题记录

### 自动评分规则
1. **选择题**: 答案完全匹配则正确
2. **填空题**: 答案去除空格后匹配
3. **问答题**: 需要教师手动评分

### 统计计算规则
1. **正确率**: 正确答案数 / 总答题次数 * 100%
2. **平均分**: 所有尝试总分 / 尝试次数
3. **完成率**: 完成人数 / 参与人数 * 100%

## API接口设计

### 习题管理接口
```http
GET    /api/v1/exercises                     # 获取习题列表
POST   /api/v1/exercises                     # 创建习题
GET    /api/v1/exercises/{id}                # 获取习题详情
PUT    /api/v1/exercises/{id}                # 更新习题
DELETE /api/v1/exercises/{id}                # 删除习题
GET    /api/v1/courses/{id}/exercises        # 获取课程习题
```

### 题目管理接口
```http
GET    /api/v1/exercises/{id}/questions      # 获取习题题目
POST   /api/v1/exercises/{id}/questions      # 添加题目
PUT    /api/v1/questions/{id}                # 更新题目
DELETE /api/v1/questions/{id}                # 删除题目
```

### 答题接口
```http
POST   /api/v1/exercises/{id}/start          # 开始答题
POST   /api/v1/exercises/submit-answer       # 提交单题答案
POST   /api/v1/exercises/submit              # 提交整套习题
GET    /api/v1/exercises/attempts/{id}       # 获取答题结果
```

## 前端页面对应

### 学生端页面
- **习题列表页** (`/student/exercises`): 显示所有可做习题
- **课程习题页** (`/student/courses/{id}#exercises`): 课程专属习题
- **答题页面** (`/student/exercise/{id}`): 具体答题界面
- **答题结果页** (`/student/exercise/{id}/result`): 查看答题结果

### 教师端页面
- **习题管理页** (`/teacher/exercises`): 管理所有创建的习题
- **习题创建页** (`/teacher/exercises/create`): 创建新习题
- **习题编辑页** (`/teacher/exercises/{id}/edit`): 编辑习题内容
- **课程习题页** (`/teacher/courses/{id}#exercises`): 课程习题管理
- **答题统计页** (`/teacher/exercises/{id}/stats`): 查看答题统计

## 性能优化

### 数据库优化
```sql
-- 关键索引
CREATE INDEX idx_exercises_course_published ON exercises(course_id, is_published);
CREATE INDEX idx_questions_exercise_active ON questions(exercise_id, is_active);
CREATE INDEX idx_attempts_student_completed ON exercise_attempts(student_id, is_completed);
CREATE INDEX idx_answers_attempt_question ON student_answers(attempt_id, question_id);
```

### 查询优化
- 习题列表使用分页查询，避免一次加载过多数据
- 答题记录使用增量更新，减少数据库写入频率
- 统计数据使用缓存，定期更新
- 题目内容使用预加载，提高答题体验


## 扩展功能

### 高级功能
- **智能组卷**: 根据知识点自动生成习题
- **错题本**: 自动收集错题，支持重做
- **习题推荐**: 基于学习情况推荐相关习题
- **协作答题**: 支持小组协作完成习题
- **习题分享**: 教师间习题资源共享

### 数据分析
- **学习分析**: 学生答题行为数据分析
- **题目质量**: 题目难度和区分度分析
- **教学效果**: 习题完成情况与学习效果关联分析
- **知识点掌握**: 基于答题情况分析知识点掌握程度

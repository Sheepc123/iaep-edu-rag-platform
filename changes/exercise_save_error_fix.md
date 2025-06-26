# 练习保存错误修复报告

## 🐛 问题描述

用户在点击"保存草稿"或"发布练习"时遇到错误，无法成功创建练习。

## 🔍 问题分析

经过代码审查，发现了以下几个关键问题：

### 1. 数据格式不匹配
- **前端发送字段**: `question_text`
- **后端期望字段**: `content`

### 2. 枚举值处理错误
- 后端服务层错误地使用了 `.value` 来获取枚举值
- 数据库模型中的字段是字符串类型，不需要 `.value`

### 3. 字段映射问题
- 前端的 `QuestionCreateRequest` 接口与后端的 `QuestionCreate` 模型不匹配

## ✅ 修复方案

### 1. 修复后端枚举值处理

#### 修复前
```python
# 错误的枚举值使用
category=exercise_data.category.value,
difficulty=exercise_data.difficulty.value,
```

#### 修复后
```python
# 正确的枚举值使用
category=exercise_data.category,
difficulty=exercise_data.difficulty,
```

### 2. 更新前端数据接口

#### 修复前
```typescript
export interface QuestionCreateRequest {
  question_text: string;  // 错误的字段名
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  // ...
  question_order: number;  // 后端不需要的字段
}
```

#### 修复后
```typescript
export interface QuestionCreateRequest {
  content: string;  // 正确的字段名
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  // ...
  // 移除了 question_order 字段
}
```

### 3. 修复前端数据映射

#### 修复前
```typescript
const questionData: QuestionCreateRequest = {
  question_text: question.question_text,  // 错误的字段名
  // ...
  question_order: question.question_order  // 不需要的字段
};
```

#### 修复后
```typescript
const questionData: QuestionCreateRequest = {
  content: question.question_text,  // 正确的字段名
  // ...
  // 移除了 question_order
};
```

## 🔧 具体修复内容

### 后端修复 (backend/app/services/exercise_service.py)

1. **练习创建方法**
```python
# 修复前
exercise = Exercise(
    category=exercise_data.category.value,  # 错误
    difficulty=exercise_data.difficulty.value,  # 错误
)

# 修复后
exercise = Exercise(
    category=exercise_data.category,  # 正确
    difficulty=exercise_data.difficulty,  # 正确
)
```

2. **题目创建方法**
```python
# 修复前
question = Question(
    question_type=question_data.question_type.value,  # 错误
    difficulty=question_data.difficulty.value,  # 错误
)

# 修复后
question = Question(
    question_type=question_data.question_type,  # 正确
    difficulty=question_data.difficulty,  # 正确
)
```

3. **查询方法**
```python
# 修复前
query.filter(Exercise.category == query_params.category.value)  # 错误

# 修复后
query.filter(Exercise.category == query_params.category)  # 正确
```

### 前端修复 (frontend/src/services/api.ts)

```typescript
// 更新接口定义
export interface QuestionCreateRequest {
  content: string;  // 改为后端期望的字段名
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  options?: string[];
  correct_answer: string;
  explanation?: string;
  points: number;
  difficulty: 'easy' | 'medium' | 'hard';
  // 移除了 question_order 字段
}
```

### 前端修复 (frontend/src/pages/teacher/ExerciseCreate.tsx)

```typescript
// 修复数据映射
const questionData: QuestionCreateRequest = {
  content: question.question_text,  // 使用正确的字段名
  question_type: question.question_type,
  options: question.question_type === "multiple_choice" ? 
    question.options.filter(opt => opt.trim()) : undefined,
  correct_answer: question.correct_answer,
  explanation: question.explanation,
  points: question.points,
  difficulty: question.difficulty
};
```

## 🧪 测试步骤

### 1. 重启服务
```bash
# 重启后端服务
cd backend
python run.py

# 重启前端服务
cd frontend
npm run dev
```

### 2. 测试练习创建
1. 登录教师账号: `teacher123 / 123456`
2. 进入练习管理页面
3. 点击"创建练习"
4. 填写基本信息:
   - 标题: "测试练习"
   - 分类: "自主练习"
   - 科目: "数学"
   - 难度: "中等"
5. 添加一道题目:
   - 类型: "选择题"
   - 内容: "1+1等于多少？"
   - 选项: ["1", "2", "3", "4"]
   - 正确答案: "2"
6. 点击"保存草稿"或"发布练习"

### 3. 检查错误信息
如果仍有错误，请检查：
- 浏览器控制台的错误信息
- 后端日志的详细错误
- 网络请求的数据格式

## 🔍 调试信息

### 前端调试
现在前端会输出详细的调试信息：
```typescript
console.log("准备创建练习，数据:", exerciseToSave);
console.log("准备创建题目，数据:", questionData);
console.error("错误详情:", error.response?.data || error.message);
```

### 后端调试
后端会记录详细的错误日志：
```python
logger.error(f"创建练习失败: {str(e)}")
logger.error(f"创建题目失败: {str(e)}")
```

## 📋 数据格式对照

### 练习数据格式
```json
{
  "title": "练习标题",
  "description": "练习描述",
  "category": "自主练习",  // 中文字符串
  "subject": "数学",
  "difficulty": "medium",  // 英文字符串
  "time_limit": 60,
  "is_published": false
}
```

### 题目数据格式
```json
{
  "content": "题目内容",  // 注意字段名是 content
  "question_type": "multiple_choice",
  "options": ["选项1", "选项2", "选项3", "选项4"],
  "correct_answer": "选项1",
  "explanation": "题目解析",
  "points": 10,
  "difficulty": "medium"
}
```

## 🎯 预期结果

修复后，用户应该能够：
1. ✅ 成功创建练习
2. ✅ 成功添加题目
3. ✅ 保存草稿状态
4. ✅ 发布练习
5. ✅ 在练习列表中看到创建的练习

## 🚨 注意事项

1. **数据库兼容性**: 确保数据库中的枚举值与代码中的字符串值匹配
2. **字段命名**: 前后端字段名必须保持一致
3. **类型验证**: 确保前端发送的数据类型与后端期望的类型匹配
4. **错误处理**: 添加了详细的错误信息输出，便于调试

如果问题仍然存在，请查看浏览器控制台和后端日志的具体错误信息，这将帮助进一步诊断问题。

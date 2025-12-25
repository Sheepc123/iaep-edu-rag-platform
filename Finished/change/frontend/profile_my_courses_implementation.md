# 个人中心"我的课程"功能实现文档

## 修改概述
在个人中心页面添加"我的课程"功能，显示学生已注册的课程列表，不显示学习进度条，提供简洁的课程信息展示。

## 修改时间
2025-06-25

## 主要修改内容

### 1. 前端页面改造

#### 文件：`frontend/src/pages/student/Profile.tsx`

##### 新增功能
- **标签页导航**：将个人中心分为"个人信息"和"我的课程"两个标签页
- **我的课程列表**：显示学生已注册的课程
- **课程卡片设计**：简洁的课程信息展示，包含课程封面、标题、分类、难度等
- **空状态处理**：当没有注册课程时显示引导用户去课程中心的提示

##### 新增导入
```typescript
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen, Clock, Star, Users, PlayCircle
} from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { courseAPI, CourseEnrollment } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";
```

##### 新增状态管理
```typescript
// 我的课程状态
const [enrolledCourses, setEnrolledCourses] = useState<EnrolledCourse[]>([]);
const [coursesLoading, setCoursesLoading] = useState(true);
```

##### 新增接口定义
```typescript
interface EnrolledCourse {
  id: number;
  title: string;
  description: string;
  cover_image: string;
  category: string;
  difficulty: string;
  instructor_name: string;
  total_lessons: number;
  duration: number;
  rating: number;
  enrolled_at: string;
}
```

##### 核心功能实现
- **数据获取**：调用`courseAPI.getMyCourses()`获取已注册课程
- **数据转换**：将`CourseEnrollment`数据转换为`EnrolledCourse`格式
- **错误处理**：使用toast显示错误信息
- **加载状态**：显示加载动画
- **点击跳转**：点击课程卡片跳转到课程详情页

### 2. 后端API增强

#### 文件：`backend/app/schemas/course.py`

##### 修改内容
- **CourseEnrollResponse模式增强**：添加可选的`course`字段
```python
class CourseEnrollResponse(BaseModel):
    # ... 原有字段
    course: Optional[CourseResponse] = Field(None, description="课程详情")
```

#### 文件：`backend/app/services/course_service.py`

##### 修改内容
- **get_student_enrollments方法增强**：使用`joinedload`预加载课程信息
```python
def get_student_enrollments(self, student_id: int) -> List[CourseEnrollment]:
    from sqlalchemy.orm import joinedload
    
    return self.db.query(CourseEnrollment).options(
        joinedload(CourseEnrollment.course)
    ).filter(
        and_(
            CourseEnrollment.student_id == student_id,
            CourseEnrollment.is_active == True
        )
    ).all()
```

### 3. 前端API服务更新

#### 文件：`frontend/src/services/api.ts`

##### 修改内容
- **CourseEnrollment接口增强**：添加可选的`course`字段
```typescript
export interface CourseEnrollment {
  // ... 原有字段
  course?: Course; // 可选的课程详情
}
```

### 4. 页面布局设计

#### 标签页结构
```
个人中心
├── 个人信息标签页
│   ├── 用户头像和基本信息
│   ├── 个人信息编辑表单
│   └── 密码修改功能
└── 我的课程标签页
    ├── 课程统计信息
    ├── 课程列表网格
    └── 空状态提示
```

#### 课程卡片设计
- **课程封面**：显示课程图片
- **难度标签**：彩色标签显示课程难度
- **课时信息**：右上角显示总课时数
- **课程信息**：标题、描述、分类
- **教师信息**：显示授课教师
- **评分信息**：显示课程评分
- **注册时间**：显示注册日期

### 5. 用户体验优化

#### 交互设计
- **悬停效果**：鼠标悬停时卡片轻微放大
- **点击跳转**：点击课程卡片跳转到课程详情页
- **加载状态**：显示加载动画和文字提示
- **空状态**：友好的空状态提示和引导按钮

#### 响应式设计
- **网格布局**：支持1-3列自适应布局
- **移动端优化**：在小屏幕上自动调整为单列布局

### 6. 数据流程

#### 获取我的课程流程
1. 用户访问个人中心页面
2. 组件挂载时调用`fetchEnrolledCourses()`
3. 调用`courseAPI.getMyCourses()`获取注册记录
4. 后端返回包含课程详情的注册记录
5. 前端转换数据格式并更新状态
6. 渲染课程列表

#### 错误处理流程
1. API调用失败时捕获异常
2. 使用toast显示用户友好的错误信息
3. 设置加载状态为false
4. 保持页面可用性

### 7. 测试支持

#### 测试脚本
- **`backend/test_my_courses_api.py`**：API功能测试
- **`backend/create_enrollment_test_data.py`**：创建测试数据

#### 测试用例
- 获取已注册课程列表
- 处理空课程列表
- 处理API错误
- 课程卡片点击跳转
- 响应式布局测试

## 技术特性

### 1. 性能优化
- **预加载关联数据**：使用`joinedload`减少数据库查询次数
- **数据缓存**：前端缓存课程数据，避免重复请求
- **懒加载**：只在需要时加载课程详情

### 2. 用户体验
- **即时反馈**：加载状态和错误提示
- **直观导航**：清晰的标签页结构
- **视觉层次**：合理的信息层级和视觉重点

### 3. 可维护性
- **组件化设计**：可复用的课程卡片组件
- **类型安全**：完整的TypeScript类型定义
- **错误边界**：完善的错误处理机制

## 使用说明

### 1. 访问功能
- 登录学生账户
- 进入个人中心页面
- 点击"我的课程"标签页

### 2. 功能操作
- **查看课程**：浏览已注册的课程列表
- **进入课程**：点击课程卡片进入课程详情页
- **浏览更多**：通过"浏览课程"按钮进入课程中心

### 3. 数据要求
- 学生需要先注册课程才能在此页面看到内容
- 课程需要是已发布状态
- 需要有有效的课程封面图片

## 后续扩展建议

### 1. 功能增强
- **学习进度显示**：可选择显示/隐藏学习进度
- **课程筛选**：按分类、难度、完成状态筛选
- **学习统计**：显示总学习时间、完成课程数等
- **最近学习**：显示最近访问的课程

### 2. 交互优化
- **批量操作**：支持批量取消注册
- **收藏功能**：标记重要课程
- **学习笔记**：课程级别的学习笔记
- **学习提醒**：设置学习提醒和计划

### 3. 数据分析
- **学习报告**：生成个人学习报告
- **进度分析**：学习进度趋势图
- **推荐系统**：基于学习历史推荐相关课程

## 维护说明

- 定期检查API响应时间和错误率
- 监控课程数据的完整性
- 根据用户反馈优化界面设计
- 保持与课程中心页面的设计一致性

# 智能教育实训平台前端设计方案

## 1. 技术栈选型

### 1.1 核心框架
- Vue 3.0+ (组合式API)
- TypeScript
- Vite (构建工具)

### 1.2 UI框架
- Element Plus (桌面端组件库)
- TailwindCSS (原子化CSS)

### 1.3 状态管理
- Pinia
- Pinia Persist (状态持久化)

### 1.4 路由
- Vue Router 4

### 1.5 工具库
- Axios (HTTP请求)
- ECharts (图表可视化)
- Monaco Editor (代码编辑器)
- Day.js (时间处理)
- lodash-es (工具函数)

## 2. 项目结构

```
frontend/
├── src/
│   ├── api/              # API接口定义
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   │   ├── base/        # 基础组件
│   │   ├── business/    # 业务组件
│   │   └── layout/      # 布局组件
│   ├── composables/      # 组合式函数
│   ├── config/          # 配置文件
│   ├── directives/      # 自定义指令
│   ├── hooks/           # 自定义钩子
│   ├── layouts/         # 布局模板
│   ├── router/          # 路由配置
│   ├── store/           # 状态管理
│   ├── styles/          # 全局样式
│   ├── types/           # TS类型定义
│   ├── utils/           # 工具函数
│   └── views/           # 页面组件
├── public/              # 公共资源
└── index.html           # 入口HTML
```

## 3. 页面布局设计

### 3.1 布局模板
```
[Layout]
├── AdminLayout    # 管理员布局
├── TeacherLayout  # 教师布局
└── StudentLayout  # 学生布局

[公共组件]
├── Header        # 顶部导航
├── Sidebar       # 侧边菜单
└── Footer        # 底部信息
```

### 3.2 响应式设计
- 断点设计
  * xs: < 768px (移动端)
  * sm: >= 768px (平板)
  * md: >= 992px (桌面)
  * lg: >= 1200px (大屏)
  * xl: >= 1920px (超大屏)

## 4. 路由设计

```typescript
// 路由配置
const routes = [
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/admin/Dashboard.vue')
      },
      {
        path: 'users',
        component: () => import('@/views/admin/Users.vue')
      }
    ]
  },
  {
    path: '/teacher',
    component: TeacherLayout,
    children: [
      {
        path: 'courses',
        component: () => import('@/views/teacher/Courses.vue')
      },
      {
        path: 'exercises',
        component: () => import('@/views/teacher/Exercises.vue')
      }
    ]
  },
  {
    path: '/student',
    component: StudentLayout,
    children: [
      {
        path: 'learning',
        component: () => import('@/views/student/Learning.vue')
      },
      {
        path: 'practice',
        component: () => import('@/views/student/Practice.vue')
      }
    ]
  }
]
```

## 5. 核心业务组件

### 5.1 课程相关
```typescript
// 课程卡片组件
interface CourseCard {
  title: string
  description: string
  cover: string
  progress: number
  teacher: string
}

// 课程大纲组件
interface CourseOutline {
  chapters: Chapter[]
  currentChapter: number
}

// 课程内容展示组件
interface CourseContent {
  content: string
  type: 'text' | 'video' | 'code'
  resources: Resource[]
}
```

### 5.2 练习相关
```typescript
// 练习题组件
interface Exercise {
  type: 'choice' | 'coding' | 'essay'
  content: string
  options?: string[]
  answer: string
}

// 代码编辑器组件
interface CodeEditor {
  language: string
  theme: string
  value: string
  readonly: boolean
}

// 评测结果组件
interface TestResult {
  status: 'success' | 'error'
  score: number
  feedback: string
  details: TestCase[]
}
```

### 5.3 AI对话相关
```typescript
// 对话框组件
interface ChatBox {
  messages: Message[]
  loading: boolean
  inputValue: string
}

// 消息气泡组件
interface MessageBubble {
  content: string
  type: 'user' | 'assistant'
  timestamp: number
}
```

## 6. 状态管理设计

```typescript
// 用户状态
interface UserState {
  token: string
  userInfo: UserInfo
  permissions: string[]
}

// 课程状态
interface CourseState {
  currentCourse: Course
  courseList: Course[]
  learningProgress: Record<string, number>
}

// AI对话状态
interface ChatState {
  conversations: Conversation[]
  currentConversation: Conversation
  messageHistory: Message[]
}
```

## 7. 主题定制

```typescript
// 主题变量
:root {
  // 品牌色
  --primary-color: #1890ff;
  --success-color: #52c41a;
  --warning-color: #faad14;
  --error-color: #f5222d;
  
  // 文字色
  --text-primary: #2c3e50;
  --text-regular: #606266;
  --text-secondary: #909399;
  
  // 边框色
  --border-color: #dcdfe6;
  
  // 背景色
  --bg-primary: #ffffff;
  --bg-secondary: #f5f7fa;
}
```

## 8. 性能优化策略

1. 路由懒加载
2. 组件按需加载
3. 虚拟滚动列表
4. 图片懒加载
5. 大文件分片上传
6. 请求防抖和节流
7. 静态资源CDN加速

## 9. 开发规范

1. 组件命名：PascalCase
2. 文件命名：kebab-case
3. TypeScript类型定义
4. ESLint + Prettier代码格式化
5. Git Commit规范
6. 组件文档规范

## 10. 构建优化

1. 代码分割策略
2. 资源压缩
3. Tree-shaking
4. 缓存策略
5. 打包分析 
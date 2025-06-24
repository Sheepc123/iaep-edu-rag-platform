# 智能教育平台后端 API

基于 FastAPI + SQLite + JWT 的现代化教育平台后端服务

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip 或 pipenv

### 安装依赖
```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt
```

### 配置环境
```bash
# 复制环境配置文件
copy .env.example .env

# 编辑配置文件 (Windows)
notepad .env
```

### 启动服务
```bash
# 方式1: 使用启动脚本
python run.py

# 方式2: 直接使用uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 访问服务
- API文档: http://127.0.0.1:8000/docs
- 健康检查: http://127.0.0.1:8000/health
- 根路径: http://127.0.0.1:8000/

## 📁 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   │   └── v1/           # API版本1
│   │       ├── endpoints/ # 端点实现
│   │       └── api.py    # 路由汇总
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   ├── database.py   # 数据库配置
│   │   └── security.py   # 安全认证
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── course.py     # 课程模型
│   │   ├── exercise.py   # 练习模型
│   │   └── chat.py       # 聊天模型
│   ├── schemas/          # 数据验证模式
│   ├── services/         # 业务逻辑服务
│   └── main.py          # 应用入口
├── tests/               # 测试文件
├── uploads/            # 文件上传目录
├── logs/               # 日志目录
├── requirements.txt    # 依赖列表
├── run.py             # 启动脚本
└── .env.example       # 环境配置模板
```

## 🎯 功能模块

### 1. 用户认证模块
- ✅ 用户注册/登录
- ✅ JWT令牌管理
- ✅ 权限验证
- ✅ 密码加密

### 2. 课程管理模块
- ✅ 课程CRUD操作
- ✅ 课程进度跟踪
- ✅ 课程分类管理
- ✅ 学习计划

### 3. 练习系统模块
- ✅ 题目管理
- ✅ 答题记录
- ✅ 练习统计
- ✅ 错题本

### 4. 聊天通信模块
- ✅ 实时消息
- ✅ 联系人管理
- ✅ 聊天室管理
- ✅ 在线状态

### 5. AI助手模块
- ✅ AI对话
- ✅ 对话历史
- ✅ 智能推荐
- ✅ 学习建议

### 6. 用户资料模块
- ✅ 个人信息管理
- ✅ 学习数据统计
- ✅ 偏好设置
- ✅ 活动记录

## 🔧 技术栈

- **Web框架**: FastAPI 0.104.1
- **数据库**: SQLite + SQLAlchemy 2.0
- **认证**: JWT + bcrypt
- **数据验证**: Pydantic 2.5
- **ASGI服务器**: Uvicorn
- **日志**: Loguru

## 📊 数据库设计

### 核心表结构
- `users` - 用户基础信息
- `student_profiles` - 学生档案
- `teacher_profiles` - 教师档案
- `courses` - 课程信息
- `exercises` - 练习集
- `questions` - 题目
- `chat_rooms` - 聊天室
- `ai_conversations` - AI对话

## 🛠️ 开发指南

### 添加新的API端点
1. 在 `app/api/v1/endpoints/` 创建新的路由文件
2. 在 `app/api/v1/api.py` 中注册路由
3. 创建对应的数据模型和验证模式

### 数据库迁移
```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

### 运行测试
```bash
pytest tests/
```

## 🔒 安全配置

### 生产环境配置
1. 修改 `SECRET_KEY` 为强密码
2. 设置 `DEBUG=false`
3. 配置HTTPS
4. 限制CORS来源
5. 配置防火墙规则

## 📝 API文档

启动服务后访问 http://127.0.0.1:8000/docs 查看完整的API文档

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

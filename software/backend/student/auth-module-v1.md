# 用户认证模块开发文档 v1.0

## 📋 模块概述

### 基本信息
- **模块名称**: 用户认证模块 (Authentication Module)
- **开发状态**: ✅ 完成开发
- **技术栈**: FastAPI + JWT + bcrypt + SQLAlchemy
- **文档版本**: v1.0
- **最后更新**: 2024-06-24

### 功能定位
提供完整的用户认证和授权功能，包括用户注册、登录、令牌管理、权限控制、学生档案管理等核心功能。

## 🎯 功能特性

### 1. 用户认证功能
- ✅ **用户注册**: 支持学生/教师角色注册
- ✅ **用户登录**: 用户名/邮箱登录，设备信息记录
- ✅ **JWT令牌**: 访问令牌 + 刷新令牌双令牌机制
- ✅ **会话管理**: 多设备登录支持，会话过期管理
- ✅ **安全登出**: 单设备/全设备登出

### 2. 密码安全
- ✅ **密码加密**: bcrypt哈希加密
- ✅ **密码验证**: 安全的密码验证机制
- ✅ **密码修改**: 当前密码验证 + 新密码设置
- ✅ **强制重登**: 密码修改后注销所有会话

### 3. 权限控制
- ✅ **角色管理**: student/teacher/admin三种角色
- ✅ **权限验证**: 基于角色的访问控制(RBAC)
- ✅ **API保护**: 依赖注入的权限检查
- ✅ **用户访问**: 用户只能访问自己的数据

### 4. 学生档案
- ✅ **档案创建**: 自动创建学生档案
- ✅ **档案管理**: 学校、学院、专业等信息
- ✅ **学习统计**: 学习时间、练习数据统计
- ✅ **偏好设置**: 学习偏好和目标设置

### 5. 活动记录
- ✅ **用户活动**: 登录、登出、操作记录
- ✅ **会话跟踪**: 设备信息、IP地址记录
- ✅ **安全审计**: 完整的操作日志

## 🏗️ 技术架构

### 模块结构
```
auth_module/
├── schemas/auth.py          # 数据验证模式
├── services/
│   ├── auth_service.py      # 认证业务逻辑
│   └── student_service.py   # 学生档案服务
├── models/user.py           # 用户数据模型
├── api/endpoints/
│   ├── auth.py             # 认证API端点
│   └── users.py            # 用户管理端点
├── dependencies.py          # 依赖注入
└── core/security.py         # 安全工具
```

### 数据模型设计

#### 1. 用户基础模型 (User)
```python
- id: 用户ID (主键)
- username: 用户名 (唯一)
- email: 邮箱 (唯一)
- hashed_password: 加密密码
- full_name: 真实姓名
- phone: 手机号码
- avatar: 头像URL
- role: 用户角色 (student/teacher/admin)
- is_active: 是否激活
- is_verified: 是否验证
- created_at: 创建时间
- updated_at: 更新时间
- last_login: 最后登录时间
```

#### 2. 学生档案模型 (StudentProfile)
```python
- id: 档案ID (主键)
- user_id: 用户ID (外键)
- student_id: 学号
- school: 学校
- college: 学院
- major: 专业
- grade: 年级
- class_name: 班级
- total_study_time: 总学习时间
- total_exercises: 总练习数
- correct_exercises: 正确练习数
- total_courses: 总课程数
- completed_courses: 完成课程数
- preferred_subjects: 偏好科目 (JSON)
- learning_goals: 学习目标
```

#### 3. 用户会话模型 (UserSession)
```python
- id: 会话ID (主键)
- user_id: 用户ID (外键)
- refresh_token: 刷新令牌
- device_info: 设备信息
- ip_address: IP地址
- user_agent: 用户代理
- is_active: 是否活跃
- created_at: 创建时间
- expires_at: 过期时间
- last_used: 最后使用时间
```

## 🔧 API接口设计

### 认证相关接口

#### 1. 用户注册
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "student123",
  "email": "student@example.com", 
  "password": "password123",
  "full_name": "张同学",
  "phone": "13800138000",
  "role": "student"
}
```

#### 2. 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "student123",
  "password": "password123",
  "remember_me": true,
  "device_info": "Chrome Browser"
}
```

#### 3. 刷新令牌
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 4. 获取用户信息
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### 5. 修改密码
```http
POST /api/v1/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "oldpassword",
  "new_password": "newpassword123",
  "confirm_password": "newpassword123"
}
```

### 用户管理接口

#### 1. 获取用户资料
```http
GET /api/v1/users/profile
Authorization: Bearer <access_token>
```

#### 2. 更新用户资料
```http
PUT /api/v1/users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "张同学",
  "phone": "13800138001",
  "avatar": "https://example.com/avatar.jpg"
}
```

#### 3. 获取学生档案
```http
GET /api/v1/users/student-profile
Authorization: Bearer <access_token>
```

#### 4. 更新学生档案
```http
PUT /api/v1/users/student-profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "student_id": "2021012345",
  "school": "清华大学",
  "college": "计算机科学与技术学院",
  "major": "计算机科学与技术",
  "grade": "2021级",
  "class_name": "计科1班"
}
```

## 🔒 安全机制

### 1. JWT令牌机制
- **访问令牌**: 30分钟有效期，用于API访问
- **刷新令牌**: 7天有效期，用于获取新的访问令牌
- **令牌类型**: Bearer Token，在Authorization头中传递
- **令牌验证**: 每个受保护的端点都验证令牌有效性

### 2. 密码安全
- **加密算法**: bcrypt哈希，自动加盐
- **密码强度**: 最少6字符，支持字母数字特殊字符
- **密码验证**: 安全的时间常数比较
- **密码修改**: 验证当前密码，强制重新登录

### 3. 会话管理
- **多设备支持**: 每个设备独立会话
- **会话过期**: 自动清理过期会话
- **设备跟踪**: 记录设备信息和IP地址
- **安全登出**: 支持单设备或全设备登出

### 4. 权限控制
- **角色验证**: 基于用户角色的访问控制
- **资源保护**: 用户只能访问自己的资源
- **管理员权限**: 管理员可访问所有资源
- **API保护**: 所有敏感端点都需要认证

## 🧪 测试验证

### 测试脚本
提供了完整的测试脚本 `test_auth.py`，包含：

1. **健康检查**: 验证服务器状态
2. **用户注册**: 测试注册功能
3. **用户登录**: 测试登录功能
4. **获取信息**: 测试用户信息获取
5. **令牌刷新**: 测试令牌刷新机制
6. **用户登出**: 测试登出功能

### 运行测试
```bash
# 启动后端服务
python run.py

# 运行测试脚本
python test_auth.py
```

## 📊 数据流程

### 用户注册流程
```
1. 客户端提交注册信息
2. 验证用户名和邮箱唯一性
3. 加密用户密码
4. 创建用户记录
5. 根据角色创建对应档案
6. 记录注册活动
7. 返回注册结果
```

### 用户登录流程
```
1. 客户端提交登录凭据
2. 验证用户名/邮箱和密码
3. 检查用户状态
4. 生成JWT令牌对
5. 创建用户会话
6. 更新最后登录时间
7. 记录登录活动
8. 返回令牌和用户信息
```

### 令牌刷新流程
```
1. 客户端提交刷新令牌
2. 验证刷新令牌有效性
3. 检查会话状态
4. 生成新的令牌对
5. 更新会话信息
6. 返回新令牌
```

## 🚀 部署说明

### 环境要求
- Python 3.8+
- FastAPI 0.104+
- SQLAlchemy 2.0+
- python-jose[cryptography]
- passlib[bcrypt]

### 配置项
```env
# JWT配置
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 数据库配置
DATABASE_URL=sqlite:///./education_platform.db
```

### 启动服务
```bash
cd backend
pip install -r requirements.txt
python run.py
```

## 📈 性能优化

### 1. 数据库优化
- 用户名和邮箱字段建立唯一索引
- 会话表按用户ID和过期时间建立索引
- 定期清理过期会话和活动记录

### 2. 安全优化
- 令牌过期时间合理设置
- 密码哈希使用适当的成本因子
- 限制登录尝试次数（待实现）

### 3. 缓存策略
- 用户信息缓存（待实现）
- 权限信息缓存（待实现）
- 会话状态缓存（待实现）

## 🔄 后续扩展

### 短期计划
- [ ] 邮箱验证功能
- [ ] 密码重置功能
- [ ] 登录限制和验证码
- [ ] 用户头像上传

### 中期计划
- [ ] 第三方登录集成
- [ ] 多因素认证(MFA)
- [ ] 设备管理功能
- [ ] 安全日志分析

### 长期计划
- [ ] 单点登录(SSO)
- [ ] OAuth2.0支持
- [ ] 生物识别认证
- [ ] 风险评估系统

---

**文档维护**: 后端开发团队  
**版本**: v1.0  
**日期**: 2024-06-24

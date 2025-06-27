# 用户认证模块数据库文档

## 概述
用户认证模块是整个智能教育平台的基础核心模块，负责用户注册、登录验证、会话管理、权限控制和用户信息存储。该模块支持教师和学生两种角色的差异化管理，提供完整的用户生命周期管理功能。

## 功能特性
- **多角色支持**: 支持学生(student)、教师(teacher)、管理员(admin)三种用户角色
- **安全认证**: 使用bcrypt加密存储密码，JWT令牌进行身份验证
- **会话管理**: 支持多设备登录，会话状态跟踪和管理
- **用户档案**: 为不同角色提供专门的档案信息存储
- **活动记录**: 完整的用户行为日志记录
- **权限控制**: 基于角色的访问控制(RBAC)

## 数据库表结构

### 1. users 表 - 用户基础信息
**用途**: 存储所有用户的基础信息和认证数据

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 用户唯一标识 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名，用于登录 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | 邮箱地址 |
| hashed_password | VARCHAR(255) | NOT NULL | 加密后的密码 |
| role | VARCHAR(20) | NOT NULL | 用户角色：student/teacher/admin |
| is_active | BOOLEAN | DEFAULT TRUE | 账户是否激活 |
| is_verified | BOOLEAN | DEFAULT FALSE | 邮箱是否验证 |
| avatar_url | VARCHAR(255) | NULL | 头像URL |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |
| last_login_at | DATETIME | NULL | 最后登录时间 |

**索引**:
- `idx_users_username` ON username
- `idx_users_email` ON email
- `idx_users_role` ON role

**默认数据**:
```sql
-- 教师用户
INSERT INTO users (username, email, hashed_password, role, is_active)
VALUES ('teacher1', 'teacher1@example.com', '$2b$12$...', 'teacher', 1);

-- 学生用户
INSERT INTO users (username, email, hashed_password, role, is_active)
VALUES ('student1', 'student1@example.com', '$2b$12$...', 'student', 1);
```

**业务规则**:
- 用户名必须唯一，3-50字符，支持字母、数字、下划线、连字符
- 邮箱必须唯一且格式正确
- 密码使用bcrypt加密，最少6位字符
- 支持用户名或邮箱登录
- 新注册用户默认未验证状态(is_verified=false)
- 用户创建后自动生成对应角色的档案记录

### 2. student_profiles 表 - 学生档案
**用途**: 存储学生的详细信息和学习统计

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 档案唯一标识 |
| user_id | INTEGER | FOREIGN KEY, UNIQUE | 关联用户ID |
| student_id | VARCHAR(20) | UNIQUE | 学号 |
| real_name | VARCHAR(50) | NULL | 真实姓名 |
| major | VARCHAR(100) | NULL | 专业 |
| grade | VARCHAR(20) | NULL | 年级 |
| class_name | VARCHAR(50) | NULL | 班级 |
| phone | VARCHAR(20) | NULL | 联系电话 |
| total_study_time | INTEGER | DEFAULT 0 | 总学习时长(分钟) |
| courses_completed | INTEGER | DEFAULT 0 | 完成课程数 |
| exercises_completed | INTEGER | DEFAULT 0 | 完成练习数 |
| average_score | DECIMAL(5,2) | DEFAULT 0 | 平均分数 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_student_profiles_user_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_student_profiles_student_id` ON student_id
- `idx_student_profiles_major` ON major

### 3. teacher_profiles 表 - 教师档案
**用途**: 存储教师的详细信息和教学统计

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 档案唯一标识 |
| user_id | INTEGER | FOREIGN KEY, UNIQUE | 关联用户ID |
| employee_id | VARCHAR(20) | UNIQUE | 工号 |
| real_name | VARCHAR(50) | NULL | 真实姓名 |
| department | VARCHAR(100) | NULL | 所属部门 |
| title | VARCHAR(50) | NULL | 职称 |
| bio | TEXT | NULL | 个人简介 |
| phone | VARCHAR(20) | NULL | 联系电话 |
| office_location | VARCHAR(100) | NULL | 办公室位置 |
| courses_created | INTEGER | DEFAULT 0 | 创建课程数 |
| students_taught | INTEGER | DEFAULT 0 | 教授学生数 |
| total_teaching_hours | INTEGER | DEFAULT 0 | 总教学时长(小时) |
| rating | DECIMAL(3,2) | DEFAULT 0 | 教师评分 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**外键约束**:
- `fk_teacher_profiles_user_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_teacher_profiles_employee_id` ON employee_id
- `idx_teacher_profiles_department` ON department

### 4. user_sessions 表 - 用户会话管理
**用途**: 管理用户登录会话，支持多设备登录和会话控制

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 会话唯一标识 |
| user_id | INTEGER | FOREIGN KEY | 关联用户ID |
| session_token | VARCHAR(255) | UNIQUE, NOT NULL | 会话令牌 |
| refresh_token | VARCHAR(255) | UNIQUE, NOT NULL | 刷新令牌 |
| device_info | VARCHAR(255) | NULL | 设备信息 |
| ip_address | VARCHAR(45) | NULL | IP地址 |
| user_agent | TEXT | NULL | 用户代理 |
| is_active | BOOLEAN | DEFAULT TRUE | 会话是否活跃 |
| expires_at | DATETIME | NOT NULL | 过期时间 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| last_accessed_at | DATETIME | NOT NULL | 最后访问时间 |

**外键约束**:
- `fk_user_sessions_user_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_user_sessions_token` ON session_token
- `idx_user_sessions_user_id` ON user_id
- `idx_user_sessions_expires_at` ON expires_at

### 5. user_activities 表 - 用户活动记录
**用途**: 记录用户的各种活动，用于数据分析和行为追踪

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 活动记录唯一标识 |
| user_id | INTEGER | FOREIGN KEY | 关联用户ID |
| activity_type | VARCHAR(50) | NOT NULL | 活动类型 |
| activity_data | JSON | NULL | 活动详细数据 |
| ip_address | VARCHAR(45) | NULL | IP地址 |
| user_agent | TEXT | NULL | 用户代理 |
| created_at | DATETIME | NOT NULL | 创建时间 |

**外键约束**:
- `fk_user_activities_user_id` REFERENCES users(id) ON DELETE CASCADE

**索引**:
- `idx_user_activities_user_id` ON user_id
- `idx_user_activities_type` ON activity_type
- `idx_user_activities_created_at` ON created_at

## 活动类型说明

### 常见活动类型
- `login` - 用户登录
- `logout` - 用户登出
- `register` - 用户注册
- `profile_update` - 更新个人资料
- `password_change` - 修改密码
- `course_access` - 访问课程
- `exercise_start` - 开始练习
- `exercise_complete` - 完成练习

## 数据关系图

```
users (1) ←→ (1) student_profiles
users (1) ←→ (1) teacher_profiles
users (1) ←→ (n) user_sessions
users (1) ←→ (n) user_activities
```

## 业务逻辑说明

### 用户注册流程
1. 创建 users 记录
2. 根据角色创建对应的 profile 记录
3. 记录注册活动到 user_activities

### 用户登录流程
1. 验证用户名/密码
2. 创建 user_sessions 记录
3. 生成 JWT 令牌
4. 更新 last_login_at
5. 记录登录活动

### 权限控制
- **学生权限**: 只能访问学生相关功能
- **教师权限**: 可以访问教师功能和部分学生功能
- **管理员权限**: 可以访问所有功能

## 安全考虑

### 密码安全
- 使用 bcrypt 加密存储密码
- 密码强度要求：至少6位
- 支持密码重置功能

### 会话安全
- JWT 令牌有效期：30分钟
- 刷新令牌有效期：7天
- 支持令牌撤销
- 记录设备信息防止异常登录

### 数据保护
- 敏感信息加密存储
- 用户活动日志记录
- 支持账户锁定机制

## 登录页面功能实现

### 登录流程详解

#### 1. 前端登录请求
```typescript
// 登录请求数据结构
interface LoginRequest {
  username: string;      // 用户名或邮箱
  password: string;      // 明文密码
  remember_me: boolean;  // 是否记住登录
  device_info?: string;  // 设备信息(可选)
}
```

#### 2. 后端认证处理
```python
# API端点: POST /api/v1/auth/login
async def login(login_data: UserLogin, request: Request):
    # 1. 获取客户端信息
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # 2. 用户认证
    user, tokens = auth_service.authenticate_user(login_data)

    # 3. 返回用户信息和令牌
    return TokenResponse(...)
```

#### 3. 认证服务逻辑
```python
def authenticate_user(self, login_data: UserLogin):
    # 1. 查询用户(支持用户名或邮箱)
    user = db.query(User).filter(
        or_(User.username == login_data.username.lower(),
            User.email == login_data.username.lower())
    ).first()

    # 2. 验证用户存在性和状态
    if not user or not user.is_active:
        raise HTTPException(401, "用户名或密码错误")

    # 3. 验证密码
    if not PasswordManager.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(401, "用户名或密码错误")

    # 4. 更新最后登录时间
    user.last_login = datetime.utcnow()

    # 5. 创建JWT令牌
    tokens = JWTManager.create_tokens(user.id, user.username, user.role)

    # 6. 创建用户会话
    session = self._create_user_session(user.id, tokens.refresh_token, ...)

    # 7. 记录登录活动
    self._log_user_activity(user.id, "login", {...})

    return user, tokens
```

### 数据库操作详解

#### 1. 用户查询
```sql
-- 支持用户名或邮箱登录
SELECT id, username, email, hashed_password, role, is_active, is_verified,
       full_name, phone, avatar, created_at, last_login
FROM users
WHERE (username = ? OR email = ?) AND is_active = 1;
```

#### 2. 密码验证
```python
# 使用bcrypt验证密码
import bcrypt
is_valid = bcrypt.checkpw(
    plain_password.encode('utf-8'),
    hashed_password.encode('utf-8')
)
```

#### 3. 会话创建
```sql
-- 创建用户会话记录
INSERT INTO user_sessions (
    user_id, session_token, refresh_token, device_info,
    ip_address, user_agent, is_active, expires_at,
    created_at, last_used, last_accessed_at
) VALUES (?, ?, ?, ?, ?, ?, 1, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

#### 4. 活动记录
```sql
-- 记录登录活动
INSERT INTO user_activities (
    user_id, activity_type, activity_data, ip_address, user_agent, created_at
) VALUES (?, 'login', ?, ?, ?, CURRENT_TIMESTAMP);
```

#### 5. 更新登录时间
```sql
-- 更新用户最后登录时间
UPDATE users
SET last_login = CURRENT_TIMESTAMP
WHERE id = ?;
```

### JWT令牌管理

#### 1. 令牌结构
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### 2. 访问令牌载荷
```json
{
  "sub": "1",                    // 用户ID
  "username": "teacher1",        // 用户名
  "role": "teacher",            // 用户角色
  "exp": 1751040958,            // 过期时间
  "type": "access"              // 令牌类型
}
```

#### 3. 刷新令牌载荷
```json
{
  "sub": "1",                    // 用户ID
  "username": "teacher1",        // 用户名
  "role": "teacher",            // 用户角色
  "exp": 1751645758,            // 过期时间(7天后)
  "type": "refresh"             // 令牌类型
}
```

### 错误处理机制

#### 1. 常见错误类型
| 错误代码 | HTTP状态 | 错误信息 | 处理方式 |
|---------|---------|----------|----------|
| 401 | Unauthorized | 用户名或密码错误 | 用户重新输入 |
| 401 | Unauthorized | 账户已被禁用 | 联系管理员 |
| 400 | Bad Request | 用户名已存在 | 选择其他用户名 |
| 400 | Bad Request | 邮箱已被注册 | 使用其他邮箱 |
| 500 | Internal Server Error | 服务器内部错误 | 稍后重试 |

#### 2. 前端错误处理
```typescript
try {
  const response = await api.post('/auth/login', loginData);
  // 登录成功处理
  localStorage.setItem('access_token', response.data.access_token);
  localStorage.setItem('refresh_token', response.data.refresh_token);
  router.push('/dashboard');
} catch (error) {
  if (error.response?.status === 401) {
    setError('用户名或密码错误');
  } else if (error.response?.status === 500) {
    setError('服务器错误，请稍后重试');
  } else {
    setError('登录失败，请检查网络连接');
  }
}
```

### 安全特性

#### 1. 密码安全
- **加密算法**: bcrypt with salt
- **最小长度**: 6位字符
- **复杂度**: 支持字母、数字、特殊字符
- **存储**: 只存储哈希值，不存储明文

#### 2. 会话安全
- **令牌过期**: 访问令牌30分钟，刷新令牌7天
- **设备跟踪**: 记录设备信息和IP地址
- **会话管理**: 支持主动注销和会话撤销
- **多设备**: 支持同一用户多设备登录

#### 3. 防护机制
- **SQL注入**: 使用参数化查询
- **XSS攻击**: 输入验证和输出编码
- **CSRF攻击**: JWT令牌验证
- **暴力破解**: 可扩展账户锁定机制

### 性能优化

#### 1. 数据库优化
```sql
-- 关键索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
```

#### 2. 缓存策略
- **用户信息**: Redis缓存用户基本信息
- **会话状态**: 内存缓存活跃会话
- **权限信息**: 缓存用户权限列表

#### 3. 连接池配置
```python
# SQLAlchemy连接池配置
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # 连接池大小
    max_overflow=20,        # 最大溢出连接
    pool_timeout=30,        # 连接超时
    pool_recycle=3600       # 连接回收时间
)
```

## 部署和维护

### 1. 数据库初始化脚本
```bash
# 创建数据库表
python recreate_auth_tables.py

# 创建默认用户
python create_default_users.py

# 验证数据完整性
python check_users.py
```

### 2. 监控指标
- **登录成功率**: 成功登录 / 总登录尝试
- **会话活跃度**: 活跃会话数 / 总会话数
- **用户增长**: 新注册用户数量趋势
- **错误率**: 认证错误 / 总认证请求

### 3. 日志记录
```python
# 登录成功日志
logger.info(f"User {username} logged in successfully from {client_ip}")

# 登录失败日志
logger.warning(f"Failed login attempt for {username} from {client_ip}")

# 会话创建日志
logger.info(f"Session created for user {user_id}, expires at {expires_at}")
```

### 4. 备份策略
- **用户数据**: 每日全量备份
- **会话数据**: 每周备份(可定期清理过期数据)
- **活动日志**: 按月归档备份

## 扩展功能

### 1. 第三方登录
- **OAuth2集成**: 支持Google、GitHub等第三方登录
- **LDAP集成**: 企业用户目录集成
- **SSO支持**: 单点登录功能

### 2. 高级安全
- **双因素认证**: SMS、邮箱、TOTP验证
- **设备指纹**: 设备唯一标识验证
- **异常检测**: 异常登录行为检测

### 3. 用户体验
- **记住密码**: 安全的密码记忆功能
- **自动登录**: 基于设备的自动登录
- **密码重置**: 邮箱验证密码重置

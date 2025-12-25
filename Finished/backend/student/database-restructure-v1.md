# 数据库文件夹重构文档 v1.0

## 📋 重构概述

### 重构目标
将后端项目中分散的数据库相关文件重新组织到专门的 `database/` 文件夹中，提高项目结构的清晰度和可维护性。

### 重构日期
2024-06-24

### 重构范围
- 数据库连接管理
- 数据库迁移系统
- 种子数据管理
- 数据库管理工具

## 🏗️ 新的文件结构

### 重构前
```
backend/
├── app/
│   ├── core/
│   │   └── database.py          # 数据库连接
│   └── ...
├── education_platform.db        # 数据库文件（根目录）
├── create_test_users.py         # 测试用户创建脚本
└── ...
```

### 重构后
```
backend/
├── app/
│   ├── core/
│   │   └── database.py          # 兼容性模块（重定向到新模块）
│   └── ...
├── database/                    # 🆕 数据库管理模块
│   ├── __init__.py             # 模块初始化
│   ├── connection.py           # 数据库连接和会话管理
│   ├── migrations.py           # 数据库迁移管理
│   ├── seeds.py                # 种子数据管理
│   ├── manager.py              # 数据库管理CLI工具
│   ├── README.md               # 数据库模块文档
│   ├── .gitignore              # 数据库文件忽略规则
│   ├── data/                   # 🆕 数据库文件存储目录
│   │   ├── .gitkeep           # 确保目录被跟踪
│   │   └── *.db               # SQLite数据库文件
│   └── migrations/             # 🆕 迁移文件目录
│       └── *.sql              # SQL迁移文件
├── init_database.py            # 🆕 数据库初始化脚本
├── db.py                       # 🆕 数据库管理便捷脚本
└── ...
```

## 🔧 核心功能模块

### 1. 连接管理 (connection.py)
**功能**:
- 数据库引擎创建和配置
- 会话工厂管理
- 依赖注入支持
- 数据库健康检查
- 表结构创建和删除

**主要类和函数**:
```python
# 核心组件
engine: Engine                    # SQLAlchemy引擎
SessionLocal: sessionmaker        # 会话工厂
Base: DeclarativeMeta             # 模型基类

# 主要函数
get_db() -> Generator[Session]    # 依赖注入会话
init_database()                   # 初始化数据库
check_database_health() -> bool   # 健康检查

# 管理器类
class DatabaseManager:
    get_session() -> Session
    commit_session(db: Session)
    rollback_session(db: Session)
    close_session(db: Session)
```

### 2. 迁移管理 (migrations.py)
**功能**:
- 创建和管理数据库迁移文件
- 跟踪迁移应用状态
- 批量应用迁移
- 迁移状态查询

**主要类和函数**:
```python
class MigrationManager:
    create_migration(name, description)    # 创建迁移文件
    apply_migration(filepath)              # 应用单个迁移
    apply_all_migrations()                 # 应用所有迁移
    get_migration_status()                 # 获取迁移状态

# 便捷函数
create_migration(name, description)       # 创建迁移
apply_migrations()                        # 应用迁移
migration_status()                        # 查询状态
```

### 3. 种子数据 (seeds.py)
**功能**:
- 创建测试用户（管理员、教师、学生）
- 创建示例课程和课时
- 创建课程注册记录
- 幂等性数据填充

**主要类和函数**:
```python
class SeedManager:
    create_admin_user()           # 创建管理员
    create_test_teacher()         # 创建测试教师
    create_test_student()         # 创建测试学生
    create_sample_course()        # 创建示例课程
    create_sample_lessons()       # 创建示例课时
    seed_all()                    # 创建所有种子数据

# 便捷函数
seed_database()                   # 填充所有数据
create_test_users()              # 只创建用户
```

### 4. 管理工具 (manager.py)
**功能**:
- 命令行数据库管理界面
- 数据库备份和恢复
- 状态查询和监控
- 批量操作支持

**可用命令**:
```bash
python db.py init              # 初始化数据库
python db.py reset             # 重置数据库
python db.py seed              # 填充种子数据
python db.py status            # 显示状态
python db.py migrate           # 应用迁移
python db.py create-migration  # 创建迁移
python db.py backup            # 备份数据库
python db.py restore           # 恢复数据库
```

## 🔄 兼容性处理

### 向后兼容
为了确保现有代码不受影响，保留了原有的导入路径：

```python
# 原有导入方式仍然有效
from app.core.database import get_db, SessionLocal, Base

# 新的导入方式
from database.connection import get_db, SessionLocal, Base
```

### 配置更新
更新了数据库文件路径配置：
```python
# 原配置
DATABASE_URL = "sqlite:///./education_platform.db"

# 新配置
DATABASE_URL = "sqlite:///./database/data/education_platform.db"
```

## 🚀 使用指南

### 快速开始
```bash
# 1. 初始化数据库（推荐方式）
python init_database.py

# 2. 或者使用管理工具
python db.py init
python db.py seed

# 3. 启动应用
python run.py
```

### 开发工作流
```bash
# 1. 创建新迁移
python db.py create-migration add_user_avatar --description "添加用户头像字段"

# 2. 编辑迁移文件
# 编辑 database/migrations/20241224_120000_add_user_avatar.sql

# 3. 应用迁移
python db.py migrate

# 4. 检查状态
python db.py status
```

### 数据管理
```bash
# 备份数据库
python db.py backup --path backup_$(date +%Y%m%d).db

# 恢复数据库
python db.py restore backup_20241224.db

# 重置开发环境
python db.py reset
python db.py seed
```

## 📊 文件组织优势

### 1. 清晰的职责分离
- **connection.py**: 专注于数据库连接管理
- **migrations.py**: 专注于数据库结构变更
- **seeds.py**: 专注于测试数据管理
- **manager.py**: 专注于运维管理工具

### 2. 统一的数据存储
- 所有数据库文件存储在 `database/data/` 目录
- 便于备份、迁移和版本控制管理
- 避免数据库文件散落在项目各处

### 3. 完善的工具链
- 命令行管理工具覆盖常用操作
- 自动化的初始化和种子数据脚本
- 完整的迁移管理系统

### 4. 良好的可维护性
- 模块化设计，易于扩展和修改
- 详细的文档和注释
- 统一的错误处理和日志记录

## 🔒 安全考虑

### 1. 文件权限
- 数据库文件只有应用有读写权限
- 敏感配置通过环境变量管理
- 备份文件加密存储（生产环境）

### 2. 数据保护
- 自动备份机制
- 迁移前数据验证
- 回滚机制支持

### 3. 访问控制
- 管理命令需要适当权限
- 生产环境禁用危险操作
- 审计日志记录

## 📈 性能优化

### 1. 连接池管理
- 合理的连接池大小配置
- 连接超时和重试机制
- 连接泄漏检测

### 2. 查询优化
- 索引策略优化
- 查询性能监控
- 慢查询日志分析

### 3. 存储优化
- 定期数据清理
- 数据压缩策略
- 分区表支持（未来）

## 🔄 未来扩展

### 短期计划
- [ ] 添加数据库性能监控
- [ ] 实现自动备份调度
- [ ] 添加数据验证工具
- [ ] 支持多环境配置

### 中期计划
- [ ] 支持PostgreSQL数据库
- [ ] 实现读写分离
- [ ] 添加数据同步工具
- [ ] 集成监控告警

### 长期计划
- [ ] 支持分布式数据库
- [ ] 实现数据分片
- [ ] 添加数据治理功能
- [ ] 支持实时数据流

## 📝 维护说明

### 日常维护
1. 定期检查数据库状态
2. 监控磁盘空间使用
3. 执行数据备份
4. 清理过期日志

### 故障处理
1. 数据库连接失败 → 检查配置和权限
2. 迁移失败 → 查看错误日志，手动修复
3. 数据损坏 → 从备份恢复
4. 性能问题 → 分析慢查询，优化索引

---

**文档维护**: 后端开发团队  
**版本**: v1.0  
**日期**: 2024-06-24

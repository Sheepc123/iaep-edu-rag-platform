# 数据库模块

## 📁 文件结构

```
database/
├── __init__.py          # 模块初始化
├── connection.py        # 数据库连接和会话管理
├── migrations.py        # 数据库迁移管理
├── seeds.py            # 种子数据管理
├── manager.py          # 数据库管理CLI工具
├── README.md           # 本文档
├── data/               # 数据库文件存储目录
│   └── *.db           # SQLite数据库文件
└── migrations/         # 迁移文件目录
    └── *.sql          # SQL迁移文件
```

## 🚀 快速开始

### 1. 初始化数据库
```bash
# 方法1: 使用管理工具
python -m database.manager init

# 方法2: 使用Python代码
python -c "from database.connection import init_database; init_database()"
```

### 2. 填充测试数据
```bash
# 创建测试用户和示例课程
python -m database.manager seed
```

### 3. 检查数据库状态
```bash
python -m database.manager status
```

## 🔧 数据库管理

### 连接管理 (connection.py)

#### 基本用法
```python
from database.connection import get_db, SessionLocal

# 方法1: 使用依赖注入（推荐）
def some_function(db: Session = Depends(get_db)):
    # 使用数据库会话
    pass

# 方法2: 手动管理会话
db = SessionLocal()
try:
    # 数据库操作
    pass
finally:
    db.close()
```

#### 数据库管理器
```python
from database.connection import DatabaseManager

# 获取会话
db = DatabaseManager.get_session()

# 提交事务
DatabaseManager.commit_session(db)

# 回滚事务
DatabaseManager.rollback_session(db)

# 关闭会话
DatabaseManager.close_session(db)
```

### 迁移管理 (migrations.py)

#### 创建迁移
```bash
# 创建新迁移文件
python -m database.manager create-migration add_user_avatar --description "添加用户头像字段"
```

#### 应用迁移
```bash
# 应用所有待应用的迁移
python -m database.manager migrate
```

#### 迁移状态
```bash
# 查看迁移状态
python -m database.manager status
```

#### 编程方式使用
```python
from database.migrations import MigrationManager, apply_migrations

# 创建迁移管理器
manager = MigrationManager()

# 创建迁移文件
manager.create_migration("add_new_table", "添加新表")

# 应用所有迁移
apply_migrations()

# 获取迁移状态
status = manager.get_migration_status()
```

### 种子数据 (seeds.py)

#### 填充所有种子数据
```bash
python -m database.manager seed
```

#### 只创建测试用户
```bash
python -m database.manager create-users
```

#### 编程方式使用
```python
from database.seeds import SeedManager, seed_database

# 使用上下文管理器
with SeedManager() as seed_manager:
    seed_manager.create_admin_user()
    seed_manager.create_test_teacher()
    seed_manager.create_test_student()

# 或使用便捷函数
seed_database()
```

## 🛠️ 命令行工具

### 可用命令

```bash
# 初始化数据库
python -m database.manager init

# 重置数据库（删除所有数据）
python -m database.manager reset

# 填充种子数据
python -m database.manager seed

# 创建测试用户
python -m database.manager create-users

# 显示数据库状态
python -m database.manager status

# 应用迁移
python -m database.manager migrate

# 创建新迁移
python -m database.manager create-migration <name> [--description <desc>]

# 备份数据库
python -m database.manager backup [--path <backup_path>]

# 恢复数据库
python -m database.manager restore <backup_path>
```

### 使用示例

```bash
# 完整的数据库设置流程
python -m database.manager init     # 初始化
python -m database.manager seed     # 填充数据
python -m database.manager status   # 检查状态

# 开发流程
python -m database.manager create-migration add_course_tags --description "添加课程标签功能"
# 编辑生成的迁移文件
python -m database.manager migrate  # 应用迁移

# 备份和恢复
python -m database.manager backup --path backup_20241224.db
python -m database.manager restore backup_20241224.db
```

## 📊 数据库配置

数据库配置在 `app/core/config.py` 中定义：

```python
class DatabaseConfig:
    DATABASE_URL = "sqlite:///./education_platform.db"
    
    @classmethod
    def get_database_url(cls) -> str:
        return cls.DATABASE_URL
    
    @classmethod
    def get_engine_args(cls) -> dict:
        return {
            "connect_args": {"check_same_thread": False},
            "echo": False  # 设为True可以看到SQL语句
        }
```

## 🔒 最佳实践

### 1. 会话管理
- 优先使用依赖注入 `Depends(get_db)`
- 确保会话正确关闭
- 使用事务处理复杂操作

### 2. 迁移管理
- 迁移文件按时间戳命名
- 每个迁移只做一件事
- 提供回滚方案（手动）
- 测试迁移脚本

### 3. 种子数据
- 保持幂等性（可重复执行）
- 检查数据是否已存在
- 使用真实但安全的测试数据

### 4. 备份策略
- 定期备份生产数据
- 测试恢复流程
- 保留多个备份版本

## 🚨 注意事项

1. **数据库文件位置**: SQLite文件存储在 `database/data/` 目录中
2. **迁移顺序**: 迁移按文件名时间戳顺序执行
3. **种子数据**: 可以安全地重复执行种子数据脚本
4. **备份恢复**: 只支持SQLite数据库的备份恢复
5. **权限管理**: 确保数据库文件有适当的读写权限

## 🔗 相关文件

- `app/models/` - 数据模型定义
- `app/core/config.py` - 数据库配置
- `app/core/database.py` - 原始数据库连接（已迁移到此模块）

## 📝 更新日志

- **2024-06-24**: 创建数据库模块，重构文件结构
- 迁移数据库连接管理到独立模块
- 添加迁移管理系统
- 添加种子数据管理
- 添加命令行管理工具

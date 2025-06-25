"""
数据库管理工具
"""
import os
import shutil
import argparse
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .connection import init_database, check_database_health, drop_tables
from .migrations import MigrationManager, apply_migrations, migration_status
from .seeds import seed_database, create_test_users


class DatabaseCLI:
    """数据库命令行工具"""
    
    def __init__(self):
        self.migration_manager = MigrationManager()
    
    def init(self):
        """初始化数据库"""
        print("🚀 初始化数据库...")
        init_database()
        apply_migrations()
        print("✅ 数据库初始化完成")
    
    def reset(self):
        """重置数据库（删除所有数据）"""
        print("⚠️  重置数据库...")
        confirm = input("这将删除所有数据，确定继续吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return
        
        drop_tables()
        self.init()
        print("✅ 数据库重置完成")
    
    def seed(self):
        """填充种子数据"""
        print("🌱 填充种子数据...")
        seed_database()
        print("✅ 种子数据填充完成")
    
    def create_users(self):
        """创建测试用户"""
        print("👥 创建测试用户...")
        create_test_users()
        print("✅ 测试用户创建完成")
    
    def status(self):
        """显示数据库状态"""
        print("📊 数据库状态:")
        
        # 检查连接
        if check_database_health():
            print("✅ 数据库连接正常")
        else:
            print("❌ 数据库连接失败")
            return
        
        # 迁移状态
        status = migration_status()
        print(f"📋 迁移状态:")
        print(f"   总迁移数: {status['total_migrations']}")
        print(f"   已应用: {status['applied_migrations']}")
        print(f"   待应用: {status['pending_migrations']}")
        
        if status['migrations']:
            print("   迁移列表:")
            for migration in status['migrations']:
                status_icon = "✅" if migration['applied'] else "⏳"
                print(f"     {status_icon} {migration['name']}")
    
    def migrate(self):
        """应用迁移"""
        print("🔄 应用数据库迁移...")
        if apply_migrations():
            print("✅ 迁移应用完成")
        else:
            print("❌ 迁移应用失败")
    
    def create_migration(self, name: str, description: str = ""):
        """创建新迁移"""
        print(f"📝 创建迁移: {name}")
        filepath = self.migration_manager.create_migration(name, description)
        print(f"✅ 迁移文件已创建: {filepath}")
    
    def backup(self, backup_path: str = None):
        """备份数据库"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"database_backup_{timestamp}.db"
        
        print(f"💾 备份数据库到: {backup_path}")
        
        # 获取当前数据库文件路径
        from ..app.core.config import DatabaseConfig
        db_url = DatabaseConfig.get_database_url()
        if db_url.startswith("sqlite:///"):
            db_file = db_url.replace("sqlite:///", "")
            if os.path.exists(db_file):
                shutil.copy2(db_file, backup_path)
                print(f"✅ 数据库备份完成: {backup_path}")
            else:
                print(f"❌ 数据库文件不存在: {db_file}")
        else:
            print("❌ 只支持SQLite数据库备份")
    
    def restore(self, backup_path: str):
        """恢复数据库"""
        if not os.path.exists(backup_path):
            print(f"❌ 备份文件不存在: {backup_path}")
            return
        
        print(f"🔄 从备份恢复数据库: {backup_path}")
        confirm = input("这将覆盖当前数据库，确定继续吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return
        
        # 获取当前数据库文件路径
        from ..app.core.config import DatabaseConfig
        db_url = DatabaseConfig.get_database_url()
        if db_url.startswith("sqlite:///"):
            db_file = db_url.replace("sqlite:///", "")
            shutil.copy2(backup_path, db_file)
            print(f"✅ 数据库恢复完成")
        else:
            print("❌ 只支持SQLite数据库恢复")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="数据库管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init命令
    subparsers.add_parser("init", help="初始化数据库")
    
    # reset命令
    subparsers.add_parser("reset", help="重置数据库")
    
    # seed命令
    subparsers.add_parser("seed", help="填充种子数据")
    
    # create-users命令
    subparsers.add_parser("create-users", help="创建测试用户")
    
    # status命令
    subparsers.add_parser("status", help="显示数据库状态")
    
    # migrate命令
    subparsers.add_parser("migrate", help="应用迁移")
    
    # create-migration命令
    migration_parser = subparsers.add_parser("create-migration", help="创建新迁移")
    migration_parser.add_argument("name", help="迁移名称")
    migration_parser.add_argument("--description", help="迁移描述", default="")
    
    # backup命令
    backup_parser = subparsers.add_parser("backup", help="备份数据库")
    backup_parser.add_argument("--path", help="备份文件路径")
    
    # restore命令
    restore_parser = subparsers.add_parser("restore", help="恢复数据库")
    restore_parser.add_argument("path", help="备份文件路径")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = DatabaseCLI()
    
    try:
        if args.command == "init":
            cli.init()
        elif args.command == "reset":
            cli.reset()
        elif args.command == "seed":
            cli.seed()
        elif args.command == "create-users":
            cli.create_users()
        elif args.command == "status":
            cli.status()
        elif args.command == "migrate":
            cli.migrate()
        elif args.command == "create-migration":
            cli.create_migration(args.name, args.description)
        elif args.command == "backup":
            cli.backup(args.path)
        elif args.command == "restore":
            cli.restore(args.path)
        else:
            print(f"未知命令: {args.command}")
            parser.print_help()
    
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")


if __name__ == "__main__":
    main()

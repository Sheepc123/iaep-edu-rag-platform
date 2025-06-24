"""
依赖安装脚本
"""
import subprocess
import sys

# 核心依赖列表
dependencies = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "sqlalchemy==2.0.23",
    "python-jose[cryptography]==3.3.0",
    "passlib[bcrypt]==1.7.4",
    "python-multipart==0.0.6",
    "pydantic==2.5.0",
    "pydantic-settings==2.1.0",
    "python-dateutil==2.8.2",
    "email-validator==2.1.0",
    "aiofiles==23.2.1",
    "loguru==0.7.2",
    "requests==2.31.0"  # 用于测试脚本
]

def install_package(package):
    """安装单个包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package} 安装失败: {e}")
        return False

def main():
    """主安装函数"""
    print("🚀 开始安装后端依赖...")
    print("=" * 50)
    
    success_count = 0
    total_count = len(dependencies)
    
    for package in dependencies:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"安装完成: {success_count}/{total_count} 个包安装成功")
    
    if success_count == total_count:
        print("🎉 所有依赖安装成功！")
        return True
    else:
        print("⚠️ 部分依赖安装失败，请检查错误信息")
        return False

if __name__ == "__main__":
    main()

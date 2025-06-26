"""
安装向量数据库依赖
"""
import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
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
    print("🚀 开始安装向量数据库依赖...")
    
    # 需要安装的包列表（按依赖顺序）
    packages = [
        "numpy==1.24.3",
        "scikit-learn==1.3.2",
        "huggingface-hub==0.17.3",
        "sentence-transformers==2.2.2",
        "chromadb==0.4.15",
        "jieba==0.42.1",
        "openai==1.3.7",
        "langchain==0.0.350",
    ]

    success_count = 0
    failed_packages = []
    
    for package in packages:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    print(f"\n📊 安装结果:")
    print(f"✅ 成功安装: {success_count}/{len(packages)} 个包")
    
    if failed_packages:
        print(f"❌ 安装失败的包:")
        for pkg in failed_packages:
            print(f"   - {pkg}")
        print(f"\n💡 建议:")
        print(f"1. 检查网络连接")
        print(f"2. 尝试手动安装失败的包")
        print(f"3. 考虑使用国内镜像源")
    else:
        print(f"🎉 所有依赖安装成功!")
        
        # 测试导入
        print(f"\n🧪 测试依赖导入...")
        test_imports()

def test_imports():
    """测试依赖导入"""
    test_cases = [
        ("chromadb", "Chroma向量数据库"),
        ("sentence_transformers", "Sentence Transformers"),
        ("numpy", "NumPy"),
        ("sklearn", "Scikit-learn"),
        ("jieba", "Jieba中文分词"),
        ("langchain", "LangChain")
    ]
    
    for module, name in test_cases:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")

if __name__ == "__main__":
    main()

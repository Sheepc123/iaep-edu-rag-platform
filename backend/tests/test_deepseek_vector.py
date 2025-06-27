"""
测试DeepSeek向量化方案的可行性
"""
import os
import sys
import json
import requests
import numpy as np
from typing import List, Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_deepseek_api():
    """测试DeepSeek API的基本功能"""
    print("🔍 研究DeepSeek向量化方案...")
    
    # 从环境变量或配置获取API信息
    try:
        from app.core.config import settings
        api_key = settings.DEEPSEEK_API_KEY
        base_url = settings.DEEPSEEK_BASE_URL
        model = settings.DEEPSEEK_MODEL
    except:
        # 备用配置
        api_key = "sk-12d474502bc54621b3888eb6a8e4035e"
        base_url = "https://api.deepseek.com/v1"
        model = "deepseek-chat"
    
    print(f"📡 API配置:")
    print(f"   - Base URL: {base_url}")
    print(f"   - Model: {model}")
    print(f"   - API Key: {'已设置' if api_key else '未设置'}")
    
    if not api_key:
        print("❌ 未设置DeepSeek API Key")
        return False
    
    # 1. 测试基本聊天功能
    print("\n1. 测试基本聊天功能...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        chat_data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "你好，请简单介绍一下你自己"}
            ],
            "max_tokens": 100
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ 聊天功能正常: {content[:50]}...")
        else:
            print(f"❌ 聊天功能失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天功能测试异常: {e}")
        return False
    
    # 2. 测试是否支持embeddings端点
    print("\n2. 测试embeddings端点...")
    try:
        embedding_data = {
            "model": "text-embedding-ada-002",  # 尝试OpenAI兼容的模型名
            "input": "这是一个测试文本"
        }
        
        response = requests.post(
            f"{base_url}/embeddings",
            headers=headers,
            json=embedding_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "data" in result and len(result["data"]) > 0:
                embedding = result["data"][0]["embedding"]
                print(f"✅ 支持embeddings端点，向量维度: {len(embedding)}")
                return True
            else:
                print("⚠️  embeddings端点响应格式异常")
        else:
            print(f"❌ embeddings端点不支持: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ embeddings端点测试异常: {e}")
    
    # 3. 尝试其他可能的embedding模型名
    print("\n3. 尝试其他embedding模型...")
    embedding_models = [
        "deepseek-embedding",
        "text-embedding-3-small",
        "text-embedding-3-large",
        "embedding-001"
    ]
    
    for model_name in embedding_models:
        try:
            embedding_data = {
                "model": model_name,
                "input": "测试文本"
            }
            
            response = requests.post(
                f"{base_url}/embeddings",
                headers=headers,
                json=embedding_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if "data" in result and len(result["data"]) > 0:
                    embedding = result["data"][0]["embedding"]
                    print(f"✅ 模型 {model_name} 可用，向量维度: {len(embedding)}")
                    return True
            else:
                print(f"⚠️  模型 {model_name} 不可用: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  模型 {model_name} 测试异常: {e}")
    
    return False

def test_deepseek_text_to_vector():
    """测试使用DeepSeek聊天模型生成向量的方案"""
    print("\n4. 测试聊天模型生成向量方案...")
    
    try:
        from app.core.config import settings
        api_key = settings.DEEPSEEK_API_KEY
        base_url = settings.DEEPSEEK_BASE_URL
        model = settings.DEEPSEEK_MODEL
    except:
        api_key = "sk-12d474502bc54621b3888eb6a8e4035e"
        base_url = "https://api.deepseek.com/v1"
        model = "deepseek-chat"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 方案1: 让AI生成数值向量
    print("\n方案1: 让AI直接生成数值向量...")
    try:
        prompt = """请将以下文本转换为384维的数值向量，用于语义搜索。
请返回一个包含384个浮点数的JSON数组，数值范围在-1到1之间。

文本: "Python是一种高级编程语言"

请只返回JSON数组，不要其他解释。"""

        chat_data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.1
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 尝试解析JSON
            try:
                vector = json.loads(content)
                if isinstance(vector, list) and len(vector) == 384:
                    print(f"✅ 方案1可行: 生成了{len(vector)}维向量")
                    print(f"   向量示例: {vector[:5]}...")
                    return True
                else:
                    print(f"⚠️  方案1部分可行: 生成了{len(vector) if isinstance(vector, list) else 0}维向量")
            except:
                print(f"⚠️  方案1响应格式问题: {content[:100]}...")
        else:
            print(f"❌ 方案1失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 方案1异常: {e}")
    
    # 方案2: 让AI生成关键词，然后用传统方法向量化
    print("\n方案2: AI提取关键词 + 传统向量化...")
    try:
        prompt = """请分析以下文本，提取5-10个最重要的关键词，用逗号分隔。
只返回关键词，不要其他解释。

文本: "Python是一种高级编程语言，具有简洁的语法和强大的功能。它广泛应用于Web开发、数据科学、人工智能等领域。"""

        chat_data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            keywords = result["choices"][0]["message"]["content"].strip()
            print(f"✅ 方案2可行: 提取关键词 '{keywords}'")
            
            # 可以用这些关键词进行传统的TF-IDF或哈希向量化
            return True
        else:
            print(f"❌ 方案2失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 方案2异常: {e}")
    
    # 方案3: 让AI生成文本摘要，然后向量化摘要
    print("\n方案3: AI生成摘要 + 摘要向量化...")
    try:
        prompt = """请将以下文本总结为一句话，保留核心语义信息：

"机器学习是人工智能的一个重要分支，它使计算机能够在没有明确编程的情况下学习和改进。常见的机器学习算法包括线性回归、决策树、神经网络等。"

只返回总结，不要其他内容。"""

        chat_data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result["choices"][0]["message"]["content"].strip()
            print(f"✅ 方案3可行: 生成摘要 '{summary}'")
            return True
        else:
            print(f"❌ 方案3失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 方案3异常: {e}")
    
    return False

def analyze_feasibility():
    """分析各种方案的可行性"""
    print("\n📊 DeepSeek向量化方案可行性分析:")
    
    print("\n🎯 方案对比:")
    print("1. 直接embeddings API:")
    print("   ✅ 优点: 高质量向量，语义理解好")
    print("   ❌ 缺点: 可能不支持，需要验证")
    print("   💰 成本: 按token计费")
    
    print("\n2. AI生成数值向量:")
    print("   ✅ 优点: 灵活，可控制维度")
    print("   ❌ 缺点: 质量不稳定，计算成本高")
    print("   💰 成本: 按生成token计费，较高")
    
    print("\n3. AI提取关键词:")
    print("   ✅ 优点: 成本低，质量稳定")
    print("   ✅ 优点: 可结合传统方法")
    print("   ⚠️  缺点: 语义信息有损失")
    print("   💰 成本: 较低")
    
    print("\n4. AI生成摘要:")
    print("   ✅ 优点: 保留核心语义")
    print("   ✅ 优点: 可结合传统向量化")
    print("   ⚠️  缺点: 信息压缩")
    print("   💰 成本: 中等")
    
    print("\n💡 推荐方案:")
    print("1. 优先尝试: DeepSeek embeddings API（如果支持）")
    print("2. 备选方案: AI关键词提取 + TF-IDF")
    print("3. 混合方案: AI摘要 + 哈希向量")

def main():
    """主测试函数"""
    print("🚀 DeepSeek向量化方案研究开始...")
    
    # 测试基本API功能
    api_works = test_deepseek_api()
    
    if api_works:
        print("\n🎉 DeepSeek支持embeddings API!")
    else:
        print("\n⚠️  DeepSeek不支持标准embeddings API，测试替代方案...")
        # 测试替代方案
        alternative_works = test_deepseek_text_to_vector()
        
        if alternative_works:
            print("\n✅ 找到可行的替代方案!")
        else:
            print("\n❌ 替代方案也有问题")
    
    # 分析可行性
    analyze_feasibility()
    
    print("\n🎯 结论:")
    if api_works:
        print("✅ 推荐使用DeepSeek embeddings API")
    else:
        print("✅ 推荐使用AI关键词提取 + 传统向量化的混合方案")
    
    print("\n🚀 下一步:")
    print("1. 实现推荐的方案")
    print("2. 与现有向量服务集成")
    print("3. 性能和成本测试")

if __name__ == "__main__":
    main()

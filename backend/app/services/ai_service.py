"""
AI助手服务
"""
import asyncio
import json
import time
import httpx
import os
from typing import Dict, List, Optional, AsyncGenerator, Any
from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger

from ..core.config import settings
from ..models.chat import AIConversation, AIMessage, AIRecommendation
from ..models.user import User
from ..schemas.ai import (
    AIMessageCreate, AIMessageResponse, AIConversationCreate,
    AIConversationResponse, AIStreamResponse, MessageSender, MessageType
)

# 创建专门的AI日志记录器
ai_logger = logger.bind(name="AI_SERVICE")

# 确保AI日志目录存在
ai_log_dir = "logs"
if not os.path.exists(ai_log_dir):
    os.makedirs(ai_log_dir)

# 配置AI专用日志文件（不输出到控制台）
ai_logger.add(
    "logs/ai_service.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | AI_SERVICE | {message}",
    filter=lambda record: record["extra"].get("name") == "AI_SERVICE"
)


class AIService:
    """AI助手服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _build_system_prompt(self, user_role: str = "student") -> str:
        """根据用户角色构建系统提示词"""
        if user_role == "teacher":
            return """你是一个专为教师设计的AI助手，专门帮助教师进行教学工作。

你的主要职责：
1. 📚 课程设计：帮助设计课程大纲、教学计划、课时安排、学习目标等
2. 📝 题目生成：根据教学内容生成各种类型的练习题、考试题、作业题
3. 🎯 教学建议：提供教学方法、课堂管理、学生激励、互动技巧等建议
4. 📊 成绩分析：帮助分析学生成绩分布、学习效果，提出改进建议
5. 📖 教学资源：推荐相关的教学材料、参考资料、教学工具等
6. 👥 学生管理：提供学生学习指导、问题解答、个性化教学建议

你的特点：
- 专业、实用、具有教育经验
- 了解各种教学理论和方法
- 能够提供具体可行的教学方案
- 关注教学效果和学生发展
- 支持多种学科的教学需求

回复格式要求：
- 提供结构化、可操作的建议
- 包含具体的实施步骤
- 适当使用教育术语
- 考虑不同学生的学习特点
- 提供多种解决方案供选择

请根据教师的需求提供专业的教学指导和建议。"""
        else:
            return """你是一个专业的AI学习助手，名叫小智，专门帮助学生学习和解答问题。

你的特点：
1. 友好、耐心、专业
2. 善于解释复杂概念，用简单易懂的语言
3. 能够提供学习建议和方法指导
4. 会推荐相关的练习和资源
5. 支持多种学科，特别擅长数学、编程、科学等

回复格式要求：
- 使用清晰的结构化回复
- 适当使用emoji增加亲和力
- 提供具体可行的建议
- 鼓励学生继续学习

请根据学生的问题提供有帮助的回答。"""

    async def create_conversation(
        self,
        user_id: int,
        conversation_data: AIConversationCreate
    ) -> AIConversationResponse:
        """创建新的AI对话"""
        try:
            # 创建对话记录
            conversation = AIConversation(
                user_id=user_id,
                title=conversation_data.title or "新对话",
                context=conversation_data.context
            )
            
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            
            # 获取用户角色以生成相应的欢迎消息
            user = self.db.query(User).filter(User.id == user_id).first()
            user_role = user.role if user else "student"

            # 根据用户角色生成欢迎消息
            if user_role == "teacher":
                welcome_content = """👋 您好！我是您的AI教学助手，专门为教师提供教学支持。

我可以帮助您：

📚 **课程设计** - 制定教学大纲、课程规划、学习目标
📝 **题目生成** - 创建练习题、考试题、作业题
🎯 **教学建议** - 提供教学方法、课堂管理、学生激励策略
📊 **成绩分析** - 分析学生表现，制定个性化教学方案
📖 **资源推荐** - 推荐教学材料、参考资料、教学工具

请告诉我您需要哪方面的教学帮助？"""
            else:
                welcome_content = "你好！我是你的AI学习助手小智，我可以帮助你：\n\n📚 解答学习问题\n🎯 制定学习计划\n📊 分析学习进度\n💡 提供学习建议\n\n有什么可以帮助你的吗？"

            welcome_message = AIMessage(
                conversation_id=conversation.id,
                content=welcome_content,
                sender=MessageSender.AI,
                message_type=MessageType.TEXT,
                model_used=settings.DEEPSEEK_MODEL
            )
            
            self.db.add(welcome_message)
            conversation.message_count = 1
            conversation.last_message_at = datetime.utcnow()
            
            self.db.commit()
            
            return AIConversationResponse.from_orm(conversation)
            
        except Exception as e:
            logger.error(f"创建AI对话失败: {e}")
            self.db.rollback()
            raise Exception("创建对话失败")

    async def get_conversations(self, user_id: int) -> List[AIConversationResponse]:
        """获取用户的所有对话"""
        try:
            conversations = self.db.query(AIConversation).filter(
                AIConversation.user_id == user_id,
                AIConversation.is_active == True
            ).order_by(AIConversation.last_message_at.desc()).all()
            
            return [AIConversationResponse.from_orm(conv) for conv in conversations]
            
        except Exception as e:
            logger.error(f"获取对话列表失败: {e}")
            raise Exception("获取对话列表失败")

    async def get_conversation_messages(
        self, 
        user_id: int, 
        conversation_id: int
    ) -> List[AIMessageResponse]:
        """获取对话的所有消息"""
        try:
            # 验证对话所有权
            conversation = self.db.query(AIConversation).filter(
                AIConversation.id == conversation_id,
                AIConversation.user_id == user_id
            ).first()
            
            if not conversation:
                raise Exception("对话不存在或无权限访问")
            
            messages = self.db.query(AIMessage).filter(
                AIMessage.conversation_id == conversation_id
            ).order_by(AIMessage.created_at.asc()).all()
            
            return [AIMessageResponse.from_orm(msg) for msg in messages]
            
        except Exception as e:
            logger.error(f"获取对话消息失败: {e}")
            raise Exception("获取对话消息失败")

    async def send_message(
        self, 
        user_id: int, 
        message_data: AIMessageCreate
    ) -> AIMessageResponse:
        """发送消息并获取AI回复"""
        try:
            ai_logger.info(f"🚀 AI服务开始处理消息")
            ai_logger.info(f"📝 用户ID: {user_id}")
            ai_logger.info(f"💬 用户消息: {message_data.content}")
            ai_logger.info(f"📋 消息类型: {message_data.message_type}")
            ai_logger.info(f"🔗 指定对话ID: {message_data.conversation_id}")

            # 获取或创建对话
            conversation = None
            if message_data.conversation_id:
                try:
                    conversation_id = message_data.conversation_id
                    ai_logger.info(f"🔍 查找现有对话: {conversation_id}")
                    conversation = self.db.query(AIConversation).filter(
                        AIConversation.id == conversation_id,
                        AIConversation.user_id == user_id
                    ).first()

                    if conversation:
                        ai_logger.info(f"✅ 找到现有对话: {conversation.title}")
                        ai_logger.info(f"📊 对话统计 - 消息数: {conversation.message_count}, Token数: {conversation.total_tokens}")
                    else:
                        ai_logger.warning(f"❌ 对话ID {conversation_id} 不存在或无权限访问，将创建新对话")
                except Exception as e:
                    ai_logger.warning(f"⚠️ 处理对话ID时出错: {e}，将创建新对话")

            if not conversation:
                # 创建新对话
                ai_logger.info("🆕 创建新的AI对话")
                conversation_title = message_data.content[:20] + "..." if len(message_data.content) > 20 else message_data.content
                ai_logger.info(f"📝 新对话标题: {conversation_title}")
                conversation_create = AIConversationCreate(title=conversation_title)
                conversation_response = await self.create_conversation(user_id, conversation_create)
                conversation = self.db.query(AIConversation).filter(
                    AIConversation.id == int(conversation_response.id)
                ).first()
                ai_logger.info(f"✅ 新对话创建成功，ID: {conversation.id}")
            
            # 保存用户消息
            ai_logger.info("💾 保存用户消息到数据库")
            user_message = AIMessage(
                conversation_id=conversation.id,
                content=message_data.content,
                sender=MessageSender.USER,
                message_type=message_data.message_type
            )

            self.db.add(user_message)
            self.db.commit()
            self.db.refresh(user_message)
            ai_logger.info(f"✅ 用户消息已保存，消息ID: {user_message.id}")

            # 获取用户信息以确定角色
            user = self.db.query(User).filter(User.id == user_id).first()
            user_role = user.role if user else "student"

            # 生成AI回复
            ai_logger.info(f"🤖 开始生成AI回复")
            ai_logger.info(f"👤 用户角色: {user_role}")
            ai_logger.info(f"📝 输入内容: {message_data.content}")
            ai_response = await self._generate_ai_response(
                message_data.content,
                conversation.id,
                message_data.context,
                user_role
            )
            ai_logger.info(f"✅ AI回复生成完成")
            ai_logger.info(f"📝 回复内容: {ai_response['content'][:100]}...")
            ai_logger.info(f"🔧 使用模型: {ai_response.get('model_used', 'mock')}")
            ai_logger.info(f"🎯 Token使用: {ai_response.get('tokens_used', 0)}")
            ai_logger.info(f"⏱️ 响应时间: {ai_response.get('response_time', 0.0):.2f}秒")
            
            # 保存AI回复
            ai_logger.info("💾 保存AI回复到数据库")
            ai_message = AIMessage(
                conversation_id=conversation.id,
                content=ai_response["content"],
                sender=MessageSender.AI,
                message_type=MessageType.TEXT,
                model_used=settings.DEEPSEEK_MODEL,
                tokens_used=ai_response.get("tokens_used"),
                response_time=ai_response.get("response_time")
            )

            self.db.add(ai_message)

            # 更新对话统计
            ai_logger.info("📊 更新对话统计信息")
            old_message_count = conversation.message_count
            old_total_tokens = conversation.total_tokens
            conversation.message_count += 2
            conversation.total_tokens += ai_response.get("tokens_used", 0)
            conversation.last_message_at = datetime.utcnow()

            ai_logger.info(f"📈 消息数: {old_message_count} → {conversation.message_count}")
            ai_logger.info(f"🎯 Token数: {old_total_tokens} → {conversation.total_tokens}")

            # 自动更新对话标题
            if conversation.title == "新对话":
                new_title = message_data.content[:20] + ("..." if len(message_data.content) > 20 else "")
                ai_logger.info(f"📝 更新对话标题: {conversation.title} → {new_title}")
                conversation.title = new_title

            self.db.commit()
            self.db.refresh(ai_message)
            ai_logger.info("✅ 数据库事务提交成功")

            ai_logger.info(f"🎉 AI消息处理完成")
            ai_logger.info(f"📋 最终结果 - 对话ID: {conversation.id}, AI消息ID: {ai_message.id}")

            return AIMessageResponse.from_orm(ai_message)
            
        except Exception as e:
            ai_logger.error(f"❌ 发送消息失败: {e}")
            ai_logger.error(f"🔄 数据库事务已回滚")
            self.db.rollback()
            raise Exception(f"发送消息失败: {str(e)}")

    async def _generate_ai_response(
        self,
        user_input: str,
        conversation_id: int,
        context: Optional[Dict[str, Any]] = None,
        user_role: str = "student"
    ) -> Dict[str, Any]:
        """生成AI回复"""
        start_time = time.time()

        ai_logger.info(f"🔧 开始生成AI回复，用户输入: {user_input[:50]}...")
        ai_logger.info(f"🔑 DeepSeek API密钥状态: {'已配置' if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != 'your-deepseek-api-key-here' else '未配置'}")

        # 如果配置了DeepSeek API密钥，使用真实API
        if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "your-deepseek-api-key-here":
            try:
                ai_logger.info("🌐 尝试调用DeepSeek API...")
                ai_logger.info(f"🔗 API地址: {settings.DEEPSEEK_BASE_URL}")
                ai_logger.info(f"🤖 使用模型: {settings.DEEPSEEK_MODEL}")
                result = await self._call_deepseek_api(user_input, conversation_id, context, user_role)
                ai_logger.info("✅ DeepSeek API调用成功")
                return result
            except Exception as e:
                ai_logger.error(f"❌ DeepSeek API调用失败，使用模拟回复: {e}")

        # 否则使用模拟回复
        ai_logger.info("🎭 使用模拟回复")
        await asyncio.sleep(1.0)  # 模拟API调用延迟
        response_content = self._generate_mock_response(user_input, user_role)
        ai_logger.info(f"✅ 模拟回复生成完成: {response_content[:50]}...")
        response_time = time.time() - start_time

        return {
            "content": response_content,
            "tokens_used": len(response_content) // 4,  # 粗略估算
            "response_time": response_time
        }

    async def _call_deepseek_api(
        self,
        user_input: str,
        conversation_id: int,
        context: Optional[Dict[str, Any]] = None,
        user_role: str = "student"
    ) -> Dict[str, Any]:
        """调用DeepSeek API"""
        start_time = time.time()

        ai_logger.info(f"🚀 准备调用DeepSeek API，对话ID: {conversation_id}")
        ai_logger.info(f"📝 用户输入: {user_input}")

        # 获取对话历史
        ai_logger.info(f"📚 获取对话历史消息")
        recent_messages = self.db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation_id
        ).order_by(AIMessage.created_at.desc()).limit(10).all()

        ai_logger.info(f"📖 获取到 {len(recent_messages)} 条历史消息")

        # 构建消息历史
        ai_logger.info(f"🔧 构建API消息历史")
        system_prompt = self._build_system_prompt(user_role)
        messages = [{"role": "system", "content": system_prompt}]
        ai_logger.info(f"✅ 添加系统提示 ({user_role}): {system_prompt[:50]}...")

        # 添加最近的对话历史（倒序添加）
        for msg in reversed(recent_messages):
            role = "user" if msg.sender == MessageSender.USER else "assistant"
            messages.append({"role": role, "content": msg.content})
            ai_logger.info(f"➕ 添加历史消息 ({role}): {msg.content[:30]}...")

        # 添加当前用户输入
        messages.append({"role": "user", "content": user_input})
        ai_logger.info(f"➕ 添加当前用户输入: {user_input[:30]}...")

        ai_logger.info(f"📋 构建了 {len(messages)} 条消息用于API调用")

        # 准备API请求
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY[:10]}...{settings.DEEPSEEK_API_KEY[-4:]}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": messages,
            "max_tokens": settings.AI_MAX_TOKENS,
            "temperature": settings.AI_TEMPERATURE,
            "stream": False
        }

        ai_logger.info(f"🌐 发送API请求到: {settings.DEEPSEEK_BASE_URL}/chat/completions")
        ai_logger.info(f"🤖 使用模型: {settings.DEEPSEEK_MODEL}")
        ai_logger.info(f"📦 请求参数: max_tokens={settings.AI_MAX_TOKENS}, temperature={settings.AI_TEMPERATURE}")

        # 发送API请求
        try:
            ai_logger.info(f"⏱️ 设置超时时间: {settings.AI_TIMEOUT}秒")
            async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT) as client:
                response = await client.post(
                    f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

                ai_logger.info(f"📡 API响应状态码: {response.status_code}")

                if response.status_code != 200:
                    ai_logger.error(f"❌ API请求失败: {response.status_code} - {response.text}")
                    raise Exception(f"API请求失败: {response.status_code} - {response.text}")

                result = response.json()
                ai_logger.info("✅ API响应解析成功")

                if "choices" not in result or not result["choices"]:
                    ai_logger.error(f"❌ API返回格式错误: {result}")
                    raise Exception("API返回格式错误")

                content = result["choices"][0]["message"]["content"]
                tokens_used = result.get("usage", {}).get("total_tokens", 0)
                response_time = time.time() - start_time

                ai_logger.info(f"🎉 API调用成功")
                ai_logger.info(f"📝 回复内容: {content[:100]}...")
                ai_logger.info(f"🎯 使用token: {tokens_used}")
                ai_logger.info(f"⏱️ 响应时间: {response_time:.2f}s")

                return {
                    "content": content,
                    "tokens_used": tokens_used,
                    "response_time": response_time
                }
        except httpx.TimeoutException:
            ai_logger.error("⏰ API请求超时")
            raise Exception("API请求超时")
        except httpx.RequestError as e:
            ai_logger.error(f"🌐 API请求错误: {e}")
            raise Exception(f"API请求错误: {e}")
        except Exception as e:
            ai_logger.error(f"❌ API调用异常: {e}")
            raise

    def _generate_mock_response(self, user_input: str, user_role: str = "student") -> str:
        """生成模拟AI回复"""
        lower_input = user_input.lower()

        if user_role == "teacher":
            # 教师专用回复逻辑
            if any(keyword in lower_input for keyword in ['课程设计', '课程大纲', '教学计划', '课程']):
                return """📚 **课程设计建议**

我来帮您设计课程大纲！以数据结构课程为例：

**第1-2周：基础概念**
- 数据结构概述、算法复杂度分析
- 线性表：数组、链表的实现与应用

**第3-4周：栈与队列**
- 栈的应用：表达式求值、括号匹配
- 队列的应用：BFS、任务调度

**第5-6周：树结构**
- 二叉树遍历、二叉搜索树
- 平衡树、堆的实现

**第7-8周：图与算法**
- 图的表示、DFS/BFS
- 最短路径、最小生成树

**教学建议：**
- 每章配合编程实践
- 设置阶段性测试
- 鼓励学生实现经典算法

需要我为特定章节制定更详细的教学方案吗？"""

            elif any(keyword in lower_input for keyword in ['题目生成', '练习题', '考试题', '作业题']):
                return """📝 **题目生成方案**

**算法基础练习题：**

1. **选择题（5道）**
   - 时间复杂度分析
   - 数据结构特性判断

2. **编程题（3道）**
   - 链表反转实现
   - 二叉树遍历算法
   - 排序算法优化

3. **分析题（2道）**
   - 算法效率对比分析
   - 数据结构选择依据

**难度分布：**
- 基础题：60%（巩固概念）
- 中等题：30%（应用能力）
- 提高题：10%（创新思维）

**评分标准：**
- 代码正确性：50%
- 算法效率：30%
- 代码规范：20%

需要我生成具体的题目内容吗？"""

            elif any(keyword in lower_input for keyword in ['教学建议', '课堂管理', '学生激励', '教学方法']):
                return """🎯 **教学建议与方法**

**提高学生积极性的策略：**

1. **互动式教学**
   - 课堂提问、小组讨论
   - 实时编程演示
   - 学生上台讲解

2. **项目驱动学习**
   - 设计有趣的编程项目
   - 分阶段完成，及时反馈
   - 展示优秀作品

3. **激励机制**
   - 设置学习积分系统
   - 定期表彰进步学生
   - 组织编程竞赛

4. **个性化指导**
   - 了解学生基础差异
   - 提供不同难度的练习
   - 一对一答疑时间

**课堂管理技巧：**
- 建立清晰的课堂规则
- 营造积极的学习氛围
- 及时处理学习困难

需要针对特定问题提供更详细的建议吗？"""

            elif any(keyword in lower_input for keyword in ['成绩分析', '学习效果', '数据分析']):
                return """📊 **成绩分析与改进建议**

**典型成绩分布分析：**

**优秀（90-100分）：15%**
- 特点：基础扎实，思维活跃
- 建议：提供挑战性项目，培养创新能力

**良好（80-89分）：35%**
- 特点：理解能力强，需要更多练习
- 建议：增加综合性题目，提升应用能力

**中等（70-79分）：35%**
- 特点：基础概念掌握，实践能力待提升
- 建议：加强编程练习，提供更多指导

**待提高（60-69分）：15%**
- 特点：基础薄弱，需要重点关注
- 建议：个别辅导，从基础概念重新梳理

**改进措施：**
1. 针对薄弱环节设计专项练习
2. 建立学习小组，互帮互助
3. 增加实践环节，理论结合实际
4. 定期测试，及时调整教学策略

需要我分析特定知识点的掌握情况吗？"""

            elif any(keyword in lower_input for keyword in ['你好', 'hello', 'hi', '您好']):
                return """👋 您好！我是您的AI教学助手。

我可以为您提供以下帮助：

📚 **课程设计** - 制定教学大纲、课程规划
📝 **题目生成** - 创建各类练习题、考试题
🎯 **教学建议** - 提供教学方法、课堂管理建议
📊 **成绩分析** - 分析学生表现，制定改进方案
📖 **资源推荐** - 推荐教学材料和参考资料

请告诉我您需要哪方面的帮助？"""

            else:
                teacher_responses = [
                    "作为您的教学助手，我需要更多具体信息才能提供准确的建议。请详细描述您遇到的教学问题或需求。",
                    "请告诉我您希望在课程设计、题目生成、教学方法还是成绩分析方面获得帮助？",
                    "我可以协助您解决各种教学相关问题。请具体说明您的需求，我会提供专业的建议。"
                ]
                import random
                return random.choice(teacher_responses)

        else:
            # 学生专用回复逻辑（原有逻辑）
            if any(keyword in lower_input for keyword in ['1+1', '1 + 1', '一加一']):
                return "1 + 1 = 2\n\n这是最基本的数学运算。如果你想了解更深入的数学概念，比如不同进制下的运算或者数学证明，我很乐意为你详细解释！"

            if any(keyword in lower_input for keyword in ['数学', '计算', '公式', '函数']):
                return "我来帮你解决数学问题！\n\n请告诉我具体是哪个知识点遇到了困难，比如函数与极限、导数与微分、积分计算、线性代数、概率统计等。我会为你提供详细的解答和练习建议。"

            elif any(keyword in lower_input for keyword in ['学习计划', '计划', '安排']):
                return "制定学习计划是个好习惯！\n\n我建议你可以这样安排：\n\n上午进行理论学习（2小时），下午做练习巩固（1.5小时），晚上复习总结（30分钟）。\n\n本周目标可以设定为完成2-3个章节的学习，每天练习10-15道题，并复习之前的错题。\n\n需要我为你制定更详细的个性化计划吗？"

            elif any(keyword in lower_input for keyword in ['练习', '题目', '作业']):
                return "我为你推荐一些练习题！\n\n根据你的学习情况，可以先从基础练习开始：函数极限计算、导数基本公式等。\n\n等基础练习的正确率达到80%后，再进行提高练习：复合函数求导、积分应用题等。\n\n需要我为你生成具体的题目吗？"

            elif any(keyword in lower_input for keyword in ['你好', 'hello', 'hi', '您好']):
                return "你好！我是你的AI学习助手小智。\n\n我可以帮助你解答学习问题、制定学习计划、推荐练习题目，还能为你分析学习进度。\n\n有什么可以帮助你的吗？"

            else:
                responses = [
                    "抱歉当前网络异常，请稍后重试"
                ]
                import random
                return random.choice(responses)

    async def delete_conversation(self, user_id: int, conversation_id: int) -> bool:
        """删除对话"""
        try:
            conversation = self.db.query(AIConversation).filter(
                AIConversation.id == conversation_id,
                AIConversation.user_id == user_id
            ).first()
            
            if not conversation:
                raise Exception("对话不存在或无权限访问")
            
            conversation.is_active = False
            self.db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"删除对话失败: {e}")
            self.db.rollback()
            raise Exception("删除对话失败")

    async def generate_questions(
        self,
        user_id: int,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        question_types: List[str],
        additional_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """AI生成题目功能"""
        try:
            ai_logger.info(f"🎯 开始生成题目 - 科目: {subject}, 主题: {topic}, 难度: {difficulty}, 数量: {question_count}")

            # 构建题目生成的提示词
            prompt = self._build_question_generation_prompt(
                subject, topic, difficulty, question_count, question_types, additional_requirements
            )

            # 调用AI API生成题目
            if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "your-deepseek-api-key-here":
                try:
                    result = await self._call_deepseek_for_questions(prompt)
                except Exception as e:
                    ai_logger.warning(f"AI API调用失败，回退到模拟数据: {e}")
                    result = self._generate_mock_questions(subject, topic, difficulty, question_count, question_types)
            else:
                ai_logger.info("未配置AI API密钥，使用模拟数据生成题目")
                result = self._generate_mock_questions(subject, topic, difficulty, question_count, question_types)

            # 标准化题目格式
            if "questions" in result:
                result["questions"] = self._normalize_question_format(result["questions"])

            ai_logger.info(f"✅ 题目生成完成，共生成 {len(result.get('questions', []))} 道题目")
            return result

        except Exception as e:
            ai_logger.error(f"❌ 题目生成失败: {e}")
            ai_logger.warning("回退到模拟数据生成")
            # 回退到模拟数据生成
            try:
                result = self._generate_mock_questions(subject, topic, difficulty, question_count, question_types)
                ai_logger.info(f"✅ 使用模拟数据生成完成，共生成 {len(result.get('questions', []))} 道题目")
                return result
            except Exception as mock_e:
                ai_logger.error(f"❌ 模拟数据生成也失败: {mock_e}")
                raise Exception(f"题目生成失败: {str(e)}")

    def _build_question_generation_prompt(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        question_types: List[str],
        additional_requirements: Optional[str] = None
    ) -> str:
        """构建题目生成的提示词"""

        difficulty_map = {
            "easy": "简单",
            "medium": "中等",
            "hard": "困难"
        }

        type_map = {
            "multiple_choice": "选择题",
            "fill_blank": "填空题",
            "essay": "问答题"
        }

        types_text = "、".join([type_map.get(t, t) for t in question_types])

        prompt = f"""你是一位专业的教育专家和题目设计师，请为以下要求生成高质量的练习题目：

**题目要求：**
- 科目：{subject}
- 主题：{topic}
- 难度：{difficulty_map.get(difficulty, difficulty)}
- 题目数量：{question_count}道
- 题目类型：{types_text}

**生成规则：**
1. 题目内容要准确、清晰、符合教学大纲
2. 难度要与要求匹配，循序渐进
3. 选择题需要4个选项，其中只有1个正确答案
4. 填空题要有明确的标准答案
5. 问答题要有详细的参考答案
6. 每道题目都要提供解析说明

**输出格式（严格按照JSON格式）：**
```json
{{
  "questions": [
    {{
      "question_text": "题目内容",
      "question_type": "multiple_choice/fill_blank/essay",
      "options": {{"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}},  // 仅选择题需要，必须是字典格式
      "correct_answer": "A",  // 选择题答案必须是字母A/B/C/D，填空题和问答题是具体内容
      "explanation": "题目解析",
      "points": 10,
      "difficulty": "easy/medium/hard"
    }}
  ]
}}
```

**重要说明：**
- 选择题的options必须是字典格式：{{"A": "选项内容", "B": "选项内容", ...}}
- 选择题的correct_answer必须是字母：A、B、C、D中的一个
- 填空题和问答题的correct_answer是具体的答案内容

**特殊要求：**
{additional_requirements if additional_requirements else "无特殊要求"}

请严格按照上述格式生成题目，确保JSON格式正确，可以直接解析。"""

        return prompt

    async def _call_deepseek_for_questions(self, prompt: str) -> Dict[str, Any]:
        """调用DeepSeek API生成题目"""
        ai_logger.info("🌐 调用DeepSeek API生成题目")

        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": "你是一位专业的教育专家和题目设计师，擅长生成高质量的教学题目。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7,
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload
                )

                if response.status_code != 200:
                    raise Exception(f"API请求失败: {response.status_code}")

                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # 解析JSON格式的题目
                import re

                # 提取JSON部分
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    # 如果没有代码块，尝试直接解析
                    json_str = content

                questions_data = json.loads(json_str)
                ai_logger.info(f"✅ 成功解析生成的题目数据")

                return questions_data

        except json.JSONDecodeError as e:
            ai_logger.error(f"❌ JSON解析失败: {e}")
            raise Exception("AI返回的题目格式错误，请重试")
        except Exception as e:
            ai_logger.error(f"❌ DeepSeek API调用失败: {e}")
            raise Exception(f"AI题目生成失败: {str(e)}")

    def _generate_mock_questions(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        question_types: List[str]
    ) -> Dict[str, Any]:
        """生成模拟题目（当API不可用时）"""
        ai_logger.info("🎭 生成模拟题目")

        questions = []

        # 模拟题目模板
        templates = {
            "数学": {
                "multiple_choice": [
                    {
                        "question_text": f"关于{topic}的基本概念，下列说法正确的是？",
                        "options": ["概念A是正确的", "概念B是正确的", "概念C是正确的", "概念D是正确的"],
                        "correct_answer": "概念A是正确的",
                        "explanation": f"根据{topic}的定义，概念A符合基本原理。"
                    }
                ],
                "fill_blank": [
                    {
                        "question_text": f"在{topic}中，当x趋向于0时，sin(x)/x的极限值是____。",
                        "correct_answer": "1",
                        "explanation": f"这是{topic}中的重要极限公式。"
                    }
                ],
                "essay": [
                    {
                        "question_text": f"请详细说明{topic}的基本原理和应用场景。",
                        "correct_answer": f"{topic}的基本原理包括定义、性质和应用方法。在实际应用中，{topic}广泛用于解决各种数学问题。",
                        "explanation": f"这道题考查对{topic}的深入理解和应用能力。"
                    }
                ]
            },
            "语文": {
                "multiple_choice": [
                    {
                        "question_text": f"关于{topic}的理解，下列表述正确的是？",
                        "options": ["表述A正确", "表述B正确", "表述C正确", "表述D正确"],
                        "correct_answer": "表述A正确",
                        "explanation": f"根据{topic}的文学特点，表述A最为准确。"
                    }
                ],
                "fill_blank": [
                    {
                        "question_text": f"在{topic}中，作者通过____的手法表达了深刻的主题。",
                        "correct_answer": "对比",
                        "explanation": f"作者在{topic}中运用对比手法突出主题。"
                    }
                ],
                "essay": [
                    {
                        "question_text": f"请分析{topic}的主要特点和文学价值。",
                        "correct_answer": f"{topic}具有独特的文学特色，体现了深刻的思想内涵和艺术价值。",
                        "explanation": f"这道题考查对{topic}的综合分析能力。"
                    }
                ]
            }
        }

        # 默认模板（当科目不在预设中时）
        default_templates = {
            "multiple_choice": [
                {
                    "question_text": f"关于{topic}，下列说法正确的是？",
                    "options": {"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
                    "correct_answer": "A",  # 使用字母格式
                    "explanation": f"根据{topic}的相关知识，选项A是正确的。"
                }
            ],
            "fill_blank": [
                {
                    "question_text": f"在{topic}中，重要概念是____。",
                    "correct_answer": "核心概念",
                    "explanation": f"这是{topic}中的核心概念。"
                }
            ],
            "essay": [
                {
                    "question_text": f"请阐述{topic}的重要性和应用。",
                    "correct_answer": f"{topic}在相关领域具有重要意义和广泛应用。",
                    "explanation": f"这道题考查对{topic}的理解和应用。"
                }
            ]
        }

        # 选择合适的模板
        subject_templates = templates.get(subject, default_templates)

        # 为每种题目类型生成题目
        for i in range(question_count):
            question_type = question_types[i % len(question_types)]

            if question_type in subject_templates:
                template = subject_templates[question_type][0]
                question = {
                    "question_text": template["question_text"],
                    "question_type": question_type,
                    "correct_answer": template["correct_answer"],
                    "explanation": template["explanation"],
                    "points": 10,
                    "difficulty": difficulty
                }

                if question_type == "multiple_choice":
                    question["options"] = template["options"]

                questions.append(question)

        return {"questions": questions}

    def _normalize_question_format(self, questions: List[Dict]) -> List[Dict]:
        """标准化题目格式，确保选择题使用正确的格式"""
        normalized_questions = []

        for question in questions:
            normalized_question = question.copy()

            # 处理选择题格式
            if question.get("question_type") == "multiple_choice":
                options = question.get("options")
                correct_answer = question.get("correct_answer")

                # 如果选项是数组格式，转换为字典格式
                if isinstance(options, list):
                    options_dict = {}
                    for i, option in enumerate(options):
                        letter = chr(65 + i)  # A, B, C, D
                        options_dict[letter] = option

                    normalized_question["options"] = options_dict

                    # 如果答案是完整选项内容，转换为字母
                    if correct_answer in options:
                        letter_index = options.index(correct_answer)
                        normalized_question["correct_answer"] = chr(65 + letter_index)

                # 如果选项已经是字典格式，检查答案格式
                elif isinstance(options, dict):
                    # 如果答案是完整选项内容，转换为字母
                    if correct_answer not in ["A", "B", "C", "D"]:
                        for letter, option_text in options.items():
                            if option_text == correct_answer:
                                normalized_question["correct_answer"] = letter
                                break

            normalized_questions.append(normalized_question)

        return normalized_questions

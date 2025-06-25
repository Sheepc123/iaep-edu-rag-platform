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
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
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
            
            # 添加欢迎消息
            welcome_message = AIMessage(
                conversation_id=conversation.id,
                content="你好！我是你的AI学习助手小智，我可以帮助你：\n\n📚 解答学习问题\n🎯 制定学习计划\n📊 分析学习进度\n💡 提供学习建议\n\n有什么可以帮助你的吗？",
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

            # 生成AI回复
            ai_logger.info(f"🤖 开始生成AI回复")
            ai_logger.info(f"📝 输入内容: {message_data.content}")
            ai_response = await self._generate_ai_response(
                message_data.content,
                conversation.id,
                message_data.context
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
        context: Optional[Dict[str, Any]] = None
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
                result = await self._call_deepseek_api(user_input, conversation_id, context)
                ai_logger.info("✅ DeepSeek API调用成功")
                return result
            except Exception as e:
                ai_logger.error(f"❌ DeepSeek API调用失败，使用模拟回复: {e}")

        # 否则使用模拟回复
        ai_logger.info("🎭 使用模拟回复")
        await asyncio.sleep(1.0)  # 模拟API调用延迟
        response_content = self._generate_mock_response(user_input)
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
        context: Optional[Dict[str, Any]] = None
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
        messages = [{"role": "system", "content": self.system_prompt}]
        ai_logger.info(f"✅ 添加系统提示: {self.system_prompt[:50]}...")

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

    def _generate_mock_response(self, user_input: str) -> str:
        """生成模拟AI回复"""
        lower_input = user_input.lower()

        # 简单的数学问题处理
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

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  User,
  Send,
  Sparkles,
  Copy,
  ThumbsUp,
  ThumbsDown,
  RefreshCw,
  BookOpen,
  Calculator,
  Lightbulb,
  Target,
  MessageCircle,
  History,
  Trash2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import StudentLayout from "@/components/layouts/StudentLayout";
import { useAI, Message } from "@/contexts/AIContext";

export const AIAssistant = () => {
  const {
    conversations,
    currentConversationId,
    currentMessages: messages,
    isTyping,
    setIsTyping,
    addMessage,
    createNewConversation,
    switchConversation,
    deleteConversation
  } = useAI();

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到最新消息
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);



  // 发送消息
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    addMessage(userMessage);
    const userInput = inputValue;
    setInputValue('');
    setIsTyping(true);

    // 模拟AI回复
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: generateAIResponse(userInput),
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      };

      addMessage(aiMessage);
      setIsTyping(false);
    }, 1500);
  };

  // 模拟AI回复生成
  const generateAIResponse = (userInput: string): string => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('数学') || lowerInput.includes('计算')) {
      return "我来帮你解决数学问题！请告诉我具体是哪个知识点遇到了困难，比如：\n\n• 函数与极限\n• 导数与微分\n• 积分计算\n• 线性代数\n• 概率统计\n\n我会为你提供详细的解答和练习建议。";
    }
    
    if (lowerInput.includes('学习计划') || lowerInput.includes('计划')) {
      return "制定学习计划是个好习惯！根据你的学习进度，我建议：\n\n📅 **本周目标**\n• 完成2-3个章节的学习\n• 每天练习10-15道题\n• 复习之前的错题\n\n⏰ **时间安排**\n• 上午：理论学习（2小时）\n• 下午：练习巩固（1.5小时）\n• 晚上：复习总结（30分钟）\n\n需要我为你制定更详细的计划吗？";
    }
    
    if (lowerInput.includes('练习') || lowerInput.includes('题目')) {
      return "我为你推荐一些练习题！根据你的学习情况：\n\n🎯 **基础练习**\n• 函数极限计算 - 10题\n• 导数基本公式 - 8题\n\n🔥 **提高练习**\n• 复合函数求导 - 6题\n• 积分应用题 - 5题\n\n📊 **建议**\n先完成基础练习，正确率达到80%后再进行提高练习。需要我为你生成具体的题目吗？";
    }
    
    const responses = [
      "这是一个很好的问题！让我来帮你分析一下...\n\n根据你的学习情况，我建议你可以从以下几个方面入手：\n\n1. 先理解基本概念\n2. 多做相关练习\n3. 总结解题方法\n\n需要我详细解释某个步骤吗？",
      "我理解你的困惑！这个知识点确实需要仔细理解。\n\n让我用更简单的方式来解释：\n\n💡 **核心思路**\n把复杂问题分解成简单步骤\n\n📝 **解题步骤**\n1. 分析题目条件\n2. 选择合适方法\n3. 逐步计算求解\n\n你想从哪个步骤开始练习？",
      "基于你之前的学习记录，我发现你在这个领域有很好的基础！\n\n🌟 **你的优势**\n• 基础概念掌握扎实\n• 计算能力较强\n\n📈 **提升建议**\n• 多练习综合应用题\n• 加强解题速度训练\n• 学习更多解题技巧\n\n要不要我为你推荐一些进阶练习？"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  // 快捷功能
  const quickActions = [
    { icon: <BookOpen className="w-4 h-4" />, label: "学习指导", action: "请为我制定今天的学习计划" },
    { icon: <Calculator className="w-4 h-4" />, label: "解题帮助", action: "我在数学题目上遇到了困难，需要帮助" },
    { icon: <Target className="w-4 h-4" />, label: "练习推荐", action: "请为我推荐一些适合的练习题" },
    { icon: <Lightbulb className="w-4 h-4" />, label: "学习建议", action: "根据我的学习情况给出建议" }
  ];

  // 复制消息内容
  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
    // 这里可以添加一个toast提示
  };

  return (
    <StudentLayout>
      <div className="h-[calc(100vh-1rem)] flex bg-white rounded-2xl shadow-lg overflow-hidden">
        {/* 左侧对话历史 */}
        <div className="w-72 bg-gray-50 border-r border-gray-200 flex flex-col">
          {/* 头部 */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-900 flex items-center">
                <History className="w-5 h-5 mr-2 text-purple-600" />
                对话记录
              </h2>
              <Button
                onClick={createNewConversation}
                size="sm"
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                <MessageCircle className="w-4 h-4 mr-1" />
                新对话
              </Button>
            </div>
          </div>

          {/* 对话列表 */}
          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {conversations.map((conversation) => (
              <motion.div
                key={conversation.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`p-3 rounded-lg cursor-pointer transition-all duration-200 group ${
                  currentConversationId === conversation.id
                    ? 'bg-gradient-to-r from-purple-100 to-blue-100 border border-purple-200'
                    : 'bg-white hover:bg-gray-100 border border-gray-100'
                }`}
                onClick={() => switchConversation(conversation.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium text-gray-900 truncate">
                      {conversation.title}
                    </h4>
                    <p className="text-xs text-gray-500 mt-1">
                      {conversation.lastUpdated.toLocaleDateString()}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {conversation.messages.length} 条消息
                    </p>
                  </div>
                  {conversations.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteConversation(conversation.id);
                      }}
                      className="opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 p-0 text-gray-400 hover:text-red-500"
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* 右侧聊天界面 */}
        <div className="flex-1 flex flex-col">
          {/* 聊天头部 */}
          <div className="flex items-center justify-between p-6 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white">
            <div className="flex items-center space-x-4">
              <motion.div
                className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center"
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              >
                <Bot className="w-7 h-7" />
              </motion.div>
              <div>
                <h2 className="text-xl font-bold">AI学习助手 - 小智</h2>
                <p className="text-blue-100 text-sm flex items-center">
                  <Sparkles className="w-3 h-3 mr-1" />
                  智能学习，个性化辅导
                </p>
              </div>
            </div>
            <Badge className="bg-white/20 text-white border-white/30 px-3 py-1">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse" />
              在线服务
            </Badge>
          </div>

          {/* 消息区域 */}
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-gray-50 to-white">
              {messages.map((message, index) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[75%] ${message.sender === 'user' ? 'order-2' : 'order-1'}`}>
                    <div
                      className={`relative p-4 rounded-2xl shadow-sm ${
                        message.sender === 'user'
                          ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white ml-4'
                          : 'bg-white text-gray-800 border border-gray-100 mr-4'
                      }`}
                    >
                      <div className="whitespace-pre-line text-sm leading-relaxed">
                        {message.content}
                      </div>

                      {/* AI消息的操作按钮 */}
                      {message.sender === 'ai' && (
                        <div className="flex items-center justify-end space-x-2 mt-3 pt-3 border-t border-gray-100">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => copyMessage(message.content)}
                            className="h-6 px-2 text-xs text-gray-500 hover:text-gray-700"
                          >
                            <Copy className="w-3 h-3 mr-1" />
                            复制
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 px-2 text-xs text-gray-500 hover:text-green-600"
                          >
                            <ThumbsUp className="w-3 h-3" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 px-2 text-xs text-gray-500 hover:text-red-600"
                          >
                            <ThumbsDown className="w-3 h-3" />
                          </Button>
                        </div>
                      )}
                    </div>
                    <p className="text-xs text-gray-400 mt-2 px-2">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>

                  {/* 头像 */}
                  {message.sender === 'ai' ? (
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mr-3 order-0 flex-shrink-0 shadow-md">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                  ) : (
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center ml-3 order-3 flex-shrink-0">
                      <User className="w-5 h-5 text-gray-600" />
                    </div>
                  )}
                </motion.div>
              ))}

              {/* 正在输入指示器 */}
              {isTyping && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start"
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center shadow-md">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div className="bg-white border border-gray-100 p-4 rounded-2xl shadow-sm">
                      <div className="flex space-x-1">
                        {[0, 1, 2].map((i) => (
                          <motion.div
                            key={i}
                            className="w-2 h-2 bg-gray-400 rounded-full"
                            animate={{ scale: [1, 1.3, 1], opacity: [0.5, 1, 0.5] }}
                            transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.2 }}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* 快捷操作 */}
            {messages.length === 1 && (
              <div className="px-6 py-3 bg-gray-50 border-t">
                <p className="text-xs text-gray-600 mb-2 font-medium">快速开始：</p>
                <div className="grid grid-cols-4 gap-2">
                  {quickActions.map((action, index) => (
                    <motion.button
                      key={index}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.1 }}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setInputValue(action.action)}
                      className="flex flex-col items-center space-y-1 p-2 bg-white hover:bg-blue-50 rounded-lg border border-gray-100 hover:border-blue-200 text-center transition-all duration-200"
                    >
                      <div className="p-1.5 bg-blue-100 rounded-md text-blue-600">
                        {action.icon}
                      </div>
                      <span className="text-xs font-medium text-gray-700">{action.label}</span>
                    </motion.button>
                  ))}
                </div>
              </div>
            )}

            {/* 输入区域 */}
            <div className="p-6 bg-white border-t">
              <div className="flex items-end space-x-3">
                <div className="flex-1 relative">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                      }
                    }}
                    placeholder="输入你的问题... (Shift+Enter 换行)"
                    className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none min-h-[44px] max-h-32"
                    disabled={isTyping}
                    rows={1}
                  />
                </div>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isTyping}
                  className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-2xl flex items-center justify-center text-white transition-all duration-200 shadow-lg"
                >
                  <Send className="w-5 h-5" />
                </motion.button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </StudentLayout>
  );
};

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, X, Send, History, Plus, MessageCircle, Trash2, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface ChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
  messageCount: number;
}

export const SimpleAIButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'chat' | 'history'>('chat');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: '你好！我是你的AI学习助手小智，我可以帮助你：\n\n📚 解答学习问题\n🎯 制定学习计划\n📊 分析学习进度\n💡 提供学习建议\n\n有什么可以帮助你的吗？',
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 模拟历史会话数据
  const [chatHistory] = useState<ChatSession[]>([
    {
      id: '1',
      title: '数学学习计划制定',
      lastMessage: '建议你每天完成2-3个章节的学习...',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2小时前
      messageCount: 12
    },
    {
      id: '2',
      title: '函数极限问题解答',
      lastMessage: '这个极限可以通过洛必达法则来求解...',
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1天前
      messageCount: 8
    },
    {
      id: '3',
      title: '线性代数练习推荐',
      lastMessage: '我为你推荐以下矩阵运算练习题...',
      timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3天前
      messageCount: 15
    },
    {
      id: '4',
      title: '概率论学习方法',
      lastMessage: '概率论的学习重点在于理解概念...',
      timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 1周前
      messageCount: 6
    }
  ]);

  const handleOpenChat = () => {
    console.log('Opening AI chat...');
    setIsOpen(true);
  };

  const handleCloseChat = () => {
    console.log('Closing AI chat...');
    setIsOpen(false);
    setActiveTab('chat');
  };

  // 自动滚动到最新消息
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 发送消息
  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // 模拟AI回复
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: generateAIResponse(inputValue),
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
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

    const responses = [
      "这是一个很好的问题！让我来帮你分析一下...\n\n根据你的学习情况，我建议你可以从以下几个方面入手：\n\n1. 先理解基本概念\n2. 多做相关练习\n3. 总结解题方法\n\n需要我详细解释某个步骤吗？",
      "我理解你的困惑！这个知识点确实需要仔细理解。\n\n让我用更简单的方式来解释：\n\n💡 **核心思路**\n把复杂问题分解成简单步骤\n\n📝 **解题步骤**\n1. 分析题目条件\n2. 选择合适方法\n3. 逐步计算求解\n\n你想从哪个步骤开始练习？",
      "基于你之前的学习记录，我发现你在这个领域有很好的基础！\n\n🌟 **你的优势**\n• 基础概念掌握扎实\n• 计算能力较强\n\n📈 **提升建议**\n• 多练习综合应用题\n• 加强解题速度训练\n• 学习更多解题技巧\n\n要不要我为你推荐一些进阶练习？"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  // 格式化时间
  const formatTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);

    if (hours < 1) return '刚刚';
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;
    return date.toLocaleDateString();
  };

  return (
    <>
      {/* 简单的浮动按钮 */}
      <div className="fixed bottom-6 right-6 z-40">
        <Button
          onClick={handleOpenChat}
          className="w-16 h-16 rounded-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-lg hover:shadow-xl transition-all duration-300"
        >
          <Bot className="w-8 h-8 text-white" />
        </Button>
      </div>

      {/* AI对话界面 - 增大显示 */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={handleCloseChat}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0, y: 50 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.8, opacity: 0, y: 50 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="w-full max-w-6xl h-[90vh] bg-white rounded-2xl shadow-2xl overflow-hidden flex"
              onClick={(e) => e.stopPropagation()}
            >
              {/* 左侧边栏 - 历史会话 */}
              <div className="w-80 bg-gray-50 border-r border-gray-200 flex flex-col">
                {/* 侧边栏头部 */}
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-900">AI助手</h3>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleCloseChat}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>

                  {/* 标签切换 */}
                  <div className="flex bg-gray-200 rounded-lg p-1">
                    <button
                      onClick={() => setActiveTab('chat')}
                      className={`flex-1 flex items-center justify-center space-x-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                        activeTab === 'chat'
                          ? 'bg-white text-purple-600 shadow-sm'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <MessageCircle className="w-4 h-4" />
                      <span>对话</span>
                    </button>
                    <button
                      onClick={() => setActiveTab('history')}
                      className={`flex-1 flex items-center justify-center space-x-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                        activeTab === 'history'
                          ? 'bg-white text-purple-600 shadow-sm'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <History className="w-4 h-4" />
                      <span>历史</span>
                    </button>
                  </div>
                </div>

                {/* 侧边栏内容 */}
                <div className="flex-1 overflow-y-auto">
                  {activeTab === 'chat' && (
                    <div className="p-4">
                      <Button
                        className="w-full mb-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                        onClick={() => {
                          setMessages([{
                            id: '1',
                            content: '你好！我是你的AI学习助手小智，我可以帮助你：\n\n📚 解答学习问题\n🎯 制定学习计划\n📊 分析学习进度\n💡 提供学习建议\n\n有什么可以帮助你的吗？',
                            sender: 'ai',
                            timestamp: new Date()
                          }]);
                        }}
                      >
                        <Plus className="w-4 h-4 mr-2" />
                        新建对话
                      </Button>

                      <div className="space-y-2">
                        <h4 className="text-sm font-medium text-gray-700 mb-3">快速开始</h4>
                        {[
                          "如何提高数学成绩？",
                          "制定学习计划",
                          "推荐练习题",
                          "解答疑难问题"
                        ].map((question, index) => (
                          <button
                            key={index}
                            onClick={() => setInputValue(question)}
                            className="w-full text-left p-3 bg-white rounded-lg border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-colors text-sm"
                          >
                            {question}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {activeTab === 'history' && (
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-4">
                        <h4 className="text-sm font-medium text-gray-700">历史会话</h4>
                        <Button variant="ghost" size="sm" className="text-gray-500 hover:text-red-600">
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>

                      <div className="space-y-3">
                        {chatHistory.map((session) => (
                          <motion.div
                            key={session.id}
                            whileHover={{ scale: 1.02 }}
                            className="p-3 bg-white rounded-lg border border-gray-200 hover:border-purple-300 hover:shadow-sm transition-all cursor-pointer"
                          >
                            <div className="flex items-start justify-between mb-2">
                              <h5 className="font-medium text-gray-900 text-sm line-clamp-1">
                                {session.title}
                              </h5>
                              <Badge variant="secondary" className="text-xs">
                                {session.messageCount}
                              </Badge>
                            </div>
                            <p className="text-xs text-gray-600 line-clamp-2 mb-2">
                              {session.lastMessage}
                            </p>
                            <div className="flex items-center text-xs text-gray-400">
                              <Clock className="w-3 h-3 mr-1" />
                              {formatTime(session.timestamp)}
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* 右侧主要对话区域 */}
              <div className="flex-1 flex flex-col">
                {/* 对话头部 */}
                <div className="p-6 bg-gradient-to-r from-purple-600 to-blue-600 text-white">
                  <div className="flex items-center space-x-3">
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
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse" />
                        在线服务中，随时为你答疑解惑
                      </p>
                    </div>
                  </div>
                </div>

                {/* 消息显示区域 */}
                <div className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-gray-50 to-white">
                  <div className="space-y-6 max-w-4xl mx-auto">
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
                            <div className="w-6 h-6 bg-gray-400 rounded-full"></div>
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
                </div>

                {/* 输入区域 */}
                <div className="p-6 bg-white border-t border-gray-200">
                  <div className="max-w-4xl mx-auto">
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

                    {/* 输入提示 */}
                    <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
                      <span>AI助手会根据你的学习情况提供个性化建议</span>
                      <span>{inputValue.length}/500</span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

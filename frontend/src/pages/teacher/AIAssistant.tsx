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

  MessageCircle,
  History,
  Trash2,
  Users,
  ClipboardList,
  BarChart3
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

import TeacherLayout from "@/components/layouts/TeacherLayout";
import { useAI } from "@/contexts/AIContext";

export const TeacherAIAssistant = () => {
  const {
    conversations,
    currentConversationId,
    currentMessages: messages,
    isTyping,

    createNewConversation,
    switchConversation,
    deleteConversation,
    sendMessageToAPI
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

    const userInput = inputValue;
    setInputValue('');

    // 使用API发送消息
    await sendMessageToAPI(userInput, currentConversationId);
  };



  // 教师专用快捷功能
  const quickActions = [
    { icon: <BookOpen className="w-4 h-4" />, label: "课程设计", action: "请帮我设计一个关于数据结构的课程大纲" },
    { icon: <ClipboardList className="w-4 h-4" />, label: "题目生成", action: "请为我生成一些关于算法的练习题" },
    { icon: <Users className="w-4 h-4" />, label: "教学建议", action: "如何提高学生的学习积极性？" },
    { icon: <BarChart3 className="w-4 h-4" />, label: "成绩分析", action: "请分析学生成绩分布并给出改进建议" }
  ];

  // 复制消息内容
  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
    // 这里可以添加一个toast提示
  };

  return (
    <TeacherLayout>
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
                      onClick={async (e) => {
                        e.stopPropagation();
                        try {
                          await deleteConversation(conversation.id);
                        } catch (error) {
                          console.error('删除对话失败:', error);
                          // 可以添加用户提示
                        }
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
                <h2 className="text-xl font-bold">AI教学助手</h2>
                <p className="text-blue-100 text-sm flex items-center">
                  <Sparkles className="w-3 h-3 mr-1" />
                  专为教师设计的智能助手
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
    </TeacherLayout>
  );
};

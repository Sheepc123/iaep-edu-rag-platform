import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  User,
  Send,
  Sparkles,
  Copy,
  ThumbsUp,
  MessageSquare,
  Plus,
  Minimize2,
  Maximize2,
  X,
  BookOpen,
  Calculator,
  Lightbulb,
  Target
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAI } from "@/contexts/AIContext";

interface DraggableAIChatProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DraggableAIChat = ({ isOpen, onClose }: DraggableAIChatProps) => {
  const {
    currentMessages: messages,
    conversations,
    isTyping,
    sendMessageToAPI,
    currentConversationId,
    switchConversation
  } = useAI();

  const [inputValue, setInputValue] = useState('');
  const [showConversations, setShowConversations] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [position, setPosition] = useState({ x: 100, y: 100 });
  const [size, setSize] = useState({ width: 384, height: 600 }); // 默认大小
  const [isResizing, setIsResizing] = useState(false);
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
    await sendMessageToAPI(userInput, currentConversationId);
  };

  // 拖拽处理
  const handleDragEnd = (event: any, info: any) => {
    setPosition(prev => ({
      x: prev.x + info.offset.x,
      y: prev.y + info.offset.y
    }));
  };

  // 调整大小处理
  const handleResize = (direction: string, deltaX: number, deltaY: number) => {
    setSize(prev => {
      let newWidth = prev.width;
      let newHeight = prev.height;
      let newX = position.x;
      let newY = position.y;

      // 最小和最大尺寸限制
      const minWidth = 300;
      const minHeight = 400;
      const maxWidth = window.innerWidth - 50;
      const maxHeight = window.innerHeight - 50;

      switch (direction) {
        case 'right':
          newWidth = Math.max(minWidth, Math.min(maxWidth, prev.width + deltaX));
          break;
        case 'bottom':
          newHeight = Math.max(minHeight, Math.min(maxHeight, prev.height + deltaY));
          break;
        case 'left':
          newWidth = Math.max(minWidth, Math.min(maxWidth, prev.width - deltaX));
          if (newWidth !== prev.width) {
            newX = position.x + deltaX;
            setPosition(p => ({ ...p, x: newX }));
          }
          break;
        case 'top':
          newHeight = Math.max(minHeight, Math.min(maxHeight, prev.height - deltaY));
          if (newHeight !== prev.height) {
            newY = position.y + deltaY;
            setPosition(p => ({ ...p, y: newY }));
          }
          break;
        case 'bottom-right':
          newWidth = Math.max(minWidth, Math.min(maxWidth, prev.width + deltaX));
          newHeight = Math.max(minHeight, Math.min(maxHeight, prev.height + deltaY));
          break;
        case 'bottom-left':
          newWidth = Math.max(minWidth, Math.min(maxWidth, prev.width - deltaX));
          newHeight = Math.max(minHeight, Math.min(maxHeight, prev.height + deltaY));
          if (newWidth !== prev.width) {
            newX = position.x + deltaX;
            setPosition(p => ({ ...p, x: newX }));
          }
          break;
        case 'top-right':
          newWidth = Math.max(minWidth, Math.min(maxWidth, prev.width + deltaX));
          newHeight = Math.max(minHeight, Math.min(maxHeight, prev.height - deltaY));
          if (newHeight !== prev.height) {
            newY = position.y + deltaY;
            setPosition(p => ({ ...p, y: newY }));
          }
          break;
        case 'top-left':
          newWidth = Math.max(minWidth, Math.min(maxWidth, prev.width - deltaX));
          newHeight = Math.max(minHeight, Math.min(maxHeight, prev.height - deltaY));
          if (newWidth !== prev.width) {
            newX = position.x + deltaX;
          }
          if (newHeight !== prev.height) {
            newY = position.y + deltaY;
          }
          if (newWidth !== prev.width || newHeight !== prev.height) {
            setPosition({ x: newX, y: newY });
          }
          break;
      }

      return { width: newWidth, height: newHeight };
    });
  };

  // 切换对话
  const handleSwitchConversation = async (conversationId: string) => {
    await switchConversation(conversationId);
    setShowConversations(false);
  };

  // 快捷功能
  const quickActions = [
    { icon: <BookOpen className="w-3 h-3" />, label: "学习指导", action: "请为我制定今天的学习计划" },
    { icon: <Calculator className="w-3 h-3" />, label: "解题帮助", action: "我在数学题目上遇到了困难，需要帮助" }
  ];

  // 复制消息内容
  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          drag
          dragMomentum={false}
          onDragEnd={handleDragEnd}
          initial={{
            opacity: 0,
            scale: 0.8,
            x: 100,
            y: 100
          }}
          animate={{
            opacity: 1,
            scale: 1,
            x: position.x + 100,
            y: position.y + 100
          }}
          exit={{ opacity: 0, scale: 0.8 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          className={`fixed z-50 bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col border border-gray-200 ${isResizing ? 'select-none' : ''}`}
          style={{
            width: isMinimized ? '320px' : `${size.width}px`,
            height: isMinimized ? '64px' : `${size.height}px`,
            cursor: isResizing ? 'grabbing' : 'default'
          }}
        >
          {/* 头部 - 可拖拽区域 */}
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white cursor-move">
            <div className="flex items-center space-x-3">
              <motion.div 
                className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center"
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              >
                <Bot className="w-4 h-4" />
              </motion.div>
              <div>
                <h2 className="text-sm font-bold">AI学习助手</h2>
                {!isMinimized && (
                  <p className="text-blue-100 text-xs flex items-center">
                    <Sparkles className="w-2 h-2 mr-1" />
                    智能学习助手
                  </p>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {!isMinimized && (
                <>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowConversations(!showConversations)}
                    className="text-white hover:bg-white/20 rounded-full w-6 h-6 p-0"
                  >
                    <MessageSquare className="w-3 h-3" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowConversations(false)}
                    className="text-white hover:bg-white/20 rounded-full w-6 h-6 p-0"
                  >
                    <Plus className="w-3 h-3" />
                  </Button>
                </>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMinimized(!isMinimized)}
                className="text-white hover:bg-white/20 rounded-full w-6 h-6 p-0"
              >
                {isMinimized ? <Maximize2 className="w-3 h-3" /> : <Minimize2 className="w-3 h-3" />}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="text-white hover:bg-white/20 rounded-full w-6 h-6 p-0"
              >
                <X className="w-3 h-3" />
              </Button>
            </div>
          </div>

          {!isMinimized && (
            <>
              {/* 对话列表侧边栏 */}
              {showConversations && (
                <div className="w-full h-48 bg-gray-50 border-b overflow-y-auto">
                  <div className="p-3">
                    <h3 className="text-sm font-medium text-gray-700 mb-2">对话历史</h3>
                    <div className="space-y-1">
                      {conversations.map((conversation) => (
                        <button
                          key={conversation.id}
                          onClick={() => handleSwitchConversation(conversation.id)}
                          className={`w-full text-left p-2 rounded-lg text-xs hover:bg-gray-100 transition-colors ${
                            conversation.id === currentConversationId ? 'bg-blue-100 text-blue-700' : 'text-gray-600'
                          }`}
                        >
                          <div className="truncate font-medium">{conversation.title}</div>
                          <div className="text-gray-400 text-xs">
                            {new Date(conversation.lastUpdated).toLocaleDateString()}
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* 消息区域 */}
              <div className="flex-1 flex flex-col overflow-hidden">
                <div className="flex-1 overflow-y-auto p-3 space-y-3 bg-gradient-to-b from-gray-50 to-white">
                  {messages.map((message, index) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[85%] ${message.sender === 'user' ? 'order-2' : 'order-1'}`}>
                        <div
                          className={`relative p-3 rounded-xl shadow-sm ${
                            message.sender === 'user'
                              ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white ml-2'
                              : 'bg-white text-gray-800 border border-gray-100 mr-2'
                          }`}
                        >
                          <div className="whitespace-pre-line text-xs leading-relaxed">
                            {message.content}
                          </div>
                          
                          {/* AI消息的操作按钮 */}
                          {message.sender === 'ai' && (
                            <div className="flex items-center justify-end space-x-1 mt-2 pt-2 border-t border-gray-100">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => copyMessage(message.content)}
                                className="h-5 px-1 text-xs text-gray-500 hover:text-gray-700"
                              >
                                <Copy className="w-2 h-2 mr-1" />
                                复制
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-5 px-1 text-xs text-gray-500 hover:text-green-600"
                              >
                                <ThumbsUp className="w-2 h-2" />
                              </Button>
                            </div>
                          )}
                        </div>
                        <p className="text-xs text-gray-400 mt-1 px-1">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                      
                      {/* 头像 */}
                      {message.sender === 'ai' ? (
                        <div className="w-6 h-6 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mr-2 order-0 flex-shrink-0 shadow-sm">
                          <Bot className="w-3 h-3 text-white" />
                        </div>
                      ) : (
                        <div className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center ml-2 order-3 flex-shrink-0">
                          <User className="w-3 h-3 text-gray-600" />
                        </div>
                      )}
                    </motion.div>
                  ))}
                  
                  {/* 正在输入指示器 */}
                  {isTyping && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex justify-start"
                    >
                      <div className="flex items-start space-x-2">
                        <div className="w-6 h-6 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center shadow-sm">
                          <Bot className="w-3 h-3 text-white" />
                        </div>
                        <div className="bg-white border border-gray-100 p-2 rounded-xl shadow-sm">
                          <div className="flex space-x-1">
                            {[0, 1, 2].map((i) => (
                              <motion.div
                                key={i}
                                className="w-1 h-1 bg-gray-400 rounded-full"
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
                {messages.length <= 1 && (
                  <div className="px-3 py-2 bg-gray-50 border-t">
                    <p className="text-xs text-gray-600 mb-2 font-medium">快速开始：</p>
                    <div className="grid grid-cols-1 gap-2">
                      {quickActions.map((action, index) => (
                        <motion.button
                          key={index}
                          onClick={() => setInputValue(action.action)}
                          className="flex items-center space-x-2 p-2 bg-white hover:bg-blue-50 rounded-lg border border-gray-100 text-left transition-all duration-200"
                        >
                          <div className="p-1 bg-blue-100 rounded-md text-blue-600">
                            {action.icon}
                          </div>
                          <span className="text-xs font-medium text-gray-700">{action.label}</span>
                        </motion.button>
                      ))}
                    </div>
                  </div>
                )}

                {/* 输入区域 */}
                <div className="p-3 bg-white border-t">
                  <div className="flex items-end space-x-2">
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
                        placeholder="输入你的问题..."
                        className="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none min-h-[32px] max-h-20 text-sm"
                        disabled={isTyping}
                        rows={1}
                      />
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleSendMessage}
                      disabled={!inputValue.trim() || isTyping}
                      className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl flex items-center justify-center text-white transition-all duration-200 shadow-lg"
                    >
                      <Send className="w-3 h-3" />
                    </motion.button>
                  </div>
                </div>
              </div>
            </>
          )}

          {/* 调整大小控制点 */}
          {!isMinimized && (
            <>
              {/* 边缘调整点 */}
              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('right', info.delta.x, 0)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute top-0 right-0 w-1 h-full cursor-ew-resize bg-transparent hover:bg-blue-500/20 transition-colors"
                style={{ right: '-2px' }}
              />

              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('bottom', 0, info.delta.y)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute bottom-0 left-0 w-full h-1 cursor-ns-resize bg-transparent hover:bg-blue-500/20 transition-colors"
                style={{ bottom: '-2px' }}
              />

              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('left', info.delta.x, 0)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute top-0 left-0 w-1 h-full cursor-ew-resize bg-transparent hover:bg-blue-500/20 transition-colors"
                style={{ left: '-2px' }}
              />

              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('top', 0, info.delta.y)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute top-0 left-0 w-full h-1 cursor-ns-resize bg-transparent hover:bg-blue-500/20 transition-colors"
                style={{ top: '-2px' }}
              />

              {/* 角落调整点 */}
              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('bottom-right', info.delta.x, info.delta.y)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute bottom-0 right-0 w-4 h-4 cursor-nw-resize bg-transparent hover:bg-blue-500/30 transition-colors"
                style={{ bottom: '-2px', right: '-2px' }}
              />

              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('bottom-left', info.delta.x, info.delta.y)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute bottom-0 left-0 w-4 h-4 cursor-ne-resize bg-transparent hover:bg-blue-500/30 transition-colors"
                style={{ bottom: '-2px', left: '-2px' }}
              />

              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('top-right', info.delta.x, info.delta.y)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute top-0 right-0 w-4 h-4 cursor-ne-resize bg-transparent hover:bg-blue-500/30 transition-colors"
                style={{ top: '-2px', right: '-2px' }}
              />

              <motion.div
                drag
                dragMomentum={false}
                onDrag={(e, info) => handleResize('top-left', info.delta.x, info.delta.y)}
                onDragStart={() => setIsResizing(true)}
                onDragEnd={() => setIsResizing(false)}
                className="absolute top-0 left-0 w-4 h-4 cursor-nw-resize bg-transparent hover:bg-blue-500/30 transition-colors"
                style={{ top: '-2px', left: '-2px' }}
              />
            </>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
};

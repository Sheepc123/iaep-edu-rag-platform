import { useState } from "react";
import { motion, PanInfo } from "framer-motion";
import { Bot, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DraggableAIChat } from "./DraggableAIChat";

export const FloatingAIButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  // 处理拖拽
  const handleDrag = (event: any, info: PanInfo) => {
    setPosition({ x: info.offset.x, y: info.offset.y });
  };

  // 处理AI按钮点击 - 独立的点击区域
  const handleAIClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('🎯 AI Button clicked!', { isOpen, timestamp: new Date().toLocaleTimeString() }); // 调试日志
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* 浮动按钮 - 简化版本 */}
      <div className="fixed bottom-6 right-6 z-40">
        {/* 拖拽区域 */}
        <motion.div
          drag
          dragConstraints={{ left: -300, right: 300, top: -300, bottom: 300 }}
          dragElastic={0.1}
          onDrag={handleDrag}
          className="w-20 h-20 rounded-full bg-gradient-to-r from-purple-600/20 via-blue-600/20 to-indigo-600/20 flex items-center justify-center cursor-move"
          style={{ x: position.x, y: position.y }}
          onHoverStart={() => setIsHovered(true)}
          onHoverEnd={() => setIsHovered(false)}
        >
          {/* 点击按钮 - 完全独立 */}
          <button
            onClick={handleAIClick}
            className="w-14 h-14 rounded-full bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 hover:from-purple-700 hover:via-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-2xl transition-all duration-300 border-0 relative overflow-hidden flex items-center justify-center cursor-pointer"
            style={{ pointerEvents: 'auto' }}
          >
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
            >
              <Bot className="w-6 h-6 text-white" />
            </motion.div>

            {/* 内部光效 */}
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent"
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            />
          </button>

          {/* 外部呼吸光效 */}
          <motion.div
            className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 opacity-30 pointer-events-none"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.3, 0.1, 0.3],
            }}
            transition={{
              duration: 2.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />

          {/* 脉冲效果 */}
          <motion.div
            className="absolute inset-0 rounded-full border-2 border-purple-400 pointer-events-none"
            animate={{
              scale: [1, 1.5, 2],
              opacity: [0.8, 0.3, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeOut"
            }}
          />
        </motion.div>
      </div>

      {/* 悬浮提示 */}
      {isHovered && (
        <motion.div
          initial={{ opacity: 0, x: 10, scale: 0.8 }}
          animate={{ opacity: 1, x: -10, scale: 1 }}
          className="absolute right-full top-1/2 transform -translate-y-1/2 mr-4 pointer-events-none"
        >
          <div className="bg-gray-900 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap shadow-lg">
            <div className="flex flex-col space-y-1">
              <div className="flex items-center space-x-2">
                <Bot className="w-3 h-3" />
                <span>点击中心打开AI助手</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-gray-300">
                <MessageCircle className="w-3 h-3" />
                <span>拖拽外圈移动位置</span>
              </div>
            </div>
            <div className="absolute left-full top-1/2 transform -translate-y-1/2">
              <div className="w-0 h-0 border-l-4 border-l-gray-900 border-t-4 border-t-transparent border-b-4 border-b-transparent"></div>
            </div>
          </div>
        </motion.div>
      )}

      {/* AI对话界面 */}
      <DraggableAIChat isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
};

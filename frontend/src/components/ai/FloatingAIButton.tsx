import { useState, useRef } from "react";
import { motion, PanInfo } from "framer-motion";
import { Bot, MessageCircle, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { AIChat } from "./AIChat";

export const FloatingAIButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const constraintsRef = useRef(null);

  // 处理拖拽
  const handleDrag = (event: any, info: PanInfo) => {
    setPosition({ x: info.offset.x, y: info.offset.y });
  };

  // 处理点击事件
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('AI Button clicked!', { isDragging, isOpen }); // 调试日志
    if (!isDragging) {
      setIsOpen(true);
    }
  };

  return (
    <>
      {/* 浮动按钮 */}
      <motion.div
        ref={constraintsRef}
        className="fixed inset-0 pointer-events-none z-40"
      >
        <motion.div
          drag
          dragConstraints={constraintsRef}
          dragElastic={0.1}
          onDrag={handleDrag}
          onDragStart={() => setIsDragging(true)}
          onDragEnd={() => setTimeout(() => setIsDragging(false), 100)}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="absolute bottom-6 right-6 pointer-events-auto"
          style={{ x: position.x, y: position.y }}
          onHoverStart={() => setIsHovered(true)}
          onHoverEnd={() => setIsHovered(false)}
        >
          <motion.div className="relative group">
            {/* 主按钮 */}
            <motion.div
              className="relative"
              animate={{
                rotate: isOpen ? 180 : 0,
              }}
              transition={{ duration: 0.3 }}
            >
              <Button
                onClick={handleClick}
                className="w-16 h-16 rounded-full bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 hover:from-purple-700 hover:via-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-2xl transition-all duration-300 border-0 relative overflow-hidden"
              >
                <motion.div
                  animate={{ rotate: [0, 360] }}
                  transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                >
                  <Bot className="w-8 h-8 text-white" />
                </motion.div>

                {/* 内部光效 */}
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent"
                  animate={{ rotate: [0, 360] }}
                  transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                />
              </Button>

              {/* 外部呼吸光效 */}
              <motion.div
                className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 opacity-30"
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
                className="absolute inset-0 rounded-full border-2 border-purple-400"
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

            {/* 悬浮提示 */}
            <motion.div
              initial={{ opacity: 0, x: 10, scale: 0.8 }}
              animate={{
                opacity: isHovered ? 1 : 0,
                x: isHovered ? -10 : 10,
                scale: isHovered ? 1 : 0.8
              }}
              transition={{ duration: 0.2 }}
              className="absolute right-full top-1/2 transform -translate-y-1/2 mr-4 pointer-events-none"
            >
              <div className="bg-gray-900 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap shadow-lg">
                <div className="flex items-center space-x-2">
                  <MessageCircle className="w-4 h-4" />
                  <span>AI学习助手</span>
                </div>
                <div className="absolute left-full top-1/2 transform -translate-y-1/2">
                  <div className="w-0 h-0 border-l-4 border-l-gray-900 border-t-4 border-t-transparent border-b-4 border-b-transparent"></div>
                </div>
              </div>
            </motion.div>

            {/* 装饰性粒子效果 */}
            {isHovered && (
              <div className="absolute inset-0 pointer-events-none">
                {[...Array(6)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 bg-blue-400 rounded-full"
                    initial={{
                      x: 32,
                      y: 32,
                      scale: 0,
                      opacity: 0
                    }}
                    animate={{
                      x: 32 + Math.cos(i * 60 * Math.PI / 180) * 40,
                      y: 32 + Math.sin(i * 60 * Math.PI / 180) * 40,
                      scale: [0, 1, 0],
                      opacity: [0, 1, 0]
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      delay: i * 0.1,
                      ease: "easeOut"
                    }}
                  />
                ))}
              </div>
            )}
          </motion.div>
        </motion.div>
      </motion.div>

      {/* AI对话界面 */}
      <AIChat isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
};

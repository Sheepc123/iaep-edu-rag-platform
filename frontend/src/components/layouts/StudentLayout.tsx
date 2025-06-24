import {
  LayoutDashboard,
  BookCopy,
  PencilRuler,
  BrainCircuit,
  Bot,
  MessageCircle,
  Settings,
  LogOut,
  User,
} from "lucide-react";
import { ReactNode, useState } from "react";
import { cn } from "@/lib/utils";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { SimpleAIButton } from "@/components/ai/SimpleAIButton";
import { motion, AnimatePresence } from "framer-motion";

const StudentLayout = ({ children }: { children: ReactNode }) => {
  return (
    <div className="flex min-h-screen w-full bg-white font-sans relative">
      <Sidebar />
      <main className="flex-1 p-8 tech-background">
        {children}
      </main>
      <SimpleAIButton />
    </div>
  );
};

const Sidebar = () => {
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();

    // 显示退出确认对话框
    const handleLogoutClick = () => {
        setIsSettingsOpen(false);
        setShowLogoutConfirm(true);
    };

    // 确认退出登录
    const confirmLogout = () => {
        // 清除本地存储的用户信息（如果有的话）
        localStorage.removeItem('userToken');
        localStorage.removeItem('userInfo');
        localStorage.removeItem('aiConversations'); // 清除AI对话记录

        // 关闭确认对话框
        setShowLogoutConfirm(false);

        // 跳转到主页
        navigate('/');
    };

    // 取消退出
    const cancelLogout = () => {
        setShowLogoutConfirm(false);
    };

    const navItems = [
      { icon: <LayoutDashboard size={20} />, label: "个人中心", path: "/student/dashboard" },
      { icon: <BookCopy size={20} />, label: "课程中心", path: "/student/courses" },
      { icon: <PencilRuler size={20} />, label: "练习系统", path: "/student/exercises" },
      { icon: <BrainCircuit size={20} />, label: "学习中心", path: "/student/learning" },
      { icon: <MessageCircle size={20} />, label: "聊天室", path: "/student/chatroom" },
      { icon: <Bot size={20} />, label: "AI助手", path: "/student/ai-assistant" }
    ];

    return (
      <>
        <aside className="w-64 flex flex-col bg-white border-r border-subtle-border">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-brand">智能教育平台</h1>
        </div>
        <nav className="flex-1 px-4 space-y-2">
          {navItems.map((item) => (
            <NavItem
              key={item.path}
              icon={item.icon}
              label={item.label}
              path={item.path}
              isActive={location.pathname === item.path}
            />
          ))}
        </nav>
        <div className="p-4 border-t border-subtle-border">
            <div className="relative">
                {isSettingsOpen && (
                    <div className="absolute bottom-full left-0 w-full mb-2 bg-white rounded-lg shadow-lg border border-subtle-border">
                        <div onClick={() => setIsSettingsOpen(false)}>
                            <NavItem icon={<Settings size={20} />} label="账户设置" path="/student/profile" isSubItem />
                        </div>
                        <div onClick={handleLogoutClick}>
                            <NavItem icon={<LogOut size={20} />} label="退出登录" isSubItem />
                        </div>
                    </div>
                )}
                <div
                    className="flex items-center p-2 rounded-lg cursor-pointer hover:bg-subtle-background"
                    onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                >
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                        <User className="w-5 h-5 text-gray-600" />
                    </div>
                    <span className="ml-4 font-semibold text-gray-700">学生姓名</span>
                </div>
            </div>
        </div>
        </aside>

        {/* 退出登录确认对话框 */}
        <AnimatePresence>
          {showLogoutConfirm && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center"
              onClick={cancelLogout}
            >
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                className="bg-white rounded-2xl p-6 shadow-2xl max-w-md w-full mx-4"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="text-center">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <LogOut className="w-8 h-8 text-red-600" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">确认退出登录</h3>
                  <p className="text-gray-600 mb-6">
                    您确定要退出登录吗？退出后需要重新登录才能访问学生功能。
                  </p>
                  <div className="flex space-x-3">
                    <button
                      onClick={cancelLogout}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                    >
                      取消
                    </button>
                    <button
                      onClick={confirmLogout}
                      className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                    >
                      确认退出
                    </button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </>
    );
};
  

interface NavItemProps {
    icon: ReactNode;
    label: string;
    path?: string;
    isActive?: boolean;
    isSubItem?: boolean;
}

const NavItem = ({ icon, label, path, isActive, isSubItem }: NavItemProps) => {
    const itemClasses = cn(
        "flex items-center py-2 px-4 rounded-lg cursor-pointer transition-colors duration-200",
        {
            "text-brand font-semibold bg-brand-light": isActive && !isSubItem,
            "text-gray-600 hover:bg-subtle-background": !isActive && !isSubItem,
            "text-gray-600 hover:bg-subtle-background w-full text-left": isSubItem,
        }
    );

    if (path) {
      return (
        <Link to={path} className={itemClasses}>
          <div className="mr-4">{icon}</div>
          <span>{label}</span>
        </Link>
      );
    }

    return (
      <a href="#" className={itemClasses}>
        <div className="mr-4">{icon}</div>
        <span>{label}</span>
      </a>
    );
};

export default StudentLayout; 
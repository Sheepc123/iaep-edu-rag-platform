import {
  LayoutDashboard,
  BookOpen,
  Users,
  ClipboardList,
  BarChart3,
  Settings,
  LogOut,
  User,
  PlusCircle,
  Bot,
  MessageCircle,
  Database
} from "lucide-react";
import { ReactNode, useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { FloatingAIButton } from "@/components/ai/FloatingAIButton";
import { motion, AnimatePresence } from "framer-motion";
import { authAPI, tokenManager } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";

interface TeacherLayoutProps {
  children: ReactNode;
  fullScreen?: boolean;
}

interface UserInfo {
  id: number;
  username: string;
  email: string;
  full_name: string;
  avatar?: string;
  role: string;
}

const TeacherLayout = ({ children, fullScreen = false }: TeacherLayoutProps) => {
  return (
    <div className="flex min-h-screen w-full bg-white font-sans relative">
      <Sidebar />
      <main className={`flex-1 tech-background ${fullScreen ? 'p-0' : 'p-8'}`}>
        {children}
      </main>
      <FloatingAIButton />
    </div>
  );
};

const Sidebar = () => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();
  const { toast } = useToast();

  // 检查用户权限
  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (!tokenManager.isLoggedIn()) {
          navigate('/');
          return;
        }

        const user = await authAPI.getCurrentUser();
        if (user.role !== 'teacher' && user.role !== 'admin') {
          toast({
            title: "权限不足",
            description: "您没有访问教师端的权限",
            variant: "destructive",
          });
          navigate('/');
          return;
        }

        setUserInfo(user);
      } catch (error) {
        console.error('获取用户信息失败:', error);
        toast({
          title: "认证失败",
          description: "请重新登录",
          variant: "destructive",
        });
        navigate('/');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [navigate, toast]);

  // 显示退出确认对话框
  const handleLogoutClick = () => {
    setIsSettingsOpen(false);
    setShowLogoutConfirm(true);
  };

  // 确认退出登录
  const confirmLogout = async () => {
    try {
      await authAPI.logout();
      tokenManager.clearTokens();
      localStorage.removeItem('userToken');
      localStorage.removeItem('userInfo');
      localStorage.removeItem('aiConversations');

      setShowLogoutConfirm(false);

      toast({
        title: "登出成功",
        description: "您已成功登出系统",
      });
      navigate('/');
    } catch (error) {
      console.error('登出失败:', error);
      tokenManager.clearTokens();
      navigate('/');
    }
  };

  // 取消退出
  const cancelLogout = () => {
    setShowLogoutConfirm(false);
  };

  const navItems = [
    { icon: <LayoutDashboard size={20} />, label: "教学中心", path: "/teacher/dashboard" },
    { icon: <BookOpen size={20} />, label: "课程管理", path: "/teacher/courses" },
    { icon: <ClipboardList size={20} />, label: "练习管理", path: "/teacher/exercises" },
    { icon: <Database size={20} />, label: "本地知识库", path: "/teacher/knowledge-base" },
    { icon: <Users size={20} />, label: "学生管理", path: "/teacher/students" },
    { icon: <BarChart3 size={20} />, label: "成绩分析", path: "/teacher/grades" },
    { icon: <MessageCircle size={20} />, label: "聊天室", path: "/teacher/chatroom" },
    { icon: <Bot size={20} />, label: "AI助手", path: "/teacher/ai-assistant" }
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

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
                  <NavItem icon={<Settings size={20} />} label="账户设置" path="/teacher/profile" isSubItem />
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
              <span className="ml-4 font-semibold text-gray-700">
                {userInfo?.full_name || userInfo?.username || "教师姓名"}
              </span>
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
                  您确定要退出登录吗？退出后需要重新登录才能访问教师功能。
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

export default TeacherLayout;

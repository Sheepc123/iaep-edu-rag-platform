import {
  LayoutDashboard,
  Users,
  UserCheck,
  GraduationCap,
  BarChart3,
  Settings,
  LogOut,
  User,
  Shield,
  Activity,
  Database,
  TrendingUp
} from "lucide-react";
import { ReactNode, useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { authAPI, tokenManager } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";

interface AdminLayoutProps {
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

const AdminLayout = ({ children, fullScreen = false }: AdminLayoutProps) => {
  return (
    <div className="flex min-h-screen w-full bg-white font-sans relative">
      <Sidebar />
      <main className={`flex-1 tech-background ${fullScreen ? 'p-0' : 'p-8'}`}>
        {children}
      </main>
    </div>
  );
};

const Sidebar = () => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [userLoading, setUserLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();
  const { toast } = useToast();

  // 获取用户信息
  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        // 首先检查本地存储的用户信息（与学生端和教师端一致）
        const storedUserInfo = localStorage.getItem('user_info');
        if (storedUserInfo) {
          const userInfo = JSON.parse(storedUserInfo);
          setUserInfo(userInfo);

          // 验证管理员权限
          if (userInfo.role !== 'admin') {
            toast({
              title: "权限不足",
              description: "您没有管理员权限",
              variant: "destructive",
            });
            navigate('/');
            return;
          }
          setUserLoading(false);
          return;
        }

        // 如果没有本地用户信息，尝试从API获取
        const token = localStorage.getItem('access_token');
        if (!token) {
          navigate('/');
          return;
        }

        const response = await authAPI.getProfile();
        setUserInfo(response);

        // 验证管理员权限
        if (response.role !== 'admin') {
          toast({
            title: "权限不足",
            description: "您没有管理员权限",
            variant: "destructive",
          });
          navigate('/');
          return;
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        navigate('/');
      } finally {
        setUserLoading(false);
      }
    };

    fetchUserInfo();
  }, [navigate, toast]);

  const handleLogout = async () => {
    try {
      // 使用与学生端和教师端相同的退出方法
      await authAPI.logout();
      tokenManager.clearTokens();
      localStorage.removeItem('user_info'); // 清除用户信息
      navigate('/');
      toast({
        title: "退出成功",
        description: "您已安全退出系统",
      });
    } catch (error) {
      console.error('退出失败:', error);
      // 即使API调用失败，也要清除本地数据
      tokenManager.clearTokens();
      localStorage.removeItem('user_info');
      navigate('/');
    }
  };

  const menuItems = [
    {
      icon: LayoutDashboard,
      label: "大屏概览",
      path: "/admin/overview",
      description: "实时数据大屏展示"
    },
    {
      icon: Users,
      label: "用户管理",
      path: "/admin/users",
      description: "管理员/教师/学生管理"
    },
    {
      icon: Database,
      label: "资源管理",
      path: "/admin/resources",
      description: "课件资源与知识库管理"
    },
    {
      icon: UserCheck,
      label: "教师统计",
      path: "/admin/teachers",
      description: "教师使用次数统计/活跃板块"
    },
    {
      icon: GraduationCap,
      label: "学生统计",
      path: "/admin/students",
      description: "学生使用次数统计/学习效果"
    },
    {
      icon: Activity,
      label: "使用统计",
      path: "/admin/usage-stats",
      description: "AI使用量统计"
    },
    {
      icon: BarChart3,
      label: "教学效率",
      path: "/admin/efficiency",
      description: "教学效率指数分析"
    }
  ];

  if (userLoading) {
    return (
      <div className="w-80 bg-gradient-to-b from-blue-900 via-blue-800 to-blue-900 text-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="w-80 bg-gradient-to-b from-blue-900 via-blue-800 to-blue-900 text-white flex flex-col relative overflow-hidden">
      {/* 背景装饰 */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white/20 to-transparent"></div>
        <div className="absolute top-20 right-10 w-32 h-32 bg-white/5 rounded-full blur-xl"></div>
        <div className="absolute bottom-20 left-10 w-24 h-24 bg-white/5 rounded-full blur-xl"></div>
      </div>

      {/* Logo区域 */}
      <div className="p-8 border-b border-white/10 relative z-10">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
            <Shield className="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold">管理员控制台</h1>
            <p className="text-blue-200 text-sm">系统管理平台</p>
          </div>
        </div>
      </div>

      {/* 用户信息 */}
      <div className="p-6 border-b border-white/10 relative z-10">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
            {userInfo?.avatar ? (
              <img src={userInfo.avatar} alt="头像" className="w-full h-full rounded-full object-cover" />
            ) : (
              <User className="w-6 h-6 text-white" />
            )}
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium text-white truncate">
              {userInfo?.full_name || userInfo?.username || '管理员'}
            </p>
            <p className="text-blue-200 text-sm truncate">
              {userInfo?.email}
            </p>
            <div className="flex items-center space-x-1 mt-1">
              <Shield className="w-3 h-3 text-yellow-400" />
              <span className="text-xs text-yellow-400">管理员</span>
            </div>
          </div>
        </div>
      </div>

      {/* 导航菜单 */}
      <nav className="flex-1 p-4 relative z-10">
        <div className="space-y-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden",
                  isActive
                    ? "bg-white/20 text-white shadow-lg backdrop-blur-sm"
                    : "text-blue-100 hover:bg-white/10 hover:text-white"
                )}
              >
                <item.icon className={cn(
                  "w-5 h-5 transition-transform duration-200",
                  isActive ? "scale-110" : "group-hover:scale-105"
                )} />
                <div className="flex-1">
                  <span className="font-medium">{item.label}</span>
                  <p className="text-xs opacity-75 mt-0.5">{item.description}</p>
                </div>
                {isActive && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="absolute right-2 w-2 h-2 bg-white rounded-full"
                    initial={false}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* 底部操作 */}
      <div className="p-4 border-t border-white/10 relative z-10">
        <div className="space-y-2">
          <button
            onClick={() => setIsSettingsOpen(!isSettingsOpen)}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-blue-100 hover:bg-white/10 hover:text-white transition-all duration-200"
          >
            <Settings className="w-5 h-5" />
            <span>系统设置</span>
          </button>
          
          <button
            onClick={() => setShowLogoutConfirm(true)}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-blue-100 hover:bg-red-500/20 hover:text-red-200 transition-all duration-200"
          >
            <LogOut className="w-5 h-5" />
            <span>退出登录</span>
          </button>
        </div>
      </div>

      {/* 退出确认对话框 */}
      <AnimatePresence>
        {showLogoutConfirm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
            onClick={() => setShowLogoutConfirm(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-xl p-6 max-w-sm mx-4"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-2">确认退出</h3>
              <p className="text-gray-600 mb-4">您确定要退出管理员控制台吗？</p>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowLogoutConfirm(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  取消
                </button>
                <button
                  onClick={handleLogout}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  退出
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AdminLayout;

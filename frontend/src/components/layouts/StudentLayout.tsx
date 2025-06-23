import {
  LayoutDashboard,
  BookCopy,
  PencilRuler,
  BrainCircuit,
  Bot,
  Settings,
  LogOut,
} from "lucide-react";
import { ReactNode, useState } from "react";
import { cn } from "@/lib/utils";
import { Link, useLocation } from "react-router-dom";
import { SimpleAIButton } from "@/components/ai/SimpleAIButton";

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
    const location = useLocation();

    const navItems = [
      { icon: <LayoutDashboard size={20} />, label: "个人中心", path: "/student/dashboard" },
      { icon: <BookCopy size={20} />, label: "课程中心", path: "/student/courses" },
      { icon: <PencilRuler size={20} />, label: "练习系统", path: "/student/exercises" },
      { icon: <BrainCircuit size={20} />, label: "学习中心", path: "/student/learning" },
      { icon: <Bot size={20} />, label: "AI助手", path: "/student/ai-assistant" }
    ];

    return (
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
                        <NavItem icon={<Settings size={20} />} label="账户设置" isSubItem />
                        <NavItem icon={<LogOut size={20} />} label="退出登录" isSubItem />
                    </div>
                )}
                <div
                    className="flex items-center p-2 rounded-lg cursor-pointer hover:bg-subtle-background"
                    onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                >
                    <img src="https://i.pravatar.cc/40" alt="avatar" className="w-10 h-10 rounded-full" />
                    <span className="ml-4 font-semibold text-gray-700">学生姓名</span>
                </div>
            </div>
        </div>
      </aside>
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

    if (path && !isSubItem) {
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
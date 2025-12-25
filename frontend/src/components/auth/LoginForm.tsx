import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { ArrowLeftIcon } from "@radix-ui/react-icons";
import { authAPI, tokenManager } from "@/services/api";

type Role = "student" | "teacher" | "administrator";

interface LoginFormProps {
  role: Role;
  onBack: () => void;
}

const getTitleForRole = (role: Role) => {
    switch (role) {
      case "student":
        return "学生登录";
      case "teacher":
        return "老师登录";
      case "administrator":
        return "管理员登录";
    }
};

export const LoginForm = ({ role, onBack }: LoginFormProps) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 基本验证
    if (!username.trim() || !password.trim()) {
      toast({
        variant: "destructive",
        title: "登录失败",
        description: "请输入用户名和密码",
      });
      return;
    }

    setIsLoading(true);

    try {
      // 调用后端登录API
      const response = await authAPI.login({
        username: username.trim(),
        password: password,
        remember_me: true,
        device_info: `Web Browser - ${role}`,
      });

      // 验证用户角色
      const userRole = response.user_info.role;
      if (role === "administrator" && userRole !== "admin") {
        throw new Error("您没有管理员权限");
      }
      if (role === "teacher" && userRole !== "teacher" && userRole !== "admin") {
        throw new Error("您没有教师权限");
      }
      if (role === "student" && userRole !== "student" && userRole !== "admin") {
        throw new Error("您没有学生权限");
      }

      // 保存令牌和用户信息
      tokenManager.saveTokens(response.access_token, response.refresh_token);
      localStorage.setItem("user_info", JSON.stringify(response.user_info));

      toast({
        title: "登录成功",
        description: `欢迎回来，${response.user_info.full_name}！`,
      });

      // 根据用户实际角色和选择的角色跳转
      if (role === "administrator" && userRole === "admin") {
        // 如果选择的是管理员角色且用户确实是管理员，跳转到管理员端
        navigate("/admin/dashboard");
      } else {
        // 其他情况按用户实际角色跳转
        switch (userRole) {
          case "student":
            navigate("/student/dashboard");
            break;
          case "teacher":
            navigate("/teacher/dashboard");
            break;
          case "admin":
            // 管理员选择学生或教师角色时，跳转到对应端
            if (role === "student") {
              navigate("/student/dashboard");
            } else {
              navigate("/teacher/dashboard");
            }
            break;
          default:
            navigate("/");
        }
      }

    } catch (error: any) {
      console.error("登录失败:", error);

      let errorMessage = "登录失败，请稍后重试";

      if (error.message) {
        if (error.message.includes("用户名或密码错误")) {
          errorMessage = "用户名或密码错误";
        } else if (error.message.includes("权限")) {
          errorMessage = error.message;
        } else if (error.message.includes("账户已被禁用")) {
          errorMessage = "账户已被禁用，请联系管理员";
        } else if (error.message.includes("Failed to fetch")) {
          errorMessage = "无法连接到服务器，请检查网络连接";
        } else {
          errorMessage = error.message;
        }
      }

      toast({
        variant: "destructive",
        title: "登录失败",
        description: errorMessage,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const title = getTitleForRole(role);

  return (
    <div className="flex flex-col items-center justify-center h-full text-white w-full">
      <div className="w-full max-w-lg p-8">
        <div className="relative mb-10 text-center">
          <button onClick={onBack} className="absolute left-0 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors p-2 rounded-full hover:bg-white/10">
            <ArrowLeftIcon className="w-7 h-7" />
          </button>
          <h2 className="text-4xl font-bold">{title}</h2>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="space-y-3">
            <Label htmlFor="username-login" className="text-xl text-gray-300 font-medium">邮箱 / 用户名</Label>
            <Input
              id="username-login"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="bg-white/10 border-2 border-gray-600 h-16 text-xl text-white placeholder:text-gray-400 focus:border-blue-400 focus:ring-blue-400 rounded-lg"
              placeholder="请输入您的用户名"
            />
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
                <Label htmlFor="password-login" className="text-xl text-gray-300 font-medium">密码</Label>
                <a href="#" className="text-md text-blue-400 hover:underline">忘记密码？</a>
            </div>
            <Input
              id="password-login"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-white/10 border-2 border-gray-600 h-16 text-xl text-white placeholder:text-gray-400 focus:border-blue-400 focus:ring-blue-400 rounded-lg"
              placeholder="请输入您的密码"
            />
          </div>
          <Button
            type="submit"
            className="w-full text-2xl h-20 bg-blue-500 hover:bg-blue-600 transition-colors rounded-lg font-bold"
            disabled={isLoading}
          >
            {isLoading ? "登录中..." : "登 录"}
          </Button>
        </form>
      </div>
    </div>
  );
}; 
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

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
    setIsLoading(true);

    try {
      // TODO: 实现登录逻辑
      const response = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password, role }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.token);
        toast({
          title: "登录成功",
          description: "欢迎回来！",
        });
        navigate("/dashboard");
      } else {
        throw new Error("登录失败");
      }
    } catch (error) {
      toast({
        variant: "destructive",
        title: "登录失败",
        description: "请检查用户名和密码是否正确",
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
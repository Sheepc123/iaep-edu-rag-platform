import {
  Dialog,
  DialogContent,
  DialogTrigger,
  DialogOverlay,
} from "@/components/ui/dialog";
import { LoginForm } from "./LoginForm";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { GraduationCap, Presentation, UserCog } from 'lucide-react';
import { cn } from "@/lib/utils";

interface LoginModalProps {
  trigger?: React.ReactNode;
}

type Role = "student" | "teacher" | "administrator";
type Step = "role-selection" | "login-form";

const RoleSelection = ({ onSelectRole }: { onSelectRole: (role: Role) => void }) => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-white p-8">
      <h2 className="text-4xl font-bold mb-16">请选择您的角色</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-10 w-full max-w-5xl">
        <RoleCard
          icon={<GraduationCap className="w-20 h-20 mb-6" />}
          title="我是学生"
          onClick={() => onSelectRole("student")}
        />
        <RoleCard
          icon={<Presentation className="w-20 h-20 mb-6" />}
          title="我是老师"
          onClick={() => onSelectRole("teacher")}
        />
        <RoleCard
          icon={<UserCog className="w-20 h-20 mb-6" />}
          title="我是管理员"
          onClick={() => onSelectRole("administrator")}
        />
      </div>
    </div>
  );
};

const RoleCard = ({ icon, title, onClick }: { icon: React.ReactNode; title: string; onClick: () => void; }) => {
  return (
    <div
      onClick={onClick}
      className="bg-white/5 p-10 rounded-2xl flex flex-col items-center justify-center cursor-pointer border-2 border-transparent hover:border-blue-400 hover:bg-white/10 transition-all duration-300 transform hover:scale-105"
      style={{
        backdropFilter: "blur(10px)",
        boxShadow: "0 0 20px rgba(80, 150, 255, 0.2), 0 0 40px rgba(80, 150, 255, 0.1)",
      }}
    >
      {icon}
      <p className="text-3xl font-semibold">{title}</p>
    </div>
  );
};

export const LoginModal = ({ trigger }: LoginModalProps) => {
  const [step, setStep] = useState<Step>("role-selection");
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [direction, setDirection] = useState("forward");

  const handleSelectRole = (role: Role) => {
    setSelectedRole(role);
    setDirection("forward");
    setStep("login-form");
  };

  const handleBack = () => {
    setDirection("backward");
    setStep("role-selection");
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        {trigger || <Button variant="outline">登录</Button>}
      </DialogTrigger>
      <DialogOverlay className="bg-black/80 backdrop-blur-md" />
      <DialogContent 
        className="bg-transparent border-none shadow-none p-0 max-w-6xl w-full overflow-hidden"
        style={{
            fontFamily: "'Inter', sans-serif",
        }}
      >
        <div className="relative h-[700px] flex items-center justify-center">
          {/* Role Selection Step */}
          <div
            className={cn(
              "absolute w-full h-full transition-all duration-500 ease-in-out flex items-center justify-center",
              step === "role-selection"
                ? "opacity-100 transform translate-x-0"
                : direction === "forward" 
                ? "opacity-0 transform -translate-x-full" 
                : "opacity-0 transform translate-x-full"
            )}
          >
            <RoleSelection onSelectRole={handleSelectRole} />
          </div>

          {/* Login Form Step */}
          {selectedRole && (
            <div
              className={cn(
                "absolute w-full h-full transition-all duration-500 ease-in-out flex items-center justify-center",
                step === "login-form"
                  ? "opacity-100 transform translate-x-0"
                  : direction === "forward"
                  ? "opacity-0 transform translate-x-full"
                  : "opacity-0 transform -translate-x-full"
              )}
            >
              <LoginForm role={selectedRole} onBack={handleBack} />
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogOverlay,
} from "@/components/ui/dialog";
import { Bot, School, Users } from "lucide-react";

interface AboutModalProps {
  trigger?: React.ReactNode;
}

const TeamMember = ({ name, description }: { name: string; description: string }) => (
  <div className="bg-white/5 p-5 rounded-lg border border-gray-700 hover:border-green-400 transition-colors duration-300">
    <h4 className="text-xl font-bold text-green-300">{name}</h4>
    <p className="text-gray-400 mt-2 text-sm leading-relaxed">{description}</p>
  </div>
);

export const AboutModal = ({ trigger }: AboutModalProps) => {
  return (
    <Dialog>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogOverlay className="bg-black/80 backdrop-blur-md" />
      <DialogContent
        className="bg-gray-900/80 border-blue-400/30 text-white p-10 max-w-4xl w-full rounded-2xl"
        style={{ backdropFilter: "blur(12px)" }}
      >
        <DialogHeader className="text-center mb-10">
          <DialogTitle className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-4">
            关于我们的项目
          </DialogTitle>
          <DialogDescription className="text-lg text-gray-300 max-w-3xl mx-auto">
            基于开源AI大模型的教学实训智能体软件项目
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-12">
          <div className="flex items-start gap-6">
            <div className="p-3 bg-blue-500/20 rounded-lg mt-1">
              <Bot className="w-8 h-8 text-blue-300" />
            </div>
            <div>
              <h3 className="text-2xl font-semibold mb-2">项目简介</h3>
              <p className="text-gray-300 leading-relaxed">
                本项目旨在利用先进的开源人工智能大模型，打造一款创新的教学实训智能体软件。它能够为师生提供高度个性化、智能化的学习与实训体验，模拟真实世界的场景，并通过智能反馈与评估，有效提升教学效率与学生的实践能力。
              </p>
            </div>
          </div>

          <div className="flex items-start gap-6">
            <div className="p-3 bg-purple-500/20 rounded-lg mt-1">
              <School className="w-8 h-8 text-purple-300" />
            </div>
            <div>
              <h3 className="text-2xl font-semibold mb-2">团队归属</h3>
              <p className="text-gray-300 leading-relaxed">
                我们是来自{" "}
                <span className="font-bold text-purple-300">
                  CUMT (中国矿业大学)
                </span>{" "}
                的充满激情的开发团队，致力于探索AI技术在教育领域的创新应用。
              </p>
            </div>
          </div>

          <div className="flex items-start gap-6">
            <div className="p-3 bg-green-500/20 rounded-lg mt-1">
              <Users className="w-8 h-8 text-green-300" />
            </div>
            <div>
              <h3 className="text-2xl font-semibold mb-2">核心成员</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
                <TeamMember
                  name="LYY"
                  description="负责项目总体架构与后端开发，对AI模型集成有深入研究。"
                />
                <TeamMember
                  name="WWQ"
                  description="专注前端界面与用户体验设计，致力于打造流畅、美观的交互界面。"
                />
                <TeamMember
                  name="SH"
                  description="负责算法设计与数据处理，确保智能体软件的核心功能高效稳定。"
                />
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}; 
import { ParticleBackground } from "@/components/backgrounds/ParticleBackground";
import { LoginModal } from "@/components/auth/LoginModal";
import { Button } from "@/components/ui/button";
import { AboutModal } from "@/components/public/AboutModal";

export const Home = () => {
  return (
    <div className="h-screen flex flex-col bg-[#020817] overflow-hidden">
      <div className="absolute inset-0">
        <ParticleBackground />
      </div>
      
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-full max-w-[1200px] px-4">
          <div className="flex flex-col items-center justify-center gap-12">
            <h1 className="text-7xl md:text-8xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-blue-400 tracking-tight animate-fade-in">
              智能教育平台
            </h1>
            <p className="text-2xl md:text-3xl text-gray-300 leading-relaxed font-light animate-fade-in-up max-w-3xl text-center">
              基于人工智能的新一代教育解决方案，为师生提供个性化学习体验
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center animate-fade-in-up">
              <LoginModal
                trigger={
                  <Button size="lg" className="text-xl px-12 py-6 rounded-full hover:scale-105 transition-transform w-full sm:w-auto">
                    开始使用
                  </Button>
                }
              />
              <AboutModal
                trigger={
                  <Button 
                    size="lg" 
                    variant="outline" 
                    className="text-xl px-12 py-6 rounded-full hover:scale-105 transition-transform hover:bg-gray-800/50 w-full sm:w-auto"
                  >
                    了解更多
                  </Button>
                }
              />
            </div>
          </div>
        </div>
      </div>



      <footer className="absolute bottom-0 w-full py-8 text-center text-gray-400 text-lg bg-gradient-to-t from-[#020817] to-transparent z-10">
        <p>© 2025 智能教育平台.中国矿业大学 All rights reserved.</p>
      </footer>
    </div>
  );
}; 
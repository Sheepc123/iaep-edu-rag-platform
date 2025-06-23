import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { AIProvider } from "./contexts/AIContext";
import { Home } from "./pages/public/Home";
import { Dashboard } from "./pages/student/Dashboard";
import { Courses } from "./pages/student/Courses";
import { Exercises } from "./pages/student/Exercises";
import { Learning } from "./pages/student/Learning";
import { AIAssistant } from "./pages/student/AIAssistant";

function App() {
  return (
    <AIProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/student/dashboard" element={<Dashboard />} />
          <Route path="/student/courses" element={<Courses />} />
          <Route path="/student/exercises" element={<Exercises />} />
          <Route path="/student/learning" element={<Learning />} />
          <Route path="/student/ai-assistant" element={<AIAssistant />} />
          {/* 添加更多路由 */}
        </Routes>
        <Toaster />
      </Router>
    </AIProvider>
  );
}

export default App;

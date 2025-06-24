import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { AIProvider } from "./contexts/AIContext";
import { Home } from "./pages/public/Home";
import { Dashboard } from "./pages/student/Dashboard";
import { Courses } from "./pages/student/Courses";
import { Exercises } from "./pages/student/Exercises";
import { ExercisePractice } from "./pages/student/ExercisePractice";
import { ExerciseResult } from "./pages/student/ExerciseResult";
import { Learning } from "./pages/student/Learning";
import { ChatRoom } from "./pages/student/ChatRoom";
import { AIAssistant } from "./pages/student/AIAssistant";
import { Profile } from "./pages/student/Profile";

function App() {
  return (
    <AIProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/student/dashboard" element={<Dashboard />} />
          <Route path="/student/courses" element={<Courses />} />
          <Route path="/student/exercises" element={<Exercises />} />
          <Route path="/student/exercises/practice/:exerciseId" element={<ExercisePractice />} />
          <Route path="/student/exercises/result/:exerciseId" element={<ExerciseResult />} />
          <Route path="/student/learning" element={<Learning />} />
          <Route path="/student/chatroom" element={<ChatRoom />} />
          <Route path="/student/ai-assistant" element={<AIAssistant />} />
          <Route path="/student/profile" element={<Profile />} />
          {/* 添加更多路由 */}
        </Routes>
        <Toaster />
      </Router>
    </AIProvider>
  );
}

export default App;

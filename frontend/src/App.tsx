import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { Home } from "./pages/public/Home";
import { Dashboard } from "./pages/student/Dashboard";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/student/dashboard" element={<Dashboard />} />
        {/* 添加更多路由 */}
      </Routes>
      <Toaster />
    </Router>
  );
}

export default App;

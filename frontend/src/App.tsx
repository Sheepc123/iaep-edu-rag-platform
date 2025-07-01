import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { AIProvider } from "./contexts/AIContext";
import { Home } from "./pages/public/Home";
import { Dashboard } from "./pages/student/Dashboard";
import { Courses } from "./pages/student/Courses";
import { CourseDetail } from "./pages/student/CourseDetail";
import { Exercises } from "./pages/student/Exercises";
import { ExercisePractice } from "./pages/student/ExercisePractice";
import { ExerciseResult } from "./pages/student/ExerciseResult";
import { Learning } from "./pages/student/Learning";
import { ChatRoom } from "./pages/student/ChatRoom";
import { AIAssistant } from "./pages/student/AIAssistant";
import { Profile } from "./pages/student/Profile";

// 教师端页面导入
import { TeacherDashboard } from "./pages/teacher/Dashboard";
import { TeacherCourses } from "./pages/teacher/Courses";
import { TeacherCourseDetail } from "./pages/teacher/CourseDetail";
import { TeacherCourseCreate } from "./pages/teacher/CourseCreate";
import { TeacherCourseEdit } from "./pages/teacher/CourseEdit";
import { TeacherExercises } from "./pages/teacher/Exercises";
import { TeacherExerciseDetail } from "./pages/teacher/ExerciseDetail";
import { TeacherExerciseCreate } from "./pages/teacher/ExerciseCreate";
import { TeacherExerciseEdit } from "./pages/teacher/ExerciseEdit";
import { TeacherStudents } from "./pages/teacher/Students";
import { TeacherStudentDetail } from "./pages/teacher/StudentDetail";
import { TeacherGrades } from "./pages/teacher/Grades";
import { TeacherProfile } from "./pages/teacher/Profile";
import { TeacherAIAssistant } from "./pages/teacher/AIAssistant";
import { TeacherChatRoom } from "./pages/teacher/ChatRoom";
import { TeacherKnowledgeBase } from "./pages/teacher/KnowledgeBase";

function App() {
  return (
    <AIProvider>
      <Router>
        <Routes>
          {/* 公共页面 */}
          <Route path="/" element={<Home />} />

          {/* 学生端路由 */}
          <Route path="/student/dashboard" element={<Dashboard />} />
          <Route path="/student/courses" element={<Courses />} />
          <Route path="/student/courses/:courseId" element={<CourseDetail />} />
          <Route path="/student/exercises" element={<Exercises />} />
          <Route path="/student/exercise/:exerciseId" element={<ExercisePractice />} />
          <Route path="/student/exercises/practice/:exerciseId" element={<ExercisePractice />} />
          <Route path="/student/exercises/result/:exerciseId" element={<ExerciseResult />} />
          <Route path="/student/learning" element={<Learning />} />
          <Route path="/student/chatroom" element={<ChatRoom />} />
          <Route path="/student/ai-assistant" element={<AIAssistant />} />
          <Route path="/student/profile" element={<Profile />} />

          {/* 教师端路由 */}
          <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
          <Route path="/teacher/courses" element={<TeacherCourses />} />
          <Route path="/teacher/courses/create" element={<TeacherCourseCreate />} />
          <Route path="/teacher/courses/:courseId" element={<TeacherCourseDetail />} />
          <Route path="/teacher/courses/:courseId/edit" element={<TeacherCourseEdit />} />
          <Route path="/teacher/exercises" element={<TeacherExercises />} />
          <Route path="/teacher/exercises/create" element={<TeacherExerciseCreate />} />
          <Route path="/teacher/exercises/:exerciseId" element={<TeacherExerciseDetail />} />
          <Route path="/teacher/exercises/:exerciseId/edit" element={<TeacherExerciseEdit />} />
          <Route path="/teacher/knowledge-base" element={<TeacherKnowledgeBase />} />
          <Route path="/teacher/students" element={<TeacherStudents />} />
          <Route path="/teacher/students/:studentId" element={<TeacherStudentDetail />} />
          <Route path="/teacher/grades" element={<TeacherGrades />} />
          <Route path="/teacher/chatroom" element={<TeacherChatRoom />} />
          <Route path="/teacher/ai-assistant" element={<TeacherAIAssistant />} />
          <Route path="/teacher/profile" element={<TeacherProfile />} />
        </Routes>
        <Toaster />
      </Router>
    </AIProvider>
  );
}

export default App;

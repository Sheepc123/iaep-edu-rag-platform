import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useParams, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  User,
  Mail,
  Phone,
  School,
  GraduationCap,
  BookOpen,
  Clock,
  TrendingUp,
  Award,
  Calendar,
  Target,
  BarChart3,
  FileText,
  Star,
  CheckCircle,
  PlayCircle
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { teacherAPI } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";

interface StudentDetail {
  id: number;
  username: string;
  full_name: string;
  email: string;
  avatar?: string;
  created_at: string;
  last_login?: string;
  profile: {
    student_id?: string;
    school?: string;
    college?: string;
    major?: string;
    grade?: string;
    class_name?: string;
    preferred_subjects?: string;
    learning_goals?: string;
  };
  statistics: {
    total_courses: number;
    completed_courses: number;
    total_study_time: number;
    average_progress: number;
    total_exercises: number;
    average_score: number;
  };
  enrollments: Array<{
    id: number;
    course_id: number;
    course_title: string;
    course_category: string;
    progress_percentage: number;
    completed_lessons: number;
    total_study_time: number;
    rating?: number;
    enrolled_at: string;
    last_accessed?: string;
    is_completed: boolean;
  }>;
  exercise_attempts: Array<{
    id: number;
    exercise_id: number;
    score: number;
    total_points: number;
    percentage: number;
    time_spent: number;
    is_completed: boolean;
    submitted_at: string;
  }>;
}

export const TeacherStudentDetail: React.FC = () => {
  const { studentId } = useParams<{ studentId: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();

  // 状态管理
  const [student, setStudent] = useState<StudentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  // 获取学生详细信息
  const fetchStudentDetail = async () => {
    if (!studentId) return;

    try {
      setLoading(true);
      const response = await teacherAPI.getStudentDetail(parseInt(studentId));
      setStudent(response);
    } catch (error) {
      console.error('获取学生详情失败:', error);
      toast({
        title: "加载失败",
        description: "无法获取学生详细信息，请稍后重试",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudentDetail();
  }, [studentId]);

  // 动画配置
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring" as const,
        stiffness: 300,
        damping: 30
      }
    }
  };

  // 格式化时间
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // 格式化学习时间
  const formatStudyTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}分钟`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}小时${remainingMinutes > 0 ? remainingMinutes + '分钟' : ''}`;
  };

  if (loading) {
    return (
      <TeacherLayout>
        <div className="flex items-center justify-center min-h-96">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">加载中...</span>
        </div>
      </TeacherLayout>
    );
  }

  if (!student) {
    return (
      <TeacherLayout>
        <div className="text-center py-12">
          <User className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">学生不存在</h3>
          <p className="text-gray-600 mb-6">无法找到指定的学生信息</p>
          <Button onClick={() => navigate('/teacher/students')}>
            返回学生列表
          </Button>
        </div>
      </TeacherLayout>
    );
  }

  return (
    <TeacherLayout>
      <motion.div
        className="space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* 页面标题和返回按钮 */}
        <motion.div variants={cardVariants}>
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/teacher/students')}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              返回列表
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">学生详情</h1>
              <p className="text-gray-600 mt-2">查看学生的详细学习情况</p>
            </div>
          </div>
        </motion.div>

        {/* 学生基本信息卡片 */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-8">
              <div className="flex flex-col md:flex-row gap-8">
                {/* 头像和基本信息 */}
                <div className="flex flex-col items-center md:items-start">
                  <Avatar className="w-24 h-24 mb-4">
                    <AvatarImage
                      src={student.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(student.full_name)}&background=3b82f6&color=fff&size=96`}
                      alt={student.full_name}
                    />
                    <AvatarFallback className="text-2xl">{student.full_name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">{student.full_name}</h2>
                  <p className="text-gray-600 mb-4">{student.profile.student_id || "学号未设置"}</p>
                  <div className="flex flex-wrap gap-2">
                    <Badge className="bg-blue-100 text-blue-700">
                      {student.profile.grade || "年级未设置"}
                    </Badge>
                    <Badge className="bg-green-100 text-green-700">
                      {student.statistics.total_courses} 门课程
                    </Badge>
                  </div>
                </div>

                {/* 详细信息 */}
                <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">基本信息</h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <Mail className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">邮箱：</span>
                        <span className="text-sm text-gray-900">{student.email}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <School className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">学校：</span>
                        <span className="text-sm text-gray-900">{student.profile.school || "未设置"}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <GraduationCap className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">学院：</span>
                        <span className="text-sm text-gray-900">{student.profile.college || "未设置"}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <BookOpen className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">专业：</span>
                        <span className="text-sm text-gray-900">{student.profile.major || "未设置"}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <User className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">班级：</span>
                        <span className="text-sm text-gray-900">{student.profile.class_name || "未设置"}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">学习统计</h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <Calendar className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">注册时间：</span>
                        <span className="text-sm text-gray-900">{formatDate(student.created_at)}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">学习时长：</span>
                        <span className="text-sm text-gray-900">{formatStudyTime(student.statistics.total_study_time)}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <TrendingUp className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">平均进度：</span>
                        <span className="text-sm text-gray-900">{student.statistics.average_progress.toFixed(1)}%</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <Award className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">平均成绩：</span>
                        <span className="text-sm text-gray-900">{student.statistics.average_score.toFixed(1)}分</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <CheckCircle className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">完成课程：</span>
                        <span className="text-sm text-gray-900">{student.statistics.completed_courses}/{student.statistics.total_courses}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 统计卡片 */}
        <motion.div variants={cardVariants}>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">注册课程</p>
                    <p className="text-2xl font-bold text-gray-900">{student.statistics.total_courses}</p>
                  </div>
                  <div className="bg-blue-100 p-3 rounded-full">
                    <BookOpen className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">完成课程</p>
                    <p className="text-2xl font-bold text-gray-900">{student.statistics.completed_courses}</p>
                  </div>
                  <div className="bg-green-100 p-3 rounded-full">
                    <CheckCircle className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">学习时长</p>
                    <p className="text-2xl font-bold text-gray-900">{Math.round(student.statistics.total_study_time / 60)}h</p>
                  </div>
                  <div className="bg-yellow-100 p-3 rounded-full">
                    <Clock className="w-6 h-6 text-yellow-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">平均成绩</p>
                    <p className="text-2xl font-bold text-gray-900">{student.statistics.average_score.toFixed(0)}</p>
                  </div>
                  <div className="bg-purple-100 p-3 rounded-full">
                    <Award className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>

        {/* 详细信息标签页 */}
        <motion.div variants={cardVariants}>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="overview" className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                学习概览
              </TabsTrigger>
              <TabsTrigger value="courses" className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                课程进度
              </TabsTrigger>
              <TabsTrigger value="exercises" className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                练习记录
              </TabsTrigger>
            </TabsList>

            {/* 学习概览 */}
            <TabsContent value="overview" className="mt-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 学习目标 */}
                <Card className="border-0 shadow-lg">
                  <CardHeader>
                    <CardTitle className="text-lg font-bold flex items-center gap-2">
                      <Target className="w-5 h-5 text-blue-600" />
                      学习目标
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600">
                      {student.profile.learning_goals || "学生暂未设置学习目标"}
                    </p>
                  </CardContent>
                </Card>

                {/* 偏好科目 */}
                <Card className="border-0 shadow-lg">
                  <CardHeader>
                    <CardTitle className="text-lg font-bold flex items-center gap-2">
                      <Star className="w-5 h-5 text-yellow-600" />
                      偏好科目
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600">
                      {student.profile.preferred_subjects || "学生暂未设置偏好科目"}
                    </p>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* 课程进度 */}
            <TabsContent value="courses" className="mt-6">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-blue-600" />
                    课程学习进度
                    <Badge variant="secondary" className="ml-2">
                      {student.enrollments.length} 门课程
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {student.enrollments.length === 0 ? (
                    <div className="text-center py-8">
                      <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-600">学生暂未注册任何课程</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {student.enrollments.map((enrollment) => (
                        <div key={enrollment.id} className="border rounded-lg p-4 hover:bg-gray-50">
                          <div className="flex items-center justify-between mb-3">
                            <div>
                              <h4 className="font-semibold text-gray-900">{enrollment.course_title}</h4>
                              <p className="text-sm text-gray-600">{enrollment.course_category}</p>
                            </div>
                            <div className="flex items-center gap-2">
                              {enrollment.is_completed ? (
                                <Badge className="bg-green-100 text-green-700">
                                  <CheckCircle className="w-3 h-3 mr-1" />
                                  已完成
                                </Badge>
                              ) : (
                                <Badge variant="outline">
                                  学习中
                                </Badge>
                              )}
                              {enrollment.rating && (
                                <Badge variant="outline" className="flex items-center gap-1">
                                  <Star className="w-3 h-3 text-yellow-500" />
                                  {enrollment.rating}
                                </Badge>
                              )}
                            </div>
                          </div>

                          <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                              <span className="text-gray-600">学习进度</span>
                              <span className="font-medium">{enrollment.progress_percentage.toFixed(1)}%</span>
                            </div>
                            <Progress value={enrollment.progress_percentage} className="h-2" />
                          </div>

                          <div className="grid grid-cols-3 gap-4 mt-4 text-sm">
                            <div className="flex items-center gap-2">
                              <PlayCircle className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-600">已完成课时：</span>
                              <span className="font-medium">{enrollment.completed_lessons}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <Clock className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-600">学习时长：</span>
                              <span className="font-medium">{formatStudyTime(enrollment.total_study_time)}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <Calendar className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-600">注册时间：</span>
                              <span className="font-medium">{formatDate(enrollment.enrolled_at)}</span>
                            </div>
                          </div>

                          {enrollment.last_accessed && (
                            <div className="mt-2 text-sm text-gray-500">
                              最后学习：{formatDate(enrollment.last_accessed)}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* 练习记录 */}
            <TabsContent value="exercises" className="mt-6">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center gap-2">
                    <FileText className="w-5 h-5 text-blue-600" />
                    练习记录
                    <Badge variant="secondary" className="ml-2">
                      {student.exercise_attempts.length} 次练习
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {student.exercise_attempts.length === 0 ? (
                    <div className="text-center py-8">
                      <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-600">学生暂无练习记录</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {student.exercise_attempts.map((attempt) => (
                        <div key={attempt.id} className="border rounded-lg p-4 hover:bg-gray-50">
                          <div className="flex items-center justify-between mb-3">
                            <div>
                              <h4 className="font-semibold text-gray-900">练习 #{attempt.exercise_id}</h4>
                              <p className="text-sm text-gray-600">提交时间：{formatDate(attempt.submitted_at)}</p>
                            </div>
                            <div className="flex items-center gap-2">
                              {attempt.is_completed ? (
                                <Badge className="bg-green-100 text-green-700">
                                  <CheckCircle className="w-3 h-3 mr-1" />
                                  已完成
                                </Badge>
                              ) : (
                                <Badge variant="outline">
                                  未完成
                                </Badge>
                              )}
                              <Badge
                                variant="outline"
                                className={`${
                                  attempt.percentage >= 80 ? 'text-green-700 border-green-200' :
                                  attempt.percentage >= 60 ? 'text-yellow-700 border-yellow-200' :
                                  'text-red-700 border-red-200'
                                }`}
                              >
                                {attempt.percentage.toFixed(1)}%
                              </Badge>
                            </div>
                          </div>

                          <div className="grid grid-cols-3 gap-4 text-sm">
                            <div className="flex items-center gap-2">
                              <Award className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-600">得分：</span>
                              <span className="font-medium">{attempt.score}/{attempt.total_points}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <Clock className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-600">用时：</span>
                              <span className="font-medium">{Math.round(attempt.time_spent / 60)}分钟</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <TrendingUp className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-600">正确率：</span>
                              <span className="font-medium">{attempt.percentage.toFixed(1)}%</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>
      </motion.div>
    </TeacherLayout>
  );
};

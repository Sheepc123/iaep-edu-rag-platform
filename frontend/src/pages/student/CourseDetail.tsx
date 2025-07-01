import StudentLayout from "@/components/layouts/StudentLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  BookOpen,
  Clock,
  Users,
  Star,
  PlayCircle,
  Download,
  ChevronLeft,
  ChevronRight,
  CheckCircle,
  Lock,
  FileText,
  Video,
  Calendar,
  Globe,
  MessageCircle,
  Share2,
  Plus,
  BarChart3
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { courseAPI, Course, Lesson, CourseEnrollment, LessonProgress, Exercise } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

const cardVariants = {
  hidden: {
    opacity: 0,
    y: 20,
    scale: 0.95
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 15
    }
  }
};

export const CourseDetail = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = useState("overview");
  const [course, setCourse] = useState<Course | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [enrollment, setEnrollment] = useState<CourseEnrollment | null>(null);
  const [lessonProgresses, setLessonProgresses] = useState<LessonProgress[]>([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);

  // 获取课程数据
  useEffect(() => {
    const fetchCourseData = async () => {
      if (!courseId) return;

      try {
        setLoading(true);

        // 获取课程基本信息
        const courseData = await courseAPI.getCourse(parseInt(courseId));
        setCourse(courseData);

        // 获取课程课时
        const lessonsData = await courseAPI.getCourseLessons(parseInt(courseId));
        setLessons(lessonsData);

        // 获取课程练习
        try {
          const exercisesData = await courseAPI.getCourseExercises(parseInt(courseId));
          setExercises(exercisesData.exercises);
        } catch (error) {
          console.log("获取课程练习失败:", error);
        }

        // 尝试获取注册信息（如果已注册）
        try {
          const enrollmentData = await courseAPI.getCourseEnrollment(parseInt(courseId));
          setEnrollment(enrollmentData);

          // 获取学习进度
          const progressData = await courseAPI.getCourseProgress(parseInt(courseId));
          setLessonProgresses(progressData);
        } catch (error) {
          // 未注册课程，忽略错误
          console.log("未注册此课程");
        }

      } catch (error: any) {
        console.error("获取课程数据失败:", error);
        toast({
          variant: "destructive",
          title: "加载失败",
          description: "无法加载课程信息，请稍后重试",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchCourseData();
  }, [courseId, toast]);

  // 处理返回
  const handleBack = () => {
    navigate("/student/courses");
  };

  // 处理课程注册
  const handleEnrollCourse = async () => {
    if (!courseId) return;

    try {
      setEnrolling(true);
      await courseAPI.enrollCourse(parseInt(courseId));
      toast({
        title: "注册成功",
        description: "您已成功注册该课程，现在可以开始学习了！",
      });
      
      // 重新获取课程数据
      const enrollmentData = await courseAPI.getCourseEnrollment(parseInt(courseId));
      setEnrollment(enrollmentData);
      
      const progressData = await courseAPI.getCourseProgress(parseInt(courseId));
      setLessonProgresses(progressData);
    } catch (error: any) {
      console.error("注册课程失败:", error);
      toast({
        variant: "destructive",
        title: "注册失败",
        description: error.message || "注册课程失败，请稍后重试",
      });
    } finally {
      setEnrolling(false);
    }
  };

  // 处理开始学习
  const handleStartLesson = (lessonId: number) => {
    navigate(`/student/lessons/${lessonId}`);
  };

  // 计算学习进度
  const calculateProgress = () => {
    if (lessons.length === 0) return 0;
    const completedCount = lessonProgresses.filter(p => p.is_completed).length;
    return Math.round((completedCount / lessons.length) * 100);
  };

  // 计算完成的课时数
  const completedLessons = lessonProgresses.filter(p => p.is_completed).length;

  if (loading) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">加载中...</p>
          </div>
        </div>
      </StudentLayout>
    );
  }

  if (!course) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">课程不存在</h2>
            <p className="text-gray-600 mb-4">抱歉，找不到您要查看的课程</p>
            <Button onClick={handleBack}>返回课程中心</Button>
          </div>
        </div>
      </StudentLayout>
    );
  }

  return (
    <StudentLayout>
      <motion.div 
        className="space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header */}
        <motion.div variants={cardVariants}>
          <div className="flex items-center justify-between">
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={handleBack}
              className="flex items-center space-x-2"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>返回课程中心</span>
            </Button>
          </div>
        </motion.div>

        {/* Course Header */}
        <motion.div variants={cardVariants}>
          <Card className="overflow-hidden">
            <div className="relative h-64 bg-gradient-to-r from-blue-600 to-purple-600">
              <img
                src={course.cover_image || "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800"}
                alt={course.title}
                className="w-full h-full object-cover opacity-30"
              />
              <div className="absolute inset-0 bg-black bg-opacity-40" />
              <div className="absolute bottom-0 left-0 right-0 p-8 text-white">
                <div className="flex items-center space-x-3 mb-4">
                  <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                    {course.category}
                  </Badge>
                  <Badge 
                    variant="secondary" 
                    className={`border-white/30 ${
                      course.difficulty === 'easy' ? 'bg-green-500/20 text-green-100' :
                      course.difficulty === 'medium' ? 'bg-yellow-500/20 text-yellow-100' :
                      'bg-red-500/20 text-red-100'
                    }`}
                  >
                    {course.difficulty === 'easy' ? '初级' : 
                     course.difficulty === 'medium' ? '中级' : '高级'}
                  </Badge>
                </div>
                <h1 className="text-4xl font-bold mb-4">{course.title}</h1>
                <div className="flex items-center space-x-6 text-sm">
                  <div className="flex items-center space-x-2">
                    <Users className="w-4 h-4" />
                    <span>{course.enrolled_students} 学生</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    <span>{course.rating}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4" />
                    <span>{Math.floor((course.duration || 0) / 60)} 小时</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Main Content */}
        <motion.div variants={cardVariants}>
          {/* 主要内容区域 */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* 左侧主要内容 */}
            <div className="lg:col-span-2">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="overview">课程概述</TabsTrigger>
                  <TabsTrigger value="curriculum">课程内容</TabsTrigger>
                  <TabsTrigger value="exercises">课程练习</TabsTrigger>
                  <TabsTrigger value="materials">课程资料</TabsTrigger>
                </TabsList>

                {/* 课程概述 */}
                <TabsContent value="overview" className="space-y-6">
                  <motion.div variants={cardVariants}>
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center">
                          <BookOpen className="w-5 h-5 mr-2 text-blue-600" />
                          课程介绍
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                          {course.description}
                        </p>
                      </CardContent>
                    </Card>
                  </motion.div>

                  <motion.div variants={cardVariants}>
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center">
                          <Users className="w-5 h-5 mr-2 text-green-600" />
                          学习统计
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-2 gap-6">
                          <div className="text-center p-4 bg-blue-50 rounded-lg">
                            <div className="text-2xl font-bold text-blue-600">{course.enrolled_students}</div>
                            <div className="text-sm text-gray-600">注册学员</div>
                          </div>
                          <div className="text-center p-4 bg-green-50 rounded-lg">
                            <div className="text-2xl font-bold text-green-600">{completedLessons}</div>
                            <div className="text-sm text-gray-600">完成课时</div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                </TabsContent>

                {/* 课程内容 */}
                <TabsContent value="curriculum" className="space-y-6">
                  <motion.div variants={cardVariants}>
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <div className="flex items-center">
                            <PlayCircle className="w-5 h-5 mr-2 text-blue-600" />
                            课程内容
                          </div>
                          <Badge variant="outline">
                            {lessons.length} 课时
                          </Badge>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        {lessons.map((lesson, index) => {
                          const progress = lessonProgresses.find(p => p.lesson_id === lesson.id);
                          const isCompleted = progress?.is_completed || false;
                          const isLocked = !enrollment && index > 0;

                          return (
                            <motion.div
                              key={lesson.id}
                              className={`p-4 border rounded-lg transition-colors ${
                                isCompleted ? 'bg-green-50 border-green-200' :
                                isLocked ? 'bg-gray-50 border-gray-200' :
                                'bg-white border-gray-200 hover:border-blue-300'
                              }`}
                              whileHover={!isLocked ? { scale: 1.02 } : {}}
                              whileTap={!isLocked ? { scale: 0.98 } : {}}
                            >
                              <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-3">
                                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                    isCompleted ? 'bg-green-500 text-white' :
                                    isLocked ? 'bg-gray-300 text-gray-500' :
                                    'bg-blue-500 text-white'
                                  }`}>
                                    {isCompleted ? (
                                      <CheckCircle className="w-4 h-4" />
                                    ) : isLocked ? (
                                      <Lock className="w-4 h-4" />
                                    ) : (
                                      <PlayCircle className="w-4 h-4" />
                                    )}
                                  </div>
                                  <div>
                                    <h3 className="font-medium text-gray-900">{lesson.title}</h3>
                                    <p className="text-sm text-gray-500">{lesson.description}</p>
                                  </div>
                                </div>
                                <div className="flex items-center space-x-4">
                                  <div className="text-sm text-gray-500 flex items-center">
                                    <Clock className="w-4 h-4 mr-1" />
                                    {lesson.duration} 分钟
                                  </div>
                                  {!isLocked && (
                                    <Button
                                      size="sm"
                                      variant={isCompleted ? "outline" : "default"}
                                      onClick={() => handleStartLesson(lesson.id)}
                                    >
                                      {isCompleted ? "重新学习" : "开始学习"}
                                    </Button>
                                  )}
                                </div>
                              </div>
                            </motion.div>
                          );
                        })}

                        {!enrollment && (
                          <div className="mt-6 p-4 bg-blue-50 rounded-lg text-center">
                            <p className="text-blue-700 mb-3">注册课程后即可开始学习</p>
                            <Button onClick={handleEnrollCourse} disabled={enrolling}>
                              <BookOpen className="w-4 h-4 mr-2" />
                              {enrolling ? "注册中..." : "立即注册"}
                            </Button>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  </motion.div>
                </TabsContent>

                {/* 课程练习 */}
                <TabsContent value="exercises" className="space-y-6">
                  <motion.div variants={cardVariants}>
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center">
                          <FileText className="w-5 h-5 mr-2 text-purple-600" />
                          课程练习
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        {exercises.length > 0 ? (
                          <div className="space-y-4">
                            {exercises.map((exercise) => (
                              <motion.div
                                key={exercise.id}
                                className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => navigate(`/student/exercise/${exercise.id}`)}
                              >
                                <div className="flex items-start justify-between">
                                  <div className="flex-1">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                      {exercise.title}
                                    </h3>
                                    {exercise.description && (
                                      <p className="text-gray-600 mb-3 line-clamp-2">
                                        {exercise.description}
                                      </p>
                                    )}
                                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                                      <div className="flex items-center space-x-1">
                                        <FileText className="w-4 h-4" />
                                        <span>{exercise.total_questions} 题</span>
                                      </div>
                                      {exercise.time_limit && (
                                        <div className="flex items-center space-x-1">
                                          <Clock className="w-4 h-4" />
                                          <span>{exercise.time_limit} 分钟</span>
                                        </div>
                                      )}
                                      <Badge
                                        variant={
                                          exercise.difficulty === 'easy' ? 'secondary' :
                                          exercise.difficulty === 'medium' ? 'default' : 'destructive'
                                        }
                                      >
                                        {exercise.difficulty === 'easy' ? '简单' :
                                         exercise.difficulty === 'medium' ? '中等' : '困难'}
                                      </Badge>
                                    </div>
                                  </div>
                                  <div className="flex items-center space-x-2">
                                    <Button size="sm">
                                      开始练习
                                      <ChevronRight className="w-4 h-4 ml-1" />
                                    </Button>
                                  </div>
                                </div>
                              </motion.div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-12">
                            <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-gray-900 mb-2">暂无练习</h3>
                            <p className="text-gray-500">该课程暂时没有配套练习</p>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  </motion.div>
                </TabsContent>

                {/* 课程资料 */}
                <TabsContent value="materials" className="space-y-6">
                  <motion.div variants={cardVariants}>
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center">
                          <Download className="w-5 h-5 mr-2 text-green-600" />
                          课程资料
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-center py-12">
                          <Download className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                          <h3 className="text-lg font-medium text-gray-900 mb-2">暂无资料</h3>
                          <p className="text-gray-500">该课程暂时没有可下载的资料</p>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                </TabsContent>
              </Tabs>
            </div>

            {/* 右侧边栏 */}
            <div className="space-y-6">
              {/* 学习进度 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
                      学习进度
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">总体进度</span>
                        <span className="text-sm font-medium">{calculateProgress()}%</span>
                      </div>
                      <Progress value={calculateProgress()} className="h-2" />
                      <div className="text-xs text-gray-500">
                        已完成 {completedLessons} / {lessons.length} 课时
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* 课程信息 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <BookOpen className="w-5 h-5 mr-2 text-green-600" />
                      课程信息
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">课程时长</span>
                      <span className="text-sm font-medium">{Math.floor((course.duration || 0) / 60)} 小时</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">课时数量</span>
                      <span className="text-sm font-medium">{lessons.length} 课时</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">练习数量</span>
                      <span className="text-sm font-medium">{exercises.length} 个</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">难度等级</span>
                      <Badge variant="outline">
                        {course.difficulty === 'easy' ? '初级' :
                         course.difficulty === 'medium' ? '中级' : '高级'}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* 授课教师 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Users className="w-5 h-5 mr-2 text-purple-600" />
                      授课教师
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center space-x-3">
                      <Avatar className="w-12 h-12">
                        <AvatarFallback>{course.instructor_name[0]}</AvatarFallback>
                      </Avatar>
                      <div>
                        <h3 className="font-medium text-gray-900">{course.instructor_name}</h3>
                        <p className="text-sm text-gray-500">授课教师</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* 注册按钮 */}
              {!enrollment && (
                <motion.div variants={cardVariants}>
                  <Card>
                    <CardContent className="p-6">
                      <Button
                        onClick={handleEnrollCourse}
                        disabled={enrolling}
                        className="w-full"
                        size="lg"
                      >
                        <BookOpen className="w-4 h-4 mr-2" />
                        {enrolling ? "注册中..." : "立即注册课程"}
                      </Button>
                    </CardContent>
                  </Card>
                </motion.div>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </StudentLayout>
  );
};

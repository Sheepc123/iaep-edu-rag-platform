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
  CheckCircle,
  Lock,
  FileText,
  Video,
  Award,
  Calendar,
  Globe,
  MessageCircle,
  Share2
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { courseAPI, Course, Lesson, CourseEnrollment, LessonProgress } from "@/services/api";
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

// Mock materials data (这部分可以后续从后端获取)
const mockMaterials = [
  { id: 1, name: "课程教材.pdf", size: "15.2 MB", type: "pdf" },
  { id: 2, name: "课程大纲.docx", size: "2.1 MB", type: "doc" },
  { id: 3, name: "习题集.pdf", size: "8.5 MB", type: "pdf" },
  { id: 4, name: "参考资料.pdf", size: "3.2 MB", type: "pdf" }
];

export const CourseDetail = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = useState("overview");
  const [course, setCourse] = useState<Course | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [enrollment, setEnrollment] = useState<CourseEnrollment | null>(null);
  const [lessonProgresses, setLessonProgresses] = useState<LessonProgress[]>([]);
  const [loading, setLoading] = useState(true);

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

  const handleBack = () => {
    navigate("/student/courses");
  };

  const handleEnrollCourse = async () => {
    if (!courseId) return;

    try {
      const enrollmentData = await courseAPI.enrollCourse(parseInt(courseId));
      setEnrollment(enrollmentData);

      toast({
        title: "注册成功",
        description: "您已成功注册此课程，可以开始学习了！",
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "注册失败",
        description: error.message || "注册课程失败，请稍后重试",
      });
    }
  };

  const handleStartLesson = (lessonId: number) => {
    // 这里可以跳转到具体的课时学习页面
    console.log("开始学习课时:", lessonId);
    // navigate(`/student/lessons/${lessonId}`);
  };

  const handleDownloadMaterial = (materialId: number) => {
    // 这里可以实现下载功能
    console.log("下载资料:", materialId);
  };

  // 获取课时的学习进度
  const getLessonProgress = (lessonId: number) => {
    return lessonProgresses.find(p => p.lesson_id === lessonId);
  };

  if (loading) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">加载课程信息中...</p>
          </div>
        </div>
      </StudentLayout>
    );
  }

  if (!course) {
    return (
      <StudentLayout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">课程不存在</h2>
          <p className="text-gray-600 mb-6">抱歉，您访问的课程不存在或已被删除。</p>
          <Button onClick={handleBack}>返回课程中心</Button>
        </div>
      </StudentLayout>
    );
  }

  return (
    <StudentLayout>
      <motion.div 
        className="space-y-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header */}
        <motion.div variants={cardVariants}>
          <div className="flex items-center space-x-4 mb-6">
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

        {/* Course Hero Section */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg overflow-hidden">
            <div className="relative">
              <img
                src={course.cover_image || "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=400&fit=crop"}
                alt={course.title}
                className="w-full h-64 object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-end">
                <div className="p-8 text-white">
                  <div className="flex items-center space-x-4 mb-4">
                    <Badge variant="secondary" className="bg-white/20 text-white">
                      {course.difficulty}
                    </Badge>
                    {course.category && (
                      <Badge variant="secondary" className="bg-white/20 text-white">
                        {course.category}
                      </Badge>
                    )}
                  </div>
                  <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
                  <div className="flex items-center space-x-6 text-sm">
                    <div className="flex items-center space-x-1">
                      <Users className="w-4 h-4" />
                      <span>{course.enrolled_students} 学生</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span>{course.rating.toFixed(1)}</span>
                    </div>
                    {course.duration && (
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{Math.round(course.duration / 60)} 小时</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Progress Section */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold">
                    {enrollment ? "学习进度" : "课程信息"}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {enrollment
                      ? `已完成 ${enrollment.completed_lessons} / ${course.total_lessons} 课时`
                      : `共 ${course.total_lessons} 课时`
                    }
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-blue-600">
                    {enrollment ? `${Math.round(enrollment.progress_percentage)}%` : "未注册"}
                  </div>
                  <div className="text-sm text-gray-500">
                    {enrollment ? "完成度" : "状态"}
                  </div>
                </div>
              </div>
              {enrollment && (
                <Progress value={enrollment.progress_percentage} className="h-3" />
              )}
              <div className="flex justify-between mt-4">
                {enrollment ? (
                  <Button className="flex-1 mr-2">
                    <PlayCircle className="w-4 h-4 mr-2" />
                    继续学习
                  </Button>
                ) : (
                  <Button className="flex-1 mr-2" onClick={handleEnrollCourse}>
                    <BookOpen className="w-4 h-4 mr-2" />
                    注册课程
                  </Button>
                )}
                <Button variant="outline" className="flex items-center space-x-2">
                  <Share2 className="w-4 h-4" />
                  <span>分享</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Main Content Tabs */}
        <motion.div variants={cardVariants}>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">课程概述</TabsTrigger>
              <TabsTrigger value="chapters">课程内容</TabsTrigger>
              <TabsTrigger value="instructor">授课教师</TabsTrigger>
              <TabsTrigger value="materials">课程资料</TabsTrigger>
            </TabsList>

            {/* 课程概述 */}
            <TabsContent value="overview" className="space-y-6">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle>课程介绍</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">
                    {course.description || "暂无课程描述"}
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <BookOpen className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-blue-600">{course.total_lessons}</div>
                      <div className="text-sm text-gray-600">总课时</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <Clock className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-green-600">
                        {course.duration ? `${Math.round(course.duration / 60)}小时` : "待定"}
                      </div>
                      <div className="text-sm text-gray-600">总时长</div>
                    </div>
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                      <Award className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-purple-600">证书</div>
                      <div className="text-sm text-gray-600">完成获得</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* 课程内容 */}
            <TabsContent value="chapters" className="space-y-6">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>课程内容</span>
                    <Badge variant="outline">
                      {lessons.length} 课时
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {lessons.map((lesson, lessonIndex) => {
                      const progress = getLessonProgress(lesson.id);
                      const isCompleted = progress?.is_completed || false;
                      const canAccess = enrollment && (lesson.is_free || lessonIndex === 0 ||
                        (lessonIndex > 0 && getLessonProgress(lessons[lessonIndex - 1].id)?.is_completed));

                      return (
                        <motion.div
                          key={lesson.id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                          whileHover={{ scale: 1.01 }}
                          whileTap={{ scale: 0.99 }}
                        >
                          <div className="flex items-center space-x-4">
                            <div className="flex-shrink-0">
                              {isCompleted ? (
                                <CheckCircle className="w-6 h-6 text-green-500" />
                              ) : canAccess ? (
                                <PlayCircle className="w-6 h-6 text-blue-500" />
                              ) : (
                                <Lock className="w-6 h-6 text-gray-400" />
                              )}
                            </div>
                            <div className="flex items-center space-x-3">
                              {lesson.lesson_type === "video" ? (
                                <Video className="w-4 h-4 text-gray-500" />
                              ) : (
                                <FileText className="w-4 h-4 text-gray-500" />
                              )}
                              <div>
                                <h4 className="font-medium text-gray-900">{lesson.title}</h4>
                                <div className="flex items-center space-x-2 text-sm text-gray-500">
                                  <Clock className="w-3 h-3" />
                                  <span>{lesson.duration || 0} 分钟</span>
                                  {lesson.is_free && (
                                    <Badge variant="secondary" className="text-xs">免费</Badge>
                                  )}
                                  {progress && progress.progress_percentage > 0 && (
                                    <Badge variant="outline" className="text-xs">
                                      {Math.round(progress.progress_percentage)}%
                                    </Badge>
                                  )}
                                </div>
                              </div>
                            </div>
                          </div>
                          <Button
                            size="sm"
                            variant={isCompleted ? "outline" : "default"}
                            onClick={() => handleStartLesson(lesson.id)}
                            disabled={!canAccess}
                          >
                            {isCompleted ? "重新学习" : "开始学习"}
                          </Button>
                        </motion.div>
                      );
                    })}
                  </div>

                  {!enrollment && (
                    <div className="mt-6 p-4 bg-blue-50 rounded-lg text-center">
                      <p className="text-blue-700 mb-3">注册课程后即可开始学习</p>
                      <Button onClick={handleEnrollCourse}>
                        <BookOpen className="w-4 h-4 mr-2" />
                        立即注册
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* 授课教师 */}
            <TabsContent value="instructor" className="space-y-6">
              <Card className="border-0 shadow-lg">
                <CardContent className="p-8">
                  <div className="flex items-start space-x-6">
                    <Avatar className="w-24 h-24">
                      <AvatarFallback>{course.instructor_name[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">
                        {course.instructor_name}
                      </h3>
                      <p className="text-lg text-gray-600 mb-4">授课教师</p>
                      <p className="text-gray-700 leading-relaxed mb-6">
                        专业的教学团队，致力于为学生提供优质的教学内容和学习体验。
                      </p>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="text-center p-4 bg-blue-50 rounded-lg">
                          <Star className="w-8 h-8 text-yellow-500 mx-auto mb-2 fill-current" />
                          <div className="text-2xl font-bold text-gray-900">{course.rating.toFixed(1)}</div>
                          <div className="text-sm text-gray-600">课程评分</div>
                        </div>
                        <div className="text-center p-4 bg-green-50 rounded-lg">
                          <Users className="w-8 h-8 text-green-600 mx-auto mb-2" />
                          <div className="text-2xl font-bold text-gray-900">{course.enrolled_students}</div>
                          <div className="text-sm text-gray-600">注册学生</div>
                        </div>
                        <div className="text-center p-4 bg-purple-50 rounded-lg">
                          <BookOpen className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                          <div className="text-2xl font-bold text-gray-900">{course.rating_count}</div>
                          <div className="text-sm text-gray-600">评价数量</div>
                        </div>
                      </div>

                      <div className="flex space-x-4 mt-6">
                        <Button variant="outline" className="flex items-center space-x-2">
                          <MessageCircle className="w-4 h-4" />
                          <span>联系教师</span>
                        </Button>
                        <Button variant="outline" className="flex items-center space-x-2">
                          <Globe className="w-4 h-4" />
                          <span>教师主页</span>
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* 课程资料 */}
            <TabsContent value="materials" className="space-y-6">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle>课程资料下载</CardTitle>
                  <p className="text-sm text-gray-600">
                    以下是本课程的相关学习资料，您可以下载到本地进行学习
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {mockMaterials.map((material) => (
                      <motion.div
                        key={material.id}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                        whileHover={{ scale: 1.01 }}
                        whileTap={{ scale: 0.99 }}
                      >
                        <div className="flex items-center space-x-4">
                          <div className="flex-shrink-0">
                            <FileText className="w-8 h-8 text-blue-500" />
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900">{material.name}</h4>
                            <p className="text-sm text-gray-500">大小: {material.size}</p>
                          </div>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDownloadMaterial(material.id)}
                          className="flex items-center space-x-2"
                        >
                          <Download className="w-4 h-4" />
                          <span>下载</span>
                        </Button>
                      </motion.div>
                    ))}
                  </div>

                  <div className="mt-8 p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-start space-x-3">
                      <FileText className="w-5 h-5 text-blue-600 mt-0.5" />
                      <div>
                        <h4 className="font-medium text-blue-900 mb-1">下载说明</h4>
                        <p className="text-sm text-blue-700">
                          • 课程资料仅供学习使用，请勿用于商业用途<br/>
                          • 建议使用最新版本的PDF阅读器打开文档<br/>
                          • 如遇下载问题，请联系客服或教师
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>
      </motion.div>
    </StudentLayout>
  );
};

import TeacherLayout from "@/components/layouts/TeacherLayout";
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
  Calendar,
  Globe,
  MessageCircle,
  Share2,
  Edit3,
  BarChart3,
  Settings
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
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

// Mock data (这部分可以后续从后端获取)
const mockCourse = {
  id: 1,
  title: "React 从入门到精通",
  description: "全面学习React框架，包括组件、状态管理、路由等核心概念。本课程将带您从零开始，逐步掌握React的各个方面，包括JSX语法、组件生命周期、Hooks、状态管理、路由配置等。通过大量的实战项目，您将能够独立开发复杂的React应用程序。",
  category: "编程开发",
  difficulty: "中级",
  duration: 1200,
  totalLessons: 24,
  enrolledStudents: 156,
  rating: 4.8,
  ratingCount: 89,
  coverImage: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800",
  instructor: {
    id: 1,
    name: "张教授",
    avatar: "https://i.pravatar.cc/100?img=1",
    title: "高级前端工程师",
    experience: "8年教学经验",
    students: 2340,
    courses: 12,
    rating: 4.9
  },
  isPublished: true,
  createdAt: "2024-01-15",
  updatedAt: "2024-01-20"
};

const mockLessons = [
  {
    id: 1,
    title: "React 简介与环境搭建",
    description: "了解React的基本概念，学习如何搭建开发环境",
    duration: 45,
    type: "video",
    isFree: true,
    isCompleted: true,
    order: 1
  },
  {
    id: 2,
    title: "JSX 语法详解",
    description: "深入学习JSX语法，理解虚拟DOM的概念",
    duration: 60,
    type: "video",
    isFree: true,
    isCompleted: true,
    order: 2
  },
  {
    id: 3,
    title: "组件基础",
    description: "学习如何创建和使用React组件",
    duration: 75,
    type: "video",
    isFree: false,
    isCompleted: false,
    order: 3
  },
  {
    id: 4,
    title: "Props 和 State",
    description: "理解组件间的数据传递和状态管理",
    duration: 90,
    type: "video",
    isFree: false,
    isCompleted: false,
    order: 4
  },
  {
    id: 5,
    title: "事件处理",
    description: "学习在React中处理用户交互事件",
    duration: 50,
    type: "video",
    isFree: false,
    isCompleted: false,
    order: 5
  }
];

const mockMaterials = [
  { id: 1, name: "React官方文档.pdf", size: "15.2 MB", type: "pdf" },
  { id: 2, name: "课程源代码.zip", size: "2.1 MB", type: "zip" },
  { id: 3, name: "练习题集.pdf", size: "8.5 MB", type: "pdf" },
  { id: 4, name: "参考资料.pdf", size: "3.2 MB", type: "pdf" }
];

export const TeacherCourseDetail = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = useState("overview");
  const [course] = useState(mockCourse);
  const [lessons] = useState(mockLessons);
  const [loading, setLoading] = useState(false);

  // 获取课程数据
  useEffect(() => {
    const fetchCourseData = async () => {
      if (!courseId) return;

      try {
        setLoading(true);
        // 这里应该调用真实的API获取课程数据
        // const courseData = await courseAPI.getCourse(parseInt(courseId));
        // setCourse(courseData);

        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        toast({
          title: "错误",
          description: "获取课程信息失败",
          variant: "destructive"
        });
      } finally {
        setLoading(false);
      }
    };

    fetchCourseData();
  }, [courseId, toast]);

  // 处理编辑课程
  const handleEditCourse = () => {
    navigate(`/teacher/courses/${courseId}/edit`);
  };

  // 处理查看数据分析
  const handleViewAnalytics = () => {
    navigate(`/teacher/courses/${courseId}/analytics`);
  };

  // 处理课程设置
  const handleCourseSettings = () => {
    navigate(`/teacher/courses/${courseId}/settings`);
  };

  // 格式化时长
  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`;
  };

  // 计算完成进度
  const completedLessons = lessons.filter(lesson => lesson.isCompleted).length;
  const progressPercentage = (completedLessons / lessons.length) * 100;

  if (loading) {
    return (
      <TeacherLayout>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
          <div className="max-w-6xl mx-auto">
            <div className="animate-pulse space-y-6">
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-4">
                  <div className="h-32 bg-gray-200 rounded"></div>
                  <div className="h-48 bg-gray-200 rounded"></div>
                </div>
                <div className="space-y-4">
                  <div className="h-32 bg-gray-200 rounded"></div>
                  <div className="h-48 bg-gray-200 rounded"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </TeacherLayout>
    );
  }

  return (
    <TeacherLayout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        <motion.div
          className="max-w-6xl mx-auto"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* 返回按钮 */}
          <motion.div variants={cardVariants} className="mb-6">
            <Button
              variant="ghost"
              onClick={() => navigate("/teacher/courses")}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>返回课程管理</span>
            </Button>
          </motion.div>

          {/* 课程头部信息 */}
          <motion.div variants={cardVariants}>
            <Card className="mb-8 overflow-hidden">
              <div className="relative">
                <div className="h-64 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600">
                  <img
                    src={course.coverImage}
                    alt={course.title}
                    className="w-full h-full object-cover opacity-20"
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                <div className="absolute bottom-0 left-0 right-0 p-8 text-white">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-4">
                        <Badge className="bg-white/20 text-white border-white/30">
                          {course.category}
                        </Badge>
                        <Badge className="bg-white/20 text-white border-white/30">
                          {course.difficulty}
                        </Badge>
                        <Badge className={course.isPublished ? "bg-green-500" : "bg-gray-500"}>
                          {course.isPublished ? "已发布" : "草稿"}
                        </Badge>
                      </div>
                      <h1 className="text-3xl font-bold mb-3">{course.title}</h1>
                      <div className="flex items-center space-x-6 text-white/90">
                        <div className="flex items-center space-x-1">
                          <Users className="w-4 h-4" />
                          <span>{course.enrolledStudents} 学员</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{formatDuration(course.duration)}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <BookOpen className="w-4 h-4" />
                          <span>{course.totalLessons} 课时</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Star className="w-4 h-4 text-yellow-400" />
                          <span>{course.rating} ({course.ratingCount} 评价)</span>
                        </div>
                      </div>
                    </div>

                    {/* 教师操作按钮 */}
                    <div className="flex items-center space-x-3">
                      <Button
                        variant="outline"
                        onClick={handleEditCourse}
                        className="bg-white/10 border-white/20 text-white hover:bg-white/20"
                      >
                        <Edit3 className="w-4 h-4 mr-2" />
                        编辑课程
                      </Button>
                      <Button
                        variant="outline"
                        onClick={handleViewAnalytics}
                        className="bg-white/10 border-white/20 text-white hover:bg-white/20"
                      >
                        <BarChart3 className="w-4 h-4 mr-2" />
                        数据分析
                      </Button>
                      <Button
                        variant="outline"
                        onClick={handleCourseSettings}
                        className="bg-white/10 border-white/20 text-white hover:bg-white/20"
                      >
                        <Settings className="w-4 h-4 mr-2" />
                        课程设置
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>

          {/* 主要内容区域 */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* 左侧主要内容 */}
            <div className="lg:col-span-2">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="overview">课程概述</TabsTrigger>
                  <TabsTrigger value="curriculum">课程内容</TabsTrigger>
                  <TabsTrigger value="materials">课程资料</TabsTrigger>
                  <TabsTrigger value="reviews">学员评价</TabsTrigger>
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
                          学员统计
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-2 gap-6">
                          <div className="text-center p-4 bg-blue-50 rounded-lg">
                            <div className="text-2xl font-bold text-blue-600">{course.enrolledStudents}</div>
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
                            <PlayCircle className="w-5 h-5 mr-2 text-purple-600" />
                            课程大纲 ({lessons.length} 个课时)
                          </div>
                          <div className="text-sm text-gray-500">
                            总时长: {formatDuration(lessons.reduce((total, lesson) => total + lesson.duration, 0))}
                          </div>
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {lessons.map((lesson, index) => (
                            <motion.div
                              key={lesson.id}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.1 }}
                              className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                            >
                              <div className="flex items-center space-x-4">
                                <div className="flex-shrink-0">
                                  {lesson.isCompleted ? (
                                    <CheckCircle className="w-6 h-6 text-green-500" />
                                  ) : lesson.isFree ? (
                                    <PlayCircle className="w-6 h-6 text-blue-500" />
                                  ) : (
                                    <Lock className="w-6 h-6 text-gray-400" />
                                  )}
                                </div>
                                <div className="flex-1">
                                  <h4 className="font-medium text-gray-900">{lesson.title}</h4>
                                  <p className="text-sm text-gray-600">{lesson.description}</p>
                                  <div className="flex items-center space-x-4 mt-2">
                                    <div className="flex items-center text-xs text-gray-500">
                                      <Clock className="w-3 h-3 mr-1" />
                                      {lesson.duration} 分钟
                                    </div>
                                    <div className="flex items-center text-xs text-gray-500">
                                      <Video className="w-3 h-3 mr-1" />
                                      {lesson.type === 'video' ? '视频' : '文档'}
                                    </div>
                                    {lesson.isFree && (
                                      <Badge className="bg-green-100 text-green-800 text-xs">
                                        免费
                                      </Badge>
                                    )}
                                  </div>
                                </div>
                              </div>
                              <div className="flex items-center space-x-2">
                                <Button variant="ghost" size="sm">
                                  <Edit3 className="w-4 h-4" />
                                </Button>
                              </div>
                            </motion.div>
                          ))}
                        </div>
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
                          <Download className="w-5 h-5 mr-2 text-indigo-600" />
                          课程资料
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          {mockMaterials.map((material) => (
                            <div
                              key={material.id}
                              className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 transition-colors"
                            >
                              <div className="flex items-center space-x-3">
                                <FileText className="w-5 h-5 text-gray-500" />
                                <div>
                                  <p className="font-medium text-gray-900">{material.name}</p>
                                  <p className="text-sm text-gray-500">{material.size}</p>
                                </div>
                              </div>
                              <Button variant="ghost" size="sm">
                                <Download className="w-4 h-4" />
                              </Button>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                </TabsContent>

                {/* 学员评价 */}
                <TabsContent value="reviews" className="space-y-6">
                  <motion.div variants={cardVariants}>
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center">
                          <Star className="w-5 h-5 mr-2 text-yellow-600" />
                          学员评价
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-center py-12">
                          <MessageCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                          <h3 className="text-lg font-medium text-gray-900 mb-2">暂无评价</h3>
                          <p className="text-gray-500">学员完成课程后会在这里显示评价</p>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                </TabsContent>
              </Tabs>
            </div>

            {/* 右侧边栏 */}
            <div className="space-y-6">
              {/* 课程进度 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">课程进度</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-sm mb-2">
                          <span>完成进度</span>
                          <span>{Math.round(progressPercentage)}%</span>
                        </div>
                        <Progress value={progressPercentage} className="h-2" />
                      </div>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <div className="text-gray-600">已完成</div>
                          <div className="font-semibold">{completedLessons} 课时</div>
                        </div>
                        <div>
                          <div className="text-gray-600">剩余</div>
                          <div className="font-semibold">{lessons.length - completedLessons} 课时</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* 教师信息 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">教师信息</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center space-x-4 mb-4">
                      <Avatar className="w-16 h-16">
                        <AvatarImage src={course.instructor.avatar} />
                        <AvatarFallback>{course.instructor.name[0]}</AvatarFallback>
                      </Avatar>
                      <div>
                        <h3 className="font-semibold text-gray-900">{course.instructor.name}</h3>
                        <p className="text-sm text-gray-600">{course.instructor.title}</p>
                        <div className="flex items-center mt-1">
                          <Star className="w-4 h-4 text-yellow-500 mr-1" />
                          <span className="text-sm text-gray-600">{course.instructor.rating}</span>
                        </div>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">学生数量</div>
                        <div className="font-semibold">{course.instructor.students}</div>
                      </div>
                      <div>
                        <div className="text-gray-600">课程数量</div>
                        <div className="font-semibold">{course.instructor.courses}</div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mt-4">{course.instructor.experience}</p>
                  </CardContent>
                </Card>
              </motion.div>

              {/* 课程统计 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">课程统计</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Users className="w-4 h-4 text-blue-600" />
                          <span className="text-sm">注册学员</span>
                        </div>
                        <span className="font-semibold">{course.enrolledStudents}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Star className="w-4 h-4 text-yellow-600" />
                          <span className="text-sm">课程评分</span>
                        </div>
                        <span className="font-semibold">{course.rating}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <MessageCircle className="w-4 h-4 text-green-600" />
                          <span className="text-sm">评价数量</span>
                        </div>
                        <span className="font-semibold">{course.ratingCount}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Calendar className="w-4 h-4 text-purple-600" />
                          <span className="text-sm">创建时间</span>
                        </div>
                        <span className="font-semibold text-sm">{course.createdAt}</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* 快速操作 */}
              <motion.div variants={cardVariants}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">快速操作</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <Button
                        onClick={handleEditCourse}
                        className="w-full justify-start"
                        variant="outline"
                      >
                        <Edit3 className="w-4 h-4 mr-2" />
                        编辑课程
                      </Button>
                      <Button
                        onClick={handleViewAnalytics}
                        className="w-full justify-start"
                        variant="outline"
                      >
                        <BarChart3 className="w-4 h-4 mr-2" />
                        查看数据
                      </Button>
                      <Button
                        onClick={handleCourseSettings}
                        className="w-full justify-start"
                        variant="outline"
                      >
                        <Settings className="w-4 h-4 mr-2" />
                        课程设置
                      </Button>
                      <Button
                        className="w-full justify-start"
                        variant="outline"
                      >
                        <Share2 className="w-4 h-4 mr-2" />
                        分享课程
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </TeacherLayout>
  );
};

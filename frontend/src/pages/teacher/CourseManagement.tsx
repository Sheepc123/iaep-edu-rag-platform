import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Plus,
  Search,
  Filter,
  Edit3,
  Eye,
  Trash2,
  Users,
  Clock,
  Star,
  MoreVertical,
  Globe,
  FileText,
  BarChart3,
  Settings
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { useToast } from "@/components/ui/use-toast";
import TeacherLayout from "@/components/layouts/TeacherLayout";

interface Course {
  id: number;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  duration: number;
  coverImage: string;
  enrolledStudents: number;
  rating: number;
  ratingCount: number;
  isPublished: boolean;
  totalLessons: number;
  createdAt: string;
  updatedAt: string;
}

export const TeacherCourseManagement = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");

  // 模拟课程数据
  const mockCourses: Course[] = [
    {
      id: 1,
      title: "React 从入门到精通",
      description: "全面学习React框架，包括组件、状态管理、路由等核心概念",
      category: "programming",
      difficulty: "medium",
      duration: 1200,
      coverImage: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400",
      enrolledStudents: 156,
      rating: 4.8,
      ratingCount: 89,
      isPublished: true,
      totalLessons: 24,
      createdAt: "2024-01-15",
      updatedAt: "2024-01-20"
    },
    {
      id: 2,
      title: "Python 数据分析实战",
      description: "使用Python进行数据分析，包括pandas、numpy、matplotlib等库的使用",
      category: "programming",
      difficulty: "hard",
      duration: 1800,
      coverImage: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400",
      enrolledStudents: 89,
      rating: 4.6,
      ratingCount: 45,
      isPublished: true,
      totalLessons: 32,
      createdAt: "2024-01-10",
      updatedAt: "2024-01-18"
    },
    {
      id: 3,
      title: "UI/UX 设计基础",
      description: "学习用户界面和用户体验设计的基本原理和实践方法",
      category: "design",
      difficulty: "easy",
      duration: 900,
      coverImage: "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400",
      enrolledStudents: 234,
      rating: 4.9,
      ratingCount: 156,
      isPublished: true,
      totalLessons: 18,
      createdAt: "2024-01-05",
      updatedAt: "2024-01-15"
    },
    {
      id: 4,
      title: "机器学习算法详解",
      description: "深入理解机器学习算法的原理和应用",
      category: "science",
      difficulty: "hard",
      duration: 2400,
      coverImage: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400",
      enrolledStudents: 0,
      rating: 0,
      ratingCount: 0,
      isPublished: false,
      totalLessons: 15,
      createdAt: "2024-01-25",
      updatedAt: "2024-01-25"
    }
  ];

  // 课程分类选项
  const categories = [
    { value: "all", label: "全部分类" },
    { value: "programming", label: "编程开发" },
    { value: "design", label: "设计创意" },
    { value: "business", label: "商业管理" },
    { value: "language", label: "语言学习" },
    { value: "science", label: "科学技术" },
    { value: "art", label: "艺术人文" }
  ];

  // 状态选项
  const statusOptions = [
    { value: "all", label: "全部状态" },
    { value: "published", label: "已发布" },
    { value: "draft", label: "草稿" }
  ];

  // 难度级别配置
  const difficultyConfig = {
    easy: { label: "初级", color: "bg-green-100 text-green-800" },
    medium: { label: "中级", color: "bg-yellow-100 text-yellow-800" },
    hard: { label: "高级", color: "bg-red-100 text-red-800" }
  };

  // 获取课程数据
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        // 这里应该调用真实的API
        // const response = await courseAPI.getTeacherCourses();
        // setCourses(response);
        
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 1000));
        setCourses(mockCourses);
      } catch (error) {
        toast({
          title: "错误",
          description: "获取课程列表失败",
          variant: "destructive"
        });
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, [toast]);

  // 过滤课程
  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === "all" || course.category === filterCategory;
    const matchesStatus = filterStatus === "all" || 
                         (filterStatus === "published" && course.isPublished) ||
                         (filterStatus === "draft" && !course.isPublished);
    
    return matchesSearch && matchesCategory && matchesStatus;
  });

  // 处理课程操作
  const handleEditCourse = (courseId: number) => {
    navigate(`/teacher/courses/${courseId}/edit`);
  };

  const handleViewCourse = (courseId: number) => {
    navigate(`/teacher/courses/${courseId}`);
  };

  const handleDeleteCourse = async (courseId: number) => {
    try {
      // 这里应该调用删除API
      // await courseAPI.deleteCourse(courseId);
      
      setCourses(prev => prev.filter(course => course.id !== courseId));
      toast({
        title: "成功",
        description: "课程已删除"
      });
    } catch (error) {
      toast({
        title: "错误",
        description: "删除课程失败",
        variant: "destructive"
      });
    }
  };

  const handleTogglePublish = async (courseId: number, isPublished: boolean) => {
    try {
      // 这里应该调用发布/取消发布API
      // await courseAPI.togglePublish(courseId, !isPublished);
      
      setCourses(prev => prev.map(course => 
        course.id === courseId 
          ? { ...course, isPublished: !isPublished }
          : course
      ));
      
      toast({
        title: "成功",
        description: isPublished ? "课程已取消发布" : "课程已发布"
      });
    } catch (error) {
      toast({
        title: "错误",
        description: "操作失败",
        variant: "destructive"
      });
    }
  };

  // 格式化时长
  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`;
  };

  return (
    <TeacherLayout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        {/* 头部 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <BookOpen className="w-8 h-8 mr-3 text-blue-600" />
                课程管理
              </h1>
              <p className="text-gray-600 mt-1">管理您的所有课程内容</p>
            </div>
            
            <Button
              onClick={() => navigate("/teacher/courses/create")}
              className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              <Plus className="w-4 h-4" />
              <span>创建新课程</span>
            </Button>
          </div>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">总课程数</p>
                    <p className="text-2xl font-bold text-gray-900">{courses.length}</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <BookOpen className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">已发布</p>
                    <p className="text-2xl font-bold text-green-600">
                      {courses.filter(c => c.isPublished).length}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                    <Globe className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">总学员数</p>
                    <p className="text-2xl font-bold text-purple-600">
                      {courses.reduce((total, course) => total + course.enrolledStudents, 0)}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                    <Users className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">平均评分</p>
                    <p className="text-2xl font-bold text-yellow-600">
                      {courses.length > 0 
                        ? (courses.reduce((total, course) => total + course.rating, 0) / courses.filter(c => c.rating > 0).length || 0).toFixed(1)
                        : "0.0"
                      }
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                    <Star className="w-6 h-6 text-yellow-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* 搜索和过滤 */}
        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="搜索课程标题或描述..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={filterCategory} onValueChange={setFilterCategory}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category.value} value={category.value}>
                      {category.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {statusOptions.map((status) => (
                    <SelectItem key={status.value} value={status.value}>
                      {status.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* 课程列表 */}
        <div className="space-y-6">
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <Card key={i} className="animate-pulse">
                  <div className="h-48 bg-gray-200 rounded-t-lg"></div>
                  <CardContent className="p-6">
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded mb-4"></div>
                    <div className="flex justify-between">
                      <div className="h-3 bg-gray-200 rounded w-16"></div>
                      <div className="h-3 bg-gray-200 rounded w-20"></div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : filteredCourses.length === 0 ? (
            <Card>
              <CardContent className="p-12 text-center">
                <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {searchTerm || filterCategory !== "all" || filterStatus !== "all"
                    ? "没有找到匹配的课程"
                    : "还没有创建课程"
                  }
                </h3>
                <p className="text-gray-500 mb-4">
                  {searchTerm || filterCategory !== "all" || filterStatus !== "all"
                    ? "尝试调整搜索条件或过滤器"
                    : "开始创建您的第一个课程吧"
                  }
                </p>
                {!searchTerm && filterCategory === "all" && filterStatus === "all" && (
                  <Button
                    onClick={() => navigate("/teacher/courses/create")}
                    className="flex items-center space-x-2"
                  >
                    <Plus className="w-4 h-4" />
                    <span>创建新课程</span>
                  </Button>
                )}
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <AnimatePresence>
                {filteredCourses.map((course, index) => (
                  <motion.div
                    key={course.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <Card className="group hover:shadow-lg transition-all duration-300 overflow-hidden">
                      {/* 课程封面 */}
                      <div className="relative h-48 overflow-hidden">
                        <img
                          src={course.coverImage}
                          alt={course.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={(e) => {
                            e.currentTarget.src = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400";
                          }}
                        />
                        <div className="absolute top-4 left-4">
                          <Badge className={course.isPublished ? "bg-green-500" : "bg-gray-500"}>
                            {course.isPublished ? "已发布" : "草稿"}
                          </Badge>
                        </div>
                        <div className="absolute top-4 right-4">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="bg-white/80 hover:bg-white"
                              >
                                <MoreVertical className="w-4 h-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem onClick={() => handleViewCourse(course.id)}>
                                <Eye className="w-4 h-4 mr-2" />
                                查看详情
                              </DropdownMenuItem>
                              <DropdownMenuItem onClick={() => handleEditCourse(course.id)}>
                                <Edit3 className="w-4 h-4 mr-2" />
                                编辑课程
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleTogglePublish(course.id, course.isPublished)}
                              >
                                <Globe className="w-4 h-4 mr-2" />
                                {course.isPublished ? "取消发布" : "发布课程"}
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleDeleteCourse(course.id)}
                                className="text-red-600"
                              >
                                <Trash2 className="w-4 h-4 mr-2" />
                                删除课程
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </div>
                      </div>

                      {/* 课程信息 */}
                      <CardContent className="p-6">
                        <div className="space-y-4">
                          {/* 标题和描述 */}
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                              {course.title}
                            </h3>
                            <p className="text-sm text-gray-600 line-clamp-2">
                              {course.description}
                            </p>
                          </div>

                          {/* 难度和分类 */}
                          <div className="flex items-center space-x-2">
                            <Badge className={difficultyConfig[course.difficulty as keyof typeof difficultyConfig]?.color}>
                              {difficultyConfig[course.difficulty as keyof typeof difficultyConfig]?.label}
                            </Badge>
                            <Badge variant="outline">
                              {categories.find(c => c.value === course.category)?.label}
                            </Badge>
                          </div>

                          {/* 统计信息 */}
                          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                            <div className="flex items-center space-x-1">
                              <Users className="w-4 h-4" />
                              <span>{course.enrolledStudents} 学员</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Clock className="w-4 h-4" />
                              <span>{formatDuration(course.duration)}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <FileText className="w-4 h-4" />
                              <span>{course.totalLessons} 课时</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Star className="w-4 h-4 text-yellow-500" />
                              <span>
                                {course.rating > 0 ? course.rating.toFixed(1) : "暂无评分"}
                              </span>
                            </div>
                          </div>

                          {/* 操作按钮 */}
                          <div className="flex items-center space-x-2 pt-4 border-t">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleViewCourse(course.id)}
                              className="flex-1"
                            >
                              <Eye className="w-4 h-4 mr-1" />
                              查看
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleEditCourse(course.id)}
                              className="flex-1"
                            >
                              <Edit3 className="w-4 h-4 mr-1" />
                              编辑
                            </Button>
                            <Button
                              size="sm"
                              onClick={() => navigate(`/teacher/courses/${course.id}/analytics`)}
                              className="flex-1"
                            >
                              <BarChart3 className="w-4 h-4 mr-1" />
                              数据
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          )}
        </div>
      </div>
    </TeacherLayout>
  );
};

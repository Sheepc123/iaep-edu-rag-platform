import StudentLayout from "@/components/layouts/StudentLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  BookOpen,
  Clock,
  Users,
  Star,
  PlayCircle,
  Calendar,
  Filter,
  Search,
  ChevronRight,
  Award,
  TrendingUp,
  ChevronLeft,
  Loader2,
  Heart,
  Eye,
  CheckCircle,
  Plus
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { courseAPI, Course } from "@/services/api";
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

const hoverVariants = {
  hover: {
    scale: 1.02,
    y: -5,
    transition: {
      type: "spring",
      stiffness: 400,
      damping: 10
    }
  }
};



export const Courses = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCourses, setTotalCourses] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("");
  const [showFilters, setShowFilters] = useState(false);

  const { toast } = useToast();
  const navigate = useNavigate();

  const coursesPerPage = 12;
  const categories = ["数学基础", "编程语言", "计算机科学", "Web开发", "人工智能", "数据科学"];
  const difficulties = ["easy", "medium", "hard"];

  // 获取课程数据
  const fetchCourses = async (page: number = 1, reset: boolean = false) => {
    try {
      setLoading(true);

      const params = {
        skip: (page - 1) * coursesPerPage,
        limit: coursesPerPage,
        is_published: true,
        sort_by: "created_at",
        sort_order: "desc",
        ...(searchTerm && { search: searchTerm }),
        ...(selectedCategory && { category: selectedCategory }),
        ...(selectedDifficulty && { difficulty: selectedDifficulty })
      };

      console.log("🔍 正在获取课程数据，参数:", params);
      const response = await courseAPI.getCourses(params);
      console.log("📚 API响应:", response);

      if (reset || page === 1) {
        setCourses(response.courses);
      } else {
        setCourses(prev => [...prev, ...response.courses]);
      }

      setTotalCourses(response.total);
      setHasMore(response.has_more);
      setCurrentPage(page);

      console.log(`✅ 成功加载 ${response.courses.length} 门课程，总共 ${response.total} 门`);

    } catch (error: any) {
      console.error("❌ 获取课程失败:", error);
      console.error("错误详情:", error.response?.data || error.message);
      toast({
        variant: "destructive",
        title: "加载失败",
        description: `无法加载课程数据: ${error.response?.data?.detail || error.message || "请稍后重试"}`,
      });
    } finally {
      setLoading(false);
    }
  };

  // 初始加载课程数据
  useEffect(() => {
    fetchCourses(1, true);
  }, [searchTerm, selectedCategory, selectedDifficulty]);

  // 处理搜索
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchCourses(1, true);
  };

  // 处理筛选
  const handleFilter = (category: string, difficulty: string) => {
    setSelectedCategory(category);
    setSelectedDifficulty(difficulty);
    setCurrentPage(1);
  };

  // 加载更多课程
  const loadMoreCourses = () => {
    if (hasMore && !loading) {
      fetchCourses(currentPage + 1, false);
    }
  };

  // 清除筛选条件
  const clearFilters = () => {
    setSearchTerm("");
    setSelectedCategory("");
    setSelectedDifficulty("");
    setCurrentPage(1);
  };

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
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">课程中心</h1>
                <p className="text-gray-600 mt-2">探索和学习您感兴趣的课程 - 共 {totalCourses} 门课程</p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
              >
                <Filter className="w-4 h-4 mr-2" />
                筛选
              </Button>
            </div>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="flex gap-2">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="搜索课程..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <Button type="submit" size="sm">
                搜索
              </Button>
              {(searchTerm || selectedCategory || selectedDifficulty) && (
                <Button type="button" variant="outline" size="sm" onClick={clearFilters}>
                  清除
                </Button>
              )}
            </form>

            {/* Filters */}
            {showFilters && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="p-4 bg-gray-50 rounded-lg space-y-4"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">课程分类</label>
                    <select
                      value={selectedCategory}
                      onChange={(e) => handleFilter(e.target.value, selectedDifficulty)}
                      className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">全部分类</option>
                      {categories.map(category => (
                        <option key={category} value={category}>{category}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">难度级别</label>
                    <select
                      value={selectedDifficulty}
                      onChange={(e) => handleFilter(selectedCategory, e.target.value)}
                      className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">全部难度</option>
                      <option value="easy">简单</option>
                      <option value="medium">中等</option>
                      <option value="hard">困难</option>
                    </select>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </motion.div>

        {/* Stats Overview */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-4 gap-6"
          variants={containerVariants}
        >
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<BookOpen className="w-6 h-6" />}
              title="已注册课程"
              value="3"
              subtitle="门课程"
              color="blue"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<TrendingUp className="w-6 h-6" />}
              title="平均进度"
              value="58%"
              subtitle="完成度"
              color="green"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<Clock className="w-6 h-6" />}
              title="学习时长"
              value="24.5"
              subtitle="小时"
              color="purple"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<Award className="w-6 h-6" />}
              title="获得证书"
              value="1"
              subtitle="个证书"
              color="orange"
            />
          </motion.div>
        </motion.div>

        {/* Course Grid */}
        {loading && courses.length === 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {[...Array(6)].map((_, index) => (
              <div key={index} className="animate-pulse">
                <div className="bg-gray-200 h-64 rounded-lg mb-4"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        ) : courses.length > 0 ? (
          <>
            <motion.div
              className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8"
              variants={containerVariants}
            >
              {courses.map((course, index) => (
                <motion.div
                  key={course.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover="hover"
                  variants={hoverVariants}
                >
                  <CourseCard course={course} />
                </motion.div>
              ))}
            </motion.div>

            {/* Load More Button */}
            {hasMore && (
              <div className="text-center">
                <Button
                  onClick={loadMoreCourses}
                  disabled={loading}
                  variant="outline"
                  className="min-w-32"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      加载中...
                    </>
                  ) : (
                    "加载更多"
                  )}
                </Button>
              </div>
            )}

            {/* Pagination Info */}
            <div className="text-center text-sm text-gray-500">
              已显示 {courses.length} / {totalCourses} 门课程
            </div>
          </>
        ) : (
          <div className="text-center py-12">
            <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">暂无课程</h3>
            <p className="text-gray-500">没有找到符合条件的课程，请尝试调整搜索条件</p>
          </div>
        )}
      </motion.div>
    </StudentLayout>
  );
};

// Stats Card Component
interface StatsCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  subtitle: string;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

const StatsCard = ({ icon, title, value, subtitle, color }: StatsCardProps) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600 text-blue-600',
    green: 'from-green-500 to-green-600 text-green-600',
    purple: 'from-purple-500 to-purple-600 text-purple-600',
    orange: 'from-orange-500 to-orange-600 text-orange-600'
  };

  return (
    <motion.div
      whileHover="hover"
      variants={hoverVariants}
    >
      <Card className="border-0 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className={`p-3 rounded-xl bg-gradient-to-br ${colorClasses[color]} text-white`}>
              {icon}
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline space-x-1">
              <motion.span 
                className="text-2xl font-bold text-gray-900"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
              >
                {value}
              </motion.span>
              <span className="text-sm text-gray-500">{subtitle}</span>
            </div>
            <p className="text-sm text-gray-600 mt-1">{title}</p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

// Course Card Component
interface CourseCardProps {
  course: Course;
}

const CourseCard = ({ course }: CourseCardProps) => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isEnrolling, setIsEnrolling] = useState(false);

  const difficultyLabels = {
    easy: "简单",
    medium: "中等",
    hard: "困难"
  };

  const difficultyColors = {
    easy: "bg-green-100 text-green-600",
    medium: "bg-yellow-100 text-yellow-600",
    hard: "bg-red-100 text-red-600"
  };

  const handleViewCourse = () => {
    navigate(`/student/courses/${course.id}`);
  };

  const handleEnrollCourse = async (e: React.MouseEvent) => {
    e.stopPropagation();

    if (course.is_enrolled) {
      // 如果已注册，直接跳转到课程页面
      handleViewCourse();
      return;
    }

    try {
      setIsEnrolling(true);
      await courseAPI.enrollCourse(course.id);

      toast({
        title: "注册成功",
        description: `您已成功注册课程：${course.title}`,
      });

      // 刷新页面数据
      window.location.reload();
    } catch (error) {
      console.error('注册课程失败:', error);
      toast({
        title: "注册失败",
        description: "注册课程时发生错误，请稍后重试",
        variant: "destructive",
      });
    } finally {
      setIsEnrolling(false);
    }
  };

  return (
    <Card className="border-0 shadow-lg overflow-hidden h-full hover:shadow-xl transition-all duration-300">
      <div className="relative">
        <img
          src={course.cover_image || "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=200&fit=crop"}
          alt={course.title}
          className="w-full h-48 object-cover"
        />
        <div className="absolute top-4 right-4">
          <Badge
            variant="secondary"
            className={difficultyColors[course.difficulty as keyof typeof difficultyColors] || difficultyColors.medium}
          >
            {difficultyLabels[course.difficulty as keyof typeof difficultyLabels] || course.difficulty}
          </Badge>
        </div>
        {course.category && (
          <div className="absolute top-4 left-4">
            <Badge variant="secondary" className="bg-white/90 text-gray-700">
              {course.category}
            </Badge>
          </div>
        )}
      </div>

      <CardContent className="p-6">
        <div className="space-y-4">
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">{course.title}</h3>
            <p className="text-sm text-gray-600 line-clamp-2">{course.description}</p>
          </div>

          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-1">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              <span>{course.rating.toFixed(1)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Users className="w-4 h-4" />
              <span>{course.enrolled_students} 学生</span>
            </div>
            {course.duration && (
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{Math.round(course.duration / 60)}h</span>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between pt-4 border-t">
            <div className="text-sm text-gray-600">
              <span className="font-medium">{course.instructor_name}</span>
            </div>
            <div className="text-sm text-gray-500">
              {course.total_lessons} 课时
            </div>
          </div>

          <div className="flex space-x-2 pt-2">
            {course.is_enrolled ? (
              <>
                <Button className="flex-1" size="sm" onClick={handleViewCourse}>
                  <PlayCircle className="w-4 h-4 mr-2" />
                  继续学习
                </Button>
                <Button variant="outline" size="sm" onClick={handleViewCourse}>
                  <CheckCircle className="w-4 h-4 text-green-600" />
                </Button>
              </>
            ) : (
              <>
                <Button
                  className="flex-1"
                  size="sm"
                  onClick={handleEnrollCourse}
                  disabled={isEnrolling}
                >
                  {isEnrolling ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      注册中...
                    </>
                  ) : (
                    <>
                      <Plus className="w-4 h-4 mr-2" />
                      注册课程
                    </>
                  )}
                </Button>
                <Button variant="outline" size="sm" onClick={handleViewCourse}>
                  <Eye className="w-4 h-4" />
                </Button>
              </>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

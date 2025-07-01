import TeacherLayout from "@/components/layouts/TeacherLayout";
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
  Plus,
  Edit,
  Trash2,
  MoreHorizontal,
  PlusCircle
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { courseAPI, teacherAPI, Course } from "@/services/api";
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

export const TeacherCourses = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState<"all" | "published" | "draft">("all");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const { toast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    fetchCourses();
  }, [filterStatus, selectedCategory]);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      const response = await teacherAPI.getCourses({
        is_published: filterStatus === "all" ? undefined : filterStatus === "published",
        search: searchTerm || undefined,
        category: selectedCategory === "all" ? undefined : selectedCategory,
        limit: 50
      });
      setCourses(response.courses);
    } catch (error) {
      console.error('获取课程列表失败:', error);
      toast({
        title: "加载失败",
        description: "无法获取课程列表，请稍后重试",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    fetchCourses();
  };

  const handleDelete = async (courseId: number) => {
    if (!confirm('确定要删除这个课程吗？此操作不可撤销。')) {
      return;
    }

    try {
      await courseAPI.deleteCourse(courseId);
      toast({
        title: "删除成功",
        description: "课程已成功删除",
      });
      fetchCourses();
    } catch (error) {
      console.error('删除课程失败:', error);
      toast({
        title: "删除失败",
        description: "无法删除课程，请稍后重试",
        variant: "destructive",
      });
    }
  };

  const categories = [
    { id: "all", name: "全部课程" },
    { id: "programming", name: "编程开发" },
    { id: "design", name: "设计创意" },
    { id: "business", name: "商业管理" },
    { id: "language", name: "语言学习" },
    { id: "science", name: "科学技术" }
  ];

  if (loading) {
    return (
      <TeacherLayout>
        <div className="flex items-center justify-center h-64">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
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
        {/* Header Section */}
        <motion.div variants={cardVariants}>
          <HeaderSection />
        </motion.div>

        {/* Filters Section */}
        <motion.div variants={cardVariants}>
          <FiltersSection
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            filterStatus={filterStatus}
            setFilterStatus={setFilterStatus}
            selectedCategory={selectedCategory}
            setSelectedCategory={setSelectedCategory}
            categories={categories}
            onSearch={handleSearch}
          />
        </motion.div>

        {/* Courses Grid */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          variants={containerVariants}
        >
          {courses.length > 0 ? (
            courses.map((course) => (
              <motion.div key={course.id} variants={cardVariants}>
                <CourseCard course={course} onDelete={handleDelete} />
              </motion.div>
            ))
          ) : (
            <motion.div variants={cardVariants} className="col-span-full">
              <EmptyState />
            </motion.div>
          )}
        </motion.div>
      </motion.div>
    </TeacherLayout>
  );
};

// Header Section Component
const HeaderSection = () => {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">课程管理</h1>
        <p className="text-gray-600 text-lg">创建和管理您的教学课程</p>
      </div>
      <Button asChild size="lg" className="bg-blue-600 hover:bg-blue-700">
        <Link to="/teacher/courses/create">
          <PlusCircle className="mr-2 w-5 h-5" />
          创建新课程
        </Link>
      </Button>
    </div>
  );
};

// Filters Section Component
const FiltersSection = ({
  searchTerm,
  setSearchTerm,
  filterStatus,
  setFilterStatus,
  selectedCategory,
  setSelectedCategory,
  categories,
  onSearch
}: {
  searchTerm: string;
  setSearchTerm: (value: string) => void;
  filterStatus: string;
  setFilterStatus: (value: any) => void;
  selectedCategory: string;
  setSelectedCategory: (value: string) => void;
  categories: Array<{id: string, name: string}>;
  onSearch: () => void;
}) => {
  return (
    <Card className="border-0 shadow-lg">
      <CardContent className="p-6">
        <div className="space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="搜索课程名称、描述..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && onSearch()}
              className="w-full pl-12 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>

          {/* Category Filters */}
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  selectedCategory === category.id
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>

          {/* Status Filter */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">状态筛选:</span>
            </div>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">全部状态</option>
              <option value="published">已发布</option>
              <option value="draft">草稿</option>
            </select>
            <Button onClick={onSearch} className="ml-auto">
              应用筛选
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Course Card Component
const CourseCard = ({ course, onDelete }: { course: Course; onDelete: (id: number) => void }) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyText = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return '简单';
      case 'medium': return '中等';
      case 'hard': return '困难';
      default: return difficulty;
    }
  };

  return (
    <motion.div
      variants={hoverVariants}
      whileHover="hover"
      className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
    >
      {/* Course Image */}
      <div className="relative h-48 bg-gradient-to-br from-blue-500 to-purple-600">
        <div className="absolute inset-0 bg-black bg-opacity-20"></div>
        <div className="absolute top-4 left-4">
          <Badge className={getDifficultyColor(course.difficulty)}>
            {getDifficultyText(course.difficulty)}
          </Badge>
        </div>
        <div className="absolute top-4 right-4">
          <Badge variant={course.is_published ? "default" : "secondary"}>
            {course.is_published ? "已发布" : "草稿"}
          </Badge>
        </div>
        <div className="absolute bottom-4 left-4 right-4">
          <h3 className="text-white text-xl font-bold line-clamp-2">
            {course.title}
          </h3>
        </div>
      </div>

      {/* Course Content */}
      <div className="p-6">
        <p className="text-gray-600 text-sm line-clamp-3 mb-4">
          {course.description || "暂无课程描述"}
        </p>

        {/* Course Stats */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-6">
          <div className="flex items-center space-x-1">
            <Users className="w-4 h-4" />
            <span>{course.enrolled_students}</span>
          </div>
          <div className="flex items-center space-x-1">
            <BookOpen className="w-4 h-4" />
            <span>{course.total_lessons} 课时</span>
          </div>
          <div className="flex items-center space-x-1">
            <Star className="w-4 h-4 text-yellow-500" />
            <span>{course.rating.toFixed(1)}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button asChild size="sm" variant="outline" className="flex-1">
            <Link to={`/teacher/courses/${course.id}`}>
              <Eye className="mr-1 w-3 h-3" />
              查看
            </Link>
          </Button>
          <Button asChild size="sm" variant="outline" className="flex-1">
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onDelete(course.id)}
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <Trash2 className="w-3 h-3" />
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

// Empty State Component
const EmptyState = () => {
  return (
    <Card className="border-0 shadow-lg">
      <CardContent className="text-center py-16">
        <div className="max-w-md mx-auto">
          <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <BookOpen className="w-12 h-12 text-blue-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-4">还没有课程</h3>
          <p className="text-gray-600 mb-8 text-lg">
            开始创建您的第一个课程，与学生分享知识和经验
          </p>
          <Button asChild size="lg" className="bg-blue-600 hover:bg-blue-700">
            <Link to="/teacher/courses/create">
              <PlusCircle className="mr-2 w-5 h-5" />
              创建第一个课程
            </Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

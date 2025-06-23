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
  TrendingUp
} from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

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

// Mock data
const courses = [
  {
    id: 1,
    title: "高等数学 (上)",
    instructor: "李教授",
    progress: 75,
    totalLessons: 24,
    completedLessons: 18,
    rating: 4.8,
    students: 156,
    duration: "16周",
    difficulty: "中级",
    category: "数学基础",
    nextClass: "2024-03-15 14:00",
    description: "涵盖极限、导数、积分等核心概念，为后续数学课程打下坚实基础。",
    image: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=200&fit=crop"
  },
  {
    id: 2,
    title: "线性代数",
    instructor: "王教授",
    progress: 40,
    totalLessons: 20,
    completedLessons: 8,
    rating: 4.6,
    students: 142,
    duration: "12周",
    difficulty: "中级",
    category: "数学基础",
    nextClass: "2024-03-16 10:00",
    description: "学习矩阵运算、线性方程组、特征值等重要概念。",
    image: "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400&h=200&fit=crop"
  },
  {
    id: 3,
    title: "概率论与数理统计",
    instructor: "张教授",
    progress: 60,
    totalLessons: 18,
    completedLessons: 11,
    rating: 4.7,
    students: 128,
    duration: "14周",
    difficulty: "高级",
    category: "统计学",
    nextClass: "2024-03-17 16:00",
    description: "掌握概率分布、假设检验、回归分析等统计方法。",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=200&fit=crop"
  }
];

export const Courses = () => {
  const [filter, setFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

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
            <div>
              <h1 className="text-3xl font-bold text-gray-900">课程中心</h1>
              <p className="text-gray-600 mt-2">探索和学习您感兴趣的课程</p>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Filter className="w-4 h-4 mr-2" />
                筛选
              </Button>
              <Button variant="outline" size="sm">
                <Search className="w-4 h-4 mr-2" />
                搜索
              </Button>
            </div>
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
        <motion.div 
          className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8"
          variants={containerVariants}
        >
          {courses.map((course, index) => (
            <motion.div
              key={course.id}
              variants={cardVariants}
              whileHover="hover"
            >
              <CourseCard course={course} />
            </motion.div>
          ))}
        </motion.div>
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
  course: typeof courses[0];
}

const CourseCard = ({ course }: CourseCardProps) => {
  const difficultyColors = {
    '初级': 'bg-green-100 text-green-600',
    '中级': 'bg-yellow-100 text-yellow-600',
    '高级': 'bg-red-100 text-red-600'
  };

  return (
    <motion.div
      whileHover="hover"
      variants={hoverVariants}
    >
      <Card className="border-0 shadow-lg overflow-hidden h-full">
        <div className="relative">
          <img 
            src={course.image} 
            alt={course.title}
            className="w-full h-48 object-cover"
          />
          <div className="absolute top-4 right-4">
            <Badge 
              variant="secondary" 
              className={difficultyColors[course.difficulty as keyof typeof difficultyColors]}
            >
              {course.difficulty}
            </Badge>
          </div>
        </div>
        
        <CardContent className="p-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">{course.title}</h3>
              <p className="text-sm text-gray-600 line-clamp-2">{course.description}</p>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <Users className="w-4 h-4" />
                <span>{course.students}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                <span>{course.rating}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{course.duration}</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">学习进度</span>
                <span className="font-medium">{course.completedLessons}/{course.totalLessons} 课时</span>
              </div>
              <Progress value={course.progress} className="h-2" />
              <div className="text-right">
                <span className="text-sm font-medium text-gray-900">{course.progress}% 完成</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t">
              <div className="text-sm text-gray-500">
                <Calendar className="w-4 h-4 inline mr-1" />
                下次课程：{course.nextClass}
              </div>
            </div>

            <div className="flex space-x-2 pt-2">
              <Button className="flex-1" size="sm">
                <PlayCircle className="w-4 h-4 mr-2" />
                继续学习
              </Button>
              <Button variant="outline" size="sm">
                详情 <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

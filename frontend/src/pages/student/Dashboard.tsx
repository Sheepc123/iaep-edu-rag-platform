import StudentLayout from "@/components/layouts/StudentLayout";
import { AbilityRadarChart } from "@/components/charts/AbilityRadarChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  BookOpen,
  Clock,
  Zap,
  Lightbulb,
  TrendingUp,
  Calendar,
  Target,
  Award,
  PlayCircle,
  ChevronRight,
  Star,
  Brain,
  Timer,
  BookMarked
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { courseAPI, CourseEnrollment } from "@/services/api";
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

// Main Dashboard Component
export const Dashboard = () => {
  return (
    <StudentLayout>
      <motion.div
        className="space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header Section */}
        <motion.div variants={cardVariants}>
          <WelcomeSection />
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          variants={containerVariants}
        >
          <motion.div variants={cardVariants}>
            <StatCard
              icon={<Timer className="w-6 h-6" />}
              title="今日学习"
              value="2.5"
              unit="小时"
              trend="+12%"
              color="blue"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatCard
              icon={<Target className="w-6 h-6" />}
              title="完成任务"
              value="8"
              unit="个"
              trend="+25%"
              color="green"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatCard
              icon={<Award className="w-6 h-6" />}
              title="平均得分"
              value="87"
              unit="分"
              trend="+5%"
              color="purple"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatCard
              icon={<TrendingUp className="w-6 h-6" />}
              title="学习进度"
              value="68"
              unit="%"
              trend="+8%"
              color="orange"
            />
          </motion.div>
        </motion.div>

        {/* Main Content Grid */}
        <motion.div
          className="grid grid-cols-1 lg:grid-cols-2 gap-8"
          variants={containerVariants}
        >
          {/* Left Column - 我的课程 */}
          <motion.div variants={cardVariants}>
            <CoursesCard />
          </motion.div>

          {/* Right Column - AI推荐 */}
          <motion.div variants={cardVariants}>
            <AIRecommendationCard />
          </motion.div>
        </motion.div>

        {/* Full Width Section */}
        <motion.div variants={cardVariants}>
          <AbilityCard />
        </motion.div>
      </motion.div>
    </StudentLayout>
  );
};

// Welcome Section Component
const WelcomeSection = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const getGreeting = () => {
    const hour = currentTime.getHours();
    if (hour < 12) return "早上好";
    if (hour < 18) return "下午好";
    return "晚上好";
  };

  return (
    <motion.div
      className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 p-8 text-white"
      whileHover="hover"
      variants={hoverVariants}
    >
      <div className="absolute inset-0 bg-black/10" />
      <div className="relative z-10">
        <div className="flex items-center justify-between">
          <div>
            <motion.h1
              className="text-4xl font-bold mb-2"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              {getGreeting()}，张同学！
            </motion.h1>
            <motion.p
              className="text-blue-100 text-lg"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              今天是 {currentTime.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long'
              })}
            </motion.p>
          </div>
          <motion.div
            className="text-6xl opacity-20"
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          >
            🎓
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

// Stat Card Component
interface StatCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  unit: string;
  trend: string;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

const StatCard = ({ icon, title, value, unit, trend, color }: StatCardProps) => {
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
      <Card className="relative overflow-hidden border-0 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className={`p-3 rounded-xl bg-gradient-to-br ${colorClasses[color]} text-white`}>
              {icon}
            </div>
            <Badge variant="secondary" className="text-green-600 bg-green-50">
              {trend}
            </Badge>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline space-x-1">
              <motion.span
                className="text-3xl font-bold text-gray-900"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
              >
                {value}
              </motion.span>
              <span className="text-sm text-gray-500">{unit}</span>
            </div>
            <p className="text-sm text-gray-600 mt-1">{title}</p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};



// Courses Card Component
const CoursesCard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // 获取我的课程数据
  useEffect(() => {
    const fetchMyCourses = async () => {
      try {
        setLoading(true);
        const enrollments = await courseAPI.getMyCourses();

        // 转换数据格式
        const coursesData = enrollments.slice(0, 3).map((enrollment: CourseEnrollment, index: number) => ({
          id: enrollment.course_id,
          title: enrollment.course?.title || '未知课程',
          progress: Math.round(enrollment.progress_percentage || 0),
          instructor: enrollment.course?.instructor_name || '未知教师',
          nextClass: "即将开始", // 可以根据实际情况调整
          color: ['blue', 'purple', 'green'][index % 3] as 'blue' | 'purple' | 'green',
          enrollment_id: enrollment.id
        }));

        setCourses(coursesData);
      } catch (error) {
        console.error('获取我的课程失败:', error);
        // 如果获取失败，使用默认数据
        setCourses([
          {
            id: 1,
            title: "暂无课程数据",
            progress: 0,
            instructor: "请先注册课程",
            nextClass: "",
            color: "blue"
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchMyCourses();
  }, []);

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            我的课程
            {!loading && (
              <Badge variant="secondary" className="ml-2">
                {courses.length} 门课程
              </Badge>
            )}
          </CardTitle>
          <Button
            variant="ghost"
            size="sm"
            className="text-blue-600"
            onClick={() => navigate('/student/profile')}
          >
            查看全部 <ChevronRight className="w-4 h-4 ml-1" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">加载中...</span>
          </div>
        ) : courses.length === 0 ? (
          <div className="text-center py-8">
            <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <h4 className="text-lg font-medium text-gray-900 mb-2">暂无课程</h4>
            <p className="text-gray-600 mb-4">您还没有注册任何课程</p>
            <Button
              onClick={() => navigate('/student/courses')}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <BookOpen className="w-4 h-4 mr-2" />
              浏览课程
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {courses.map((course, index) => (
              <motion.div
                key={course.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <CourseItem {...course} />
              </motion.div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Course Item Component
interface CourseItemProps {
  id: number;
  title: string;
  progress: number;
  instructor: string;
  nextClass: string;
  color: 'blue' | 'purple' | 'green';
}

const CourseItem = ({ id, title, progress, instructor, nextClass, color }: CourseItemProps) => {
  const navigate = useNavigate();

  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    green: 'from-green-500 to-green-600'
  };

  const handleCourseClick = () => {
    navigate(`/student/courses/${id}`);
  };

  return (
    <motion.div
      className="p-4 rounded-xl border border-gray-100 hover:border-gray-200 transition-all cursor-pointer"
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      onClick={handleCourseClick}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h4 className="font-semibold text-gray-900 mb-1">{title}</h4>
          <p className="text-sm text-gray-500">授课教师：{instructor}</p>
        </div>
        <div className="text-right">
          <div className="text-sm font-medium text-gray-900">{progress}%</div>
          <div className="text-xs text-gray-500">完成度</div>
        </div>
      </div>

      <div className="mb-3">
        <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
          <span>学习进度</span>
          <span>{progress}/100</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className={`h-2 rounded-full bg-gradient-to-r ${colorClasses[color]}`}
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 1, delay: 0.5 }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center text-xs text-gray-500">
          <Calendar className="w-3 h-3 mr-1" />
          下次课程：{nextClass}
        </div>
        <Button
          size="sm"
          variant="ghost"
          className="h-6 px-2 text-xs"
          onClick={(e) => {
            e.stopPropagation();
            handleCourseClick();
          }}
        >
          <PlayCircle className="w-3 h-3 mr-1" />
          继续学习
        </Button>
      </div>
    </motion.div>
  );
};

// AI Recommendation Card
const AIRecommendationCard = () => {
  return (
    <Card className="border-0 shadow-lg bg-gradient-to-br from-purple-50 to-blue-50">
      <CardHeader className="pb-4">
        <CardTitle className="text-lg font-bold flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-600" />
          AI 学习建议
        </CardTitle>
      </CardHeader>
      <CardContent>
        <motion.div
          className="space-y-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-start space-x-3 p-3 bg-white rounded-lg border border-purple-100">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Lightbulb className="w-4 h-4 text-purple-600" />
            </div>
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 mb-1">重点关注</h4>
              <p className="text-sm text-gray-600">
                根据你最近的练习记录，建议加强 "函数与极限" 章节的学习。
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3 p-3 bg-white rounded-lg border border-blue-100">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Target className="w-4 h-4 text-blue-600" />
            </div>
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 mb-1">学习计划</h4>
              <p className="text-sm text-gray-600">
                建议每天完成 2-3 道相关练习题，预计 1 周内可以显著提升。
              </p>
            </div>
          </div>

        </motion.div>
      </CardContent>
    </Card>
  );
};



// Ability Assessment Card
const AbilityCard = () => {
  const abilities = [
    { name: "计算能力", score: 85, color: "blue" },
    { name: "逻辑思维", score: 92, color: "purple" },
    { name: "空间想象", score: 78, color: "green" },
    { name: "语言表达", score: 88, color: "orange" }
  ];

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-6">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            <Brain className="w-6 h-6 text-purple-600" />
            综合能力评估
          </CardTitle>
          <div className="flex items-center space-x-2">
            <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
            <span className="text-sm font-medium text-gray-600">综合评分: 86分</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Radar Chart */}
          <div className="h-80">
            <AbilityRadarChart />
          </div>

          {/* Ability Breakdown */}
          <div className="space-y-6">
            <h4 className="font-semibold text-gray-900 mb-4">能力详细分析</h4>
            {abilities.map((ability, index) => (
              <motion.div
                key={ability.name}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">{ability.name}</span>
                  <span className="text-sm font-bold text-gray-900">{ability.score}分</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    className={`h-2 rounded-full ${
                      ability.color === 'blue' ? 'bg-gradient-to-r from-blue-500 to-blue-600' :
                      ability.color === 'purple' ? 'bg-gradient-to-r from-purple-500 to-purple-600' :
                      ability.color === 'green' ? 'bg-gradient-to-r from-green-500 to-green-600' :
                      'bg-gradient-to-r from-orange-500 to-orange-600'
                    }`}
                    initial={{ width: 0 }}
                    animate={{ width: `${ability.score}%` }}
                    transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                  />
                </div>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>需要提升</span>
                  <span>优秀</span>
                </div>
              </motion.div>
            ))}

            <motion.div
              className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
            >
              <div className="flex items-center space-x-2 mb-2">
                <TrendingUp className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-900">提升建议</span>
              </div>
              <p className="text-xs text-gray-600">
                你的逻辑思维能力表现优秀！建议继续保持，同时可以加强空间想象能力的训练。
              </p>
            </motion.div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

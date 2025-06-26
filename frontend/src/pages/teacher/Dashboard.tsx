import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  BookOpen,
  Clock,
  Users,
  ClipboardList,
  TrendingUp,
  Calendar,
  Target,
  Award,
  PlayCircle,
  ChevronRight,
  Star,
  Brain,
  Timer,
  BookMarked,
  PlusCircle,
  Eye,
  BarChart3
} from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { teacherAPI, TeacherStats, TeacherActivity } from "@/services/api";
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
export const TeacherDashboard = () => {
  const [stats, setStats] = useState<TeacherStats | null>(null);
  const [activities, setActivities] = useState<TeacherActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, activitiesData] = await Promise.all([
          teacherAPI.getComprehensiveStats(),
          teacherAPI.getRecentActivities(10)
        ]);

        setStats(statsData);
        setActivities(activitiesData);
      } catch (error) {
        console.error('获取数据失败:', error);
        toast({
          title: "数据加载失败",
          description: "无法获取统计数据，请稍后重试",
          variant: "destructive",
        });

        // 设置默认数据以防API失败
        setStats({
          total_students: 0,
          total_courses: 0,
          total_exercises: 0,
          average_score: 0,
          active_students: 0,
          published_courses: 0,
          published_exercises: 0,
          total_enrollments: 0
        });
        setActivities([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [toast]);

  if (loading) {
    return (
      <TeacherLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
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
          <WelcomeSection />
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          variants={containerVariants}
        >
          <motion.div variants={cardVariants}>
            <StatCard
              icon={<Users className="w-6 h-6" />}
              title="学生总数"
              value={stats?.total_students?.toString() || "0"}
              unit="人"
              trend={`活跃: ${stats?.active_students || 0}`}
              color="blue"
            />
          </motion.div>

          <motion.div variants={cardVariants}>
            <StatCard
              icon={<BookOpen className="w-6 h-6" />}
              title="课程总数"
              value={stats?.total_courses?.toString() || "0"}
              unit="门"
              trend={`已发布: ${stats?.published_courses || 0}`}
              color="green"
            />
          </motion.div>

          <motion.div variants={cardVariants}>
            <StatCard
              icon={<ClipboardList className="w-6 h-6" />}
              title="练习总数"
              value={stats?.total_exercises?.toString() || "0"}
              unit="套"
              trend={`已发布: ${stats?.published_exercises || 0}`}
              color="purple"
            />
          </motion.div>

          <motion.div variants={cardVariants}>
            <StatCard
              icon={<Award className="w-6 h-6" />}
              title="平均成绩"
              value={stats?.average_score?.toFixed(1) || "0.0"}
              unit="分"
              trend={`注册: ${stats?.total_enrollments || 0}`}
              color="yellow"
            />
          </motion.div>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Quick Actions & Recent Activity */}
          <div className="lg:col-span-2 space-y-8">
            {/* Quick Actions */}
            <motion.div variants={cardVariants}>
              <QuickActionsSection />
            </motion.div>

            {/* Recent Activity */}
            <motion.div variants={cardVariants}>
              <RecentActivitySection activities={activities} />
            </motion.div>
          </div>

          {/* Right Column - Teaching Overview */}
          <div className="space-y-8">
            <motion.div variants={cardVariants}>
              <TeachingOverviewSection stats={stats} />
            </motion.div>
          </div>
        </div>
      </motion.div>
    </TeacherLayout>
  );
};

// Welcome Section Component
const WelcomeSection = () => {
  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold mb-2">欢迎回来，老师！</h2>
          <p className="text-blue-100 text-lg">
            今天是美好的一天，让我们一起创造精彩的教学内容
          </p>
        </div>
        <div className="hidden md:block">
          <Brain className="w-24 h-24 text-blue-200" />
        </div>
      </div>
    </div>
  );
};

// Stat Card Component
const StatCard = ({ icon, title, value, unit, trend, color }: {
  icon: React.ReactNode;
  title: string;
  value: string;
  unit: string;
  trend: string;
  color: string;
}) => {
  const colorClasses = {
    blue: "text-blue-600 bg-blue-50",
    green: "text-green-600 bg-green-50",
    purple: "text-purple-600 bg-purple-50",
    yellow: "text-yellow-600 bg-yellow-50",
    red: "text-red-600 bg-red-50"
  };

  return (
    <motion.div
      variants={hoverVariants}
      whileHover="hover"
      className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg ${colorClasses[color as keyof typeof colorClasses]}`}>
          {icon}
        </div>
        <Badge variant="secondary" className="text-xs">
          {trend}
        </Badge>
      </div>
      <div className="space-y-1">
        <p className="text-gray-600 text-sm font-medium">{title}</p>
        <div className="flex items-baseline space-x-1">
          <span className="text-2xl font-bold text-gray-900">{value}</span>
          <span className="text-gray-500 text-sm">{unit}</span>
        </div>
      </div>
    </motion.div>
  );
};

// Quick Actions Section
const QuickActionsSection = () => {
  const navigate = useNavigate();

  const quickActions = [
    {
      title: "创建新课程",
      description: "开始制作新的教学课程",
      icon: <BookOpen className="w-6 h-6" />,
      color: "blue",
      action: () => navigate("/teacher/courses/create")
    },
    {
      title: "创建练习",
      description: "为学生准备练习题目",
      icon: <ClipboardList className="w-6 h-6" />,
      color: "purple",
      action: () => navigate("/teacher/exercises/create")
    },
    {
      title: "查看学生",
      description: "管理和查看学生信息",
      icon: <Users className="w-6 h-6" />,
      color: "green",
      action: () => navigate("/teacher/students")
    },
    {
      title: "成绩分析",
      description: "分析学生学习成果",
      icon: <BarChart3 className="w-6 h-6" />,
      color: "yellow",
      action: () => navigate("/teacher/grades")
    }
  ];

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center text-xl">
          <Target className="mr-3 w-6 h-6 text-blue-600" />
          快捷操作
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {quickActions.map((action, index) => (
            <motion.div
              key={index}
              variants={hoverVariants}
              whileHover="hover"
              onClick={action.action}
              className="p-4 rounded-lg border border-gray-100 hover:border-blue-200 cursor-pointer transition-all bg-gradient-to-br from-white to-gray-50"
            >
              <div className="flex items-start space-x-3">
                <div className={`p-2 rounded-lg ${
                  action.color === 'blue' ? 'bg-blue-50 text-blue-600' :
                  action.color === 'purple' ? 'bg-purple-50 text-purple-600' :
                  action.color === 'green' ? 'bg-green-50 text-green-600' :
                  'bg-yellow-50 text-yellow-600'
                }`}>
                  {action.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1">{action.title}</h3>
                  <p className="text-gray-600 text-sm">{action.description}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400" />
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

// Recent Activity Section
const RecentActivitySection = ({ activities }: { activities: TeacherActivity[] }) => {
  return (
    <Card className="border-0 shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center text-xl">
          <Clock className="mr-3 w-6 h-6 text-blue-600" />
          最近活动
        </CardTitle>
      </CardHeader>
      <CardContent>
        {activities.length > 0 ? (
          <div className="space-y-4">
            {activities.slice(0, 5).map((activity, index) => (
              <div key={activity.id} className="flex items-start space-x-4 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                <div className="flex-shrink-0 mt-1">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 mb-1">{activity.title}</p>
                  <p className="text-gray-600 text-sm mb-2">{activity.description}</p>
                  <p className="text-gray-400 text-xs">
                    {new Date(activity.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Calendar className="mx-auto w-16 h-16 text-gray-300 mb-4" />
            <p className="text-gray-500 text-lg font-medium mb-2">暂无最近活动</p>
            <p className="text-gray-400 text-sm">开始创建课程和练习来查看活动记录</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Teaching Overview Section
const TeachingOverviewSection = ({ stats }: { stats: TeacherStats | null }) => {
  const overviewItems = [
    {
      label: "课程发布率",
      value: stats ? Math.round((stats.published_courses / Math.max(stats.total_courses, 1)) * 100) : 0,
      icon: <BookOpen className="w-5 h-5" />,
      color: "blue"
    },
    {
      label: "练习发布率",
      value: stats ? Math.round((stats.published_exercises / Math.max(stats.total_exercises, 1)) * 100) : 0,
      icon: <ClipboardList className="w-5 h-5" />,
      color: "purple"
    },
    {
      label: "学生活跃度",
      value: stats ? Math.round((stats.active_students / Math.max(stats.total_students, 1)) * 100) : 0,
      icon: <Users className="w-5 h-5" />,
      color: "green"
    }
  ];

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center text-xl">
          <TrendingUp className="mr-3 w-6 h-6 text-blue-600" />
          教学概览
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {overviewItems.map((item, index) => (
          <div key={index} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className={`p-1 rounded ${
                  item.color === 'blue' ? 'bg-blue-50 text-blue-600' :
                  item.color === 'purple' ? 'bg-purple-50 text-purple-600' :
                  'bg-green-50 text-green-600'
                }`}>
                  {item.icon}
                </div>
                <span className="text-sm font-medium text-gray-700">{item.label}</span>
              </div>
              <span className="text-sm font-bold text-gray-900">{item.value}%</span>
            </div>
            <Progress
              value={item.value}
              className={`h-2 ${
                item.color === 'blue' ? '[&>div]:bg-blue-500' :
                item.color === 'purple' ? '[&>div]:bg-purple-500' :
                '[&>div]:bg-green-500'
              }`}
            />
          </div>
        ))}

        <div className="pt-4 border-t border-gray-100">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {stats?.average_score?.toFixed(1) || '0.0'}
            </div>
            <div className="text-sm text-gray-600 mb-2">平均成绩</div>
            <Badge variant="secondary" className="text-xs">
              {stats?.total_enrollments || 0} 人次学习
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

import StudentLayout from "@/components/layouts/StudentLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { 
  PencilRuler, 
  Clock, 
  Target, 
  CheckCircle, 
  XCircle,
  AlertCircle,
  TrendingUp,
  Calendar,
  BookOpen,
  Award,
  PlayCircle,
  RotateCcw,
  Filter,
  Search
} from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

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
const exerciseCategories = [
  {
    id: 1,
    title: "自主练习",
    description: "根据个人进度自由选择练习题目",
    icon: <Target className="w-8 h-8" />,
    color: "blue",
    count: 156,
    completed: 89,
    accuracy: 85
  },
  {
    id: 2,
    title: "课后作业",
    description: "完成老师布置的作业任务",
    icon: <BookOpen className="w-8 h-8" />,
    color: "green",
    count: 24,
    completed: 18,
    accuracy: 92
  },
  {
    id: 3,
    title: "错题本",
    description: "复习和巩固之前做错的题目",
    icon: <RotateCcw className="w-8 h-8" />,
    color: "orange",
    count: 32,
    completed: 12,
    accuracy: 78
  },
  {
    id: 4,
    title: "模拟考试",
    description: "参加模拟考试检验学习成果",
    icon: <Award className="w-8 h-8" />,
    color: "purple",
    count: 8,
    completed: 3,
    accuracy: 88
  }
];

const recentExercises = [
  {
    id: 1,
    title: "函数与极限 - 基础练习",
    subject: "高等数学",
    difficulty: "中级",
    questions: 20,
    completed: 18,
    score: 85,
    timeSpent: "45分钟",
    status: "completed",
    dueDate: "2024-03-15"
  },
  {
    id: 2,
    title: "矩阵运算 - 综合练习",
    subject: "线性代数",
    difficulty: "高级",
    questions: 15,
    completed: 10,
    score: null,
    timeSpent: "30分钟",
    status: "in-progress",
    dueDate: "2024-03-16"
  },
  {
    id: 3,
    title: "概率分布 - 应用题",
    subject: "概率论",
    difficulty: "中级",
    questions: 12,
    completed: 0,
    score: null,
    timeSpent: "0分钟",
    status: "pending",
    dueDate: "2024-03-18"
  }
];

export const Exercises = () => {
  const navigate = useNavigate();

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
              <h1 className="text-3xl font-bold text-gray-900">练习系统</h1>
              <p className="text-gray-600 mt-2">通过练习巩固知识，提升学习效果</p>
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
              icon={<PencilRuler className="w-6 h-6" />}
              title="今日练习"
              value="12"
              subtitle="道题目"
              color="blue"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<CheckCircle className="w-6 h-6" />}
              title="正确率"
              value="87%"
              subtitle="平均正确率"
              color="green"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<Clock className="w-6 h-6" />}
              title="练习时长"
              value="2.5"
              subtitle="小时"
              color="purple"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<TrendingUp className="w-6 h-6" />}
              title="连续天数"
              value="7"
              subtitle="天"
              color="orange"
            />
          </motion.div>
        </motion.div>

        {/* Exercise Categories */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl font-bold">练习分类</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {exerciseCategories.map((category, index) => (
                  <motion.div
                    key={category.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover="hover"
                    variants={hoverVariants}
                  >
                    <ExerciseCategoryCard category={category} navigate={navigate} />
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Recent Exercises */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl font-bold">最近练习</CardTitle>
                <Button variant="ghost" size="sm" className="text-blue-600">
                  查看全部
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentExercises.map((exercise, index) => (
                  <motion.div
                    key={exercise.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <ExerciseItem exercise={exercise} navigate={navigate} />
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
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

// Exercise Category Card Component
interface ExerciseCategoryCardProps {
  category: typeof exerciseCategories[0];
  navigate: (path: string) => void;
}

const ExerciseCategoryCard = ({ category, navigate }: ExerciseCategoryCardProps) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600 bg-blue-50 text-blue-600',
    green: 'from-green-500 to-green-600 bg-green-50 text-green-600',
    orange: 'from-orange-500 to-orange-600 bg-orange-50 text-orange-600',
    purple: 'from-purple-500 to-purple-600 bg-purple-50 text-purple-600'
  };

  const progressPercentage = Math.round((category.completed / category.count) * 100);

  return (
    <Card className="border-0 shadow-md hover:shadow-lg transition-all cursor-pointer">
      <CardContent className="p-6">
        <div className="text-center space-y-4">
          <div className={`mx-auto w-16 h-16 rounded-2xl ${colorClasses[category.color]} flex items-center justify-center`}>
            {category.icon}
          </div>

          <div>
            <h3 className="font-bold text-gray-900 mb-1">{category.title}</h3>
            <p className="text-sm text-gray-600 mb-3">{category.description}</p>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">进度</span>
              <span className="font-medium">{category.completed}/{category.count}</span>
            </div>
            <Progress value={progressPercentage} className="h-2" />
            <div className="flex justify-between text-xs text-gray-500">
              <span>正确率: {category.accuracy}%</span>
              <span>{progressPercentage}% 完成</span>
            </div>
          </div>

          <Button
            className="w-full"
            size="sm"
            onClick={() => navigate(`/student/exercises/practice/${category.id}`)}
          >
            <PlayCircle className="w-4 h-4 mr-2" />
            开始练习
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// Exercise Item Component
interface ExerciseItemProps {
  exercise: typeof recentExercises[0];
  navigate: (path: string) => void;
}

const ExerciseItem = ({ exercise, navigate }: ExerciseItemProps) => {
  const statusConfig = {
    completed: {
      icon: <CheckCircle className="w-5 h-5 text-green-600" />,
      badge: <Badge className="bg-green-100 text-green-600">已完成</Badge>,
      color: "green"
    },
    'in-progress': {
      icon: <Clock className="w-5 h-5 text-yellow-600" />,
      badge: <Badge className="bg-yellow-100 text-yellow-600">进行中</Badge>,
      color: "yellow"
    },
    pending: {
      icon: <AlertCircle className="w-5 h-5 text-gray-600" />,
      badge: <Badge className="bg-gray-100 text-gray-600">待开始</Badge>,
      color: "gray"
    }
  };

  const difficultyColors = {
    '初级': 'bg-green-100 text-green-600',
    '中级': 'bg-yellow-100 text-yellow-600',
    '高级': 'bg-red-100 text-red-600'
  };

  const config = statusConfig[exercise.status as keyof typeof statusConfig];

  return (
    <motion.div
      whileHover={{ scale: 1.01, y: -2 }}
      whileTap={{ scale: 0.99 }}
    >
      <Card className="border border-gray-100 hover:border-gray-200 transition-all cursor-pointer">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-start space-x-4 flex-1">
              <div className="p-2 bg-gray-50 rounded-lg">
                {config.icon}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <h4 className="font-semibold text-gray-900 truncate">{exercise.title}</h4>
                  {config.badge}
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-500 mb-2">
                  <span>{exercise.subject}</span>
                  <Badge
                    variant="secondary"
                    className={difficultyColors[exercise.difficulty as keyof typeof difficultyColors]}
                  >
                    {exercise.difficulty}
                  </Badge>
                  <span>{exercise.questions} 题</span>
                </div>

                <div className="flex items-center space-x-4 text-xs text-gray-400">
                  <span>用时: {exercise.timeSpent}</span>
                  <span>截止: {exercise.dueDate}</span>
                  {exercise.score && <span>得分: {exercise.score}分</span>}
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {exercise.status === 'completed' && exercise.score && (
                <div className="text-right">
                  <div className="text-lg font-bold text-gray-900">{exercise.score}</div>
                  <div className="text-xs text-gray-500">分</div>
                </div>
              )}

              {exercise.status === 'in-progress' && (
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-900">
                    {exercise.completed}/{exercise.questions}
                  </div>
                  <div className="text-xs text-gray-500">已完成</div>
                </div>
              )}

              <Button
                size="sm"
                variant={exercise.status === 'completed' ? 'outline' : 'default'}
                onClick={() => navigate(`/student/exercises/practice/${exercise.id}`)}
              >
                {exercise.status === 'completed' ? '查看详情' :
                 exercise.status === 'in-progress' ? '继续练习' : '开始练习'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

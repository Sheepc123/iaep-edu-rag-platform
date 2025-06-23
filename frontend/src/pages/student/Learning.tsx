import StudentLayout from "@/components/layouts/StudentLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { 
  BrainCircuit, 
  Calendar, 
  BookMarked, 
  History,
  Target,
  Star,
  Clock,
  TrendingUp,
  PlayCircle,
  Download,
  Heart,
  Eye,
  Filter,
  Search,
  Plus
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
const learningPlan = {
  currentWeek: 3,
  totalWeeks: 16,
  completedTasks: 18,
  totalTasks: 24,
  weeklyGoal: "完成函数与极限章节学习",
  progress: 75
};

const resources = [
  {
    id: 1,
    title: "高等数学精讲视频",
    type: "video",
    duration: "2小时30分钟",
    views: 1234,
    rating: 4.8,
    category: "数学基础",
    thumbnail: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=300&h=200&fit=crop",
    description: "深入讲解高等数学核心概念，适合初学者"
  },
  {
    id: 2,
    title: "线性代数学习指南",
    type: "document",
    pages: 45,
    downloads: 856,
    rating: 4.6,
    category: "数学基础",
    thumbnail: "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300&h=200&fit=crop",
    description: "系统性学习线性代数的完整指南"
  },
  {
    id: 3,
    title: "概率论实战案例",
    type: "interactive",
    exercises: 20,
    completions: 432,
    rating: 4.9,
    category: "统计学",
    thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300&h=200&fit=crop",
    description: "通过实际案例学习概率论应用"
  }
];

const favorites = [
  {
    id: 1,
    title: "导数的几何意义",
    type: "video",
    addedDate: "2024-03-10",
    category: "高等数学"
  },
  {
    id: 2,
    title: "矩阵运算技巧",
    type: "document",
    addedDate: "2024-03-08",
    category: "线性代数"
  },
  {
    id: 3,
    title: "正态分布详解",
    type: "interactive",
    addedDate: "2024-03-05",
    category: "概率论"
  }
];

const recentHistory = [
  {
    id: 1,
    title: "函数极限的计算方法",
    type: "video",
    watchedAt: "2024-03-14 14:30",
    progress: 85,
    category: "高等数学"
  },
  {
    id: 2,
    title: "特征值与特征向量",
    type: "document",
    viewedAt: "2024-03-14 10:15",
    progress: 100,
    category: "线性代数"
  },
  {
    id: 3,
    title: "概率分布练习题",
    type: "interactive",
    completedAt: "2024-03-13 16:45",
    progress: 90,
    category: "概率论"
  }
];

export const Learning = () => {
  const [activeTab, setActiveTab] = useState("plan");

  const tabs = [
    { id: "plan", label: "学习计划", icon: <Target className="w-4 h-4" /> },
    { id: "resources", label: "学习资源", icon: <BookMarked className="w-4 h-4" /> },
    { id: "favorites", label: "收藏夹", icon: <Heart className="w-4 h-4" /> },
    { id: "history", label: "学习历史", icon: <History className="w-4 h-4" /> }
  ];

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
              <h1 className="text-3xl font-bold text-gray-900">学习中心</h1>
              <p className="text-gray-600 mt-2">制定学习计划，管理学习资源</p>
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
              icon={<Calendar className="w-6 h-6" />}
              title="学习计划"
              value={`${learningPlan.currentWeek}/${learningPlan.totalWeeks}`}
              subtitle="周进度"
              color="blue"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<BookMarked className="w-6 h-6" />}
              title="学习资源"
              value="156"
              subtitle="个资源"
              color="green"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<Heart className="w-6 h-6" />}
              title="收藏内容"
              value="23"
              subtitle="个收藏"
              color="purple"
            />
          </motion.div>
          <motion.div variants={cardVariants}>
            <StatsCard 
              icon={<TrendingUp className="w-6 h-6" />}
              title="学习时长"
              value="45.2"
              subtitle="小时"
              color="orange"
            />
          </motion.div>
        </motion.div>

        {/* Tab Navigation */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-0">
              <div className="flex border-b">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors ${
                      activeTab === tab.id
                        ? "text-blue-600 border-b-2 border-blue-600 bg-blue-50"
                        : "text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                    }`}
                  >
                    {tab.icon}
                    <span>{tab.label}</span>
                  </button>
                ))}
              </div>
              
              <div className="p-6">
                {activeTab === "plan" && <LearningPlanContent />}
                {activeTab === "resources" && <ResourcesContent />}
                {activeTab === "favorites" && <FavoritesContent />}
                {activeTab === "history" && <HistoryContent />}
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

// Learning Plan Content
const LearningPlanContent = () => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Current Progress */}
        <Card className="border border-gray-100">
          <CardHeader>
            <CardTitle className="text-lg">本周学习进度</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">整体进度</span>
                <span className="text-sm font-medium">{learningPlan.completedTasks}/{learningPlan.totalTasks} 任务</span>
              </div>
              <Progress value={learningPlan.progress} className="h-3" />
              <div className="text-center">
                <span className="text-2xl font-bold text-blue-600">{learningPlan.progress}%</span>
                <p className="text-sm text-gray-500 mt-1">完成度</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Weekly Goal */}
        <Card className="border border-gray-100">
          <CardHeader>
            <CardTitle className="text-lg">本周目标</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">主要目标</h4>
                <p className="text-blue-700">{learningPlan.weeklyGoal}</p>
              </div>
              <Button className="w-full">
                <Plus className="w-4 h-4 mr-2" />
                添加新目标
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Tasks */}
      <Card className="border border-gray-100">
        <CardHeader>
          <CardTitle className="text-lg">本周任务清单</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { task: "观看函数极限视频课程", completed: true, priority: "high" },
              { task: "完成导数练习题 10 道", completed: true, priority: "medium" },
              { task: "阅读积分应用案例", completed: false, priority: "medium" },
              { task: "参加在线答疑课程", completed: false, priority: "low" }
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className={`w-4 h-4 rounded-full ${item.completed ? 'bg-green-500' : 'bg-gray-300'}`} />
                  <span className={item.completed ? 'line-through text-gray-500' : 'text-gray-900'}>{item.task}</span>
                </div>
                <Badge variant="outline" className={
                  item.priority === 'high' ? 'text-red-600 border-red-200' :
                  item.priority === 'medium' ? 'text-yellow-600 border-yellow-200' :
                  'text-green-600 border-green-200'
                }>
                  {item.priority === 'high' ? '高' : item.priority === 'medium' ? '中' : '低'}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Resources Content
const ResourcesContent = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">推荐学习资源</h3>
        <Button variant="outline" size="sm">
          查看全部
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((resource, index) => (
          <motion.div
            key={resource.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover="hover"
            variants={hoverVariants}
          >
            <ResourceCard resource={resource} />
          </motion.div>
        ))}
      </div>
    </div>
  );
};

// Favorites Content
const FavoritesContent = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">我的收藏</h3>
        <span className="text-sm text-gray-500">{favorites.length} 个收藏</span>
      </div>

      <div className="space-y-4">
        {favorites.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <FavoriteItem item={item} />
          </motion.div>
        ))}
      </div>
    </div>
  );
};

// History Content
const HistoryContent = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">最近学习</h3>
        <Button variant="outline" size="sm">
          清除历史
        </Button>
      </div>

      <div className="space-y-4">
        {recentHistory.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <HistoryItem item={item} />
          </motion.div>
        ))}
      </div>
    </div>
  );
};

// Resource Card Component
interface ResourceCardProps {
  resource: typeof resources[0];
}

const ResourceCard = ({ resource }: ResourceCardProps) => {
  const typeIcons = {
    video: <PlayCircle className="w-5 h-5" />,
    document: <BookMarked className="w-5 h-5" />,
    interactive: <BrainCircuit className="w-5 h-5" />
  };

  const typeLabels = {
    video: '视频',
    document: '文档',
    interactive: '互动'
  };

  return (
    <Card className="border-0 shadow-md hover:shadow-lg transition-all cursor-pointer overflow-hidden">
      <div className="relative">
        <img
          src={resource.thumbnail}
          alt={resource.title}
          className="w-full h-40 object-cover"
        />
        <div className="absolute top-3 left-3">
          <Badge className="bg-black/70 text-white">
            {typeLabels[resource.type as keyof typeof typeLabels]}
          </Badge>
        </div>
        <div className="absolute top-3 right-3">
          <Button size="sm" variant="ghost" className="bg-white/80 hover:bg-white">
            <Heart className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <CardContent className="p-4">
        <div className="space-y-3">
          <div>
            <h4 className="font-semibold text-gray-900 mb-1">{resource.title}</h4>
            <p className="text-sm text-gray-600 line-clamp-2">{resource.description}</p>
          </div>

          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-1">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              <span>{resource.rating}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Eye className="w-4 h-4" />
              <span>
                {resource.type === 'video' ? `${resource.views} 观看` :
                 resource.type === 'document' ? `${resource.downloads} 下载` :
                 `${resource.completions} 完成`}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between text-xs text-gray-400">
            <Badge variant="outline">{resource.category}</Badge>
            <span>
              {resource.type === 'video' ? resource.duration :
               resource.type === 'document' ? `${resource.pages} 页` :
               `${resource.exercises} 练习`}
            </span>
          </div>

          <Button className="w-full" size="sm">
            {typeIcons[resource.type as keyof typeof typeIcons]}
            <span className="ml-2">
              {resource.type === 'video' ? '观看' :
               resource.type === 'document' ? '阅读' :
               '开始练习'}
            </span>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// Favorite Item Component
interface FavoriteItemProps {
  item: typeof favorites[0];
}

const FavoriteItem = ({ item }: FavoriteItemProps) => {
  const typeIcons = {
    video: <PlayCircle className="w-5 h-5 text-blue-600" />,
    document: <BookMarked className="w-5 h-5 text-green-600" />,
    interactive: <BrainCircuit className="w-5 h-5 text-purple-600" />
  };

  return (
    <Card className="border border-gray-100 hover:border-gray-200 transition-all cursor-pointer">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gray-50 rounded-lg">
              {typeIcons[item.type as keyof typeof typeIcons]}
            </div>
            <div>
              <h4 className="font-medium text-gray-900">{item.title}</h4>
              <div className="flex items-center space-x-2 text-sm text-gray-500 mt-1">
                <span>{item.category}</span>
                <span>•</span>
                <span>收藏于 {item.addedDate}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Button size="sm" variant="ghost">
              <Heart className="w-4 h-4 text-red-500 fill-red-500" />
            </Button>
            <Button size="sm">
              查看
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// History Item Component
interface HistoryItemProps {
  item: typeof recentHistory[0];
}

const HistoryItem = ({ item }: HistoryItemProps) => {
  const typeIcons = {
    video: <PlayCircle className="w-5 h-5 text-blue-600" />,
    document: <BookMarked className="w-5 h-5 text-green-600" />,
    interactive: <BrainCircuit className="w-5 h-5 text-purple-600" />
  };

  return (
    <Card className="border border-gray-100 hover:border-gray-200 transition-all cursor-pointer">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3 flex-1">
            <div className="p-2 bg-gray-50 rounded-lg">
              {typeIcons[item.type as keyof typeof typeIcons]}
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="font-medium text-gray-900 truncate">{item.title}</h4>
              <div className="flex items-center space-x-2 text-sm text-gray-500 mt-1">
                <span>{item.category}</span>
                <span>•</span>
                <span>
                  {item.type === 'video' ? `观看于 ${item.watchedAt}` :
                   item.type === 'document' ? `查看于 ${item.viewedAt}` :
                   `完成于 ${item.completedAt}`}
                </span>
              </div>
              <div className="mt-2">
                <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                  <span>进度</span>
                  <span>{item.progress}%</span>
                </div>
                <Progress value={item.progress} className="h-1" />
              </div>
            </div>
          </div>
          <Button size="sm" variant="outline">
            继续
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

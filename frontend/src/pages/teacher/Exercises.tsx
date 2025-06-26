import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/components/ui/use-toast";
import {
  Plus,
  Search,
  Filter,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Users,
  Clock,
  BookOpen,
  BarChart3,
  Settings,
  Copy,
  Archive
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { exerciseAPI, Exercise, ExerciseListQuery } from "@/services/api";

// 动画变体
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

export const TeacherExercises: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  // 状态管理
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("all");
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // 筛选选项
  const categories = [
    { value: "all", label: "全部分类" },
    { value: "自主练习", label: "自主练习" },
    { value: "课后作业", label: "课后作业" },
    { value: "模拟考试", label: "模拟考试" },
    { value: "错题本", label: "错题本" }
  ];

  const difficulties = [
    { value: "all", label: "全部难度" },
    { value: "easy", label: "简单" },
    { value: "medium", label: "中等" },
    { value: "hard", label: "困难" }
  ];

  const statuses = [
    { value: "all", label: "全部状态" },
    { value: "published", label: "已发布" },
    { value: "draft", label: "草稿" },
    { value: "archived", label: "已归档" }
  ];

  // 获取练习列表
  const fetchExercises = async () => {
    try {
      setLoading(true);

      const params: ExerciseListQuery = {
        page: currentPage,
        page_size: 12
      };

      if (selectedCategory !== "all") {
        params.category = selectedCategory;
      }
      if (selectedDifficulty !== "all") {
        params.difficulty = selectedDifficulty as any;
      }
      if (selectedStatus !== "all") {
        params.is_published = selectedStatus === "published";
      }

      const response = await exerciseAPI.getExercises(params);

      // 模拟数据，因为后端可能返回不同的结构
      if (Array.isArray(response)) {
        setExercises(response);
      } else if (response.exercises) {
        setExercises(response.exercises);
        setTotalPages(Math.ceil(response.total / 12));
      }

    } catch (error) {
      console.error("获取练习列表失败:", error);
      toast({
        title: "错误",
        description: "获取练习列表失败",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  // 初始化数据
  useEffect(() => {
    fetchExercises();
  }, [currentPage, selectedCategory, selectedDifficulty, selectedStatus]);

  // 搜索过滤
  const filteredExercises = exercises.filter(exercise =>
    exercise.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (exercise.description && exercise.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // 处理删除练习
  const handleDeleteExercise = async (exerciseId: number) => {
    if (!confirm("确定要删除这个练习吗？此操作不可恢复。")) {
      return;
    }

    try {
      await exerciseAPI.deleteExercise(exerciseId);
      toast({
        title: "成功",
        description: "练习删除成功"
      });
      fetchExercises();
    } catch (error) {
      toast({
        title: "错误",
        description: "删除练习失败",
        variant: "destructive"
      });
    }
  };

  // 处理复制练习
  const handleCopyExercise = async (exercise: Exercise) => {
    try {
      const newExercise = {
        title: `${exercise.title} (副本)`,
        description: exercise.description,
        category: exercise.category,
        subject: exercise.subject,
        difficulty: exercise.difficulty,
        time_limit: exercise.time_limit,
        is_published: false
      };

      await exerciseAPI.createExercise(newExercise);
      toast({
        title: "成功",
        description: "练习复制成功"
      });
      fetchExercises();
    } catch (error) {
      toast({
        title: "错误",
        description: "复制练习失败",
        variant: "destructive"
      });
    }
  };

  return (
    <TeacherLayout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        {/* 头部 */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <BookOpen className="w-8 h-8 mr-3 text-blue-600" />
                练习管理
              </h1>
              <p className="text-gray-600 mt-1">创建和管理您的练习内容</p>
            </div>

            <Button
              onClick={() => navigate("/teacher/exercises/create")}
              className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              <Plus className="w-4 h-4" />
              <span>创建练习</span>
            </Button>
          </div>
        </motion.div>

        {/* 搜索和筛选栏 */}
        <motion.div
          className="mb-6 bg-white rounded-lg shadow-sm border p-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div className="flex flex-col lg:flex-row gap-4">
            {/* 搜索框 */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="搜索练习标题或描述..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* 筛选器 */}
            <div className="flex gap-3">
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map(category => (
                    <SelectItem key={category.value} value={category.value}>
                      {category.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select value={selectedDifficulty} onValueChange={setSelectedDifficulty}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="难度" />
                </SelectTrigger>
                <SelectContent>
                  {difficulties.map(difficulty => (
                    <SelectItem key={difficulty.value} value={difficulty.value}>
                      {difficulty.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="状态" />
                </SelectTrigger>
                <SelectContent>
                  {statuses.map(status => (
                    <SelectItem key={status.value} value={status.value}>
                      {status.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </motion.div>

        {/* 练习列表 */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, index) => (
              <Card key={index} className="animate-pulse">
                <CardHeader>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="h-3 bg-gray-200 rounded"></div>
                    <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredExercises.length === 0 ? (
          <motion.div
            className="text-center py-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">暂无练习</h3>
            <p className="text-gray-500 mb-6">
              {searchTerm ? "没有找到匹配的练习" : "开始创建您的第一个练习吧"}
            </p>
            <Button
              onClick={() => navigate("/teacher/exercises/create")}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              创建练习
            </Button>
          </motion.div>
        ) : (
          <motion.div
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <AnimatePresence>
              {filteredExercises.map((exercise) => (
                <ExerciseCard
                  key={exercise.id}
                  exercise={exercise}
                  onEdit={() => navigate(`/teacher/exercises/${exercise.id}/edit`)}
                  onView={() => navigate(`/teacher/exercises/${exercise.id}`)}
                  onDelete={() => handleDeleteExercise(exercise.id)}
                  onCopy={() => handleCopyExercise(exercise)}
                />
              ))}
            </AnimatePresence>
          </motion.div>
        )}

        {/* 分页 */}
        {totalPages > 1 && (
          <motion.div
            className="mt-8 flex justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <div className="flex space-x-2">
              <Button
                variant="outline"
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
              >
                上一页
              </Button>

              {[...Array(totalPages)].map((_, index) => (
                <Button
                  key={index}
                  variant={currentPage === index + 1 ? "default" : "outline"}
                  onClick={() => setCurrentPage(index + 1)}
                  className="w-10"
                >
                  {index + 1}
                </Button>
              ))}

              <Button
                variant="outline"
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
              >
                下一页
              </Button>
            </div>
          </motion.div>
        )}
      </div>
    </TeacherLayout>
  );
};

// 练习卡片组件
interface ExerciseCardProps {
  exercise: Exercise;
  onEdit: () => void;
  onView: () => void;
  onDelete: () => void;
  onCopy: () => void;
}

const ExerciseCard: React.FC<ExerciseCardProps> = ({
  exercise,
  onEdit,
  onView,
  onDelete,
  onCopy
}) => {
  const [showMenu, setShowMenu] = useState(false);

  // 难度颜色映射
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // 难度文本映射
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
      variants={cardVariants}
      layout
      className="group"
    >
      <Card className="h-full hover:shadow-lg transition-all duration-300 border-l-4 border-l-blue-500 relative overflow-hidden">
        {/* 背景装饰 */}
        <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-bl-full opacity-50"></div>

        <CardHeader className="relative">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">
                {exercise.title}
              </CardTitle>
              <div className="flex items-center gap-2 mt-2">
                <Badge className={getDifficultyColor(exercise.difficulty)}>
                  {getDifficultyText(exercise.difficulty)}
                </Badge>
                <Badge variant="outline">
                  {exercise.category}
                </Badge>
                <Badge variant={exercise.is_published ? "default" : "secondary"}>
                  {exercise.is_published ? "已发布" : "草稿"}
                </Badge>
              </div>
            </div>

            {/* 操作菜单 */}
            <div className="relative">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowMenu(!showMenu)}
                className="opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <MoreVertical className="w-4 h-4" />
              </Button>

              {showMenu && (
                <div className="absolute right-0 top-8 bg-white border rounded-lg shadow-lg py-1 z-10 min-w-32">
                  <button
                    onClick={() => { onView(); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    查看
                  </button>
                  <button
                    onClick={() => { onEdit(); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                  >
                    <Edit className="w-4 h-4 mr-2" />
                    编辑
                  </button>
                  <button
                    onClick={() => { onCopy(); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                  >
                    <Copy className="w-4 h-4 mr-2" />
                    复制
                  </button>
                  <hr className="my-1" />
                  <button
                    onClick={() => { onDelete(); setShowMenu(false); }}
                    className="w-full px-3 py-2 text-left text-sm hover:bg-red-50 text-red-600 flex items-center"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    删除
                  </button>
                </div>
              )}
            </div>
          </div>

          {exercise.description && (
            <p className="text-sm text-gray-600 mt-2 line-clamp-2">
              {exercise.description}
            </p>
          )}
        </CardHeader>

        <CardContent>
          <div className="space-y-3">
            {/* 统计信息 */}
            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="bg-blue-50 rounded-lg p-2">
                <div className="text-lg font-semibold text-blue-600">
                  {exercise.total_questions}
                </div>
                <div className="text-xs text-gray-600">题目数</div>
              </div>
              <div className="bg-green-50 rounded-lg p-2">
                <div className="text-lg font-semibold text-green-600">
                  {exercise.total_attempts}
                </div>
                <div className="text-xs text-gray-600">参与人数</div>
              </div>
              <div className="bg-purple-50 rounded-lg p-2">
                <div className="text-lg font-semibold text-purple-600">
                  {exercise.average_score.toFixed(1)}
                </div>
                <div className="text-xs text-gray-600">平均分</div>
              </div>
            </div>

            {/* 其他信息 */}
            <div className="flex items-center justify-between text-sm text-gray-500">
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {exercise.time_limit ? `${exercise.time_limit}分钟` : "无限制"}
              </div>
              <div className="flex items-center">
                <Users className="w-4 h-4 mr-1" />
                {exercise.subject}
              </div>
            </div>

            {/* 操作按钮 */}
            <div className="flex gap-2 pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={onView}
                className="flex-1"
              >
                <Eye className="w-4 h-4 mr-1" />
                查看
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={onEdit}
                className="flex-1"
              >
                <Edit className="w-4 h-4 mr-1" />
                编辑
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

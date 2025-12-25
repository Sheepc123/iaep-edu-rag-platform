import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import {
  ArrowLeft,
  Edit,
  Trash2,
  Eye,
  Users,
  Clock,
  Target,
  BarChart3,
  BookOpen,
  CheckCircle,
  XCircle,
  AlertCircle,
  TrendingUp,
  Download,
  Share2,
  Copy,
  Settings
} from "lucide-react";
import { motion } from "framer-motion";
import { exerciseAPI, ExerciseDetail, Question } from "@/services/api";

export const TeacherExerciseDetail: React.FC = () => {
  const { exerciseId } = useParams<{ exerciseId: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();

  // 状态管理
  const [exercise, setExercise] = useState<ExerciseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  // 获取练习详情
  const fetchExerciseDetail = async () => {
    if (!exerciseId) return;

    try {
      setLoading(true);
      const data = await exerciseAPI.getExercise(parseInt(exerciseId));
      setExercise(data);
    } catch (error) {
      console.error("获取练习详情失败:", error);
      toast({
        title: "错误",
        description: "获取练习详情失败",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExerciseDetail();
  }, [exerciseId]);

  // 处理删除练习
  const handleDeleteExercise = async () => {
    if (!exercise || !confirm("确定要删除这个练习吗？此操作不可恢复。")) {
      return;
    }

    try {
      await exerciseAPI.deleteExercise(exercise.id);
      toast({
        title: "成功",
        description: "练习删除成功"
      });
      navigate("/teacher/exercises");
    } catch (error) {
      toast({
        title: "错误",
        description: "删除练习失败",
        variant: "destructive"
      });
    }
  };

  // 处理复制练习
  const handleCopyExercise = async () => {
    if (!exercise) return;

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
    } catch (error) {
      toast({
        title: "错误",
        description: "复制练习失败",
        variant: "destructive"
      });
    }
  };

  // 切换发布状态
  const togglePublishStatus = async () => {
    if (!exercise) return;

    try {
      await exerciseAPI.updateExercise(exercise.id, {
        is_published: !exercise.is_published
      });

      setExercise({
        ...exercise,
        is_published: !exercise.is_published
      });

      toast({
        title: "成功",
        description: exercise.is_published ? "练习已取消发布" : "练习已发布"
      });
    } catch (error) {
      toast({
        title: "错误",
        description: "更新练习状态失败",
        variant: "destructive"
      });
    }
  };

  if (loading) {
    return (
      <TeacherLayout>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        </div>
      </TeacherLayout>
    );
  }

  if (!exercise) {
    return (
      <TeacherLayout>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
          <div className="text-center py-12">
            <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">练习不存在</h3>
            <p className="text-gray-500 mb-6">请检查练习ID是否正确</p>
            <Button onClick={() => navigate("/teacher/exercises")}>
              返回练习列表
            </Button>
          </div>
        </div>
      </TeacherLayout>
    );
  }

  // 难度颜色映射
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
    <TeacherLayout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        {/* 头部 */}
        <motion.div
          className="mb-6"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Button
                variant="ghost"
                onClick={() => navigate("/teacher/exercises")}
                className="mr-4"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                  <BookOpen className="w-8 h-8 mr-3 text-blue-600" />
                  {exercise.title}
                </h1>
                <div className="flex items-center gap-2 mt-2">
                  <Badge className={getDifficultyColor(exercise.difficulty)}>
                    {getDifficultyText(exercise.difficulty)}
                  </Badge>
                  <Badge variant="outline">{exercise.category}</Badge>
                  <Badge variant={exercise.is_published ? "default" : "secondary"}>
                    {exercise.is_published ? "已发布" : "草稿"}
                  </Badge>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={handleCopyExercise}
              >
                <Copy className="w-4 h-4 mr-2" />
                复制
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate(`/teacher/exercises/${exercise.id}/edit`)}
              >
                <Edit className="w-4 h-4 mr-2" />
                编辑
              </Button>
              <Button
                variant={exercise.is_published ? "outline" : "default"}
                onClick={togglePublishStatus}
              >
                {exercise.is_published ? (
                  <>
                    <XCircle className="w-4 h-4 mr-2" />
                    取消发布
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-4 h-4 mr-2" />
                    发布练习
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                onClick={handleDeleteExercise}
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                删除
              </Button>
            </div>
          </div>
        </motion.div>

        {/* 主要内容 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">概览</TabsTrigger>
              <TabsTrigger value="questions">题目</TabsTrigger>
              <TabsTrigger value="statistics">统计</TabsTrigger>
              <TabsTrigger value="results">结果</TabsTrigger>
            </TabsList>

            {/* 概览标签页 */}
            <TabsContent value="overview" className="space-y-6">
              {/* 基本信息卡片 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="w-5 h-5 mr-2" />
                    基本信息
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-blue-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">题目数量</p>
                          <p className="text-2xl font-bold text-blue-600">{exercise.total_questions}</p>
                        </div>
                        <Target className="w-8 h-8 text-blue-600" />
                      </div>
                    </div>

                    <div className="bg-green-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">参与人数</p>
                          <p className="text-2xl font-bold text-green-600">{exercise.total_attempts}</p>
                        </div>
                        <Users className="w-8 h-8 text-green-600" />
                      </div>
                    </div>

                    <div className="bg-purple-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">平均分</p>
                          <p className="text-2xl font-bold text-purple-600">{exercise.average_score.toFixed(1)}</p>
                        </div>
                        <BarChart3 className="w-8 h-8 text-purple-600" />
                      </div>
                    </div>

                    <div className="bg-orange-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">时间限制</p>
                          <p className="text-2xl font-bold text-orange-600">
                            {exercise.time_limit ? `${exercise.time_limit}分` : "无限制"}
                          </p>
                        </div>
                        <Clock className="w-8 h-8 text-orange-600" />
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">练习信息</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">科目：</span>
                          <span className="font-medium">{exercise.subject}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">分类：</span>
                          <span className="font-medium">{exercise.category}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">难度：</span>
                          <Badge className={getDifficultyColor(exercise.difficulty)}>
                            {getDifficultyText(exercise.difficulty)}
                          </Badge>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">状态：</span>
                          <Badge variant={exercise.is_published ? "default" : "secondary"}>
                            {exercise.is_published ? "已发布" : "草稿"}
                          </Badge>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">时间信息</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">创建时间：</span>
                          <span className="font-medium">
                            {new Date(exercise.created_at).toLocaleString()}
                          </span>
                        </div>
                        {exercise.updated_at && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">更新时间：</span>
                            <span className="font-medium">
                              {new Date(exercise.updated_at).toLocaleString()}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {exercise.description && (
                    <div className="mt-6">
                      <h4 className="font-medium text-gray-900 mb-2">练习描述</h4>
                      <p className="text-gray-700 bg-gray-50 rounded-lg p-4">
                        {exercise.description}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* 题目标签页 */}
            <TabsContent value="questions" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <Target className="w-5 h-5 mr-2" />
                      题目列表 ({exercise.questions?.length || 0})
                    </span>
                    <Button
                      onClick={() => navigate(`/teacher/exercises/${exercise.id}/edit`)}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      <Edit className="w-4 h-4 mr-2" />
                      编辑题目
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {exercise.questions && exercise.questions.length > 0 ? (
                    <div className="space-y-4">
                      {exercise.questions.map((question, index) => (
                        <QuestionCard key={question.id} question={question} index={index} />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Target className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">暂无题目</h3>
                      <p className="text-gray-500 mb-4">开始添加题目来完善您的练习</p>
                      <Button
                        onClick={() => navigate(`/teacher/exercises/${exercise.id}/edit`)}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        添加题目
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* 统计标签页 */}
            <TabsContent value="statistics" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2" />
                    数据统计
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8">
                    <TrendingUp className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">统计功能开发中</h3>
                    <p className="text-gray-500">详细的数据分析功能即将上线</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* 结果标签页 */}
            <TabsContent value="results" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Users className="w-5 h-5 mr-2" />
                    学生答题结果
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8">
                    <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">答题结果功能开发中</h3>
                    <p className="text-gray-500">学生答题详情和成绩管理功能即将上线</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>
      </div>
    </TeacherLayout>
  );
};

// 题目卡片组件
interface QuestionCardProps {
  question: Question;
  index: number;
}

const QuestionCard: React.FC<QuestionCardProps> = ({ question, index }) => {
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

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'multiple_choice': return '○';
      case 'fill_blank': return '___';
      case 'essay': return '📝';
      default: return '?';
    }
  };

  const getTypeText = (type: string) => {
    switch (type) {
      case 'multiple_choice': return '选择题';
      case 'fill_blank': return '填空题';
      case 'essay': return '问答题';
      default: return type;
    }
  };

  return (
    <div className="border rounded-lg p-4 bg-white hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-600">第 {index + 1} 题</span>
          <span className="text-lg">{getTypeIcon(question.question_type)}</span>
          <Badge variant="outline">{getTypeText(question.question_type)}</Badge>
          <Badge className={getDifficultyColor(question.difficulty)}>
            {getDifficultyText(question.difficulty)}
          </Badge>
          <Badge variant="outline">{question.points} 分</Badge>
        </div>
      </div>

      <div className="mb-3">
        <p className="text-gray-900 font-medium">{question.question_text}</p>
      </div>

      {question.question_type === 'multiple_choice' && question.options && Array.isArray(question.options) && (
        <div className="space-y-2 mb-3">
          <p className="text-sm font-medium text-gray-700">选项：</p>
          {question.options.map((option, idx) => (
            <div key={idx} className="flex items-center text-sm">
              <span className={`mr-2 ${option === question.correct_answer ? 'text-green-600 font-medium' : 'text-gray-600'}`}>
                {String.fromCharCode(65 + idx)}.
              </span>
              <span className={option === question.correct_answer ? 'text-green-600 font-medium' : 'text-gray-700'}>
                {option}
              </span>
              {option === question.correct_answer && (
                <CheckCircle className="w-4 h-4 ml-2 text-green-600" />
              )}
            </div>
          ))}
        </div>
      )}

      {question.question_type === 'multiple_choice' && question.options && !Array.isArray(question.options) && (
        <div className="space-y-2 mb-3">
          <p className="text-sm font-medium text-gray-700">选项：</p>
          <div className="text-sm text-gray-600">
            选项数据格式错误，无法显示
          </div>
        </div>
      )}

      {(question.question_type === 'fill_blank' || question.question_type === 'essay') && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">
            {question.question_type === 'fill_blank' ? '正确答案：' : '参考答案：'}
          </p>
          <div className="bg-green-50 border border-green-200 rounded p-2">
            <p className="text-sm text-green-800">{question.correct_answer}</p>
          </div>
        </div>
      )}

      {question.explanation && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <p className="text-sm font-medium text-gray-700 mb-1">解析：</p>
          <p className="text-sm text-gray-600 bg-blue-50 rounded p-2">
            {question.explanation}
          </p>
        </div>
      )}
    </div>
  );
};

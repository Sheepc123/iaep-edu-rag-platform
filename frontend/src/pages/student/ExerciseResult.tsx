import { useState, useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { exerciseAPI } from "@/services/api";
import {
  CheckCircle,
  XCircle,
  Clock,
  Target,
  Award,
  TrendingUp,
  RotateCcw,
  ArrowLeft,
  BookOpen,
  Star
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import StudentLayout from "@/components/layouts/StudentLayout";

// 结果数据类型
interface ExerciseResult {
  exerciseId: number;
  title: string;
  subject: string;
  totalQuestions: number;
  correctAnswers: number;
  score: number;
  timeSpent: number; // 秒
  timeLimit: number; // 秒
  difficulty: string;
  questionResults: QuestionResult[];
}

interface QuestionResult {
  questionId: number;
  title: string;
  userAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  points: number;
  earnedPoints: number;
}



export const ExerciseResult = () => {
  const { exerciseId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const attemptId = searchParams.get('attemptId');

  const [result, setResult] = useState<ExerciseResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 获取练习结果数据
  useEffect(() => {
    const fetchResult = async () => {
      if (!attemptId) {
        setError("缺少练习尝试ID");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const attemptData = await exerciseAPI.getExerciseAttempt(parseInt(attemptId));

        // 转换数据格式
        const formattedResult: ExerciseResult = {
          exerciseId: attemptData.exercise_id,
          title: attemptData.exercise.title,
          subject: attemptData.exercise.subject,
          totalQuestions: attemptData.total_questions,
          correctAnswers: attemptData.correct_answers,
          score: Math.round(attemptData.accuracy_rate),
          timeSpent: attemptData.time_spent,
          timeLimit: (attemptData.exercise.time_limit || 60) * 60, // 转换为秒
          difficulty: attemptData.exercise.difficulty,
          questionResults: attemptData.answers.map(answer => ({
            questionId: answer.question_id,
            title: answer.question.title || `题目 ${answer.question_id}`,
            userAnswer: answer.answer,
            correctAnswer: answer.question.correct_answer,
            isCorrect: answer.is_correct,
            points: answer.question.points,
            earnedPoints: answer.points_earned
          }))
        };

        setResult(formattedResult);
      } catch (err: any) {
        console.error("获取练习结果失败:", err);
        setError(err.message || "获取练习结果失败");
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [attemptId]);

  // 加载状态
  if (loading) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">正在加载练习结果...</p>
          </div>
        </div>
      </StudentLayout>
    );
  }

  // 错误状态
  if (error) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <XCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">加载失败</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={() => navigate('/student/exercises')}>
              返回练习列表
            </Button>
          </div>
        </div>
      </StudentLayout>
    );
  }

  // 结果数据不存在
  if (!result) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">结果不存在</h2>
            <p className="text-gray-600 mb-4">未找到练习结果</p>
            <Button onClick={() => navigate('/student/exercises')}>
              返回练习列表
            </Button>
          </div>
        </div>
      </StudentLayout>
    );
  }

  const accuracy = Math.round((result.correctAnswers / result.totalQuestions) * 100);
  const timeUsedPercentage = (result.timeSpent / result.timeLimit) * 100;

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}分${secs}秒`;
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600";
    if (score >= 80) return "text-blue-600";
    if (score >= 70) return "text-yellow-600";
    return "text-red-600";
  };

  const getScoreBadge = (score: number) => {
    if (score >= 90) return { text: "优秀", color: "bg-green-100 text-green-600" };
    if (score >= 80) return { text: "良好", color: "bg-blue-100 text-blue-600" };
    if (score >= 70) return { text: "及格", color: "bg-yellow-100 text-yellow-600" };
    return { text: "不及格", color: "bg-red-100 text-red-600" };
  };

  const scoreBadge = getScoreBadge(result.score);

  return (
    <StudentLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* 头部 */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between"
        >
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/student/exercises')}
              className="text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              返回练习
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">练习结果</h1>
              <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                <span className="flex items-center">
                  <BookOpen className="w-4 h-4 mr-1" />
                  {result.subject}
                </span>
                <Badge variant="outline">{result.difficulty}</Badge>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <Button
              variant="outline"
              onClick={() => navigate(`/student/exercises/practice/${exerciseId}`)}
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              重新练习
            </Button>
            <Button onClick={() => navigate('/student/exercises')}>
              完成
            </Button>
          </div>
        </motion.div>

        {/* 总体结果卡片 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-50 to-purple-50">
            <CardHeader className="text-center pb-4">
              <div className="flex items-center justify-center mb-4">
                <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-lg">
                  <Award className="w-10 h-10 text-blue-600" />
                </div>
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                {result.title}
              </CardTitle>
              <div className="flex items-center justify-center space-x-2 mt-2">
                <Badge className={scoreBadge.color}>
                  {scoreBadge.text}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {/* 总分 */}
                <div className="text-center">
                  <div className={`text-4xl font-bold ${getScoreColor(result.score)} mb-2`}>
                    {result.score}
                  </div>
                  <div className="text-sm text-gray-600">总分</div>
                </div>

                {/* 正确率 */}
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">
                    {accuracy}%
                  </div>
                  <div className="text-sm text-gray-600">正确率</div>
                </div>

                {/* 用时 */}
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600 mb-2">
                    {formatTime(result.timeSpent)}
                  </div>
                  <div className="text-sm text-gray-600">用时</div>
                </div>

                {/* 题目数 */}
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    {result.correctAnswers}/{result.totalQuestions}
                  </div>
                  <div className="text-sm text-gray-600">正确题数</div>
                </div>
              </div>

              {/* 时间进度条 */}
              <div className="mt-6">
                <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                  <span>时间使用</span>
                  <span>{formatTime(result.timeSpent)} / {formatTime(result.timeLimit)}</span>
                </div>
                <Progress value={timeUsedPercentage} className="h-2" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 详细统计 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <Card className="border-0 shadow-md">
            <CardContent className="p-6 text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div className="text-2xl font-bold text-green-600 mb-1">
                {result.correctAnswers}
              </div>
              <div className="text-sm text-gray-600">答对题数</div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6 text-center">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <XCircle className="w-6 h-6 text-red-600" />
              </div>
              <div className="text-2xl font-bold text-red-600 mb-1">
                {result.totalQuestions - result.correctAnswers}
              </div>
              <div className="text-sm text-gray-600">答错题数</div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardContent className="p-6 text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Clock className="w-6 h-6 text-blue-600" />
              </div>
              <div className="text-2xl font-bold text-blue-600 mb-1">
                {Math.round(result.timeSpent / result.totalQuestions)}s
              </div>
              <div className="text-sm text-gray-600">平均用时</div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 题目详情 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl font-bold flex items-center">
                <Target className="w-5 h-5 mr-2 text-blue-600" />
                题目详情
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {result.questionResults.map((question, index) => (
                  <motion.div
                    key={question.questionId}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + index * 0.1 }}
                  >
                    <QuestionResultItem question={question} index={index + 1} />
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 学习建议 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card className="border-0 shadow-lg bg-gradient-to-br from-yellow-50 to-orange-50">
            <CardHeader>
              <CardTitle className="text-xl font-bold flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-orange-600" />
                学习建议
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <Star className="w-5 h-5 text-orange-500 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-gray-900">表现评价</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {result.score >= 90 ? "表现优秀！继续保持这种学习状态。" :
                       result.score >= 80 ? "表现良好，还有提升空间。" :
                       result.score >= 70 ? "基本掌握，需要加强练习。" :
                       "需要重点复习相关知识点。"}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <Star className="w-5 h-5 text-orange-500 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-gray-900">改进建议</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      建议重点复习答错的题目，理解解题思路。可以寻求AI助手的帮助来深入理解相关概念。
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </StudentLayout>
  );
};

// 题目结果项组件
interface QuestionResultItemProps {
  question: QuestionResult;
  index: number;
}

const QuestionResultItem = ({ question, index }: QuestionResultItemProps) => {
  return (
    <div className={`p-4 rounded-lg border-2 ${
      question.isCorrect 
        ? 'border-green-200 bg-green-50' 
        : 'border-red-200 bg-red-50'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            question.isCorrect 
              ? 'bg-green-500 text-white' 
              : 'bg-red-500 text-white'
          }`}>
            {question.isCorrect ? (
              <CheckCircle className="w-5 h-5" />
            ) : (
              <XCircle className="w-5 h-5" />
            )}
          </div>
          
          <div className="flex-1">
            <h4 className="font-medium text-gray-900 mb-2">
              第{index}题：{question.title}
            </h4>
            
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-gray-600">你的答案：</span>
                <span className={question.isCorrect ? 'text-green-700' : 'text-red-700'}>
                  {question.userAnswer}
                </span>
              </div>
              
              {!question.isCorrect && (
                <div>
                  <span className="text-gray-600">正确答案：</span>
                  <span className="text-green-700">{question.correctAnswer}</span>
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className={`text-lg font-bold ${
            question.isCorrect ? 'text-green-600' : 'text-red-600'
          }`}>
            {question.earnedPoints}/{question.points}
          </div>
          <div className="text-xs text-gray-500">分</div>
        </div>
      </div>
    </div>
  );
};

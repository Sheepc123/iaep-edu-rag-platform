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
  Star,
  User,
  Calendar,
  AlertTriangle,
  History,
  Eye,
  FileText
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import StudentLayout from "@/components/layouts/StudentLayout";

// 扩展的结果数据类型
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
  // 新增字段
  studentName: string;
  completedAt: string;
  attemptNumber: number;
  isCompleted: boolean;
  wrongQuestions: QuestionResult[];
}

interface QuestionResult {
  questionId: number;
  title: string;
  content: string;
  questionType: string;
  userAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  points: number;
  earnedPoints: number;
  explanation?: string;
}

// 练习历史记录类型
interface ExerciseHistory {
  id: number;
  attemptNumber: number;
  score: number;
  accuracy: number;
  timeSpent: number;
  completedAt: string;
  isCompleted: boolean;
}



export const ExerciseResult = () => {
  const { exerciseId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const attemptId = searchParams.get('attemptId');

  const [result, setResult] = useState<ExerciseResult | null>(null);
  const [history, setHistory] = useState<ExerciseHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("result");

  // 获取练习结果数据和历史记录
  useEffect(() => {
    const fetchData = async () => {
      if (!attemptId) {
        setError("缺少练习尝试ID");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);

        // 获取当前练习结果
        const attemptData = await exerciseAPI.getExerciseAttempt(parseInt(attemptId));

        // 获取练习历史记录
        const historyData = await exerciseAPI.getMyAttempts(attemptData.exercise_id);

        // 转换结果数据格式
        const wrongQuestions = attemptData.answers.filter(answer => !answer.is_correct);

        const formattedResult: ExerciseResult = {
          exerciseId: attemptData.exercise_id,
          title: attemptData.exercise.title,
          subject: attemptData.exercise.subject,
          totalQuestions: attemptData.total_questions,
          correctAnswers: attemptData.correct_answers,
          score: Math.round(attemptData.score || (attemptData.correct_answers / attemptData.total_questions * 100)),
          timeSpent: attemptData.time_spent,
          timeLimit: (attemptData.exercise.time_limit || 60) * 60, // 转换为秒
          difficulty: attemptData.exercise.difficulty,
          studentName: "当前学生", // TODO: 从用户信息获取
          completedAt: attemptData.submitted_at || attemptData.completed_at,
          attemptNumber: historyData.length,
          isCompleted: attemptData.is_completed,
          questionResults: attemptData.answers.map(answer => ({
            questionId: answer.question_id,
            title: answer.question.title || `题目 ${answer.question_id}`,
            content: answer.question.content,
            questionType: answer.question.question_type,
            userAnswer: answer.answer_content || answer.answer,
            correctAnswer: answer.question.correct_answer,
            isCorrect: answer.is_correct,
            points: answer.question.points,
            earnedPoints: answer.points_earned,
            explanation: answer.question.explanation
          })),
          wrongQuestions: wrongQuestions.map(answer => ({
            questionId: answer.question_id,
            title: answer.question.title || `题目 ${answer.question_id}`,
            content: answer.question.content,
            questionType: answer.question.question_type,
            userAnswer: answer.answer_content || answer.answer,
            correctAnswer: answer.question.correct_answer,
            isCorrect: answer.is_correct,
            points: answer.question.points,
            earnedPoints: answer.points_earned,
            explanation: answer.question.explanation
          }))
        };

        // 转换历史记录格式
        const formattedHistory: ExerciseHistory[] = historyData.map((attempt, index) => ({
          id: attempt.id,
          attemptNumber: index + 1,
          score: Math.round(attempt.score || (attempt.correct_answers / attempt.total_questions * 100)),
          accuracy: Math.round((attempt.correct_answers / attempt.total_questions) * 100),
          timeSpent: attempt.time_spent,
          completedAt: attempt.submitted_at || attempt.completed_at,
          isCompleted: attempt.is_completed
        }));

        setResult(formattedResult);
        setHistory(formattedHistory);
      } catch (err: any) {
        console.error("获取练习数据失败:", err);
        setError(err.message || "获取练习数据失败");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
      <div className="max-w-6xl mx-auto space-y-6">
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
              <h1 className="text-2xl font-bold text-gray-900">{result.title}</h1>
              <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                <span className="flex items-center">
                  <BookOpen className="w-4 h-4 mr-1" />
                  {result.subject}
                </span>
                <Badge variant="outline">{result.difficulty}</Badge>
                <span className="flex items-center">
                  <User className="w-4 h-4 mr-1" />
                  {result.studentName}
                </span>
                <span className="flex items-center">
                  <Calendar className="w-4 h-4 mr-1" />
                  第{result.attemptNumber}次练习
                </span>
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

        {/* 标签页导航 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="result" className="flex items-center space-x-2">
                <Target className="w-4 h-4" />
                <span>练习结果</span>
              </TabsTrigger>
              <TabsTrigger value="wrong" className="flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4" />
                <span>错题分析</span>
              </TabsTrigger>
              <TabsTrigger value="history" className="flex items-center space-x-2">
                <History className="w-4 h-4" />
                <span>历史记录</span>
              </TabsTrigger>
              <TabsTrigger value="details" className="flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>题目详情</span>
              </TabsTrigger>
            </TabsList>

            {/* 练习结果标签页 */}
            <TabsContent value="result" className="space-y-6 mt-6">
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
      </TabsContent>

      {/* 错题分析标签页 */}
      <TabsContent value="wrong" className="space-y-6 mt-6">
        <WrongQuestionsAnalysis wrongQuestions={result.wrongQuestions} />
      </TabsContent>

      {/* 历史记录标签页 */}
      <TabsContent value="history" className="space-y-6 mt-6">
        <ExerciseHistoryView history={history} currentAttempt={result} />
      </TabsContent>

      {/* 题目详情标签页 */}
      <TabsContent value="details" className="space-y-6 mt-6">
        <QuestionDetailsView questions={result.questionResults} />
      </TabsContent>

    </Tabs>
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

// 错题分析组件
interface WrongQuestionsAnalysisProps {
  wrongQuestions: QuestionResult[];
}

const WrongQuestionsAnalysis = ({ wrongQuestions }: WrongQuestionsAnalysisProps) => {
  if (wrongQuestions.length === 0) {
    return (
      <Card>
        <CardContent className="text-center py-12">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">全部答对！</h3>
          <p className="text-gray-600">恭喜你，这次练习没有错题。</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2 text-red-500" />
            错题分析 ({wrongQuestions.length} 道)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {wrongQuestions.map((question, index) => (
              <div key={question.questionId} className="border-l-4 border-red-500 pl-4">
                <div className="bg-red-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">
                    第{index + 1}题：{question.title}
                  </h4>

                  <div className="mb-3">
                    <p className="text-gray-700 mb-2">{question.content}</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                    <div>
                      <span className="text-sm font-medium text-gray-600">你的答案：</span>
                      <div className="mt-1 p-2 bg-red-100 rounded text-red-700">
                        {question.userAnswer}
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">正确答案：</span>
                      <div className="mt-1 p-2 bg-green-100 rounded text-green-700">
                        {question.correctAnswer}
                      </div>
                    </div>
                  </div>

                  {question.explanation && (
                    <div className="mt-3 p-3 bg-blue-50 rounded">
                      <span className="text-sm font-medium text-blue-800">解析：</span>
                      <p className="text-sm text-blue-700 mt-1">{question.explanation}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// 历史记录组件
interface ExerciseHistoryViewProps {
  history: ExerciseHistory[];
  currentAttempt: ExerciseResult;
}

const ExerciseHistoryView = ({ history, currentAttempt }: ExerciseHistoryViewProps) => {
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}分${remainingSeconds}秒`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN');
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <History className="w-5 h-5 mr-2 text-blue-500" />
            练习历史记录 ({history.length} 次)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {history.map((attempt, index) => (
              <div
                key={attempt.id}
                className={`p-4 rounded-lg border-2 ${
                  attempt.attemptNumber === currentAttempt.attemptNumber ?
                  'border-blue-500 bg-blue-50' :
                  'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      attempt.attemptNumber === currentAttempt.attemptNumber ?
                      'bg-blue-500 text-white' :
                      'bg-gray-400 text-white'
                    }`}>
                      {attempt.attemptNumber}
                    </div>

                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">第{attempt.attemptNumber}次练习</span>
                        {attempt.attemptNumber === currentAttempt.attemptNumber && (
                          <Badge variant="default">当前</Badge>
                        )}
                        {attempt.isCompleted && (
                          <Badge variant="outline" className="text-green-600 border-green-600">
                            已完成
                          </Badge>
                        )}
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        {formatDate(attempt.completedAt)}
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="flex items-center space-x-6">
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-600">
                          {attempt.score}分
                        </div>
                        <div className="text-xs text-gray-500">得分</div>
                      </div>

                      <div className="text-center">
                        <div className="text-lg font-bold text-green-600">
                          {attempt.accuracy}%
                        </div>
                        <div className="text-xs text-gray-500">正确率</div>
                      </div>

                      <div className="text-center">
                        <div className="text-lg font-bold text-orange-600">
                          {formatTime(attempt.timeSpent)}
                        </div>
                        <div className="text-xs text-gray-500">用时</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// 题目详情组件
interface QuestionDetailsViewProps {
  questions: QuestionResult[];
}

const QuestionDetailsView = ({ questions }: QuestionDetailsViewProps) => {
  const getQuestionTypeLabel = (type: string) => {
    switch (type) {
      case 'multiple_choice':
        return '选择题';
      case 'fill_blank':
        return '填空题';
      case 'essay':
        return '问答题';
      default:
        return '未知类型';
    }
  };

  const getQuestionTypeColor = (type: string) => {
    switch (type) {
      case 'multiple_choice':
        return 'bg-blue-100 text-blue-800';
      case 'fill_blank':
        return 'bg-green-100 text-green-800';
      case 'essay':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="w-5 h-5 mr-2 text-gray-500" />
            题目详情 ({questions.length} 道)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {questions.map((question, index) => (
              <div key={question.questionId} className="border rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      question.isCorrect ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                    }`}>
                      {index + 1}
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{question.title}</h4>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge className={getQuestionTypeColor(question.questionType)}>
                          {getQuestionTypeLabel(question.questionType)}
                        </Badge>
                        <span className="text-sm text-gray-500">
                          {question.points} 分
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className={`text-lg font-bold ${
                      question.isCorrect ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {question.earnedPoints}/{question.points}
                    </div>
                    <div className="text-xs text-gray-500">得分</div>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-gray-700">{question.content}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <span className="text-sm font-medium text-gray-600">你的答案：</span>
                    <div className={`mt-1 p-2 rounded ${
                      question.isCorrect ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {question.userAnswer || '未作答'}
                    </div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-600">正确答案：</span>
                    <div className="mt-1 p-2 bg-green-100 rounded text-green-700">
                      {question.correctAnswer}
                    </div>
                  </div>
                </div>

                {question.explanation && (
                  <div className="p-3 bg-blue-50 rounded">
                    <span className="text-sm font-medium text-blue-800">解析：</span>
                    <p className="text-sm text-blue-700 mt-1">{question.explanation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

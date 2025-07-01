import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { exerciseAPI } from "@/services/api";
import {
  Clock,
  CheckCircle,
  XCircle,
  ArrowLeft,
  ArrowRight,
  Flag,
  RotateCcw,
  Send,
  AlertTriangle,
  BookOpen,
  Target,
  List,
  X,
  FileText
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import StudentLayout from "@/components/layouts/StudentLayout";

// 使用API中的Question类型，不需要重复定义
import { Question } from '@/services/api';

interface Exercise {
  id: number;
  title: string;
  subject: string;
  difficulty: string;
  timeLimit: number; // 分钟
  totalQuestions: number;
  questions: Question[];
  description: string;
}



export const ExercisePractice = () => {
  const { exerciseId } = useParams();
  const navigate = useNavigate();

  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showQuestionList, setShowQuestionList] = useState(false);
  const [attemptId, setAttemptId] = useState<number | null>(null);

  // 获取练习数据
  useEffect(() => {
    const fetchExerciseData = async () => {
      if (!exerciseId) {
        setError("练习ID不存在");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);

        // 获取练习详情
        const exerciseData = await exerciseAPI.getExerciseDetail(parseInt(exerciseId));

        // 转换数据格式以匹配组件期望的格式
        const timeLimit = exerciseData.time_limit || 60; // 默认60分钟
        const formattedExercise: Exercise = {
          id: exerciseData.id,
          title: exerciseData.title,
          subject: exerciseData.subject,
          difficulty: exerciseData.difficulty,
          timeLimit: timeLimit,
          totalQuestions: exerciseData.total_questions,
          description: exerciseData.description || "",
          questions: exerciseData.questions?.map(q => {
            // 处理选项格式 - 支持对象和数组两种格式
            let formattedOptions: string[] = [];
            if (q.options) {
              if (Array.isArray(q.options)) {
                formattedOptions = q.options;
              } else if (typeof q.options === 'object') {
                // 将对象格式转换为数组格式：{"A": "选项1"} -> ["A. 选项1"]
                formattedOptions = Object.entries(q.options).map(([key, value]) => `${key}. ${value}`);
              }
            }

            // 直接返回API格式的Question对象，不需要转换
            return {
              ...q,
              options: formattedOptions
            };
          }) || []
        };

        console.log("练习数据:", formattedExercise);
        console.log("时间限制:", timeLimit, "分钟，总秒数:", timeLimit * 60);

        setExercise(formattedExercise);
        setTimeLeft(timeLimit * 60);

        // 开始练习尝试
        const attempt = await exerciseAPI.startExercise(parseInt(exerciseId));
        setAttemptId(attempt.id);

      } catch (err: any) {
        console.error("获取练习数据失败:", err);
        setError(err.message || "获取练习数据失败");
      } finally {
        setLoading(false);
      }
    };

    fetchExerciseData();
  }, [exerciseId]);

  const currentQuestion = exercise?.questions[currentQuestionIndex];
  const progress = exercise ? ((currentQuestionIndex + 1) / exercise.totalQuestions) * 100 : 0;

  // 调试信息
  console.log("当前题目索引:", currentQuestionIndex);
  console.log("总题目数:", exercise?.questions.length);
  console.log("是否最后一题:", exercise ? currentQuestionIndex === exercise.questions.length - 1 : false);
  console.log("是否已提交:", isSubmitted);
  console.log("显示解析:", showExplanation);
  console.log("showCorrect条件:", isSubmitted && showExplanation);
  console.log("当前答案:", answers);

  // 计时器
  useEffect(() => {
    if (timeLeft > 0 && !isSubmitted) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !isSubmitted) {
      // 时间到了自动提交
      handleSubmit();
    }
  }, [timeLeft, isSubmitted]);

  // 格式化时间显示
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // 处理答案选择
  const handleAnswerChange = (answer: string) => {
    if (!currentQuestion) return;
    console.log(`🔄 答案变更: 题目${currentQuestion.id}, 答案: ${answer}`);
    setAnswers(prev => {
      const newAnswers = {
        ...prev,
        [currentQuestion.id]: answer
      };
      console.log(`📝 更新后的答案状态:`, newAnswers);
      return newAnswers;
    });
  };

  // 下一题
  const handleNext = () => {
    if (exercise && currentQuestionIndex < exercise.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setShowExplanation(false);
    }
  };

  // 上一题
  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      setShowExplanation(false);
    }
  };

  // 跳转到指定题目
  const handleJumpToQuestion = (index: number) => {
    setCurrentQuestionIndex(index);
    setShowExplanation(false);
    setShowQuestionList(false);
  };

  // 检查答案是否正确
  const checkAnswer = (question: Question, userAnswer: string): boolean => {
    const correctAnswer = question.correct_answer;

    if (question.question_type === 'multiple_choice') {
      // 选择题：比较选项字母
      return userAnswer === correctAnswer;
    } else if (question.question_type === 'fill_blank') {
      // 填空题：忽略大小写和前后空格
      const normalize = (ans: string) => ans.trim().toLowerCase();
      return normalize(userAnswer) === normalize(correctAnswer);
    } else if (question.question_type === 'essay') {
      // 问答题：暂时不自动判断，需要人工评分
      return false;
    }

    return false;
  };

  // 提交练习
  const handleSubmit = async () => {
    console.log("handleSubmit 被调用");
    console.log("attemptId:", attemptId);
    console.log("exercise:", exercise);
    console.log("answers:", answers);

    if (!attemptId || !exercise) {
      console.error("缺少必要的数据：attemptId或exercise");
      console.error("attemptId:", attemptId);
      console.error("exercise:", exercise);
      return;
    }

    try {
      console.log("📝 设置提交状态...");
      setIsSubmitted(true);
      setShowExplanation(true);

      // 强制重新渲染
      console.log("✅ 状态已设置: isSubmitted=true, showExplanation=true");

      // 准备提交的答案数据
      const submitData = {
        attempt_id: attemptId,
        answers: exercise.questions.map(question => ({
          question_id: question.id,
          answer_content: answers[question.id] || "",
          time_spent: 0 // 可以后续添加每题用时统计
        }))
      };

      console.log("📤 提交答案数据:", submitData);
      console.log("🎯 现在应该显示正确答案了！");

      // 不立即跳转，让用户查看答案
      console.log("答案已提交，现在显示正确答案和解析");
      // 用户可以通过"查看结果"按钮手动跳转

      // 调用API提交答案
      try {
        console.log("📤 开始调用API提交答案...");
        const result = await exerciseAPI.submitExercise(submitData);
        console.log("✅ API调用成功，结果:", result);

        // 标记练习为已完成
        console.log("✅ 练习已完成并提交");
      } catch (apiError) {
        console.error("❌ API调用失败:", apiError);
        // 即使API失败，也显示答案（用于调试）
      }

    } catch (error: any) {
      console.error("提交答案失败:", error);
      setIsSubmitted(false);
      setShowExplanation(false);
      // 可以添加错误提示
    }
  };

  // 查看详细结果
  const handleViewResult = () => {
    navigate(`/student/exercises/result/${exerciseId}?attemptId=${attemptId}`);
  };

  // 返回练习列表
  const handleBack = () => {
    navigate('/student/exercises');
  };

  // 重新开始
  const handleRestart = () => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    if (exercise) {
      setTimeLeft(exercise.timeLimit * 60);
    }
    setIsSubmitted(false);
    setShowExplanation(false);
  };

  // 加载状态
  if (loading) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">正在加载练习数据...</p>
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
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
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

  // 练习数据不存在
  if (!exercise) {
    return (
      <StudentLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">练习不存在</h2>
            <p className="text-gray-600 mb-4">未找到指定的练习</p>
            <Button onClick={() => navigate('/student/exercises')}>
              返回练习列表
            </Button>
          </div>
        </div>
      </StudentLayout>
    );
  }

  return (
    <StudentLayout fullScreen>
      <div className="h-screen flex flex-col relative bg-gray-50">
        {/* 题目导航弹窗 */}
        {showQuestionList && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="bg-white rounded-2xl p-6 shadow-2xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-gray-900">题目导航</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowQuestionList(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

              <div className="grid grid-cols-5 gap-3">
                {exercise.questions.map((question, index) => {
                  const isAnswered = answers[question.id];
                  const isCurrent = index === currentQuestionIndex;

                  return (
                    <motion.button
                      key={question.id}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => handleJumpToQuestion(index)}
                      className={`
                        relative p-4 rounded-lg border-2 text-center transition-all
                        ${isCurrent
                          ? 'border-blue-500 bg-blue-50 text-blue-700'
                          : isAnswered
                          ? 'border-green-300 bg-green-50 text-green-700'
                          : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                        }
                      `}
                    >
                      <div className="text-lg font-bold mb-1">{index + 1}</div>
                      <div className="text-xs">
                        {isCurrent ? '当前' : isAnswered ? '已答' : '未答'}
                      </div>
                      {isCurrent && (
                        <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full"></div>
                      )}
                    </motion.button>
                  );
                })}
              </div>

              <div className="mt-6 flex items-center justify-between text-sm text-gray-600">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-200 rounded"></div>
                    <span>已答题 ({Object.keys(answers).length})</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-gray-200 rounded"></div>
                    <span>未答题 ({exercise.questions.length - Object.keys(answers).length})</span>
                  </div>
                </div>
                <div className="text-blue-600 font-medium">
                  总计 {exercise.questions.length} 题
                </div>
              </div>
            </motion.div>
          </div>
        )}

        <div className="flex-1 flex flex-col space-y-4 p-4">
          {/* 头部信息 */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-between bg-white rounded-lg shadow-sm border p-4"
          >
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleBack}
                className="text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回练习
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{exercise.title}</h1>
                <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                  <span className="flex items-center">
                    <BookOpen className="w-4 h-4 mr-1" />
                    {exercise.subject}
                  </span>
                  <Badge variant="outline">{exercise.difficulty}</Badge>
                  <span>{exercise.totalQuestions} 题</span>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* 题目导航按钮 */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowQuestionList(true)}
                className="text-blue-600 border-blue-200 hover:bg-blue-50"
              >
                <List className="w-4 h-4 mr-2" />
                题目导航
              </Button>

              {/* 计时器 */}
              <div className="flex items-center space-x-2 px-3 py-2 bg-gray-50 rounded-lg">
                <Clock className="w-4 h-4 text-gray-600" />
                <span className={`font-mono text-sm ${timeLeft < 300 ? 'text-red-600' : 'text-gray-900'}`}>
                  {formatTime(timeLeft)}
                </span>
              </div>

              {/* 进度 */}
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">进度</span>
                <div className="w-32">
                  <Progress value={progress} className="h-2" />
                </div>
                <span className="text-sm font-medium">
                  {currentQuestionIndex + 1}/{exercise.totalQuestions}
                </span>
              </div>
            </div>
          </motion.div>

          {/* 题目卡片 */}
          {currentQuestion && (
            <motion.div
              key={currentQuestion.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="flex-1 flex flex-col"
            >
            <Card className="border-0 shadow-lg flex-1 flex flex-col">
              <CardHeader className="pb-4 flex-shrink-0">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-bold flex items-center">
                    <Target className="w-5 h-5 mr-2 text-blue-600" />
                    第 {currentQuestionIndex + 1} 题
                    <Badge variant="secondary" className="ml-2">
                      {currentQuestion.points} 分
                    </Badge>
                  </CardTitle>
                  <Badge
                    variant="outline"
                    className={
                      currentQuestion.difficulty === 'easy' ? 'text-green-600 border-green-200' :
                      currentQuestion.difficulty === 'medium' ? 'text-yellow-600 border-yellow-200' :
                      'text-red-600 border-red-200'
                    }
                  >
                    {currentQuestion.difficulty === 'easy' ? '简单' :
                     currentQuestion.difficulty === 'medium' ? '中等' : '困难'}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col space-y-6 p-6">
                {/* 题目内容 */}
                <div className="flex-shrink-0">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    {currentQuestion.title}
                  </h3>
                  <p className="text-gray-700 leading-relaxed text-lg">
                    {currentQuestion.content}
                  </p>
                </div>

                {/* 答题区域 */}
                <div className="flex-1 flex flex-col justify-center">
                  <QuestionInput
                    question={currentQuestion}
                    answer={answers[currentQuestion.id] || ''}
                    onAnswerChange={handleAnswerChange}
                    disabled={isSubmitted}
                    showCorrect={isSubmitted}
                  />
                </div>

                {/* 提交成功提示 */}
                <AnimatePresence>
                  {isSubmitted && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4"
                    >
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                        <div>
                          <h4 className="font-medium text-green-900">答案已提交</h4>
                          <p className="text-green-700 text-sm">
                            您可以查看每道题的正确答案和解析，点击"查看详细结果"查看完整报告。
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* 解析 */}
                <AnimatePresence>
                  {showExplanation && isSubmitted && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="border-t pt-4"
                    >
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <div className="flex items-start space-x-2">
                          <AlertTriangle className="w-5 h-5 text-blue-600 mt-0.5" />
                          <div>
                            <h4 className="font-semibold text-blue-900 mb-2">解析</h4>
                            <p className="text-blue-800 text-sm leading-relaxed">
                              {currentQuestion.explanation}
                            </p>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </CardContent>
            </Card>
          </motion.div>
          )}

          {/* 底部操作栏 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm border flex-shrink-0"
          >
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentQuestionIndex === 0}
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                上一题
              </Button>

              {!isSubmitted && (
                <Button
                  variant="outline"
                  onClick={() => setShowExplanation(!showExplanation)}
                  className="text-orange-600 border-orange-200 hover:bg-orange-50"
                >
                  <Flag className="w-4 h-4 mr-2" />
                  标记
                </Button>
              )}
            </div>

            <div className="flex items-center space-x-3">
              {isSubmitted && (
                <>
                  <Button
                    onClick={handleViewResult}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    <FileText className="w-4 h-4 mr-2" />
                    查看详细结果
                  </Button>
                  <Button
                    variant="outline"
                    onClick={handleRestart}
                    className="text-blue-600 border-blue-200 hover:bg-blue-50"
                  >
                    <RotateCcw className="w-4 h-4 mr-2" />
                    重新开始
                  </Button>
                </>
              )}

              {!isSubmitted ? (
                currentQuestionIndex === exercise.questions.length - 1 ? (
                  <Button
                    onClick={() => {
                      console.log("提交按钮被点击");
                      handleSubmit();
                    }}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    <Send className="w-4 h-4 mr-2" />
                    提交答案
                  </Button>
                ) : (
                  <Button onClick={handleNext}>
                    下一题
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                )
              ) : (
                <Button
                  onClick={handleNext}
                  disabled={currentQuestionIndex === exercise.questions.length - 1}
                >
                  下一题
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </StudentLayout>
  );
};

// 题目输入组件
interface QuestionInputProps {
  question: Question;
  answer: string;
  onAnswerChange: (answer: string) => void;
  disabled: boolean;
  showCorrect: boolean;
}

const QuestionInput = ({ question, answer, onAnswerChange, disabled, showCorrect }: QuestionInputProps) => {
  console.log(`🎯 QuestionInput渲染: disabled=${disabled}, showCorrect=${showCorrect}, answer=${answer}`);

  if (question.question_type === 'multiple_choice') {
    // 在组件顶层计算这些值，避免作用域问题
    const correctAnswer = question.correct_answer;
    const isUserAnswerCorrect = answer === correctAnswer;

    console.log(`📝 选择题数据:`, {
      question_id: question.id,
      correct_answer: question.correct_answer,
      final_correctAnswer: correctAnswer,
      user_answer: answer,
      isUserAnswerCorrect
    });

    return (
      <div className="space-y-4">
        {question.options?.map((option, index) => {
          // 提取选项字母（支持 "A. 选项内容" 格式）
          const optionLetter = option.includes('.') ? option.split('.')[0].trim() : String.fromCharCode(65 + index);
          const isSelected = answer === optionLetter;
          const isCorrect = optionLetter === correctAnswer;

          console.log(`选项 ${optionLetter}: isSelected=${isSelected}, isCorrect=${isCorrect}, showCorrect=${showCorrect}`);

          console.log(`选项: ${option}, 字母: ${optionLetter}, 正确答案: ${correctAnswer}, 是否正确: ${isCorrect}, 是否选中: ${isSelected}, 用户答案是否正确: ${isUserAnswerCorrect}`);
          
          return (
            <motion.div
              key={index}
              whileHover={!disabled ? { scale: 1.01 } : {}}
              whileTap={!disabled ? { scale: 0.99 } : {}}
            >
              <label
                className={`flex items-center p-6 rounded-xl border-2 cursor-pointer transition-all ${
                  disabled
                    ? showCorrect && isCorrect
                      ? 'border-green-300 bg-green-50'
                      : showCorrect && isSelected && !isCorrect
                      ? 'border-red-300 bg-red-50'
                      : 'border-gray-200 bg-gray-50 cursor-not-allowed'
                    : isSelected
                    ? 'border-blue-400 bg-blue-50 shadow-md'
                    : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
                }`}
              >
                <input
                  type="radio"
                  name={`question-${question.id}`}
                  value={optionLetter}
                  checked={isSelected}
                  onChange={(e) => onAnswerChange(e.target.value)}
                  disabled={disabled}
                  className="sr-only"
                />
                <div className={`w-6 h-6 rounded-full border-2 mr-4 flex items-center justify-center ${
                  disabled && showCorrect && isCorrect
                    ? 'border-green-500 bg-green-500'
                    : disabled && showCorrect && isSelected && !isCorrect
                    ? 'border-red-500 bg-red-500'
                    : isSelected
                    ? 'border-blue-500 bg-blue-500'
                    : 'border-gray-300'
                }`}>
                  {(isSelected || (showCorrect && isCorrect)) && (
                    <div className="w-3 h-3 rounded-full bg-white" />
                  )}
                  {showCorrect && isCorrect && (
                    <CheckCircle className="w-5 h-5 text-white" />
                  )}
                  {showCorrect && isSelected && !isCorrect && (
                    <XCircle className="w-5 h-5 text-white" />
                  )}
                </div>
                <span className={`text-base leading-relaxed ${
                  disabled && showCorrect && isCorrect
                    ? 'text-green-800 font-medium'
                    : disabled && showCorrect && isSelected && !isCorrect
                    ? 'text-red-800'
                    : 'text-gray-700'
                }`}>
                  {option}
                </span>
              </label>
            </motion.div>
          );
        })}

        {/* 显示答案结果 */}
        {showCorrect && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="text-sm space-y-2">
              <div className="text-gray-600">
                正确答案：<span className="font-medium text-green-600">{correctAnswer}</span>
              </div>
              {answer && (
                <div className="text-gray-600">
                  您的答案：<span className={`font-medium ${isUserAnswerCorrect ? 'text-green-600' : 'text-red-600'}`}>
                    {answer}
                  </span>
                  {isUserAnswerCorrect && <span className="text-green-600 ml-2">✓ 正确</span>}
                  {!isUserAnswerCorrect && <span className="text-red-600 ml-2">✗ 错误</span>}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  }

  if (question.question_type === 'fill_blank') {
    // 答案比较（忽略大小写和前后空格）
    const normalizeAnswer = (ans: string) => ans.trim().toLowerCase();
    const correctAnswer = question.correct_answer;
    const isAnswerCorrect = normalizeAnswer(answer) === normalizeAnswer(correctAnswer);

    console.log(`填空题答案比较: 学生答案="${answer}", 正确答案="${question.correct_answer}", 是否正确=${isAnswerCorrect}`);

    return (
      <div className="space-y-4">
        <input
          type="text"
          value={answer}
          onChange={(e) => onAnswerChange(e.target.value)}
          disabled={disabled}
          placeholder="请输入答案..."
          className={`w-full px-6 py-4 border-2 rounded-xl text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            disabled
              ? showCorrect && isAnswerCorrect
                ? 'border-green-300 bg-green-50'
                : showCorrect && !isAnswerCorrect && answer.trim()
                ? 'border-red-300 bg-red-50'
                : 'border-gray-200 bg-gray-50'
              : 'border-gray-300 focus:border-blue-400'
          }`}
        />
        {showCorrect && (
          <div className="space-y-2">
            <div className="text-sm text-gray-600">
              正确答案：<span className="font-medium text-green-600">{correctAnswer}</span>
            </div>
            {answer.trim() && (
              <div className="text-sm">
                您的答案：<span className={`font-medium ${isAnswerCorrect ? 'text-green-600' : 'text-red-600'}`}>
                  {answer}
                </span>
                {isAnswerCorrect && <span className="text-green-600 ml-2">✓ 正确</span>}
                {!isAnswerCorrect && <span className="text-red-600 ml-2">✗ 错误</span>}
              </div>
            )}
          </div>
        )}
      </div>
    );
  }

  if (question.question_type === 'essay') {
    return (
      <div className="space-y-4">
        <textarea
          value={answer}
          onChange={(e) => onAnswerChange(e.target.value)}
          disabled={disabled}
          placeholder="请输入你的答案..."
          rows={8}
          className={`w-full px-6 py-4 border-2 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${
            disabled ? 'border-gray-200 bg-gray-50' : 'border-gray-300 focus:border-blue-400'
          }`}
        />
        {showCorrect && (
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-sm text-gray-600 mb-1">参考答案：</div>
            <div className="text-sm text-gray-800">{question.correct_answer}</div>
          </div>
        )}
      </div>
    );
  }

  return null;
};

import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
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
  X
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import StudentLayout from "@/components/layouts/StudentLayout";

// 题目类型定义
interface Question {
  id: number;
  type: 'multiple_choice' | 'fill_blank' | 'essay';
  title: string;
  content: string;
  options?: string[];
  correctAnswer: string | string[];
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
  points: number;
}

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

// 模拟数据
const mockExercise: Exercise = {
  id: 1,
  title: "函数与极限 - 基础练习",
  subject: "高等数学",
  difficulty: "中级",
  timeLimit: 60,
  totalQuestions: 10,
  description: "本练习包含函数与极限的基础概念和计算题目",
  questions: [
    {
      id: 1,
      type: 'multiple_choice',
      title: '函数极限的定义',
      content: '下列关于函数极限的描述，正确的是：',
      options: [
        'A. 函数在某点的极限值等于函数在该点的函数值',
        'B. 函数极限存在当且仅当左极限和右极限都存在且相等',
        'C. 函数极限不存在时，函数在该点一定不连续',
        'D. 函数极限的值与函数在该点是否有定义无关'
      ],
      correctAnswer: 'B',
      explanation: '函数极限存在的充要条件是左极限和右极限都存在且相等。极限值与函数在该点的函数值可能不同。',
      difficulty: 'medium',
      points: 10
    },
    {
      id: 2,
      type: 'fill_blank',
      title: '极限计算',
      content: '计算极限：lim(x→0) (sin x)/x = ____',
      correctAnswer: '1',
      explanation: '这是一个重要的极限公式：lim(x→0) (sin x)/x = 1',
      difficulty: 'easy',
      points: 8
    },
    {
      id: 3,
      type: 'essay',
      title: '连续性证明',
      content: '证明函数 f(x) = x² 在 x = 2 处连续。',
      correctAnswer: '需要证明：1) f(2)存在；2) lim(x→2) f(x)存在；3) lim(x→2) f(x) = f(2)',
      explanation: '连续性的定义需要满足三个条件：函数在该点有定义、极限存在、极限值等于函数值。',
      difficulty: 'hard',
      points: 15
    }
  ]
};

export const ExercisePractice = () => {
  const { exerciseId } = useParams();
  const navigate = useNavigate();
  
  const [exercise] = useState<Exercise>(mockExercise);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [timeLeft, setTimeLeft] = useState(exercise.timeLimit * 60); // 转换为秒
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showQuestionList, setShowQuestionList] = useState(false);

  const currentQuestion = exercise.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / exercise.totalQuestions) * 100;

  // 计时器
  useEffect(() => {
    if (timeLeft > 0 && !isSubmitted) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !isSubmitted) {
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
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: answer
    }));
  };

  // 下一题
  const handleNext = () => {
    if (currentQuestionIndex < exercise.questions.length - 1) {
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

  // 提交练习
  const handleSubmit = () => {
    setIsSubmitted(true);
    setShowExplanation(true);
    // 这里可以调用API提交答案
    // 提交后跳转到结果页面
    setTimeout(() => {
      navigate(`/student/exercises/result/${exerciseId}`);
    }, 2000); // 2秒后跳转，让用户看到提交成功的反馈
  };

  // 返回练习列表
  const handleBack = () => {
    navigate('/student/exercises');
  };

  // 重新开始
  const handleRestart = () => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    setTimeLeft(exercise.timeLimit * 60);
    setIsSubmitted(false);
    setShowExplanation(false);
  };

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
                    showCorrect={isSubmitted && showExplanation}
                  />
                </div>

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
                <Button
                  variant="outline"
                  onClick={handleRestart}
                  className="text-blue-600 border-blue-200 hover:bg-blue-50"
                >
                  <RotateCcw className="w-4 h-4 mr-2" />
                  重新开始
                </Button>
              )}

              {!isSubmitted ? (
                currentQuestionIndex === exercise.questions.length - 1 ? (
                  <Button onClick={handleSubmit} className="bg-green-600 hover:bg-green-700">
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
  if (question.type === 'multiple_choice') {
    return (
      <div className="space-y-4">
        {question.options?.map((option, index) => {
          const optionLetter = option.charAt(0);
          const isSelected = answer === optionLetter;
          const isCorrect = question.correctAnswer === optionLetter;
          
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
      </div>
    );
  }

  if (question.type === 'fill_blank') {
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
              ? showCorrect && answer === question.correctAnswer
                ? 'border-green-300 bg-green-50'
                : showCorrect && answer !== question.correctAnswer
                ? 'border-red-300 bg-red-50'
                : 'border-gray-200 bg-gray-50'
              : 'border-gray-300 focus:border-blue-400'
          }`}
        />
        {showCorrect && (
          <div className="text-sm text-gray-600">
            正确答案：<span className="font-medium text-green-600">{question.correctAnswer}</span>
          </div>
        )}
      </div>
    );
  }

  if (question.type === 'essay') {
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
            <div className="text-sm text-gray-800">{question.correctAnswer}</div>
          </div>
        )}
      </div>
    );
  }

  return null;
};

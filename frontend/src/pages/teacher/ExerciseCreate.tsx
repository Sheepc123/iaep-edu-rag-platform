import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import {
  ArrowLeft,
  Save,
  Plus,
  Trash2,
  BookOpen,
  Target,
  FileText,
  CheckCircle,
  Sparkles
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { exerciseAPI, ExerciseCreateRequest, QuestionCreateRequest, GeneratedQuestion } from "@/services/api";
import { AIQuestionGenerator } from "@/components/ai/AIQuestionGenerator";

// 题目类型选项
const questionTypes = [
  { value: "multiple_choice", label: "选择题", icon: "○" },
  { value: "fill_blank", label: "填空题", icon: "___" },
  { value: "essay", label: "问答题", icon: "📝" }
];

// 难度选项
const difficulties = [
  { value: "easy", label: "简单", color: "text-green-600" },
  { value: "medium", label: "中等", color: "text-yellow-600" },
  { value: "hard", label: "困难", color: "text-red-600" }
];

// 分类选项
const categories = [
  { value: "自主练习", label: "自主练习" },
  { value: "课后作业", label: "课后作业" },
  { value: "模拟考试", label: "模拟考试" },
  { value: "错题本", label: "错题本" }
];

// 科目选项
const subjects = [
  { value: "数学", label: "数学" },
  { value: "语文", label: "语文" },
  { value: "英语", label: "英语" },
  { value: "物理", label: "物理" },
  { value: "化学", label: "化学" },
  { value: "生物", label: "生物" },
  { value: "历史", label: "历史" },
  { value: "地理", label: "地理" },
  { value: "政治", label: "政治" },
  { value: "计算机", label: "计算机" },
  { value: "其他", label: "其他" }
];

interface Question {
  id: string;
  question_text: string;
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  options: string[] | Record<string, string>;
  correct_answer: string;
  explanation: string;
  points: number;
  difficulty: 'easy' | 'medium' | 'hard';
  question_order: number;
}

export const TeacherExerciseCreate: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { toast } = useToast();

  // 从URL参数获取课程ID
  const courseId = searchParams.get('courseId');

  // 练习基本信息
  const [exerciseData, setExerciseData] = useState<ExerciseCreateRequest>({
    title: "",
    description: "",
    category: "",
    subject: "",
    difficulty: "medium",
    time_limit: undefined,
    course_id: courseId ? parseInt(courseId) : undefined,
    is_published: false
  });

  // 题目列表
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question>({
    id: "",
    question_text: "",
    question_type: "multiple_choice",
    options: ["", "", "", ""],
    correct_answer: "",
    explanation: "",
    points: 10,
    difficulty: "medium",
    question_order: 1
  });

  // 状态管理
  const [activeTab, setActiveTab] = useState("basic");
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showAIGenerator, setShowAIGenerator] = useState(false);

  // 验证练习基本信息
  const validateExerciseData = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!exerciseData.title.trim()) {
      newErrors.title = "请输入练习标题";
    }
    if (!exerciseData.category) {
      newErrors.category = "请选择练习分类";
    }
    if (!exerciseData.subject) {
      newErrors.subject = "请选择科目";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 验证题目信息
  const validateQuestion = (question: Question): boolean => {
    if (!question.question_text.trim()) {
      toast({
        title: "错误",
        description: "请输入题目内容",
        variant: "destructive"
      });
      return false;
    }

    if (question.question_type === "multiple_choice") {
      // 处理选项格式：支持数组和字典两种格式
      const validOptions = Array.isArray(question.options)
        ? question.options.filter(opt => opt && opt.trim())
        : Object.values(question.options || {}).filter(opt => opt && opt.trim());

      if (validOptions.length < 2) {
        toast({
          title: "错误",
          description: "选择题至少需要2个选项",
          variant: "destructive"
        });
        return false;
      }
      if (!question.correct_answer.trim()) {
        toast({
          title: "错误",
          description: "请设置正确答案",
          variant: "destructive"
        });
        return false;
      }
    }

    if (question.points <= 0) {
      toast({
        title: "错误",
        description: "题目分值必须大于0",
        variant: "destructive"
      });
      return false;
    }

    return true;
  };

  // 添加题目
  const addQuestion = () => {
    if (!validateQuestion(currentQuestion)) {
      return;
    }

    const newQuestion: Question = {
      ...currentQuestion,
      id: Date.now().toString(),
      question_order: questions.length + 1
    };

    setQuestions([...questions, newQuestion]);

    // 重置当前题目
    setCurrentQuestion({
      id: "",
      question_text: "",
      question_type: "multiple_choice",
      options: ["", "", "", ""],
      correct_answer: "",
      explanation: "",
      points: 10,
      difficulty: "medium",
      question_order: questions.length + 2
    });

    toast({
      title: "成功",
      description: "题目添加成功"
    });
  };

  // 删除题目
  const removeQuestion = (questionId: string) => {
    setQuestions(questions.filter(q => q.id !== questionId));
    toast({
      title: "成功",
      description: "题目删除成功"
    });
  };

  // 处理AI生成的题目
  const handleAIQuestionsGenerated = (generatedQuestions: GeneratedQuestion[]) => {
    const newQuestions: Question[] = generatedQuestions.map((gq, index) => ({
      id: Date.now().toString() + index,
      question_text: gq.question_text,
      question_type: gq.question_type,
      options: gq.options
        ? (Array.isArray(gq.options) ? gq.options : Object.values(gq.options))
        : ["", "", "", ""],
      correct_answer: gq.correct_answer,
      explanation: gq.explanation,
      points: gq.points,
      difficulty: gq.difficulty,
      question_order: questions.length + index + 1
    }));

    setQuestions([...questions, ...newQuestions]);

    toast({
      title: "成功",
      description: `已添加 ${generatedQuestions.length} 道AI生成的题目`
    });
  };

  // 保存练习
  const saveExercise = async (publish: boolean = false) => {
    if (!validateExerciseData()) {
      setActiveTab("basic");
      return;
    }

    if (questions.length === 0) {
      toast({
        title: "错误",
        description: "请至少添加一道题目",
        variant: "destructive"
      });
      setActiveTab("questions");
      return;
    }

    let exerciseToSave: any = null;

    try {
      setSaving(true);

      // 创建练习
      exerciseToSave = {
        ...exerciseData,
        is_published: publish
      };

      console.log("准备创建练习，数据:", exerciseToSave);
      const createdExercise = await exerciseAPI.createExercise(exerciseToSave);

      // 添加题目
      for (const question of questions) {
        const questionData: QuestionCreateRequest = {
          content: question.question_text,  // 后端期望的字段名
          question_type: question.question_type,
          options: question.question_type === "multiple_choice"
            ? (Array.isArray(question.options)
                ? question.options.filter(opt => opt && opt.trim())
                : Object.values(question.options || {}).filter(opt => opt && opt.trim()))
            : undefined,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          points: question.points,
          difficulty: question.difficulty
        };

        console.log("准备创建题目，数据:", questionData);
        await exerciseAPI.addQuestion(createdExercise.id, questionData);
      }

      toast({
        title: "成功",
        description: publish ? "练习创建并发布成功" : "练习创建成功"
      });

      // 如果有课程ID，跳转回课程详情页，否则跳转到练习列表
      if (courseId) {
        navigate(`/teacher/courses/${courseId}`);
      } else {
        navigate("/teacher/exercises");
      }

    } catch (error: any) {
      console.error("保存练习失败:", error);
      console.error("错误详情:", error);
      console.log("发送的练习数据:", exerciseToSave);
      console.log("题目数据:", questions);

      let errorMessage = "保存练习失败";

      // 检查不同类型的错误
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        errorMessage = "网络连接失败，请检查后端服务是否正常运行";
      } else if (error.message === 'Failed to fetch') {
        errorMessage = "无法连接到服务器，请检查网络连接和后端服务";
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      toast({
        title: "错误",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setSaving(false);
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
                onClick={() => courseId ? navigate(`/teacher/courses/${courseId}`) : navigate("/teacher/exercises")}
                className="mr-4"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                  <Plus className="w-8 h-8 mr-3 text-blue-600" />
                  创建练习
                </h1>
                <p className="text-gray-600 mt-1">设计您的练习内容和题目</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={() => saveExercise(false)}
                disabled={saving}
              >
                <Save className="w-4 h-4 mr-2" />
                保存草稿
              </Button>
              <Button
                onClick={() => saveExercise(true)}
                disabled={saving}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <CheckCircle className="w-4 h-4 mr-2" />
                发布练习
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
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="basic" className="flex items-center">
                <FileText className="w-4 h-4 mr-2" />
                基本信息
              </TabsTrigger>
              <TabsTrigger value="questions" className="flex items-center">
                <Target className="w-4 h-4 mr-2" />
                题目管理
              </TabsTrigger>
            </TabsList>

            {/* 基本信息标签页 */}
            <TabsContent value="basic">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="w-5 h-5 mr-2" />
                    练习基本信息
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* 练习标题 */}
                    <div className="md:col-span-2">
                      <Label htmlFor="title">练习标题 *</Label>
                      <Input
                        id="title"
                        placeholder="请输入练习标题"
                        value={exerciseData.title}
                        onChange={(e) => setExerciseData({...exerciseData, title: e.target.value})}
                        className={errors.title ? "border-red-500" : ""}
                      />
                      {errors.title && (
                        <p className="text-red-500 text-sm mt-1">{errors.title}</p>
                      )}
                    </div>

                    {/* 练习描述 */}
                    <div className="md:col-span-2">
                      <Label htmlFor="description">练习描述</Label>
                      <Textarea
                        id="description"
                        placeholder="请输入练习描述（可选）"
                        value={exerciseData.description}
                        onChange={(e) => setExerciseData({...exerciseData, description: e.target.value})}
                        rows={3}
                      />
                    </div>

                    {/* 练习分类 */}
                    <div>
                      <Label>练习分类 *</Label>
                      <Select
                        value={exerciseData.category}
                        onValueChange={(value) => setExerciseData({...exerciseData, category: value})}
                      >
                        <SelectTrigger className={errors.category ? "border-red-500" : ""}>
                          <SelectValue placeholder="选择练习分类" />
                        </SelectTrigger>
                        <SelectContent>
                          {categories.map(category => (
                            <SelectItem key={category.value} value={category.value}>
                              {category.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      {errors.category && (
                        <p className="text-red-500 text-sm mt-1">{errors.category}</p>
                      )}
                    </div>

                    {/* 科目 */}
                    <div>
                      <Label>科目 *</Label>
                      <Select
                        value={exerciseData.subject}
                        onValueChange={(value) => setExerciseData({...exerciseData, subject: value})}
                      >
                        <SelectTrigger className={errors.subject ? "border-red-500" : ""}>
                          <SelectValue placeholder="选择科目" />
                        </SelectTrigger>
                        <SelectContent>
                          {subjects.map(subject => (
                            <SelectItem key={subject.value} value={subject.value}>
                              {subject.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      {errors.subject && (
                        <p className="text-red-500 text-sm mt-1">{errors.subject}</p>
                      )}
                    </div>

                    {/* 难度级别 */}
                    <div>
                      <Label>难度级别</Label>
                      <Select
                        value={exerciseData.difficulty}
                        onValueChange={(value: any) => setExerciseData({...exerciseData, difficulty: value})}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="选择难度" />
                        </SelectTrigger>
                        <SelectContent>
                          {difficulties.map(difficulty => (
                            <SelectItem key={difficulty.value} value={difficulty.value}>
                              <span className={difficulty.color}>{difficulty.label}</span>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    {/* 时间限制 */}
                    <div>
                      <Label htmlFor="timeLimit">时间限制（分钟）</Label>
                      <Input
                        id="timeLimit"
                        type="number"
                        placeholder="不限制时间请留空"
                        value={exerciseData.time_limit || ""}
                        onChange={(e) => setExerciseData({
                          ...exerciseData,
                          time_limit: e.target.value ? parseInt(e.target.value) : undefined
                        })}
                        min="1"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <Button
                      onClick={() => setActiveTab("questions")}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      下一步：添加题目
                      <Target className="w-4 h-4 ml-2" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* 题目管理标签页 */}
            <TabsContent value="questions" className="space-y-6">
              {/* 已添加的题目列表 */}
              {questions.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>已添加题目 ({questions.length})</span>
                      <span className="text-sm font-normal text-gray-500">
                        总分值: {questions.reduce((sum, q) => sum + q.points, 0)} 分
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {questions.map((question, index) => (
                        <QuestionCard
                          key={question.id}
                          question={question}
                          index={index}
                          onRemove={() => removeQuestion(question.id)}
                        />
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* 添加新题目 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <Plus className="w-5 h-5 mr-2" />
                      添加新题目
                    </span>
                    <Button
                      onClick={() => setShowAIGenerator(true)}
                      className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    >
                      <Sparkles className="w-4 h-4 mr-2" />
                      AI智能生成
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <QuestionForm
                    question={currentQuestion}
                    onChange={setCurrentQuestion}
                    onAdd={addQuestion}
                  />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>

        {/* AI题目生成器 */}
        <AnimatePresence>
          {showAIGenerator && (
            <AIQuestionGenerator
              onQuestionsGenerated={handleAIQuestionsGenerated}
              onClose={() => setShowAIGenerator(false)}
            />
          )}
        </AnimatePresence>
      </div>
    </TeacherLayout>
  );
};

// 题目卡片组件
interface QuestionCardProps {
  question: Question;
  index: number;
  onRemove: () => void;
}

const QuestionCard: React.FC<QuestionCardProps> = ({ question, index, onRemove }) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
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

  return (
    <div className="border rounded-lg p-4 bg-gray-50">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-sm font-medium text-gray-600">第 {index + 1} 题</span>
            <span className="text-lg">{getTypeIcon(question.question_type)}</span>
            <Badge className={getDifficultyColor(question.difficulty)}>
              {question.difficulty === 'easy' ? '简单' :
               question.difficulty === 'medium' ? '中等' : '困难'}
            </Badge>
            <Badge variant="outline">{question.points} 分</Badge>
          </div>

          <p className="text-gray-900 mb-2">{question.question_text}</p>

          {question.question_type === 'multiple_choice' && question.options && (
            <div className="space-y-1">
              {(() => {
                // 处理选项格式：支持数组和字典两种格式
                const options = Array.isArray(question.options)
                  ? question.options
                      .filter(opt => opt && opt.trim())
                      .map((opt, idx) => ({ key: String.fromCharCode(65 + idx), value: opt }))
                  : Object.entries(question.options)
                      .filter(([key, value]) => value && value.trim())
                      .map(([key, value]) => ({ key, value }));

                return options.map(({ key, value }) => {
                  const isCorrect = question.correct_answer === key || question.correct_answer === value;
                  return (
                    <div key={key} className="flex items-center text-sm">
                      <span className={`mr-2 ${isCorrect ? 'text-green-600 font-medium' : 'text-gray-600'}`}>
                        {key}.
                      </span>
                      <span className={isCorrect ? 'text-green-600 font-medium' : 'text-gray-700'}>
                        {value}
                      </span>
                      {isCorrect && (
                        <CheckCircle className="w-4 h-4 ml-2 text-green-600" />
                      )}
                    </div>
                  );
                });
              })()}
            </div>
          )}

          {question.question_type === 'fill_blank' && (
            <div className="text-sm text-gray-600">
              <span className="font-medium">答案：</span>
              <span className="text-green-600">{question.correct_answer}</span>
            </div>
          )}

          {question.explanation && (
            <div className="mt-2 text-sm text-gray-600">
              <span className="font-medium">解析：</span>
              {question.explanation}
            </div>
          )}
        </div>

        <Button
          variant="ghost"
          size="sm"
          onClick={onRemove}
          className="text-red-600 hover:text-red-700 hover:bg-red-50"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
};

// 题目表单组件
interface QuestionFormProps {
  question: Question;
  onChange: (question: Question) => void;
  onAdd: () => void;
}

const QuestionForm: React.FC<QuestionFormProps> = ({ question, onChange, onAdd }) => {
  const updateQuestion = (updates: Partial<Question>) => {
    onChange({ ...question, ...updates });
  };

  const addOption = () => {
    if (question.options.length < 6) {
      updateQuestion({ options: [...question.options, ""] });
    }
  };

  const removeOption = (index: number) => {
    if (question.options.length > 2) {
      const newOptions = question.options.filter((_, i) => i !== index);
      updateQuestion({ options: newOptions });

      // 如果删除的是正确答案，清空正确答案
      if (question.correct_answer === question.options[index]) {
        updateQuestion({ correct_answer: "" });
      }
    }
  };

  const updateOption = (index: number, value: string) => {
    const newOptions = [...question.options];
    newOptions[index] = value;
    updateQuestion({ options: newOptions });
  };

  return (
    <div className="space-y-6">
      {/* 题目类型和基本信息 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <Label>题目类型</Label>
          <Select
            value={question.question_type}
            onValueChange={(value: any) => updateQuestion({
              question_type: value,
              options: value === 'multiple_choice' ? ["", "", "", ""] : [],
              correct_answer: ""
            })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {questionTypes.map(type => (
                <SelectItem key={type.value} value={type.value}>
                  <span className="flex items-center">
                    <span className="mr-2">{type.icon}</span>
                    {type.label}
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label>难度</Label>
          <Select
            value={question.difficulty}
            onValueChange={(value: any) => updateQuestion({ difficulty: value })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {difficulties.map(difficulty => (
                <SelectItem key={difficulty.value} value={difficulty.value}>
                  <span className={difficulty.color}>{difficulty.label}</span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label htmlFor="points">分值</Label>
          <Input
            id="points"
            type="number"
            value={question.points}
            onChange={(e) => updateQuestion({ points: parseInt(e.target.value) || 0 })}
            min="1"
            max="100"
          />
        </div>
      </div>

      {/* 题目内容 */}
      <div>
        <Label htmlFor="questionText">题目内容 *</Label>
        <Textarea
          id="questionText"
          placeholder="请输入题目内容"
          value={question.question_text}
          onChange={(e) => updateQuestion({ question_text: e.target.value })}
          rows={3}
        />
      </div>

      {/* 选择题选项 */}
      {question.question_type === 'multiple_choice' && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <Label>选项设置</Label>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={addOption}
              disabled={question.options.length >= 6}
            >
              <Plus className="w-4 h-4 mr-1" />
              添加选项
            </Button>
          </div>

          <div className="space-y-3">
            {question.options.map((option, index) => (
              <div key={index} className="flex items-center gap-3">
                <span className="text-sm font-medium text-gray-600 w-6">
                  {String.fromCharCode(65 + index)}.
                </span>
                <Input
                  placeholder={`选项 ${String.fromCharCode(65 + index)}`}
                  value={option}
                  onChange={(e) => updateOption(index, e.target.value)}
                  className="flex-1"
                />
                <Button
                  type="button"
                  variant={question.correct_answer === option ? "default" : "outline"}
                  size="sm"
                  onClick={() => updateQuestion({ correct_answer: option })}
                  disabled={!option.trim()}
                >
                  {question.correct_answer === option ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    "设为答案"
                  )}
                </Button>
                {question.options.length > 2 && (
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => removeOption(index)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 填空题和问答题答案 */}
      {(question.question_type === 'fill_blank' || question.question_type === 'essay') && (
        <div>
          <Label htmlFor="correctAnswer">
            {question.question_type === 'fill_blank' ? '正确答案' : '参考答案'} *
          </Label>
          <Textarea
            id="correctAnswer"
            placeholder={question.question_type === 'fill_blank' ? '请输入正确答案' : '请输入参考答案'}
            value={question.correct_answer}
            onChange={(e) => updateQuestion({ correct_answer: e.target.value })}
            rows={question.question_type === 'essay' ? 4 : 2}
          />
        </div>
      )}

      {/* 解析 */}
      <div>
        <Label htmlFor="explanation">题目解析（可选）</Label>
        <Textarea
          id="explanation"
          placeholder="请输入题目解析，帮助学生理解"
          value={question.explanation}
          onChange={(e) => updateQuestion({ explanation: e.target.value })}
          rows={2}
        />
      </div>

      {/* 添加按钮 */}
      <div className="flex justify-end">
        <Button
          onClick={onAdd}
          className="bg-green-600 hover:bg-green-700"
        >
          <Plus className="w-4 h-4 mr-2" />
          添加题目
        </Button>
      </div>
    </div>
  );
};

import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
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
  Edit3,
  BookOpen,
  Target,
  FileText,
  CheckCircle,
  AlertCircle,
  GripVertical
} from "lucide-react";
import { motion } from "framer-motion";
import {
  exerciseAPI,
  ExerciseDetail,
  ExerciseUpdateRequest,
  Question,
  QuestionCreateRequest,
  QuestionUpdateRequest
} from "@/services/api";

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

interface EditableQuestion extends Question {
  isNew?: boolean;
  isEditing?: boolean;
}

export const TeacherExerciseEdit: React.FC = () => {
  const { exerciseId } = useParams<{ exerciseId: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();

  // 状态管理
  const [exercise, setExercise] = useState<ExerciseDetail | null>(null);
  const [exerciseData, setExerciseData] = useState<ExerciseUpdateRequest>({});
  const [questions, setQuestions] = useState<EditableQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState("basic");
  const [errors, setErrors] = useState<Record<string, string>>({});

  // 新题目模板
  const createNewQuestion = (): EditableQuestion => ({
    id: Date.now(),
    exercise_id: parseInt(exerciseId!),
    question_text: "",
    question_type: "multiple_choice",
    options: ["", "", "", ""],
    correct_answer: "",
    explanation: "",
    points: 10,
    difficulty: "medium",
    question_order: questions.length + 1,
    is_active: true,
    created_at: new Date().toISOString(),
    isNew: true,
    isEditing: true
  });

  // 获取练习详情
  const fetchExerciseDetail = async () => {
    if (!exerciseId) return;

    try {
      setLoading(true);
      const data = await exerciseAPI.getExercise(parseInt(exerciseId));
      setExercise(data);

      // 初始化编辑数据
      setExerciseData({
        title: data.title,
        description: data.description,
        category: data.category,
        subject: data.subject,
        difficulty: data.difficulty,
        time_limit: data.time_limit,
        is_published: data.is_published
      });

      // 初始化题目列表
      if (data.questions) {
        setQuestions(data.questions.map(q => ({ ...q, isEditing: false })));
      }

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

  // 验证练习基本信息
  const validateExerciseData = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!exerciseData.title?.trim()) {
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

  // 保存练习基本信息
  const saveExerciseInfo = async () => {
    if (!validateExerciseData() || !exercise) {
      return;
    }

    try {
      setSaving(true);
      await exerciseAPI.updateExercise(exercise.id, exerciseData);

      toast({
        title: "成功",
        description: "练习信息更新成功"
      });

      // 更新本地状态
      setExercise({ ...exercise, ...exerciseData });

    } catch (error) {
      console.error("更新练习失败:", error);
      toast({
        title: "错误",
        description: "更新练习失败",
        variant: "destructive"
      });
    } finally {
      setSaving(false);
    }
  };

  // 添加新题目
  const addNewQuestion = () => {
    const newQuestion = createNewQuestion();
    setQuestions([...questions, newQuestion]);
  };

  // 保存题目
  const saveQuestion = async (question: EditableQuestion) => {
    if (!validateQuestion(question)) {
      return;
    }

    try {
      if (question.isNew) {
        // 创建新题目
        const questionData: QuestionCreateRequest = {
          question_text: question.question_text,
          question_type: question.question_type,
          options: question.question_type === "multiple_choice" ?
            question.options?.filter(opt => opt.trim()) : undefined,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          points: question.points,
          difficulty: question.difficulty,
          question_order: question.question_order
        };

        const createdQuestion = await exerciseAPI.addQuestion(exercise!.id, questionData);

        // 更新本地状态
        setQuestions(questions.map(q =>
          q.id === question.id
            ? { ...createdQuestion, isNew: false, isEditing: false }
            : q
        ));

      } else {
        // 更新现有题目
        const questionData: QuestionUpdateRequest = {
          question_text: question.question_text,
          question_type: question.question_type,
          options: question.question_type === "multiple_choice" ?
            question.options?.filter(opt => opt.trim()) : undefined,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          points: question.points,
          difficulty: question.difficulty,
          question_order: question.question_order
        };

        const updatedQuestion = await exerciseAPI.updateQuestion(question.id, questionData);

        // 更新本地状态
        setQuestions(questions.map(q =>
          q.id === question.id
            ? { ...updatedQuestion, isEditing: false }
            : q
        ));
      }

      toast({
        title: "成功",
        description: "题目保存成功"
      });

    } catch (error) {
      console.error("保存题目失败:", error);
      toast({
        title: "错误",
        description: "保存题目失败",
        variant: "destructive"
      });
    }
  };

  // 删除题目
  const deleteQuestion = async (question: EditableQuestion) => {
    if (!confirm("确定要删除这道题目吗？")) {
      return;
    }

    try {
      if (!question.isNew) {
        await exerciseAPI.deleteQuestion(question.id);
      }

      setQuestions(questions.filter(q => q.id !== question.id));

      toast({
        title: "成功",
        description: "题目删除成功"
      });

    } catch (error) {
      console.error("删除题目失败:", error);
      toast({
        title: "错误",
        description: "删除题目失败",
        variant: "destructive"
      });
    }
  };

  // 验证题目
  const validateQuestion = (question: EditableQuestion): boolean => {
    if (!question.question_text.trim()) {
      toast({
        title: "错误",
        description: "请输入题目内容",
        variant: "destructive"
      });
      return false;
    }

    if (question.question_type === "multiple_choice") {
      const validOptions = question.options?.filter(opt => opt.trim()) || [];
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
                onClick={() => navigate(`/teacher/exercises/${exercise.id}`)}
                className="mr-4"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回详情
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                  <Edit3 className="w-8 h-8 mr-3 text-blue-600" />
                  编辑练习
                </h1>
                <p className="text-gray-600 mt-1">修改练习信息和题目内容</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={() => navigate(`/teacher/exercises/${exercise.id}`)}
              >
                取消编辑
              </Button>
              <Button
                onClick={saveExerciseInfo}
                disabled={saving}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <Save className="w-4 h-4 mr-2" />
                保存更改
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
                        value={exerciseData.title || ""}
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
                        value={exerciseData.description || ""}
                        onChange={(e) => setExerciseData({...exerciseData, description: e.target.value})}
                        rows={3}
                      />
                    </div>

                    {/* 练习分类 */}
                    <div>
                      <Label>练习分类 *</Label>
                      <Select
                        value={exerciseData.category || ""}
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
                        value={exerciseData.subject || ""}
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
                        value={exerciseData.difficulty || ""}
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

                  <div className="flex justify-between">
                    <div className="flex items-center space-x-4">
                      <Label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={exerciseData.is_published || false}
                          onChange={(e) => setExerciseData({...exerciseData, is_published: e.target.checked})}
                          className="rounded"
                        />
                        <span>发布练习</span>
                      </Label>
                    </div>

                    <div className="flex gap-3">
                      <Button
                        variant="outline"
                        onClick={() => setActiveTab("questions")}
                      >
                        下一步：管理题目
                        <Target className="w-4 h-4 ml-2" />
                      </Button>
                      <Button
                        onClick={saveExerciseInfo}
                        disabled={saving}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        <Save className="w-4 h-4 mr-2" />
                        保存信息
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* 题目管理标签页 */}
            <TabsContent value="questions" className="space-y-6">
              {/* 题目列表 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <Target className="w-5 h-5 mr-2" />
                      题目管理 ({questions.length})
                    </span>
                    <Button
                      onClick={addNewQuestion}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      添加题目
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {questions.length > 0 ? (
                    <div className="space-y-4">
                      {questions.map((question, index) => (
                        <EditableQuestionCard
                          key={question.id}
                          question={question}
                          index={index}
                          onSave={() => saveQuestion(question)}
                          onDelete={() => deleteQuestion(question)}
                          onEdit={(updatedQuestion) => {
                            setQuestions(questions.map(q =>
                              q.id === question.id ? updatedQuestion : q
                            ));
                          }}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Target className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">暂无题目</h3>
                      <p className="text-gray-500 mb-4">开始添加题目来完善您的练习</p>
                      <Button
                        onClick={addNewQuestion}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <Plus className="w-4 h-4 mr-2" />
                        添加第一道题目
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>
      </div>
    </TeacherLayout>
  );
};

// 可编辑题目卡片组件
interface EditableQuestionCardProps {
  question: EditableQuestion;
  index: number;
  onSave: () => void;
  onDelete: () => void;
  onEdit: (question: EditableQuestion) => void;
}

const EditableQuestionCard: React.FC<EditableQuestionCardProps> = ({
  question,
  index,
  onSave,
  onDelete,
  onEdit
}) => {
  const [isEditing, setIsEditing] = useState(question.isEditing || false);

  const updateQuestion = (updates: Partial<EditableQuestion>) => {
    onEdit({ ...question, ...updates });
  };

  const handleSave = () => {
    onSave();
    setIsEditing(false);
  };

  const handleCancel = () => {
    if (question.isNew) {
      onDelete();
    } else {
      setIsEditing(false);
    }
  };

  const addOption = () => {
    if ((question.options?.length || 0) < 6) {
      updateQuestion({ options: [...(question.options || []), ""] });
    }
  };

  const removeOption = (optionIndex: number) => {
    if ((question.options?.length || 0) > 2) {
      const newOptions = question.options?.filter((_, i) => i !== optionIndex) || [];
      updateQuestion({ options: newOptions });

      // 如果删除的是正确答案，清空正确答案
      if (question.correct_answer === question.options?.[optionIndex]) {
        updateQuestion({ correct_answer: "" });
      }
    }
  };

  const updateOption = (optionIndex: number, value: string) => {
    const newOptions = [...(question.options || [])];
    newOptions[optionIndex] = value;
    updateQuestion({ options: newOptions });
  };

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

  if (isEditing) {
    return (
      <Card className="border-2 border-blue-200 bg-blue-50/50">
        <CardHeader>
          <CardTitle className="text-lg">
            {question.isNew ? "添加新题目" : `编辑第 ${index + 1} 题`}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* 题目基本信息 */}
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
                  disabled={(question.options?.length || 0) >= 6}
                >
                  <Plus className="w-4 h-4 mr-1" />
                  添加选项
                </Button>
              </div>

              <div className="space-y-3">
                {question.options?.map((option, optionIndex) => (
                  <div key={optionIndex} className="flex items-center gap-3">
                    <span className="text-sm font-medium text-gray-600 w-6">
                      {String.fromCharCode(65 + optionIndex)}.
                    </span>
                    <Input
                      placeholder={`选项 ${String.fromCharCode(65 + optionIndex)}`}
                      value={option}
                      onChange={(e) => updateOption(optionIndex, e.target.value)}
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
                    {(question.options?.length || 0) > 2 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeOption(optionIndex)}
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

          {/* 操作按钮 */}
          <div className="flex justify-end gap-3">
            <Button
              variant="outline"
              onClick={handleCancel}
            >
              取消
            </Button>
            <Button
              onClick={handleSave}
              className="bg-green-600 hover:bg-green-700"
            >
              <Save className="w-4 h-4 mr-2" />
              保存题目
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // 显示模式
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
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
              {question.isNew && (
                <Badge variant="secondary">新题目</Badge>
              )}
            </div>

            <p className="text-gray-900 mb-2">{question.question_text}</p>

            {question.question_type === 'multiple_choice' && question.options && (
              <div className="space-y-1">
                {question.options.filter(opt => opt.trim()).map((option, idx) => (
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
          </div>

          <div className="flex gap-2 ml-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsEditing(true)}
            >
              <Edit3 className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onDelete}
              className="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

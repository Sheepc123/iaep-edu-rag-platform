import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/components/ui/use-toast";
import { 
  Sparkles, 
  Loader2, 
  CheckCircle, 
  XCircle, 
  RefreshCw,
  Wand2,
  Brain,
  Target,
  BookOpen,
  Plus
} from "lucide-react";
import { aiAPI, GeneratedQuestion, QuestionGenerationRequest } from "@/services/api";

interface AIQuestionGeneratorProps {
  onQuestionsGenerated: (questions: GeneratedQuestion[]) => void;
  onClose: () => void;
}

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

// 难度选项
const difficulties = [
  { value: "easy", label: "简单", color: "text-green-600" },
  { value: "medium", label: "中等", color: "text-yellow-600" },
  { value: "hard", label: "困难", color: "text-red-600" }
];

// 题目类型选项
const questionTypes = [
  { value: "multiple_choice", label: "选择题", icon: "○" },
  { value: "fill_blank", label: "填空题", icon: "___" },
  { value: "essay", label: "问答题", icon: "📝" }
];

export const AIQuestionGenerator: React.FC<AIQuestionGeneratorProps> = ({
  onQuestionsGenerated,
  onClose
}) => {
  const { toast } = useToast();

  // 表单状态
  const [formData, setFormData] = useState<QuestionGenerationRequest>({
    subject: "",
    topic: "",
    difficulty: "medium",
    question_count: 5,
    question_types: ["multiple_choice"],
    additional_requirements: ""
  });

  // 生成状态
  const [generating, setGenerating] = useState(false);
  const [generatedQuestions, setGeneratedQuestions] = useState<GeneratedQuestion[]>([]);
  const [showPreview, setShowPreview] = useState(false);

  // 处理表单提交
  const handleGenerate = async () => {
    // 验证表单
    if (!formData.subject || !formData.topic) {
      toast({
        title: "错误",
        description: "请填写科目和主题",
        variant: "destructive"
      });
      return;
    }

    if (formData.question_types.length === 0) {
      toast({
        title: "错误", 
        description: "请至少选择一种题目类型",
        variant: "destructive"
      });
      return;
    }

    try {
      setGenerating(true);
      
      const response = await aiAPI.generateQuestions(formData);
      setGeneratedQuestions(response.questions);
      setShowPreview(true);
      
      toast({
        title: "成功",
        description: `成功生成 ${response.questions.length} 道题目`
      });

    } catch (error: any) {
      console.error("生成题目失败:", error);
      toast({
        title: "生成失败",
        description: error.message || "AI题目生成失败，请重试",
        variant: "destructive"
      });
    } finally {
      setGenerating(false);
    }
  };

  // 处理题目类型选择
  const handleTypeToggle = (type: string) => {
    const newTypes = formData.question_types.includes(type)
      ? formData.question_types.filter(t => t !== type)
      : [...formData.question_types, type];
    
    setFormData({ ...formData, question_types: newTypes });
  };

  // 确认使用生成的题目
  const handleConfirm = () => {
    onQuestionsGenerated(generatedQuestions);
    onClose();
  };

  // 重新生成
  const handleRegenerate = () => {
    setShowPreview(false);
    setGeneratedQuestions([]);
    handleGenerate();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
      >
        {/* 头部 */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">AI智能题目生成</h2>
                <p className="text-purple-100">让AI为您快速生成高质量的练习题目</p>
              </div>
            </div>
            <Button
              variant="ghost"
              onClick={onClose}
              className="text-white hover:bg-white hover:bg-opacity-20"
            >
              <XCircle className="w-5 h-5" />
            </Button>
          </div>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {!showPreview ? (
            /* 生成表单 */
            <div className="space-y-6">
              {/* 基本信息 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="w-5 h-5 mr-2" />
                    基本信息
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="subject">科目 *</Label>
                      <Select
                        value={formData.subject}
                        onValueChange={(value) => setFormData({...formData, subject: value})}
                      >
                        <SelectTrigger>
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
                    </div>

                    <div>
                      <Label htmlFor="difficulty">难度</Label>
                      <Select
                        value={formData.difficulty}
                        onValueChange={(value: any) => setFormData({...formData, difficulty: value})}
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
                  </div>

                  <div>
                    <Label htmlFor="topic">主题 *</Label>
                    <Input
                      id="topic"
                      placeholder="例如：函数与极限、古诗词鉴赏、化学反应原理等"
                      value={formData.topic}
                      onChange={(e) => setFormData({...formData, topic: e.target.value})}
                    />
                  </div>

                  <div>
                    <Label htmlFor="count">题目数量</Label>
                    <Input
                      id="count"
                      type="number"
                      min="1"
                      max="20"
                      value={formData.question_count}
                      onChange={(e) => setFormData({...formData, question_count: parseInt(e.target.value) || 1})}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* 题目类型 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Target className="w-5 h-5 mr-2" />
                    题目类型
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {questionTypes.map(type => (
                      <div
                        key={type.value}
                        onClick={() => handleTypeToggle(type.value)}
                        className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                          formData.question_types.includes(type.value)
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{type.icon}</span>
                          <div>
                            <h4 className="font-medium">{type.label}</h4>
                          </div>
                          {formData.question_types.includes(type.value) && (
                            <CheckCircle className="w-5 h-5 text-blue-500 ml-auto" />
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 额外要求 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Brain className="w-5 h-5 mr-2" />
                    额外要求（可选）
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Textarea
                    placeholder="例如：重点考查计算能力、包含实际应用场景、难度递增等"
                    value={formData.additional_requirements}
                    onChange={(e) => setFormData({...formData, additional_requirements: e.target.value})}
                    rows={3}
                  />
                </CardContent>
              </Card>

              {/* 生成按钮 */}
              <div className="flex justify-center">
                <Button
                  onClick={handleGenerate}
                  disabled={generating}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-3 text-lg"
                >
                  {generating ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      AI正在生成题目...
                    </>
                  ) : (
                    <>
                      <Wand2 className="w-5 h-5 mr-2" />
                      开始生成题目
                    </>
                  )}
                </Button>
              </div>
            </div>
          ) : (
            /* 题目预览 */
            <QuestionPreview
              questions={generatedQuestions}
              onConfirm={handleConfirm}
              onRegenerate={handleRegenerate}
              onBack={() => setShowPreview(false)}
            />
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

// 题目预览组件
interface QuestionPreviewProps {
  questions: GeneratedQuestion[];
  onConfirm: () => void;
  onRegenerate: () => void;
  onBack: () => void;
}

const QuestionPreview: React.FC<QuestionPreviewProps> = ({
  questions,
  onConfirm,
  onRegenerate,
  onBack
}) => {
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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold">生成的题目预览 ({questions.length}道)</h3>
        <div className="flex gap-3">
          <Button variant="outline" onClick={onBack}>
            返回编辑
          </Button>
          <Button variant="outline" onClick={onRegenerate}>
            <RefreshCw className="w-4 h-4 mr-2" />
            重新生成
          </Button>
          <Button onClick={onConfirm} className="bg-green-600 hover:bg-green-700">
            <Plus className="w-4 h-4 mr-2" />
            使用这些题目
          </Button>
        </div>
      </div>

      <div className="space-y-4">
        {questions.map((question, index) => (
          <Card key={index} className="border-l-4 border-l-blue-500">
            <CardContent className="p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-600">第 {index + 1} 题</span>
                  <span className="text-lg">{getTypeIcon(question.question_type)}</span>
                  <Badge className={getDifficultyColor(question.difficulty)}>
                    {question.difficulty === 'easy' ? '简单' : 
                     question.difficulty === 'medium' ? '中等' : '困难'}
                  </Badge>
                  <Badge variant="outline">{question.points} 分</Badge>
                </div>
              </div>
              
              <div className="mb-3">
                <p className="text-gray-900 font-medium">{question.question_text}</p>
              </div>
              
              {question.question_type === 'multiple_choice' && question.options && (
                <div className="space-y-2 mb-3">
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
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

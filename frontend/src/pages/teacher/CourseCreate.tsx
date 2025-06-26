import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Upload,
  Save,
  Eye,
  ArrowLeft,
  Plus,
  Trash2,
  Edit3,
  Clock,
  Users,
  Star,
  Globe,
  Sparkles,
  FileText,
  Wand2,
  X,
  Loader2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import { DocumentUpload } from "@/components/ui/DocumentUpload";
import TeacherLayout from "@/components/layouts/TeacherLayout";

interface Lesson {
  id: string;
  title: string;
  description: string;
  content: string;
  duration: number;
  lessonType: string;
  videoUrl: string;
  materials: string[];
  isPublished: boolean;
  isFree: boolean;
}

interface CourseData {
  title: string;
  description: string;
  category: string;
  difficulty: string;
  duration: number;
  coverImage: string;
  isPublished: boolean;
  lessons: Lesson[];
}

export const TeacherCourseCreate = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = useState("basic");
  const [courseData, setCourseData] = useState<CourseData>({
    title: "",
    description: "",
    category: "",
    difficulty: "medium",
    duration: 0,
    coverImage: "",
    isPublished: false,
    lessons: []
  });

  const [currentLesson, setCurrentLesson] = useState<Lesson>({
    id: "",
    title: "",
    description: "",
    content: "",
    duration: 0,
    lessonType: "video",
    videoUrl: "",
    materials: [],
    isPublished: false,
    isFree: false
  });

  const [editingLessonIndex, setEditingLessonIndex] = useState<number | null>(null);
  const [showLessonForm, setShowLessonForm] = useState(false);

  // AI生成相关状态
  const [showAIGenerator, setShowAIGenerator] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [generatedCourse, setGeneratedCourse] = useState<any>(null);

  // 课程分类选项
  const categories = [
    { value: "programming", label: "编程开发" },
    { value: "design", label: "设计创意" },
    { value: "business", label: "商业管理" },
    { value: "language", label: "语言学习" },
    { value: "science", label: "科学技术" },
    { value: "art", label: "艺术人文" }
  ];

  // 难度级别选项
  const difficulties = [
    { value: "easy", label: "初级", color: "bg-green-100 text-green-800" },
    { value: "medium", label: "中级", color: "bg-yellow-100 text-yellow-800" },
    { value: "hard", label: "高级", color: "bg-red-100 text-red-800" }
  ];

  // 课时类型选项
  const lessonTypes = [
    { value: "video", label: "视频课程" },
    { value: "text", label: "图文教程" },
    { value: "interactive", label: "互动练习" }
  ];

  // 处理基本信息变更
  const handleBasicInfoChange = (field: keyof CourseData, value: any) => {
    setCourseData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // 处理课时信息变更
  const handleLessonChange = (field: keyof Lesson, value: any) => {
    setCurrentLesson(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // 添加或更新课时
  const handleSaveLesson = () => {
    if (!currentLesson.title.trim()) {
      toast({
        title: "错误",
        description: "请输入课时标题",
        variant: "destructive"
      });
      return;
    }

    const lessonWithId = {
      ...currentLesson,
      id: currentLesson.id || Date.now().toString()
    };

    if (editingLessonIndex !== null) {
      // 更新现有课时
      const updatedLessons = [...courseData.lessons];
      updatedLessons[editingLessonIndex] = lessonWithId;
      setCourseData(prev => ({ ...prev, lessons: updatedLessons }));
    } else {
      // 添加新课时
      setCourseData(prev => ({
        ...prev,
        lessons: [...prev.lessons, lessonWithId]
      }));
    }

    // 重置表单
    setCurrentLesson({
      id: "",
      title: "",
      description: "",
      content: "",
      duration: 0,
      lessonType: "video",
      videoUrl: "",
      materials: [],
      isPublished: false,
      isFree: false
    });
    setEditingLessonIndex(null);
    setShowLessonForm(false);

    toast({
      title: "成功",
      description: editingLessonIndex !== null ? "课时已更新" : "课时已添加"
    });
  };

  // 编辑课时
  const handleEditLesson = (index: number) => {
    setCurrentLesson(courseData.lessons[index]);
    setEditingLessonIndex(index);
    setShowLessonForm(true);
    setActiveTab("lessons");
  };

  // 删除课时
  const handleDeleteLesson = (index: number) => {
    const updatedLessons = courseData.lessons.filter((_, i) => i !== index);
    setCourseData(prev => ({ ...prev, lessons: updatedLessons }));

    toast({
      title: "成功",
      description: "课时已删除"
    });
  };

  // 保存课程
  const handleSaveCourse = async (publish: boolean = false) => {
    if (!courseData.title.trim()) {
      toast({
        title: "错误",
        description: "请输入课程标题",
        variant: "destructive"
      });
      return;
    }

    try {
      // 这里调用API保存课程
      const courseToSave = {
        ...courseData,
        isPublished: publish,
        duration: courseData.lessons.reduce((total, lesson) => total + lesson.duration, 0)
      };

      console.log("保存课程:", courseToSave);

      toast({
        title: "成功",
        description: publish ? "课程已发布" : "课程已保存为草稿"
      });

      // 跳转到课程管理页面
      navigate("/teacher/courses");

    } catch (error) {
      toast({
        title: "错误",
        description: "保存课程失败",
        variant: "destructive"
      });
    }
  };

  // 预览课程
  const handlePreviewCourse = () => {
    // 这里可以打开预览模态框或跳转到预览页面
    toast({
      title: "提示",
      description: "预览功能开发中..."
    });
  };

  // AI生成相关函数
  const handleFileSelect = (file: File) => {
    setUploadedFile(file);
  };

  const handleGenerateCourse = async () => {
    if (!uploadedFile) {
      toast({
        title: "错误",
        description: "请先上传文档",
        variant: "destructive"
      });
      return;
    }

    setIsGenerating(true);

    try {
      // 创建FormData
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('auto_save', 'false');

      // 调用AI生成API
      const response = await fetch('/api/v1/ai-course/generate-course', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('生成失败');
      }

      const result = await response.json();

      if (result.success) {
        const generated = result.generated_course;
        setGeneratedCourse(generated);

        // 应用生成的课程数据
        setCourseData({
          title: generated.title,
          description: generated.description,
          category: generated.category,
          difficulty: generated.difficulty,
          duration: generated.duration,
          coverImage: generated.cover_image || "",
          isPublished: false,
          lessons: generated.lessons.map((lesson: any, index: number) => ({
            id: `lesson-${index}`,
            title: lesson.title,
            description: lesson.description,
            content: lesson.content,
            duration: lesson.duration,
            lessonType: lesson.lesson_type,
            videoUrl: lesson.video_url || "",
            materials: lesson.materials || [],
            isPublished: lesson.is_published,
            isFree: lesson.is_free
          }))
        });

        toast({
          title: "成功",
          description: "AI课程生成完成！请检查并调整课程内容。"
        });

        // 切换到基本信息标签页
        setActiveTab("basic");
        setShowAIGenerator(false);
      }

    } catch (error) {
      toast({
        title: "错误",
        description: "AI生成失败，请重试",
        variant: "destructive"
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePreviewGeneration = async () => {
    if (!uploadedFile) {
      toast({
        title: "错误",
        description: "请先上传文档",
        variant: "destructive"
      });
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);

      const response = await fetch('/api/v1/ai-course/generate-course-preview', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('预览生成失败');
      }

      const result = await response.json();

      if (result.success) {
        // 显示预览信息
        toast({
          title: "预览生成成功",
          description: `将生成课程"${result.preview.course_title}"，包含${result.preview.total_lessons}个课时`
        });
      }

    } catch (error) {
      toast({
        title: "错误",
        description: "预览生成失败",
        variant: "destructive"
      });
    }
  };

  return (
    <TeacherLayout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        {/* 头部 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                onClick={() => navigate("/teacher/courses")}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>返回课程管理</span>
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                  <BookOpen className="w-8 h-8 mr-3 text-blue-600" />
                  创建新课程
                </h1>
                <p className="text-gray-600 mt-1">设计并发布您的专业课程</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                onClick={() => setShowAIGenerator(true)}
                className="flex items-center space-x-2 border-purple-200 text-purple-700 hover:bg-purple-50"
              >
                <Sparkles className="w-4 h-4" />
                <span>AI智能生成</span>
              </Button>
              <Button
                variant="outline"
                onClick={handlePreviewCourse}
                className="flex items-center space-x-2"
              >
                <Eye className="w-4 h-4" />
                <span>预览</span>
              </Button>
              <Button
                variant="outline"
                onClick={() => handleSaveCourse(false)}
                className="flex items-center space-x-2"
              >
                <Save className="w-4 h-4" />
                <span>保存草稿</span>
              </Button>
              <Button
                onClick={() => handleSaveCourse(true)}
                className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <Globe className="w-4 h-4" />
                <span>发布课程</span>
              </Button>
            </div>
          </div>
        </div>

        {/* AI生成器模态框 */}
        {showAIGenerator && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Wand2 className="w-6 h-6 text-purple-600" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">AI智能生成课程</h2>
                    <p className="text-gray-600">上传文档，让AI为您智能生成课程结构</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  onClick={() => setShowAIGenerator(false)}
                  className="h-8 w-8 p-0"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <div className="space-y-6">
                {/* 功能介绍 */}
                <Card className="border-purple-200 bg-purple-50">
                  <CardContent className="p-4">
                    <div className="flex items-start space-x-3">
                      <Sparkles className="w-5 h-5 text-purple-600 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-purple-900 mb-2">AI智能分析功能</h3>
                        <ul className="text-sm text-purple-700 space-y-1">
                          <li>• 自动提取文档内容和结构</li>
                          <li>• 智能生成课程标题和描述</li>
                          <li>• 自动划分课程章节和课时</li>
                          <li>• 估算课程难度和学习时长</li>
                        </ul>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* 文档上传 */}
                <div>
                  <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <FileText className="w-5 h-5 mr-2 text-blue-600" />
                    上传课程文档
                  </h3>
                  <DocumentUpload
                    onFileSelect={handleFileSelect}
                    onUploadComplete={(result) => {
                      console.log('Upload complete:', result);
                    }}
                    onUploadError={(error) => {
                      toast({
                        title: "上传失败",
                        description: error,
                        variant: "destructive"
                      });
                    }}
                  />
                </div>

                {/* 操作按钮 */}
                <div className="flex items-center justify-between pt-4 border-t">
                  <Button
                    variant="outline"
                    onClick={handlePreviewGeneration}
                    disabled={!uploadedFile}
                    className="flex items-center space-x-2"
                  >
                    <Eye className="w-4 h-4" />
                    <span>预览生成</span>
                  </Button>

                  <div className="flex items-center space-x-3">
                    <Button
                      variant="outline"
                      onClick={() => setShowAIGenerator(false)}
                    >
                      取消
                    </Button>
                    <Button
                      onClick={handleGenerateCourse}
                      disabled={!uploadedFile || isGenerating}
                      className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    >
                      {isGenerating ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          生成中...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-4 h-4 mr-2" />
                          开始生成
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 主要内容 */}
        <div className="max-w-6xl mx-auto">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="basic">基本信息</TabsTrigger>
              <TabsTrigger value="lessons">课程内容</TabsTrigger>
              <TabsTrigger value="settings">发布设置</TabsTrigger>
            </TabsList>

            {/* 基本信息标签页 */}
            <TabsContent value="basic" className="space-y-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Card>
                  <CardHeader>
                    <CardTitle>课程基本信息</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* 课程标题 */}
                    <div className="space-y-2">
                      <Label htmlFor="title">课程标题 *</Label>
                      <Input
                        id="title"
                        placeholder="输入吸引人的课程标题..."
                        value={courseData.title}
                        onChange={(e) => handleBasicInfoChange("title", e.target.value)}
                        className="text-lg"
                      />
                    </div>

                    {/* 课程描述 */}
                    <div className="space-y-2">
                      <Label htmlFor="description">课程描述</Label>
                      <Textarea
                        id="description"
                        placeholder="详细描述您的课程内容、学习目标和适用人群..."
                        value={courseData.description}
                        onChange={(e) => handleBasicInfoChange("description", e.target.value)}
                        rows={4}
                      />
                    </div>

                    {/* 课程分类和难度 */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label>课程分类</Label>
                        <Select
                          value={courseData.category}
                          onValueChange={(value) => handleBasicInfoChange("category", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="选择课程分类" />
                          </SelectTrigger>
                          <SelectContent>
                            {categories.map((category) => (
                              <SelectItem key={category.value} value={category.value}>
                                {category.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label>难度级别</Label>
                        <Select
                          value={courseData.difficulty}
                          onValueChange={(value) => handleBasicInfoChange("difficulty", value)}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            {difficulties.map((difficulty) => (
                              <SelectItem key={difficulty.value} value={difficulty.value}>
                                <div className="flex items-center space-x-2">
                                  <Badge className={difficulty.color}>
                                    {difficulty.label}
                                  </Badge>
                                </div>
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                    </div>

                    {/* 封面图片 */}
                    <div className="space-y-2">
                      <Label htmlFor="coverImage">封面图片URL</Label>
                      <div className="flex space-x-3">
                        <Input
                          id="coverImage"
                          placeholder="输入封面图片URL..."
                          value={courseData.coverImage}
                          onChange={(e) => handleBasicInfoChange("coverImage", e.target.value)}
                        />
                        <Button variant="outline" className="flex items-center space-x-2">
                          <Upload className="w-4 h-4" />
                          <span>上传</span>
                        </Button>
                      </div>
                      {courseData.coverImage && (
                        <div className="mt-3">
                          <img
                            src={courseData.coverImage}
                            alt="课程封面预览"
                            className="w-48 h-32 object-cover rounded-lg border"
                            onError={(e) => {
                              e.currentTarget.style.display = 'none';
                            }}
                          />
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>

            {/* 课程内容标签页 */}
            <TabsContent value="lessons" className="space-y-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-6"
              >
                {/* 课时列表 */}
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle>课程内容 ({courseData.lessons.length} 个课时)</CardTitle>
                      <Button
                        onClick={() => {
                          setShowLessonForm(true);
                          setEditingLessonIndex(null);
                          setCurrentLesson({
                            id: "",
                            title: "",
                            description: "",
                            content: "",
                            duration: 0,
                            lessonType: "video",
                            videoUrl: "",
                            materials: [],
                            isPublished: false,
                            isFree: false
                          });
                        }}
                        className="flex items-center space-x-2"
                      >
                        <Plus className="w-4 h-4" />
                        <span>添加课时</span>
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {courseData.lessons.length === 0 ? (
                      <div className="text-center py-12">
                        <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 mb-2">还没有课时内容</h3>
                        <p className="text-gray-500 mb-4">开始添加您的第一个课时吧</p>
                        <Button
                          onClick={() => setShowLessonForm(true)}
                          className="flex items-center space-x-2"
                        >
                          <Plus className="w-4 h-4" />
                          <span>添加课时</span>
                        </Button>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        {courseData.lessons.map((lesson, index) => (
                          <div
                            key={lesson.id}
                            className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                          >
                            <div className="flex items-center space-x-4">
                              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-medium">
                                {index + 1}
                              </div>
                              <div>
                                <h4 className="font-medium text-gray-900">{lesson.title}</h4>
                                <div className="flex items-center space-x-4 text-sm text-gray-500 mt-1">
                                  <span className="flex items-center">
                                    <Clock className="w-3 h-3 mr-1" />
                                    {lesson.duration} 分钟
                                  </span>
                                  <Badge variant="outline">
                                    {lessonTypes.find(t => t.value === lesson.lessonType)?.label}
                                  </Badge>
                                  {lesson.isFree && (
                                    <Badge className="bg-green-100 text-green-800">免费</Badge>
                                  )}
                                </div>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleEditLesson(index)}
                              >
                                <Edit3 className="w-4 h-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteLesson(index)}
                                className="text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* 课时编辑表单 */}
                {showLessonForm && (
                  <Card>
                    <CardHeader>
                      <CardTitle>
                        {editingLessonIndex !== null ? "编辑课时" : "添加新课时"}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      {/* 课时标题 */}
                      <div className="space-y-2">
                        <Label htmlFor="lessonTitle">课时标题 *</Label>
                        <Input
                          id="lessonTitle"
                          placeholder="输入课时标题..."
                          value={currentLesson.title}
                          onChange={(e) => handleLessonChange("title", e.target.value)}
                        />
                      </div>

                      {/* 课时描述 */}
                      <div className="space-y-2">
                        <Label htmlFor="lessonDescription">课时描述</Label>
                        <Textarea
                          id="lessonDescription"
                          placeholder="描述这个课时的主要内容..."
                          value={currentLesson.description}
                          onChange={(e) => handleLessonChange("description", e.target.value)}
                          rows={3}
                        />
                      </div>

                      {/* 课时类型和时长 */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                          <Label>课时类型</Label>
                          <Select
                            value={currentLesson.lessonType}
                            onValueChange={(value) => handleLessonChange("lessonType", value)}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              {lessonTypes.map((type) => (
                                <SelectItem key={type.value} value={type.value}>
                                  {type.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor="lessonDuration">时长 (分钟)</Label>
                          <Input
                            id="lessonDuration"
                            type="number"
                            placeholder="0"
                            value={currentLesson.duration}
                            onChange={(e) => handleLessonChange("duration", parseInt(e.target.value) || 0)}
                          />
                        </div>
                      </div>

                      {/* 视频URL */}
                      {currentLesson.lessonType === "video" && (
                        <div className="space-y-2">
                          <Label htmlFor="videoUrl">视频URL</Label>
                          <Input
                            id="videoUrl"
                            placeholder="输入视频链接..."
                            value={currentLesson.videoUrl}
                            onChange={(e) => handleLessonChange("videoUrl", e.target.value)}
                          />
                        </div>
                      )}

                      {/* 课时内容 */}
                      <div className="space-y-2">
                        <Label htmlFor="lessonContent">课时内容</Label>
                        <Textarea
                          id="lessonContent"
                          placeholder="输入详细的课时内容..."
                          value={currentLesson.content}
                          onChange={(e) => handleLessonChange("content", e.target.value)}
                          rows={6}
                        />
                      </div>

                      {/* 操作按钮 */}
                      <div className="flex items-center justify-end space-x-3">
                        <Button
                          variant="outline"
                          onClick={() => {
                            setShowLessonForm(false);
                            setEditingLessonIndex(null);
                          }}
                        >
                          取消
                        </Button>
                        <Button onClick={handleSaveLesson}>
                          {editingLessonIndex !== null ? "更新课时" : "添加课时"}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </motion.div>
            </TabsContent>

            {/* 发布设置标签页 */}
            <TabsContent value="settings" className="space-y-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Card>
                  <CardHeader>
                    <CardTitle>发布设置</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* 课程统计 */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <BookOpen className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-blue-600">
                          {courseData.lessons.length}
                        </div>
                        <div className="text-sm text-gray-600">课时数量</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <Clock className="w-8 h-8 text-green-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-green-600">
                          {courseData.lessons.reduce((total, lesson) => total + lesson.duration, 0)}
                        </div>
                        <div className="text-sm text-gray-600">总时长 (分钟)</div>
                      </div>
                      <div className="text-center p-4 bg-purple-50 rounded-lg">
                        <Users className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-purple-600">0</div>
                        <div className="text-sm text-gray-600">预计学员</div>
                      </div>
                    </div>

                    {/* 发布检查清单 */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-medium">发布检查清单</h3>
                      <div className="space-y-3">
                        <div className="flex items-center space-x-3">
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center ${
                            courseData.title ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                          }`}>
                            {courseData.title && <span className="text-xs">✓</span>}
                          </div>
                          <span className={courseData.title ? 'text-green-600' : 'text-gray-500'}>
                            课程标题已设置
                          </span>
                        </div>
                        <div className="flex items-center space-x-3">
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center ${
                            courseData.description ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                          }`}>
                            {courseData.description && <span className="text-xs">✓</span>}
                          </div>
                          <span className={courseData.description ? 'text-green-600' : 'text-gray-500'}>
                            课程描述已填写
                          </span>
                        </div>
                        <div className="flex items-center space-x-3">
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center ${
                            courseData.category ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                          }`}>
                            {courseData.category && <span className="text-xs">✓</span>}
                          </div>
                          <span className={courseData.category ? 'text-green-600' : 'text-gray-500'}>
                            课程分类已选择
                          </span>
                        </div>
                        <div className="flex items-center space-x-3">
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center ${
                            courseData.lessons.length > 0 ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                          }`}>
                            {courseData.lessons.length > 0 && <span className="text-xs">✓</span>}
                          </div>
                          <span className={courseData.lessons.length > 0 ? 'text-green-600' : 'text-gray-500'}>
                            至少添加一个课时
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* 发布按钮 */}
                    <div className="pt-6 border-t">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-lg font-medium">准备发布</h3>
                          <p className="text-gray-600 text-sm">
                            发布后学生将能够在课程中心看到您的课程
                          </p>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Button
                            variant="outline"
                            onClick={() => handleSaveCourse(false)}
                            className="flex items-center space-x-2"
                          >
                            <Save className="w-4 h-4" />
                            <span>保存草稿</span>
                          </Button>
                          <Button
                            onClick={() => handleSaveCourse(true)}
                            disabled={!courseData.title || !courseData.category || courseData.lessons.length === 0}
                            className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                          >
                            <Globe className="w-4 h-4" />
                            <span>立即发布</span>
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </TeacherLayout>
  );
};

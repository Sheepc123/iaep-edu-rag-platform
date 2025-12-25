import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Switch } from "@/components/ui/switch";
import { useToast } from "@/components/ui/use-toast";
import { courseAPI, teacherAPI, Course, Lesson } from "@/services/api";
import {
  ArrowLeft,
  Save,
  Users,
  FileText,
  Upload,
  Download,
  Trash2,
  UserMinus,
  Clock,
  BookOpen,
  TrendingUp,
  Plus,
  Edit,
  PlayCircle
} from "lucide-react";

interface CourseStudent {
  id: number;
  username: string;
  full_name: string;
  email: string;
  avatar_url?: string;
  enrolled_at: string;
  progress_percentage: number;
  completed_lessons: number;
  total_study_time: number;
  is_completed: boolean;
  last_accessed_at?: string;
}

interface CourseFile {
  id: string;
  name: string;
  size: number;
  type: string;
  url: string;
  uploaded_at: string;
}

export const TeacherCourseEdit: React.FC = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();

  // 状态管理
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [course, setCourse] = useState<Course | null>(null);
  const [students, setStudents] = useState<CourseStudent[]>([]);
  const [files, setFiles] = useState<CourseFile[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [activeTab, setActiveTab] = useState("basic");
  const [showLessonForm, setShowLessonForm] = useState(false);
  const [editingLesson, setEditingLesson] = useState<Lesson | null>(null);

  // 表单数据
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    difficulty: "medium",
    duration: 0,
    cover_image: "",
    is_published: false
  });

  // 课时表单数据
  const [lessonFormData, setLessonFormData] = useState<{
    title: string;
    description: string;
    content: string;
    lesson_order: number;
    duration: number;
    lesson_type: "video" | "text" | "interactive" | "quiz";
    video_url: string;
    materials: string;
    is_published: boolean;
    is_free: boolean;
  }>({
    title: "",
    description: "",
    content: "",
    lesson_order: 1,
    duration: 30,
    lesson_type: "video",
    video_url: "",
    materials: "",
    is_published: true,
    is_free: false
  });

  // 获取课程数据
  useEffect(() => {
    const fetchCourseData = async () => {
      if (!courseId) return;

      try {
        setLoading(true);
        const courseData = await courseAPI.getCourse(parseInt(courseId));
        setCourse(courseData);
        setFormData({
          title: courseData.title,
          description: courseData.description || "",
          category: courseData.category || "",
          difficulty: courseData.difficulty || "medium",
          duration: courseData.duration || 0,
          cover_image: courseData.cover_image || "",
          is_published: courseData.is_published
        });
      } catch (error) {
        console.error('获取课程数据失败:', error);
        toast({
          title: "加载失败",
          description: "无法加载课程数据，请刷新页面重试",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchCourseData();
  }, [courseId, toast]);

  // 获取学生列表
  const fetchStudents = async () => {
    if (!courseId) return;

    try {
      const studentsData = await teacherAPI.getCourseStudents(parseInt(courseId));
      setStudents(studentsData);
    } catch (error) {
      console.error('获取学生列表失败:', error);
      toast({
        title: "加载失败",
        description: "无法加载学生列表",
        variant: "destructive",
      });
    }
  };

  // 获取文件列表
  const fetchFiles = async () => {
    if (!courseId) return;

    try {
      const filesData = await teacherAPI.getCourseFiles(parseInt(courseId));
      setFiles(filesData);
    } catch (error) {
      console.error('获取文件列表失败:', error);
      toast({
        title: "加载失败",
        description: "无法加载文件列表",
        variant: "destructive",
      });
    }
  };

  // 获取课时列表
  const fetchLessons = async () => {
    if (!courseId) return;

    try {
      const lessonsData = await courseAPI.getCourseLessons(parseInt(courseId), true);
      setLessons(lessonsData);
    } catch (error) {
      console.error('获取课时列表失败:', error);
      toast({
        title: "加载失败",
        description: "无法加载课时列表",
        variant: "destructive",
      });
    }
  };

  // 当切换到学生、文件或课时标签时加载数据
  useEffect(() => {
    if (activeTab === "students") {
      fetchStudents();
    } else if (activeTab === "files") {
      fetchFiles();
    } else if (activeTab === "lessons") {
      fetchLessons();
    }
  }, [activeTab, courseId]);

  // 保存课程信息
  const handleSave = async () => {
    if (!courseId || !formData.title.trim()) {
      toast({
        title: "错误",
        description: "请输入课程标题",
        variant: "destructive"
      });
      return;
    }

    try {
      setSaving(true);
      await teacherAPI.updateCourse(parseInt(courseId), formData);

      toast({
        title: "成功",
        description: "课程信息已更新"
      });
    } catch (error) {
      console.error('保存课程失败:', error);
      toast({
        title: "保存失败",
        description: "无法保存课程信息，请重试",
        variant: "destructive"
      });
    } finally {
      setSaving(false);
    }
  };

  // 移除学生
  const handleRemoveStudent = async (studentId: number, studentName: string) => {
    if (!courseId) return;

    if (!confirm(`确定要将学生 ${studentName} 从课程中移除吗？`)) {
      return;
    }

    try {
      await teacherAPI.removeCourseStudent(parseInt(courseId), studentId);

      toast({
        title: "成功",
        description: `学生 ${studentName} 已从课程中移除`
      });

      // 刷新学生列表
      fetchStudents();
    } catch (error) {
      console.error('移除学生失败:', error);
      toast({
        title: "操作失败",
        description: "无法移除学生，请重试",
        variant: "destructive"
      });
    }
  };

  // 删除文件
  const handleDeleteFile = async (fileId: string, fileName: string) => {
    if (!courseId) return;

    if (!confirm(`确定要删除文件 ${fileName} 吗？`)) {
      return;
    }

    try {
      await teacherAPI.deleteCourseFile(parseInt(courseId), fileId);

      toast({
        title: "成功",
        description: `文件 ${fileName} 已删除`
      });

      // 刷新文件列表
      fetchFiles();
    } catch (error) {
      console.error('删除文件失败:', error);
      toast({
        title: "删除失败",
        description: "无法删除文件，请重试",
        variant: "destructive"
      });
    }
  };

  // 切换发布状态
  const handleTogglePublish = async () => {
    if (!courseId) return;

    try {
      const updatedCourse = await teacherAPI.toggleCoursePublish(parseInt(courseId));

      // 更新本地状态
      setCourse(updatedCourse);
      setFormData(prev => ({
        ...prev,
        is_published: updatedCourse.is_published
      }));

      toast({
        title: "成功",
        description: updatedCourse.is_published ? "课程已发布" : "课程已取消发布"
      });
    } catch (error: any) {
      console.error('切换发布状态失败:', error);
      toast({
        title: "操作失败",
        description: error.response?.data?.detail || "无法切换发布状态，请重试",
        variant: "destructive"
      });
    }
  };

  // 创建或更新课时
  const handleCreateLesson = async () => {
    if (!courseId) return;

    try {
      if (editingLesson) {
        // 更新课时
        await teacherAPI.updateLesson(editingLesson.id, lessonFormData);
        toast({
          title: "成功",
          description: "课时更新成功"
        });
      } else {
        // 创建课时
        await teacherAPI.createLesson(parseInt(courseId), {
          ...lessonFormData,
          lesson_order: lessonFormData.lesson_order || lessons.length + 1
        });
        toast({
          title: "成功",
          description: "课时创建成功"
        });
      }

      // 重置表单并刷新列表
      setLessonFormData({
        title: "",
        description: "",
        content: "",
        lesson_order: 1,
        duration: 30,
        lesson_type: "video",
        video_url: "",
        materials: "",
        is_published: true,
        is_free: false
      });
      setShowLessonForm(false);
      setEditingLesson(null);
      fetchLessons();
    } catch (error) {
      console.error('保存课时失败:', error);
      toast({
        title: editingLesson ? "更新失败" : "创建失败",
        description: "无法保存课时，请重试",
        variant: "destructive"
      });
    }
  };

  // 删除课时
  const handleDeleteLesson = async (lessonId: number, lessonTitle: string) => {
    if (!confirm(`确定要删除课时 "${lessonTitle}" 吗？此操作不可撤销。`)) {
      return;
    }

    try {
      await teacherAPI.deleteLesson(lessonId);

      toast({
        title: "成功",
        description: `课时 "${lessonTitle}" 已删除`
      });

      fetchLessons();
    } catch (error) {
      console.error('删除课时失败:', error);
      toast({
        title: "删除失败",
        description: "无法删除课时，请重试",
        variant: "destructive"
      });
    }
  };

  // 格式化文件大小
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // 格式化学习时间
  const formatStudyTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}分钟`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}小时${mins > 0 ? mins + '分钟' : ''}`;
  };

  if (loading) {
    return (
      <TeacherLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">加载中...</p>
          </div>
        </div>
      </TeacherLayout>
    );
  }

  if (!course) {
    return (
      <TeacherLayout>
        <div className="text-center py-12">
          <p className="text-gray-600">课程不存在或无权访问</p>
          <Button
            onClick={() => navigate('/teacher/courses')}
            className="mt-4"
          >
            返回课程列表
          </Button>
        </div>
      </TeacherLayout>
    );
  }

  return (
    <TeacherLayout>
      <div className="space-y-6">
        {/* 页面头部 */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/teacher/courses')}
              className="flex items-center space-x-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>返回</span>
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">编辑课程</h1>
              <p className="text-gray-600 mt-1">{course.title}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Switch
                checked={formData.is_published}
                onCheckedChange={handleTogglePublish}
                disabled={saving}
              />
              <Badge variant={course.is_published ? "default" : "secondary"}>
                {course.is_published ? "已发布" : "草稿"}
              </Badge>
            </div>
            <Button
              onClick={handleSave}
              disabled={saving}
              className="flex items-center space-x-2"
            >
              <Save className="h-4 w-4" />
              <span>{saving ? "保存中..." : "保存"}</span>
            </Button>
          </div>
        </div>

        {/* 标签页 */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="basic" className="flex items-center space-x-2">
              <BookOpen className="h-4 w-4" />
              <span>基本信息</span>
            </TabsTrigger>
            <TabsTrigger value="lessons" className="flex items-center space-x-2">
              <Clock className="h-4 w-4" />
              <span>课时管理</span>
            </TabsTrigger>
            <TabsTrigger value="students" className="flex items-center space-x-2">
              <Users className="h-4 w-4" />
              <span>学生管理</span>
            </TabsTrigger>
            <TabsTrigger value="files" className="flex items-center space-x-2">
              <FileText className="h-4 w-4" />
              <span>文件管理</span>
            </TabsTrigger>
          </TabsList>

          {/* 基本信息标签页 */}
          <TabsContent value="basic" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>课程基本信息</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="title">课程标题 *</Label>
                    <Input
                      id="title"
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      placeholder="请输入课程标题"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="category">课程分类</Label>
                    <Input
                      id="category"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      placeholder="请输入课程分类"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">课程描述</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="请输入课程描述"
                    rows={4}
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="difficulty">难度级别</Label>
                    <Select
                      value={formData.difficulty}
                      onValueChange={(value) => setFormData({ ...formData, difficulty: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="easy">简单</SelectItem>
                        <SelectItem value="medium">中等</SelectItem>
                        <SelectItem value="hard">困难</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="duration">课程时长（分钟）</Label>
                    <Input
                      id="duration"
                      type="number"
                      value={formData.duration}
                      onChange={(e) => setFormData({ ...formData, duration: parseInt(e.target.value) || 0 })}
                      placeholder="0"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="cover_image">封面图片URL</Label>
                    <Input
                      id="cover_image"
                      value={formData.cover_image}
                      onChange={(e) => setFormData({ ...formData, cover_image: e.target.value })}
                      placeholder="请输入图片URL"
                    />
                  </div>
                </div>

                {/* 发布状态设置 */}
                <div className="border-t pt-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-base font-medium">发布设置</Label>
                      <p className="text-sm text-gray-600 mt-1">
                        控制课程是否对学生可见。发布后学生可以注册和学习此课程。
                      </p>
                    </div>

                    <div className="flex items-center justify-between p-4 border rounded-lg bg-gray-50">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <Switch
                            checked={formData.is_published}
                            onCheckedChange={handleTogglePublish}
                            disabled={saving}
                          />
                          <div>
                            <Label className="text-sm font-medium">
                              {formData.is_published ? "课程已发布" : "课程未发布"}
                            </Label>
                            <p className="text-xs text-gray-600">
                              {formData.is_published
                                ? "学生可以看到并注册此课程"
                                : "课程处于草稿状态，学生无法看到"}
                            </p>
                          </div>
                        </div>
                      </div>
                      <Badge variant={formData.is_published ? "default" : "secondary"}>
                        {formData.is_published ? "已发布" : "草稿"}
                      </Badge>
                    </div>

                    {!formData.is_published && (
                      <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-sm text-yellow-800">
                          💡 提示：发布课程前，建议先添加课程内容和练习，确保课程质量。
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* 课时管理标签页 */}
          <TabsContent value="lessons" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>课时管理</span>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">{lessons.length} 个课时</Badge>
                    <Button
                      onClick={() => setShowLessonForm(true)}
                      size="sm"
                      className="flex items-center space-x-2"
                    >
                      <Plus className="h-4 w-4" />
                      <span>添加课时</span>
                    </Button>
                  </div>
                </CardTitle>
                <CardDescription>
                  管理课程的课时内容，包括视频、文档、练习等
                </CardDescription>
              </CardHeader>
              <CardContent>
                {lessons.length === 0 ? (
                  <div className="text-center py-8">
                    <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">暂无课时内容</p>
                    <Button
                      onClick={() => setShowLessonForm(true)}
                      className="flex items-center space-x-2"
                    >
                      <Plus className="h-4 w-4" />
                      <span>创建第一个课时</span>
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {lessons
                      .sort((a, b) => a.lesson_order - b.lesson_order)
                      .map((lesson) => (
                        <div
                          key={lesson.id}
                          className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                        >
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-3 mb-2">
                                <Badge variant="outline" className="text-xs">
                                  第 {lesson.lesson_order} 课时
                                </Badge>
                                <Badge
                                  variant={lesson.lesson_type === 'video' ? 'default' : 'secondary'}
                                  className="text-xs"
                                >
                                  {lesson.lesson_type === 'video' && '视频'}
                                  {lesson.lesson_type === 'text' && '文档'}
                                  {lesson.lesson_type === 'interactive' && '互动'}
                                  {lesson.lesson_type === 'quiz' && '测验'}
                                </Badge>
                                <Badge
                                  variant={lesson.is_published ? 'default' : 'secondary'}
                                  className="text-xs"
                                >
                                  {lesson.is_published ? '已发布' : '草稿'}
                                </Badge>
                                {lesson.is_free && (
                                  <Badge variant="outline" className="text-xs text-green-600">
                                    免费
                                  </Badge>
                                )}
                              </div>
                              <h4 className="font-medium text-lg mb-1">{lesson.title}</h4>
                              {lesson.description && (
                                <p className="text-gray-600 text-sm mb-2">{lesson.description}</p>
                              )}
                              <div className="flex items-center space-x-4 text-sm text-gray-500">
                                <span className="flex items-center space-x-1">
                                  <Clock className="h-4 w-4" />
                                  <span>{lesson.duration} 分钟</span>
                                </span>
                                {lesson.video_url && (
                                  <span className="flex items-center space-x-1">
                                    <PlayCircle className="h-4 w-4" />
                                    <span>有视频</span>
                                  </span>
                                )}
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  setEditingLesson(lesson);
                                  setLessonFormData({
                                    title: lesson.title,
                                    description: lesson.description || "",
                                    content: lesson.content || "",
                                    lesson_order: lesson.lesson_order,
                                    duration: lesson.duration || 30,
                                    lesson_type: lesson.lesson_type as "video" | "text" | "interactive" | "quiz",
                                    video_url: lesson.video_url || "",
                                    materials: lesson.materials || "",
                                    is_published: lesson.is_published,
                                    is_free: lesson.is_free
                                  });
                                  setShowLessonForm(true);
                                }}
                              >
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleDeleteLesson(lesson.id, lesson.title)}
                                className="text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        </div>
                      ))}
                  </div>
                )}

                {/* 课时表单对话框 */}
                {showLessonForm && (
                  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold">
                          {editingLesson ? '编辑课时' : '添加课时'}
                        </h3>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setShowLessonForm(false);
                            setEditingLesson(null);
                          }}
                        >
                          取消
                        </Button>
                      </div>

                      <div className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <Label htmlFor="lesson-title">课时标题 *</Label>
                            <Input
                              id="lesson-title"
                              value={lessonFormData.title}
                              onChange={(e) => setLessonFormData({
                                ...lessonFormData,
                                title: e.target.value
                              })}
                              placeholder="请输入课时标题"
                            />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="lesson-type">课时类型</Label>
                            <Select
                              value={lessonFormData.lesson_type}
                              onValueChange={(value: any) => setLessonFormData({
                                ...lessonFormData,
                                lesson_type: value
                              })}
                            >
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="video">视频课程</SelectItem>
                                <SelectItem value="text">文档阅读</SelectItem>
                                <SelectItem value="interactive">互动练习</SelectItem>
                                <SelectItem value="quiz">课时测验</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor="lesson-description">课时描述</Label>
                          <Textarea
                            id="lesson-description"
                            value={lessonFormData.description}
                            onChange={(e) => setLessonFormData({
                              ...lessonFormData,
                              description: e.target.value
                            })}
                            placeholder="请输入课时描述"
                            rows={3}
                          />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <Label htmlFor="lesson-duration">时长（分钟）</Label>
                            <Input
                              id="lesson-duration"
                              type="number"
                              value={lessonFormData.duration}
                              onChange={(e) => setLessonFormData({
                                ...lessonFormData,
                                duration: parseInt(e.target.value) || 0
                              })}
                              placeholder="30"
                            />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="lesson-order">课时顺序</Label>
                            <Input
                              id="lesson-order"
                              type="number"
                              value={lessonFormData.lesson_order}
                              onChange={(e) => setLessonFormData({
                                ...lessonFormData,
                                lesson_order: parseInt(e.target.value) || 1
                              })}
                              placeholder="1"
                            />
                          </div>
                        </div>

                        {lessonFormData.lesson_type === 'video' && (
                          <div className="space-y-2">
                            <Label htmlFor="video-url">视频链接</Label>
                            <Input
                              id="video-url"
                              value={lessonFormData.video_url}
                              onChange={(e) => setLessonFormData({
                                ...lessonFormData,
                                video_url: e.target.value
                              })}
                              placeholder="请输入视频URL"
                            />
                          </div>
                        )}

                        <div className="space-y-2">
                          <Label htmlFor="lesson-content">课时内容</Label>
                          <Textarea
                            id="lesson-content"
                            value={lessonFormData.content}
                            onChange={(e) => setLessonFormData({
                              ...lessonFormData,
                              content: e.target.value
                            })}
                            placeholder="请输入课时的详细内容"
                            rows={6}
                          />
                        </div>

                        <div className="flex items-center space-x-6">
                          <div className="flex items-center space-x-2">
                            <Switch
                              checked={lessonFormData.is_published}
                              onCheckedChange={(checked) => setLessonFormData({
                                ...lessonFormData,
                                is_published: checked
                              })}
                            />
                            <Label>立即发布</Label>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Switch
                              checked={lessonFormData.is_free}
                              onCheckedChange={(checked) => setLessonFormData({
                                ...lessonFormData,
                                is_free: checked
                              })}
                            />
                            <Label>免费试看</Label>
                          </div>
                        </div>

                        <div className="flex justify-end space-x-2 pt-4">
                          <Button
                            variant="outline"
                            onClick={() => {
                              setShowLessonForm(false);
                              setEditingLesson(null);
                            }}
                          >
                            取消
                          </Button>
                          <Button
                            onClick={handleCreateLesson}
                            disabled={!lessonFormData.title.trim()}
                          >
                            {editingLesson ? '更新课时' : '创建课时'}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* 学生管理标签页 */}
          <TabsContent value="students" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>课程学生列表</span>
                  <Badge variant="outline">{students.length} 名学生</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {students.length === 0 ? (
                  <div className="text-center py-8">
                    <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">暂无学生注册此课程</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {students.map((student) => (
                      <div
                        key={student.id}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                      >
                        <div className="flex items-center space-x-4">
                          <Avatar>
                            <AvatarImage src={student.avatar_url} />
                            <AvatarFallback>
                              {student.full_name.charAt(0)}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <h4 className="font-medium">{student.full_name}</h4>
                            <p className="text-sm text-gray-600">{student.email}</p>
                            <p className="text-xs text-gray-500">
                              注册时间: {new Date(student.enrolled_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center space-x-6">
                          <div className="text-right">
                            <div className="flex items-center space-x-2 text-sm">
                              <TrendingUp className="h-4 w-4 text-green-600" />
                              <span>{student.progress_percentage.toFixed(1)}%</span>
                            </div>
                            <div className="flex items-center space-x-2 text-sm text-gray-600">
                              <Clock className="h-4 w-4" />
                              <span>{formatStudyTime(student.total_study_time)}</span>
                            </div>
                          </div>

                          <div className="flex items-center space-x-2">
                            <Badge variant={student.is_completed ? "default" : "secondary"}>
                              {student.is_completed ? "已完成" : "学习中"}
                            </Badge>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleRemoveStudent(student.id, student.full_name)}
                              className="text-red-600 hover:text-red-700 hover:bg-red-50"
                            >
                              <UserMinus className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* 文件管理标签页 */}
          <TabsContent value="files" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>课程文件管理</span>
                  <Button size="sm" className="flex items-center space-x-2">
                    <Upload className="h-4 w-4" />
                    <span>上传文件</span>
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {files.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">暂无课程文件</p>
                    <p className="text-sm text-gray-500 mt-2">
                      您可以上传课程相关的文档、资料等文件
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {files.map((file) => (
                      <div
                        key={file.id}
                        className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50"
                      >
                        <div className="flex items-center space-x-3">
                          <FileText className="h-8 w-8 text-blue-600" />
                          <div>
                            <h4 className="font-medium">{file.name}</h4>
                            <p className="text-sm text-gray-600">
                              {formatFileSize(file.size)} • {new Date(file.uploaded_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => window.open(file.url, '_blank')}
                          >
                            <Download className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleDeleteFile(file.id, file.name)}
                            className="text-red-600 hover:text-red-700 hover:bg-red-50"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </TeacherLayout>
  );
};

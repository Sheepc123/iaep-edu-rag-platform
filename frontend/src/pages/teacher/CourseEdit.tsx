import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useToast } from "@/components/ui/use-toast";
import { courseAPI, teacherAPI, Course } from "@/services/api";
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
  TrendingUp
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
  const [activeTab, setActiveTab] = useState("basic");

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

  // 当切换到学生或文件标签时加载数据
  useEffect(() => {
    if (activeTab === "students") {
      fetchStudents();
    } else if (activeTab === "files") {
      fetchFiles();
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
            <Badge variant={course.is_published ? "default" : "secondary"}>
              {course.is_published ? "已发布" : "草稿"}
            </Badge>
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
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="basic" className="flex items-center space-x-2">
              <BookOpen className="h-4 w-4" />
              <span>基本信息</span>
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

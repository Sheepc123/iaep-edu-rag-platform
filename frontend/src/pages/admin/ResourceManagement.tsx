import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BookOpen,
  FileText,
  Download,
  Search,
  Filter,
  Calendar,
  User,
  BarChart3,
  Eye,
  Edit,
  Trash2,
  Database,
  Brain,
  Folder,
  File,
  Clock,
  Tag
} from 'lucide-react';
import { motion } from 'framer-motion';
import { adminAPI } from '@/services/api';

interface CourseResource {
  id: number;
  title: string;
  type: 'courseware' | 'exercise' | 'material';
  subject: string;
  teacher: string;
  teacher_id: number;
  created_at: string;
  updated_at: string;
  file_size: number;
  download_count: number;
  view_count: number;
  status: 'active' | 'draft' | 'archived';
}

interface ExerciseResource {
  id: number;
  title: string;
  subject: string;
  teacher: string;
  question_count: number;
  completion_rate: number;
  average_score: number;
  created_at: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

interface KnowledgeBaseItem {
  id: number;
  title: string;
  filename: string;
  file_path: string;
  file_type: string;
  file_size: number;
  text_content: string;
  summary: string;
  category: string;
  tags: string;
  upload_time: string;
  status: string;
  teacher_id: number;
  teacher_name: string;
  teacher_username: string;
  teacher_email: string;
}

interface TeacherKnowledgeGroup {
  teacher_id: number;
  teacher_name: string;
  teacher_username: string;
  teacher_email: string;
  document_count: number;
  total_size: number;
  categories: string[];
  documents: KnowledgeBaseItem[];
}

const ResourceManagement = () => {
  const [courseResources, setCourseResources] = useState<CourseResource[]>([]);
  const [exerciseResources, setExerciseResources] = useState<ExerciseResource[]>([]);
  const [teacherKnowledgeGroups, setTeacherKnowledgeGroups] = useState<TeacherKnowledgeGroup[]>([]);
  const [knowledgeStats, setKnowledgeStats] = useState({
    total_documents: 0,
    total_teachers: 0,
    total_size: 0,
    categories: [] as string[]
  });
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [subjectFilter, setSubjectFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [teacherFilter, setTeacherFilter] = useState<string>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');

  useEffect(() => {
    fetchResources();
  }, []);

  // 按教师分组知识库数据
  const groupKnowledgeByTeacher = (documents: any[]): TeacherKnowledgeGroup[] => {
    const groups: { [key: number]: TeacherKnowledgeGroup } = {};

    documents.forEach(doc => {
      const teacherId = doc.teacher_id;
      if (!groups[teacherId]) {
        groups[teacherId] = {
          teacher_id: teacherId,
          teacher_name: doc.teacher?.full_name || doc.teacher?.username || '未知教师',
          teacher_username: doc.teacher?.username || '',
          teacher_email: doc.teacher?.email || '',
          document_count: 0,
          total_size: 0,
          categories: [],
          documents: []
        };
      }

      groups[teacherId].documents.push({
        id: doc.id,
        title: doc.title,
        filename: doc.filename,
        file_path: doc.file_path,
        file_type: doc.file_type,
        file_size: doc.file_size,
        text_content: doc.text_content || '',
        summary: doc.summary || '',
        category: doc.category || '未分类',
        tags: doc.tags || '',
        upload_time: doc.upload_time,
        status: doc.status,
        teacher_id: teacherId,
        teacher_name: groups[teacherId].teacher_name,
        teacher_username: groups[teacherId].teacher_username,
        teacher_email: groups[teacherId].teacher_email
      });

      groups[teacherId].document_count++;
      groups[teacherId].total_size += doc.file_size;

      if (doc.category && !groups[teacherId].categories.includes(doc.category)) {
        groups[teacherId].categories.push(doc.category);
      }
    });

    return Object.values(groups);
  };

  const fetchResources = async () => {
    try {
      setLoading(true);

      // 获取知识库数据
      try {
        // 获取知识库统计
        const statsResponse = await adminAPI.getKnowledgeBaseStats();
        setKnowledgeStats(statsResponse);

        // 获取所有教师的知识库数据
        const knowledgeResponse = await adminAPI.getAllTeachersKnowledgeBase({
          page: 1,
          size: 1000 // 获取所有数据
        });

        // 按教师分组知识库数据
        const groupedData = groupKnowledgeByTeacher(knowledgeResponse.documents || []);
        setTeacherKnowledgeGroups(groupedData);

      } catch (error) {
        console.error('获取知识库数据失败:', error);
        // 使用模拟数据作为后备
        setTeacherKnowledgeGroups([
          {
            teacher_id: 1,
            teacher_name: '李老师',
            teacher_username: 'teacher1',
            teacher_email: 'teacher1@example.com',
            document_count: 2,
            total_size: 2063360,
            categories: ['编程基础', '算法设计'],
            documents: [
              {
                id: 1,
                title: 'Python基础语法总结',
                filename: 'python_basics.pdf',
                file_path: '/uploads/knowledge_base/2024/07/python_basics.pdf',
                file_type: 'pdf',
                file_size: 15360,
                text_content: 'Python基础语法包括变量定义、数据类型、控制结构等内容...',
                summary: 'Python编程语言的基础语法总结',
                category: '编程基础',
                tags: 'Python,基础语法,编程',
                upload_time: '2024-07-15T10:30:00Z',
                status: 'active',
                teacher_id: 1,
                teacher_name: '李老师',
                teacher_username: 'teacher1',
                teacher_email: 'teacher1@example.com'
              },
              {
                id: 2,
                title: '数据结构算法笔记',
                filename: 'data_structures.pdf',
                file_path: '/uploads/knowledge_base/2024/07/data_structures.pdf',
                file_type: 'pdf',
                file_size: 2048000,
                text_content: '常用数据结构包括数组、链表、栈、队列、树、图等...',
                summary: '数据结构与算法的详细笔记',
                category: '算法设计',
                tags: '数据结构,算法,编程',
                upload_time: '2024-07-12T09:15:00Z',
                status: 'active',
                teacher_id: 1,
                teacher_name: '李老师',
                teacher_username: 'teacher1',
                teacher_email: 'teacher1@example.com'
              }
            ]
          },
          {
            teacher_id: 2,
            teacher_name: '王老师',
            teacher_username: 'teacher2',
            teacher_email: 'teacher2@example.com',
            document_count: 1,
            total_size: 512000,
            categories: ['数学基础'],
            documents: [
              {
                id: 3,
                title: '高等数学公式集',
                filename: 'math_formulas.doc',
                file_path: '/uploads/knowledge_base/2024/07/math_formulas.doc',
                file_type: 'doc',
                file_size: 512000,
                text_content: '微积分、线性代数、概率论等重要公式汇总...',
                summary: '高等数学重要公式汇总',
                category: '数学基础',
                tags: '数学,公式,微积分',
                upload_time: '2024-07-10T14:20:00Z',
                status: 'active',
                teacher_id: 2,
                teacher_name: '王老师',
                teacher_username: 'teacher2',
                teacher_email: 'teacher2@example.com'
              }
            ]
          }
        ]);

        setKnowledgeStats({
          total_documents: 3,
          total_teachers: 2,
          total_size: 2575360,
          categories: ['编程基础', '算法设计', '数学基础']
        });
      }

      // 模拟课件数据
      setCourseResources([
        {
          id: 1,
          title: 'Python基础编程课件',
          type: 'courseware',
          subject: '计算机科学',
          teacher: '李老师',
          teacher_id: 1,
          created_at: '2024-07-15T10:30:00Z',
          updated_at: '2024-07-20T14:20:00Z',
          file_size: 2048000,
          download_count: 45,
          view_count: 128,
          status: 'active'
        },
        {
          id: 2,
          title: '高等数学练习题集',
          type: 'exercise',
          subject: '数学',
          teacher: '王老师',
          teacher_id: 2,
          created_at: '2024-07-18T09:15:00Z',
          updated_at: '2024-07-19T16:45:00Z',
          file_size: 1536000,
          download_count: 32,
          view_count: 89,
          status: 'active'
        },
        {
          id: 3,
          title: '数据结构算法讲义',
          type: 'material',
          subject: '计算机科学',
          teacher: '张老师',
          teacher_id: 3,
          created_at: '2024-07-12T14:20:00Z',
          updated_at: '2024-07-16T11:30:00Z',
          file_size: 3072000,
          download_count: 67,
          view_count: 156,
          status: 'active'
        }
      ]);

      setExerciseResources([
        {
          id: 1,
          title: 'Python基础语法练习',
          subject: '计算机科学',
          teacher: '李老师',
          question_count: 25,
          completion_rate: 78.5,
          average_score: 82.3,
          created_at: '2024-07-15T10:30:00Z',
          difficulty: 'easy'
        },
        {
          id: 2,
          title: '高等数学微积分练习',
          subject: '数学',
          teacher: '王老师',
          question_count: 40,
          completion_rate: 65.2,
          average_score: 75.8,
          created_at: '2024-07-18T09:15:00Z',
          difficulty: 'hard'
        }
      ]);
    } catch (error) {
      console.error('获取资源失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTypeLabel = (type: string) => {
    const typeMap = {
      courseware: '课件',
      exercise: '练习',
      material: '教材'
    };
    return typeMap[type as keyof typeof typeMap] || type;
  };

  const getTypeBadge = (type: string) => {
    const colorMap = {
      courseware: 'bg-blue-100 text-blue-800',
      exercise: 'bg-green-100 text-green-800',
      material: 'bg-purple-100 text-purple-800'
    };
    return <Badge className={colorMap[type as keyof typeof colorMap]}>{getTypeLabel(type)}</Badge>;
  };

  const getDifficultyBadge = (difficulty: string) => {
    const colorMap = {
      easy: 'bg-green-100 text-green-800',
      medium: 'bg-yellow-100 text-yellow-800',
      hard: 'bg-red-100 text-red-800'
    };
    const labelMap = {
      easy: '简单',
      medium: '中等',
      hard: '困难'
    };
    return <Badge className={colorMap[difficulty as keyof typeof colorMap]}>
      {labelMap[difficulty as keyof typeof labelMap]}
    </Badge>;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getFileTypeIcon = (fileType: string) => {
    switch (fileType) {
      case 'pdf':
        return <FileText className="w-4 h-4 text-red-500" />;
      case 'doc':
        return <FileText className="w-4 h-4 text-blue-500" />;
      case 'image':
        return <File className="w-4 h-4 text-green-500" />;
      default:
        return <File className="w-4 h-4 text-gray-500" />;
    }
  };

  const getFileTypeBadge = (fileType: string) => {
    const colorMap = {
      text: 'bg-gray-100 text-gray-800',
      pdf: 'bg-red-100 text-red-800',
      doc: 'bg-blue-100 text-blue-800',
      image: 'bg-green-100 text-green-800'
    };
    const labelMap = {
      text: '文本',
      pdf: 'PDF',
      doc: '文档',
      image: '图片'
    };
    return <Badge className={colorMap[fileType as keyof typeof colorMap]}>
      {labelMap[fileType as keyof typeof labelMap]}
    </Badge>;
  };

  const filteredCourseResources = courseResources.filter(resource => {
    const matchesSearch = resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         resource.teacher.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSubject = subjectFilter === 'all' || resource.subject === subjectFilter;
    const matchesType = typeFilter === 'all' || resource.type === typeFilter;

    return matchesSearch && matchesSubject && matchesType;
  });

  // 筛选教师知识库组
  const filteredTeacherGroups = teacherKnowledgeGroups.filter(group => {
    const matchesTeacher = teacherFilter === 'all' || group.teacher_name === teacherFilter;
    const matchesCategory = categoryFilter === 'all' || group.categories.includes(categoryFilter);

    // 如果有搜索词，检查组内是否有匹配的文档
    if (searchTerm) {
      const hasMatchingDoc = group.documents.some(doc =>
        doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.text_content.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.tags.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.category.toLowerCase().includes(searchTerm.toLowerCase())
      );
      return matchesTeacher && matchesCategory && hasMatchingDoc;
    }

    return matchesTeacher && matchesCategory;
  }).map(group => ({
    ...group,
    documents: group.documents.filter(doc => {
      if (!searchTerm) return true;
      return doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
             doc.text_content.toLowerCase().includes(searchTerm.toLowerCase()) ||
             doc.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
             doc.tags.toLowerCase().includes(searchTerm.toLowerCase()) ||
             doc.category.toLowerCase().includes(searchTerm.toLowerCase());
    })
  }));

  // 获取所有教师名称
  const teachers = Array.from(new Set(teacherKnowledgeGroups.map(g => g.teacher_name)));

  // 获取所有分类
  const categories = Array.from(new Set(
    teacherKnowledgeGroups.flatMap(g => g.categories)
  ));

  // 获取学科（从课件资源中）
  const subjects = Array.from(new Set(courseResources.map(r => r.subject)));

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-8">
        {/* 页面标题 */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">资源管理</h1>
            <p className="text-gray-600 mt-2">管理教师创建的课件、练习、教学资源和知识库内容</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline" className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>批量导出</span>
            </Button>
          </div>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">课件资源</p>
                  <p className="text-2xl font-bold text-gray-900">{courseResources.length}</p>
                </div>
                <BookOpen className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">知识库条目</p>
                  <p className="text-2xl font-bold text-gray-900">{knowledgeStats.total_documents}</p>
                </div>
                <Database className="w-8 h-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">总下载量</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {courseResources.reduce((sum, r) => sum + r.download_count, 0)}
                  </p>
                </div>
                <Download className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">总浏览量</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {courseResources.reduce((sum, r) => sum + r.view_count, 0)}
                  </p>
                </div>
                <Eye className="w-8 h-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">活跃教师</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {new Set(courseResources.map(r => r.teacher_id)).size}
                  </p>
                </div>
                <User className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 搜索和筛选 */}
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input
                    placeholder="搜索资源标题、教师姓名、内容或标签..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <div className="flex gap-3">
                <Select value={subjectFilter} onValueChange={setSubjectFilter}>
                  <SelectTrigger className="w-40">
                    <SelectValue placeholder="学科" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有学科</SelectItem>
                    {subjects.map(subject => (
                      <SelectItem key={subject} value={subject}>{subject}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select value={teacherFilter} onValueChange={setTeacherFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="教师" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有教师</SelectItem>
                    {teachers.map(teacher => (
                      <SelectItem key={teacher} value={teacher}>{teacher}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="分类" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有分类</SelectItem>
                    {knowledgeStats.categories.map(category => (
                      <SelectItem key={category} value={category}>{category}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select value={typeFilter} onValueChange={setTypeFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="类型" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有类型</SelectItem>
                    <SelectItem value="courseware">课件</SelectItem>
                    <SelectItem value="exercise">练习</SelectItem>
                    <SelectItem value="material">教材</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 资源列表 */}
        <Tabs defaultValue="courseware" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="courseware">课件资源</TabsTrigger>
            <TabsTrigger value="exercises">练习资源</TabsTrigger>
            <TabsTrigger value="knowledge">知识库</TabsTrigger>
          </TabsList>

          <TabsContent value="courseware" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="w-5 h-5" />
                  <span>课件资源列表</span>
                  <Badge variant="secondary">{filteredCourseResources.length}</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-3 px-4 font-medium text-gray-600">资源信息</th>
                        <th className="text-left py-3 px-4 font-medium text-gray-600">类型</th>
                        <th className="text-left py-3 px-4 font-medium text-gray-600">学科</th>
                        <th className="text-left py-3 px-4 font-medium text-gray-600">教师</th>
                        <th className="text-left py-3 px-4 font-medium text-gray-600">统计</th>
                        <th className="text-left py-3 px-4 font-medium text-gray-600">创建时间</th>
                        <th className="text-right py-3 px-4 font-medium text-gray-600">操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredCourseResources.map((resource, index) => (
                        <motion.tr
                          key={resource.id}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.05 }}
                          className="border-b hover:bg-gray-50"
                        >
                          <td className="py-4 px-4">
                            <div>
                              <p className="font-medium text-gray-900">{resource.title}</p>
                              <p className="text-sm text-gray-500">{formatFileSize(resource.file_size)}</p>
                            </div>
                          </td>
                          <td className="py-4 px-4">
                            {getTypeBadge(resource.type)}
                          </td>
                          <td className="py-4 px-4">
                            <span className="text-sm text-gray-700">{resource.subject}</span>
                          </td>
                          <td className="py-4 px-4">
                            <span className="text-sm text-gray-700">{resource.teacher}</span>
                          </td>
                          <td className="py-4 px-4">
                            <div className="text-sm text-gray-600">
                              <div>下载: {resource.download_count}</div>
                              <div>浏览: {resource.view_count}</div>
                            </div>
                          </td>
                          <td className="py-4 px-4">
                            <div className="flex items-center space-x-1 text-sm text-gray-600">
                              <Calendar className="w-4 h-4" />
                              <span>{formatDate(resource.created_at)}</span>
                            </div>
                          </td>
                          <td className="py-4 px-4">
                            <div className="flex items-center justify-end space-x-2">
                              <Button variant="ghost" size="sm">
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Download className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Edit className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Trash2 className="w-4 h-4 text-red-500" />
                              </Button>
                            </div>
                          </td>
                        </motion.tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="exercises" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="w-5 h-5" />
                  <span>练习资源列表</span>
                  <Badge variant="secondary">{exerciseResources.length}</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {exerciseResources.map((exercise, index) => (
                    <motion.div
                      key={exercise.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className="hover:shadow-lg transition-shadow">
                        <CardContent className="p-6">
                          <div className="space-y-4">
                            <div className="flex items-start justify-between">
                              <h3 className="font-semibold text-gray-900">{exercise.title}</h3>
                              {getDifficultyBadge(exercise.difficulty)}
                            </div>
                            
                            <div className="space-y-2 text-sm text-gray-600">
                              <div className="flex justify-between">
                                <span>学科:</span>
                                <span>{exercise.subject}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>教师:</span>
                                <span>{exercise.teacher}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>题目数:</span>
                                <span>{exercise.question_count}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>完成率:</span>
                                <span className="text-green-600">{exercise.completion_rate}%</span>
                              </div>
                              <div className="flex justify-between">
                                <span>平均分:</span>
                                <span className="text-blue-600">{exercise.average_score}</span>
                              </div>
                            </div>
                            
                            <div className="flex items-center justify-between pt-4 border-t">
                              <span className="text-xs text-gray-500">
                                {formatDate(exercise.created_at)}
                              </span>
                              <div className="flex space-x-2">
                                <Button variant="ghost" size="sm">
                                  <Eye className="w-4 h-4" />
                                </Button>
                                <Button variant="ghost" size="sm">
                                  <Download className="w-4 h-4" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="knowledge" className="space-y-4">
            {filteredTeacherGroups.map((group) => (
              <Card key={group.teacher_id}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <User className="w-5 h-5" />
                      <span>{group.teacher_name}的知识库</span>
                      <Badge variant="secondary">{group.documents.length}</Badge>
                    </div>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <FileText className="w-4 h-4" />
                        <span>{group.document_count}个文档</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Database className="w-4 h-4" />
                        <span>{formatFileSize(group.total_size)}</span>
                      </div>
                    </div>
                  </CardTitle>
                  <CardDescription>
                    用户名: {group.teacher_username} | 邮箱: {group.teacher_email} |
                    分类: {group.categories.join(', ')}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {group.documents.map((item, index) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className="hover:shadow-lg transition-shadow h-full">
                        <CardContent className="p-6">
                          <div className="space-y-4">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{item.title}</h3>
                                <div className="flex items-center space-x-2 mb-2">
                                  {getFileTypeIcon(item.file_type)}
                                  {getFileTypeBadge(item.file_type)}
                                  {!item.is_public && (
                                    <Badge variant="outline" className="text-xs">私有</Badge>
                                  )}
                                </div>
                              </div>
                            </div>

                            <div className="space-y-2 text-sm text-gray-600">
                              <div className="flex justify-between">
                                <span>教师:</span>
                                <span className="font-medium">{item.teacher_name}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>学科:</span>
                                <span>{item.subject}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>分类:</span>
                                <span>{item.category}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>大小:</span>
                                <span>{formatFileSize(item.file_size)}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>使用次数:</span>
                                <span className="text-blue-600">{item.usage_count}</span>
                              </div>
                            </div>

                            {/* 内容预览 */}
                            <div className="border-t pt-3">
                              <p className="text-xs text-gray-500 mb-2">内容预览:</p>
                              <p className="text-sm text-gray-700 line-clamp-3">
                                {item.content}
                              </p>
                            </div>

                            {/* 标签 */}
                            {item.tags.length > 0 && (
                              <div className="border-t pt-3">
                                <p className="text-xs text-gray-500 mb-2">标签:</p>
                                <div className="flex flex-wrap gap-1">
                                  {item.tags.slice(0, 3).map((tag, i) => (
                                    <Badge key={i} variant="outline" className="text-xs">
                                      <Tag className="w-3 h-3 mr-1" />
                                      {tag}
                                    </Badge>
                                  ))}
                                  {item.tags.length > 3 && (
                                    <Badge variant="outline" className="text-xs">
                                      +{item.tags.length - 3}
                                    </Badge>
                                  )}
                                </div>
                              </div>
                            )}

                            <div className="flex items-center justify-between pt-4 border-t">
                              <div className="flex items-center space-x-1 text-xs text-gray-500">
                                <Clock className="w-3 h-3" />
                                <span>{formatDate(item.created_at)}</span>
                              </div>
                              <div className="flex space-x-2">
                                <Button variant="ghost" size="sm" title="查看详情">
                                  <Eye className="w-4 h-4" />
                                </Button>
                                <Button variant="ghost" size="sm" title="下载">
                                  <Download className="w-4 h-4" />
                                </Button>
                                <Button variant="ghost" size="sm" title="编辑">
                                  <Edit className="w-4 h-4" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>

                {group.documents.length === 0 && (
                  <div className="text-center py-8">
                    <Database className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">该教师暂无知识库文档</p>
                  </div>
                )}
              </CardContent>
            </Card>
            ))}

            {filteredTeacherGroups.length === 0 && (
              <Card>
                <CardContent className="p-12">
                  <div className="text-center">
                    <Database className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">暂无知识库内容</h3>
                    <p className="text-gray-500">没有找到符合条件的知识库内容</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </AdminLayout>
  );
};

export default ResourceManagement;

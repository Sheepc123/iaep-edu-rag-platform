import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  Users,
  Search,
  Filter,
  Eye,
  BookOpen,
  Clock,
  TrendingUp,
  GraduationCap,
  Mail,
  Calendar,
  MoreVertical,
  Download,
  RefreshCw
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { teacherAPI, StudentInfo } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";

interface StudentsListResponse {
  students: StudentInfo[];
  total: number;
  skip: number;
  limit: number;
}

export const TeacherStudents: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  // 状态管理
  const [students, setStudents] = useState<StudentInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCourse, setSelectedCourse] = useState<string>("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalStudents, setTotalStudents] = useState(0);
  const [pageSize] = useState(10);

  // 获取学生列表
  const fetchStudents = async () => {
    try {
      setLoading(true);
      const params = {
        skip: (currentPage - 1) * pageSize,
        limit: pageSize,
        search: searchTerm || undefined,
        course_id: selectedCourse !== "all" ? parseInt(selectedCourse) : undefined
      };

      const response = await teacherAPI.getStudents(params);
      setStudents(response.students);
      setTotalStudents(response.total);
    } catch (error) {
      console.error('获取学生列表失败:', error);
      toast({
        title: "加载失败",
        description: "无法获取学生列表，请稍后重试",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  // 页面加载时获取数据
  useEffect(() => {
    fetchStudents();
  }, [currentPage, selectedCourse]);

  // 搜索处理
  const handleSearch = () => {
    setCurrentPage(1);
    fetchStudents();
  };

  // 重置搜索
  const handleReset = () => {
    setSearchTerm("");
    setSelectedCourse("all");
    setCurrentPage(1);
    fetchStudents();
  };

  // 查看学生详情
  const handleViewStudent = (studentId: number) => {
    navigate(`/teacher/students/${studentId}`);
  };

  // 动画配置
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring" as const,
        stiffness: 300,
        damping: 30
      }
    }
  };

  // 格式化时间
  const formatDate = (dateString: string | null) => {
    if (!dateString) return "未知";
    return new Date(dateString).toLocaleDateString('zh-CN');
  };

  // 格式化学习时间
  const formatStudyTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}分钟`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}小时${remainingMinutes > 0 ? remainingMinutes + '分钟' : ''}`;
  };

  return (
    <TeacherLayout>
      <motion.div
        className="space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* 页面标题 */}
        <motion.div variants={cardVariants}>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">学生管理</h1>
              <p className="text-gray-600 mt-2">管理和查看学生的学习情况</p>
            </div>
            <div className="flex items-center gap-3">
              <Button
                onClick={fetchStudents}
                variant="outline"
                size="sm"
                className="flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                刷新
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                导出
              </Button>
            </div>
          </div>
        </motion.div>

        {/* 搜索和筛选 */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <Input
                      placeholder="搜索学生姓名、邮箱或学号..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                      onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    />
                  </div>
                </div>
                <div className="flex gap-3">
                  <Select value={selectedCourse} onValueChange={setSelectedCourse}>
                    <SelectTrigger className="w-48">
                      <Filter className="w-4 h-4 mr-2" />
                      <SelectValue placeholder="选择课程" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">所有课程</SelectItem>
                      {/* 这里可以动态加载教师的课程列表 */}
                    </SelectContent>
                  </Select>
                  <Button onClick={handleSearch} className="bg-blue-600 hover:bg-blue-700">
                    搜索
                  </Button>
                  <Button onClick={handleReset} variant="outline">
                    重置
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 统计卡片 */}
        <motion.div variants={cardVariants}>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">总学生数</p>
                    <p className="text-2xl font-bold text-gray-900">{totalStudents}</p>
                  </div>
                  <div className="bg-blue-100 p-3 rounded-full">
                    <Users className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">活跃学生</p>
                    <p className="text-2xl font-bold text-gray-900">{students.filter(s => s.last_active).length}</p>
                  </div>
                  <div className="bg-green-100 p-3 rounded-full">
                    <TrendingUp className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">平均进度</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {students.length > 0
                        ? Math.round(students.reduce((sum, s) => sum + (s.average_progress || 0), 0) / students.length)
                        : 0}%
                    </p>
                  </div>
                  <div className="bg-yellow-100 p-3 rounded-full">
                    <BookOpen className="w-6 h-6 text-yellow-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">总学习时长</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {formatStudyTime(students.reduce((sum, s) => sum + (s.total_study_time || 0), 0))}
                    </p>
                  </div>
                  <div className="bg-purple-100 p-3 rounded-full">
                    <Clock className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>

        {/* 学生列表 */}
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl font-bold flex items-center gap-2">
                <Users className="w-5 h-5 text-blue-600" />
                学生列表
                <Badge variant="secondary" className="ml-2">
                  {totalStudents} 名学生
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-2 text-gray-600">加载中...</span>
                </div>
              ) : students.length === 0 ? (
                <div className="text-center py-12">
                  <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">暂无学生</h3>
                  <p className="text-gray-600">还没有学生注册您的课程</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>学生信息</TableHead>
                        <TableHead>学号</TableHead>
                        <TableHead>专业班级</TableHead>
                        <TableHead>课程数量</TableHead>
                        <TableHead>学习进度</TableHead>
                        <TableHead>学习时长</TableHead>
                        <TableHead>最后活跃</TableHead>
                        <TableHead>操作</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {students.map((student) => (
                        <TableRow key={student.id} className="hover:bg-gray-50">
                          <TableCell>
                            <div className="flex items-center gap-3">
                              <Avatar className="w-10 h-10">
                                <AvatarImage
                                  src={student.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(student.full_name)}&background=3b82f6&color=fff&size=40`}
                                  alt={student.full_name}
                                />
                                <AvatarFallback>{student.full_name.charAt(0)}</AvatarFallback>
                              </Avatar>
                              <div>
                                <p className="font-medium text-gray-900">{student.full_name}</p>
                                <p className="text-sm text-gray-500 flex items-center gap-1">
                                  <Mail className="w-3 h-3" />
                                  {student.email}
                                </p>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <span className="text-sm font-mono">{student.student_id || "未设置"}</span>
                          </TableCell>
                          <TableCell>
                            <div className="text-sm">
                              <p className="font-medium">{student.major || "未设置"}</p>
                              <p className="text-gray-500">{student.class_name || "未设置"}</p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="flex items-center gap-1">
                              <BookOpen className="w-3 h-3" />
                              {student.total_courses || 0}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-blue-600 h-2 rounded-full"
                                  style={{ width: `${student.average_progress || 0}%` }}
                                ></div>
                              </div>
                              <span className="text-sm font-medium">{Math.round(student.average_progress || 0)}%</span>
                            </div>
                          </TableCell>
                          <TableCell>
                            <span className="text-sm flex items-center gap-1">
                              <Clock className="w-3 h-3" />
                              {formatStudyTime(student.total_study_time || 0)}
                            </span>
                          </TableCell>
                          <TableCell>
                            <span className="text-sm text-gray-500 flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              {formatDate(student.last_active)}
                            </span>
                          </TableCell>
                          <TableCell>
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="sm">
                                  <MoreVertical className="w-4 h-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end">
                                <DropdownMenuItem onClick={() => handleViewStudent(student.id)}>
                                  <Eye className="w-4 h-4 mr-2" />
                                  查看详情
                                </DropdownMenuItem>
                                <DropdownMenuItem>
                                  <Mail className="w-4 h-4 mr-2" />
                                  发送消息
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* 分页 */}
        {totalStudents > pageSize && (
          <motion.div variants={cardVariants}>
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">
                显示 {(currentPage - 1) * pageSize + 1} 到 {Math.min(currentPage * pageSize, totalStudents)} 条，共 {totalStudents} 条记录
              </p>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                >
                  上一页
                </Button>
                <span className="text-sm text-gray-600">
                  第 {currentPage} 页，共 {Math.ceil(totalStudents / pageSize)} 页
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => prev + 1)}
                  disabled={currentPage >= Math.ceil(totalStudents / pageSize)}
                >
                  下一页
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>
    </TeacherLayout>
  );
};

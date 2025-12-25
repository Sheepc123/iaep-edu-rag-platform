import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  GraduationCap,
  Target,
  TrendingUp,
  Activity,
  MessageSquare,
  BookOpen,
  CheckCircle,
  XCircle,
  Brain,
  Award,
  Clock
} from 'lucide-react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';
import { adminAPI } from '@/services/api';

interface StudentData {
  id: number;
  username: string;
  full_name: string;
  email: string;
  created_at: string;
  last_login: string;
  // 学习统计数据
  ai_usage_today: number;
  ai_usage_week: number;
  total_study_time: number;
  exercises_completed: number;
  exercises_correct: number;
  average_score: number;
  courses_enrolled: number;
  courses_completed: number;
  active_modules: string[];
  knowledge_points: { name: string; mastery: number }[];
}

interface StudentUsageStats {
  today_total: number;
  week_total: number;
  average_accuracy: number;
  most_active_student: string;
  total_study_hours: number;
}

const StudentStats = () => {
  const [students, setStudents] = useState<StudentData[]>([]);
  const [usageStats, setUsageStats] = useState<StudentUsageStats>({
    today_total: 0,
    week_total: 0,
    average_accuracy: 0,
    most_active_student: '',
    total_study_hours: 0
  });
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('today');

  useEffect(() => {
    fetchStudentStats();
  }, [timeRange]);

  const fetchStudentStats = async () => {
    try {
      setLoading(true);
      
      // 获取学生列表
      const studentsResponse = await adminAPI.getUsers({
        role: 'student',
        page: 1,
        size: 100
      });
      
      // 模拟学生统计数据（实际应该从API获取）
      const studentData: StudentData[] = studentsResponse.users
        .filter((user: any) => user.role === 'student')
        .map((student: any) => ({
          ...student,
          ai_usage_today: Math.floor(Math.random() * 15) + 1,
          ai_usage_week: Math.floor(Math.random() * 80) + 20,
          total_study_time: Math.floor(Math.random() * 100) + 20,
          exercises_completed: Math.floor(Math.random() * 50) + 10,
          exercises_correct: Math.floor(Math.random() * 40) + 8,
          average_score: Math.floor(Math.random() * 30) + 70,
          courses_enrolled: Math.floor(Math.random() * 8) + 2,
          courses_completed: Math.floor(Math.random() * 5) + 1,
          active_modules: ['智能练习', 'AI助手', '课程学习'].slice(0, Math.floor(Math.random() * 3) + 1),
          knowledge_points: [
            { name: 'Python基础', mastery: Math.floor(Math.random() * 30) + 70 },
            { name: '数据结构', mastery: Math.floor(Math.random() * 40) + 60 },
            { name: '算法设计', mastery: Math.floor(Math.random() * 50) + 50 }
          ]
        }));

      setStudents(studentData);

      // 计算统计数据
      const stats: StudentUsageStats = {
        today_total: studentData.reduce((sum, s) => sum + s.ai_usage_today, 0),
        week_total: studentData.reduce((sum, s) => sum + s.ai_usage_week, 0),
        average_accuracy: studentData.reduce((sum, s) => sum + (s.exercises_correct / s.exercises_completed * 100), 0) / studentData.length,
        most_active_student: studentData.sort((a, b) => b.ai_usage_week - a.ai_usage_week)[0]?.full_name || '',
        total_study_hours: studentData.reduce((sum, s) => sum + s.total_study_time, 0)
      };

      setUsageStats(stats);

    } catch (error) {
      console.error('获取学生统计失败:', error);
      // 使用模拟数据
      setStudents([
        {
          id: 1,
          username: 'student1',
          full_name: '张同学',
          email: 'student1@example.com',
          created_at: '2024-01-15T10:30:00Z',
          last_login: '2024-07-20T08:15:00Z',
          ai_usage_today: 8,
          ai_usage_week: 45,
          total_study_time: 68,
          exercises_completed: 25,
          exercises_correct: 20,
          average_score: 82,
          courses_enrolled: 5,
          courses_completed: 3,
          active_modules: ['智能练习', 'AI助手', '课程学习'],
          knowledge_points: [
            { name: 'Python基础', mastery: 85 },
            { name: '数据结构', mastery: 72 },
            { name: '算法设计', mastery: 68 }
          ]
        },
        {
          id: 2,
          username: 'student2',
          full_name: '王同学',
          email: 'student2@example.com',
          created_at: '2024-02-10T14:20:00Z',
          last_login: '2024-07-20T10:30:00Z',
          ai_usage_today: 12,
          ai_usage_week: 67,
          total_study_time: 89,
          exercises_completed: 32,
          exercises_correct: 24,
          average_score: 78,
          courses_enrolled: 4,
          courses_completed: 2,
          active_modules: ['智能练习', 'AI助手'],
          knowledge_points: [
            { name: 'Python基础', mastery: 78 },
            { name: '数据结构', mastery: 65 },
            { name: '算法设计', mastery: 71 }
          ]
        }
      ]);

      setUsageStats({
        today_total: 20,
        week_total: 112,
        average_accuracy: 78.5,
        most_active_student: '王同学',
        total_study_hours: 157
      });
    } finally {
      setLoading(false);
    }
  };

  // 学习效果趋势数据
  const accuracyTrendData = [
    { week: '第1周', accuracy: 72, students: 15 },
    { week: '第2周', accuracy: 75, students: 18 },
    { week: '第3周', accuracy: 78, students: 22 },
    { week: '第4周', accuracy: 76, students: 20 },
    { week: '第5周', accuracy: 79, students: 25 },
    { week: '第6周', accuracy: 81, students: 28 },
    { week: '第7周', accuracy: 78, students: 24 }
  ];

  // 高频错误知识点
  const errorPointsData = [
    { name: '指针操作', count: 45, difficulty: 8 },
    { name: '递归算法', count: 38, difficulty: 7 },
    { name: '数据库查询', count: 32, difficulty: 6 },
    { name: '异常处理', count: 28, difficulty: 5 },
    { name: '面向对象', count: 25, difficulty: 6 }
  ];

  // 活跃模块数据
  const moduleUsageData = [
    { name: '智能练习', count: 89, percentage: 45 },
    { name: 'AI助手', count: 156, percentage: 78 },
    { name: '课程学习', count: 134, percentage: 67 },
    { name: '在线测试', count: 78, percentage: 39 },
    { name: '知识问答', count: 92, percentage: 46 }
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

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
            <h1 className="text-3xl font-bold text-gray-900">学生学习统计</h1>
            <p className="text-gray-600 mt-2">学生使用次数统计与学习效果分析</p>
          </div>
          <div className="flex space-x-3">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="today">今日</SelectItem>
                <SelectItem value="week">本周</SelectItem>
                <SelectItem value="month">本月</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline">
              导出报告
            </Button>
          </div>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">今日使用次数</p>
                    <p className="text-2xl font-bold text-gray-900">{usageStats.today_total}</p>
                    <p className="text-green-600 text-sm">+12% vs 昨日</p>
                  </div>
                  <GraduationCap className="w-8 h-8 text-blue-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">本周使用次数</p>
                    <p className="text-2xl font-bold text-gray-900">{usageStats.week_total}</p>
                    <p className="text-green-600 text-sm">+18% vs 上周</p>
                  </div>
                  <Activity className="w-8 h-8 text-green-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">平均正确率</p>
                    <p className="text-2xl font-bold text-gray-900">{usageStats.average_accuracy.toFixed(1)}%</p>
                    <p className="text-green-600 text-sm">+2.3% vs 上周</p>
                  </div>
                  <Target className="w-8 h-8 text-purple-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">总学习时长</p>
                    <p className="text-2xl font-bold text-gray-900">{usageStats.total_study_hours}h</p>
                    <p className="text-blue-600 text-sm">最活跃: {usageStats.most_active_student}</p>
                  </div>
                  <Clock className="w-8 h-8 text-orange-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* 图表区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 学习效果趋势 */}
          <Card>
            <CardHeader>
              <CardTitle>学习效果趋势</CardTitle>
              <CardDescription>平均正确率和活跃学生数变化</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={accuracyTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="accuracy" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} name="正确率%" />
                  <Line type="monotone" dataKey="students" stroke="#10B981" strokeWidth={2} name="活跃学生" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* 活跃模块分布 */}
          <Card>
            <CardHeader>
              <CardTitle>活跃板块分布</CardTitle>
              <CardDescription>学生最常使用的功能模块</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={moduleUsageData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={80} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* 高频错误知识点 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <XCircle className="w-5 h-5 text-red-500" />
              <span>高频错误知识点</span>
            </CardTitle>
            <CardDescription>需要重点关注的薄弱环节</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {errorPointsData.map((point, index) => (
                <motion.div
                  key={point.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="text-center p-4 bg-red-50 rounded-lg border border-red-200"
                >
                  <div className="text-2xl font-bold text-red-600 mb-2">{point.count}</div>
                  <div className="text-gray-900 text-sm font-medium mb-1">{point.name}</div>
                  <div className="text-red-500 text-xs">错误次数</div>
                  <div className="mt-2 flex justify-center">
                    {Array.from({ length: 10 }, (_, i) => (
                      <div
                        key={i}
                        className={`w-1.5 h-1.5 rounded-full mr-0.5 ${
                          i < point.difficulty ? 'bg-red-400' : 'bg-gray-200'
                        }`}
                      />
                    ))}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">难度: {point.difficulty}/10</div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* 学生详细列表 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <GraduationCap className="w-5 h-5" />
              <span>学生详细统计</span>
              <Badge variant="secondary">{students.length}</Badge>
            </CardTitle>
            <CardDescription>各学生的详细学习情况</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">学生信息</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">今日使用</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">本周使用</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">学习时长</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">练习情况</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">平均分</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">课程进度</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">活跃模块</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">最后登录</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student, index) => (
                    <motion.tr
                      key={student.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b hover:bg-gray-50"
                    >
                      <td className="py-4 px-4">
                        <div>
                          <p className="font-medium text-gray-900">{student.full_name}</p>
                          <p className="text-sm text-gray-500">{student.username}</p>
                          <p className="text-sm text-gray-500">{student.email}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <MessageSquare className="w-4 h-4 text-blue-500" />
                          <span className="font-medium">{student.ai_usage_today}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <TrendingUp className="w-4 h-4 text-green-500" />
                          <span className="font-medium">{student.ai_usage_week}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4 text-purple-500" />
                          <span className="font-medium">{student.total_study_time}h</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="text-sm">
                          <div className="flex items-center space-x-1">
                            <CheckCircle className="w-4 h-4 text-green-500" />
                            <span>{student.exercises_correct}/{student.exercises_completed}</span>
                          </div>
                          <div className="text-gray-500">
                            {((student.exercises_correct / student.exercises_completed) * 100).toFixed(1)}%
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <Award className="w-4 h-4 text-yellow-500" />
                          <span className="font-medium">{student.average_score}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="text-sm">
                          <div className="flex items-center space-x-1">
                            <BookOpen className="w-4 h-4 text-indigo-500" />
                            <span>{student.courses_completed}/{student.courses_enrolled}</span>
                          </div>
                          <div className="text-gray-500">
                            {((student.courses_completed / student.courses_enrolled) * 100).toFixed(1)}%
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex flex-wrap gap-1">
                          {student.active_modules.slice(0, 2).map((module, i) => (
                            <Badge key={i} variant="secondary" className="text-xs">
                              {module}
                            </Badge>
                          ))}
                          {student.active_modules.length > 2 && (
                            <Badge variant="outline" className="text-xs">
                              +{student.active_modules.length - 2}
                            </Badge>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <span className="text-sm text-gray-600">
                          {student.last_login ? formatDate(student.last_login) : '从未登录'}
                        </span>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
};

export default StudentStats;

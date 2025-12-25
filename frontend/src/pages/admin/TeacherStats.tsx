import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  UserCheck,
  BookOpen,
  Users,
  Clock,
  TrendingUp,
  Activity,
  MessageSquare,
  FileText,
  Award,
  Target
} from 'lucide-react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { adminAPI } from '@/services/api';

interface TeacherData {
  id: number;
  username: string;
  full_name: string;
  email: string;
  created_at: string;
  last_login: string;
  // 统计数据
  courses_created: number;
  students_taught: number;
  ai_usage_today: number;
  ai_usage_week: number;
  preparation_time: number;
  correction_time: number;
  active_modules: string[];
}

interface TeacherUsageStats {
  today_total: number;
  week_total: number;
  most_active_teacher: string;
  avg_preparation_time: number;
  avg_correction_time: number;
}

const TeacherStats = () => {
  const [teachers, setTeachers] = useState<TeacherData[]>([]);
  const [usageStats, setUsageStats] = useState<TeacherUsageStats>({
    today_total: 0,
    week_total: 0,
    most_active_teacher: '',
    avg_preparation_time: 0,
    avg_correction_time: 0
  });
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('today');

  useEffect(() => {
    fetchTeacherStats();
  }, [timeRange]);

  const fetchTeacherStats = async () => {
    try {
      setLoading(true);
      
      // 获取教师列表
      const teachersResponse = await adminAPI.getUsers({
        role: 'teacher',
        page: 1,
        size: 100
      });
      
      // 模拟教师统计数据（实际应该从API获取）
      const teacherData: TeacherData[] = teachersResponse.users
        .filter((user: any) => user.role === 'teacher')
        .map((teacher: any) => ({
          ...teacher,
          courses_created: Math.floor(Math.random() * 10) + 1,
          students_taught: Math.floor(Math.random() * 50) + 10,
          ai_usage_today: Math.floor(Math.random() * 20) + 1,
          ai_usage_week: Math.floor(Math.random() * 100) + 20,
          preparation_time: Math.random() * 3 + 1,
          correction_time: Math.random() * 2 + 0.5,
          active_modules: ['AI课程生成', '智能练习', '知识库管理'].slice(0, Math.floor(Math.random() * 3) + 1)
        }));

      setTeachers(teacherData);

      // 计算统计数据
      const stats: TeacherUsageStats = {
        today_total: teacherData.reduce((sum, t) => sum + t.ai_usage_today, 0),
        week_total: teacherData.reduce((sum, t) => sum + t.ai_usage_week, 0),
        most_active_teacher: teacherData.sort((a, b) => b.ai_usage_week - a.ai_usage_week)[0]?.full_name || '',
        avg_preparation_time: teacherData.reduce((sum, t) => sum + t.preparation_time, 0) / teacherData.length,
        avg_correction_time: teacherData.reduce((sum, t) => sum + t.correction_time, 0) / teacherData.length
      };

      setUsageStats(stats);

    } catch (error) {
      console.error('获取教师统计失败:', error);
      // 使用模拟数据
      setTeachers([
        {
          id: 1,
          username: 'teacher1',
          full_name: '李老师',
          email: 'teacher1@example.com',
          created_at: '2024-01-15T10:30:00Z',
          last_login: '2024-07-20T09:30:00Z',
          courses_created: 5,
          students_taught: 45,
          ai_usage_today: 12,
          ai_usage_week: 78,
          preparation_time: 2.5,
          correction_time: 1.8,
          active_modules: ['AI课程生成', '智能练习', '知识库管理']
        },
        {
          id: 2,
          username: 'teacher2',
          full_name: '王老师',
          email: 'teacher2@example.com',
          created_at: '2024-02-10T14:20:00Z',
          last_login: '2024-07-20T11:15:00Z',
          courses_created: 3,
          students_taught: 32,
          ai_usage_today: 8,
          ai_usage_week: 56,
          preparation_time: 3.2,
          correction_time: 2.1,
          active_modules: ['AI课程生成', '智能练习']
        }
      ]);

      setUsageStats({
        today_total: 20,
        week_total: 134,
        most_active_teacher: '李老师',
        avg_preparation_time: 2.85,
        avg_correction_time: 1.95
      });
    } finally {
      setLoading(false);
    }
  };

  // 使用趋势数据
  const usageTrendData = [
    { date: '07-14', usage: 15, teachers: 8 },
    { date: '07-15', usage: 22, teachers: 12 },
    { date: '07-16', usage: 18, teachers: 10 },
    { date: '07-17', usage: 25, teachers: 14 },
    { date: '07-18', usage: 30, teachers: 16 },
    { date: '07-19', usage: 28, teachers: 15 },
    { date: '07-20', usage: 20, teachers: 11 }
  ];

  // 活跃模块数据
  const moduleUsageData = [
    { name: 'AI课程生成', count: 28, percentage: 35 },
    { name: '智能练习', count: 35, percentage: 44 },
    { name: '知识库管理', count: 18, percentage: 23 },
    { name: '成绩分析', count: 12, percentage: 15 },
    { name: '课程优化', count: 8, percentage: 10 }
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
            <h1 className="text-3xl font-bold text-gray-900">教师使用统计</h1>
            <p className="text-gray-600 mt-2">教师使用次数统计与活跃板块分析</p>
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
                    <p className="text-green-600 text-sm">+15% vs 昨日</p>
                  </div>
                  <UserCheck className="w-8 h-8 text-blue-500" />
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
                    <p className="text-green-600 text-sm">+8% vs 上周</p>
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
                    <p className="text-sm font-medium text-gray-600">平均备课时间</p>
                    <p className="text-2xl font-bold text-gray-900">{usageStats.avg_preparation_time.toFixed(1)}h</p>
                    <p className="text-green-600 text-sm">-0.3h vs 上周</p>
                  </div>
                  <Clock className="w-8 h-8 text-purple-500" />
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
                    <p className="text-sm font-medium text-gray-600">活跃教师数</p>
                    <p className="text-2xl font-bold text-gray-900">{teachers.length}</p>
                    <p className="text-blue-600 text-sm">最活跃: {usageStats.most_active_teacher}</p>
                  </div>
                  <Award className="w-8 h-8 text-orange-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* 图表区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 使用趋势图 */}
          <Card>
            <CardHeader>
              <CardTitle>教师使用趋势</CardTitle>
              <CardDescription>每日使用次数和活跃教师数变化</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={usageTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="usage" stroke="#3B82F6" strokeWidth={2} name="使用次数" />
                  <Line type="monotone" dataKey="teachers" stroke="#10B981" strokeWidth={2} name="活跃教师" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* 活跃模块分布 */}
          <Card>
            <CardHeader>
              <CardTitle>活跃板块分布</CardTitle>
              <CardDescription>教师最常使用的功能模块</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={moduleUsageData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="count"
                  >
                    {moduleUsageData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="mt-4 grid grid-cols-2 gap-2">
                {moduleUsageData.map((item, index) => (
                  <div key={item.name} className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    ></div>
                    <span className="text-sm text-gray-600">{item.name}</span>
                    <span className="text-sm font-medium">{item.count}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 教师详细列表 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Users className="w-5 h-5" />
              <span>教师详细统计</span>
              <Badge variant="secondary">{teachers.length}</Badge>
            </CardTitle>
            <CardDescription>各教师的详细使用情况</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">教师信息</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">今日使用</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">本周使用</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">创建课程</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">教授学生</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">备课时间</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">活跃模块</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">最后登录</th>
                  </tr>
                </thead>
                <tbody>
                  {teachers.map((teacher, index) => (
                    <motion.tr
                      key={teacher.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b hover:bg-gray-50"
                    >
                      <td className="py-4 px-4">
                        <div>
                          <p className="font-medium text-gray-900">{teacher.full_name}</p>
                          <p className="text-sm text-gray-500">{teacher.username}</p>
                          <p className="text-sm text-gray-500">{teacher.email}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <MessageSquare className="w-4 h-4 text-blue-500" />
                          <span className="font-medium">{teacher.ai_usage_today}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <TrendingUp className="w-4 h-4 text-green-500" />
                          <span className="font-medium">{teacher.ai_usage_week}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <BookOpen className="w-4 h-4 text-purple-500" />
                          <span className="font-medium">{teacher.courses_created}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <Users className="w-4 h-4 text-orange-500" />
                          <span className="font-medium">{teacher.students_taught}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4 text-indigo-500" />
                          <span className="font-medium">{teacher.preparation_time.toFixed(1)}h</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex flex-wrap gap-1">
                          {teacher.active_modules.slice(0, 2).map((module, i) => (
                            <Badge key={i} variant="secondary" className="text-xs">
                              {module}
                            </Badge>
                          ))}
                          {teacher.active_modules.length > 2 && (
                            <Badge variant="outline" className="text-xs">
                              +{teacher.active_modules.length - 2}
                            </Badge>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <span className="text-sm text-gray-600">
                          {teacher.last_login ? formatDate(teacher.last_login) : '从未登录'}
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

export default TeacherStats;

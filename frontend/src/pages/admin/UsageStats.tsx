import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Activity,
  MessageSquare,
  TrendingUp,
  Users,
  Clock,
  BarChart3,
  Download,
  Calendar,
  Zap
} from 'lucide-react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

interface UserUsageStats {
  id: number;
  username: string;
  full_name: string;
  role: 'student' | 'teacher';
  total_messages: number;
  total_tokens: number;
  last_usage: string;
  daily_average: number;
}

interface UsageData {
  date: string;
  messages: number;
  tokens: number;
  users: number;
}

const UsageStats = () => {
  const [userStats, setUserStats] = useState<UserUsageStats[]>([]);
  const [usageData, setUsageData] = useState<UsageData[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d');
  const [sortBy, setSortBy] = useState('total_messages');

  useEffect(() => {
    fetchUsageStats();
  }, [timeRange]);

  const fetchUsageStats = async () => {
    try {
      setLoading(true);
      // const response = await adminAPI.getUsageStats(timeRange);
      
      // 模拟数据
      setUserStats([
        {
          id: 1,
          username: 'student001',
          full_name: '张同学',
          role: 'student',
          total_messages: 245,
          total_tokens: 12500,
          last_usage: '2024-07-20T10:30:00Z',
          daily_average: 35
        },
        {
          id: 2,
          username: 'teacher001',
          full_name: '李老师',
          role: 'teacher',
          total_messages: 189,
          total_tokens: 15600,
          last_usage: '2024-07-20T09:15:00Z',
          daily_average: 27
        },
        {
          id: 3,
          username: 'student002',
          full_name: '王同学',
          role: 'student',
          total_messages: 156,
          total_tokens: 8900,
          last_usage: '2024-07-19T16:45:00Z',
          daily_average: 22
        },
        {
          id: 4,
          username: 'teacher002',
          full_name: '赵老师',
          role: 'teacher',
          total_messages: 134,
          total_tokens: 11200,
          last_usage: '2024-07-20T08:20:00Z',
          daily_average: 19
        }
      ]);

      setUsageData([
        { date: '07-14', messages: 156, tokens: 8900, users: 23 },
        { date: '07-15', messages: 189, tokens: 11200, users: 28 },
        { date: '07-16', messages: 234, tokens: 13400, users: 31 },
        { date: '07-17', messages: 198, tokens: 10800, users: 26 },
        { date: '07-18', messages: 267, tokens: 15600, users: 34 },
        { date: '07-19', messages: 245, tokens: 14200, users: 29 },
        { date: '07-20', messages: 289, tokens: 16800, users: 37 }
      ]);
    } catch (error) {
      console.error('获取使用统计失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const sortedUserStats = [...userStats].sort((a, b) => {
    switch (sortBy) {
      case 'total_messages':
        return b.total_messages - a.total_messages;
      case 'total_tokens':
        return b.total_tokens - a.total_tokens;
      case 'daily_average':
        return b.daily_average - a.daily_average;
      default:
        return 0;
    }
  });

  const totalStats = {
    totalMessages: userStats.reduce((sum, user) => sum + user.total_messages, 0),
    totalTokens: userStats.reduce((sum, user) => sum + user.total_tokens, 0),
    activeUsers: userStats.length,
    averageDaily: Math.round(userStats.reduce((sum, user) => sum + user.daily_average, 0) / userStats.length)
  };

  const roleDistribution = [
    { name: '学生', value: userStats.filter(u => u.role === 'student').length, color: '#3B82F6' },
    { name: '教师', value: userStats.filter(u => u.role === 'teacher').length, color: '#10B981' }
  ];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getRoleBadge = (role: string) => {
    return role === 'student' ? (
      <Badge className="bg-blue-100 text-blue-800">学生</Badge>
    ) : (
      <Badge className="bg-green-100 text-green-800">教师</Badge>
    );
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
            <h1 className="text-3xl font-bold text-gray-900">AI使用统计</h1>
            <p className="text-gray-600 mt-2">查看用户AI助手使用情况和统计数据</p>
          </div>
          <div className="flex space-x-3">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="7d">最近7天</SelectItem>
                <SelectItem value="30d">最近30天</SelectItem>
                <SelectItem value="90d">最近90天</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>导出报告</span>
            </Button>
          </div>
        </div>

        {/* 总览统计 */}
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
                    <p className="text-sm font-medium text-gray-600">总消息数</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">
                      {totalStats.totalMessages.toLocaleString()}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
                    <MessageSquare className="w-6 h-6 text-white" />
                  </div>
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
                    <p className="text-sm font-medium text-gray-600">总Token数</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">
                      {totalStats.totalTokens.toLocaleString()}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
                    <Zap className="w-6 h-6 text-white" />
                  </div>
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
                    <p className="text-sm font-medium text-gray-600">活跃用户</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">
                      {totalStats.activeUsers}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                    <Users className="w-6 h-6 text-white" />
                  </div>
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
                    <p className="text-sm font-medium text-gray-600">日均使用</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">
                      {totalStats.averageDaily}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* 图表区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 使用趋势图 */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>使用趋势</CardTitle>
                <CardDescription>AI助手使用量随时间变化</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={usageData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="messages" stroke="#3B82F6" strokeWidth={2} name="消息数" />
                    <Line type="monotone" dataKey="users" stroke="#10B981" strokeWidth={2} name="用户数" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* 用户角色分布 */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>用户分布</CardTitle>
                <CardDescription>按角色统计活跃用户</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={roleDistribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {roleDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <div className="mt-4 space-y-2">
                  {roleDistribution.map((item, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div className={`w-3 h-3 rounded-full`} style={{ backgroundColor: item.color }}></div>
                        <span className="text-sm text-gray-600">{item.name}</span>
                      </div>
                      <span className="text-sm font-medium">{item.value}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* 用户使用排行 */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="w-5 h-5" />
                  <span>用户使用排行</span>
                </CardTitle>
                <CardDescription>按使用量排序的用户列表</CardDescription>
              </div>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-40">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="total_messages">按消息数排序</SelectItem>
                  <SelectItem value="total_tokens">按Token数排序</SelectItem>
                  <SelectItem value="daily_average">按日均使用排序</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">排名</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">用户</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">角色</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">消息数</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Token数</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">日均使用</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">最后使用</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedUserStats.map((user, index) => (
                    <motion.tr
                      key={user.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b hover:bg-gray-50"
                    >
                      <td className="py-4 px-4">
                        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 text-sm font-medium">
                          {index + 1}
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div>
                          <p className="font-medium text-gray-900">{user.full_name}</p>
                          <p className="text-sm text-gray-500">{user.username}</p>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        {getRoleBadge(user.role)}
                      </td>
                      <td className="py-4 px-4">
                        <span className="font-medium">{user.total_messages.toLocaleString()}</span>
                      </td>
                      <td className="py-4 px-4">
                        <span className="font-medium">{user.total_tokens.toLocaleString()}</span>
                      </td>
                      <td className="py-4 px-4">
                        <span className="font-medium">{user.daily_average}</span>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1 text-sm text-gray-600">
                          <Clock className="w-4 h-4" />
                          <span>{formatDate(user.last_usage)}</span>
                        </div>
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

export default UsageStats;

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Users,
  GraduationCap,
  UserCheck,
  Activity,
  TrendingUp,
  Clock,
  MessageSquare,
  BookOpen,
  BarChart3,
  AlertCircle
} from 'lucide-react';
import { motion } from 'framer-motion';
// import { adminAPI } from '@/services/api';

interface DashboardStats {
  totalUsers: number;
  totalStudents: number;
  totalTeachers: number;
  activeUsers: number;
  totalCourses: number;
  totalExercises: number;
  aiUsageToday: number;
  aiUsageThisMonth: number;
}

interface RecentActivity {
  id: number;
  type: string;
  user: string;
  action: string;
  timestamp: string;
}

const Dashboard = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalUsers: 0,
    totalStudents: 0,
    totalTeachers: 0,
    activeUsers: 0,
    totalCourses: 0,
    totalExercises: 0,
    aiUsageToday: 0,
    aiUsageThisMonth: 0
  });
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // 这里调用管理员API获取统计数据
      // const [statsData, activitiesData] = await Promise.all([
      //   adminAPI.getDashboardStats(),
      //   adminAPI.getRecentActivities()
      // ]);
      
      // 模拟数据
      setStats({
        totalUsers: 1247,
        totalStudents: 1089,
        totalTeachers: 158,
        activeUsers: 342,
        totalCourses: 89,
        totalExercises: 456,
        aiUsageToday: 1234,
        aiUsageThisMonth: 45678
      });

      setRecentActivities([
        {
          id: 1,
          type: 'user_register',
          user: '张同学',
          action: '注册了新账户',
          timestamp: '2分钟前'
        },
        {
          id: 2,
          type: 'course_create',
          user: '李老师',
          action: '创建了新课程《Python基础》',
          timestamp: '5分钟前'
        },
        {
          id: 3,
          type: 'ai_usage',
          user: '王同学',
          action: '使用了AI助手',
          timestamp: '8分钟前'
        },
        {
          id: 4,
          type: 'exercise_complete',
          user: '赵同学',
          action: '完成了练习《数据结构》',
          timestamp: '12分钟前'
        }
      ]);
    } catch (error) {
      console.error('获取仪表板数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: '总用户数',
      value: stats.totalUsers,
      icon: Users,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'positive'
    },
    {
      title: '学生数量',
      value: stats.totalStudents,
      icon: GraduationCap,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'positive'
    },
    {
      title: '教师数量',
      value: stats.totalTeachers,
      icon: UserCheck,
      color: 'bg-purple-500',
      change: '+15%',
      changeType: 'positive'
    },
    {
      title: '活跃用户',
      value: stats.activeUsers,
      icon: Activity,
      color: 'bg-orange-500',
      change: '+5%',
      changeType: 'positive'
    },
    {
      title: '课程总数',
      value: stats.totalCourses,
      icon: BookOpen,
      color: 'bg-indigo-500',
      change: '+3%',
      changeType: 'positive'
    },
    {
      title: '练习总数',
      value: stats.totalExercises,
      icon: BarChart3,
      color: 'bg-pink-500',
      change: '+7%',
      changeType: 'positive'
    },
    {
      title: '今日AI使用',
      value: stats.aiUsageToday,
      icon: MessageSquare,
      color: 'bg-cyan-500',
      change: '+25%',
      changeType: 'positive'
    },
    {
      title: '本月AI使用',
      value: stats.aiUsageThisMonth,
      icon: TrendingUp,
      color: 'bg-emerald-500',
      change: '+18%',
      changeType: 'positive'
    }
  ];

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'user_register':
        return <Users className="w-4 h-4 text-blue-500" />;
      case 'course_create':
        return <BookOpen className="w-4 h-4 text-green-500" />;
      case 'ai_usage':
        return <MessageSquare className="w-4 h-4 text-purple-500" />;
      case 'exercise_complete':
        return <BarChart3 className="w-4 h-4 text-orange-500" />;
      default:
        return <Activity className="w-4 h-4 text-gray-500" />;
    }
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
        <div>
          <h1 className="text-3xl font-bold text-gray-900">管理员仪表板</h1>
          <p className="text-gray-600 mt-2">系统概览和关键指标</p>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((card, index) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{card.title}</p>
                      <p className="text-2xl font-bold text-gray-900 mt-1">
                        {card.value.toLocaleString()}
                      </p>
                      <div className="flex items-center mt-2">
                        <Badge 
                          variant={card.changeType === 'positive' ? 'default' : 'destructive'}
                          className="text-xs"
                        >
                          {card.change}
                        </Badge>
                        <span className="text-xs text-gray-500 ml-2">vs 上月</span>
                      </div>
                    </div>
                    <div className={`w-12 h-12 ${card.color} rounded-lg flex items-center justify-center`}>
                      <card.icon className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* 内容区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 最近活动 */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Clock className="w-5 h-5" />
                  <span>最近活动</span>
                </CardTitle>
                <CardDescription>
                  系统最新的用户活动记录
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivities.map((activity) => (
                    <div key={activity.id} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50">
                      <div className="flex-shrink-0">
                        {getActivityIcon(activity.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900">
                          {activity.user}
                        </p>
                        <p className="text-sm text-gray-600">
                          {activity.action}
                        </p>
                      </div>
                      <div className="flex-shrink-0">
                        <span className="text-xs text-gray-500">{activity.timestamp}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* 系统状态 */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <AlertCircle className="w-5 h-5" />
                  <span>系统状态</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">数据库</span>
                    <Badge variant="default" className="bg-green-100 text-green-800">
                      正常
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">AI服务</span>
                    <Badge variant="default" className="bg-green-100 text-green-800">
                      正常
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">文件存储</span>
                    <Badge variant="default" className="bg-green-100 text-green-800">
                      正常
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">邮件服务</span>
                    <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                      维护中
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 快速操作 */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>快速操作</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 text-sm">
                    创建新用户
                  </button>
                  <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 text-sm">
                    系统备份
                  </button>
                  <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 text-sm">
                    查看日志
                  </button>
                  <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 text-sm">
                    性能监控
                  </button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default Dashboard;

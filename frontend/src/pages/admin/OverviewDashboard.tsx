import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
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
  AlertCircle,
  Target,
  Award,
  Brain,
  CheckCircle,
  XCircle,
  TrendingDown,
  Zap,
  Timer,
  FileText
} from 'lucide-react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';

interface TeacherUsageStats {
  today: number;
  thisWeek: number;
  activeModules: string[];
  preparationTime: number;
  correctionTime: number;
}

interface StudentUsageStats {
  today: number;
  thisWeek: number;
  activeModules: string[];
  averageAccuracy: number;
  knowledgePoints: { name: string; mastery: number }[];
  errorPoints: { name: string; count: number }[];
}

interface TeachingEfficiency {
  preparationTime: number;
  correctionTime: number;
  exerciseDesignTime: number;
  courseOptimization: { subject: string; passRate: number; trend: string }[];
}

const OverviewDashboard = () => {
  const [timeRange, setTimeRange] = useState('today');
  const [teacherStats, setTeacherStats] = useState<TeacherUsageStats>({
    today: 45,
    thisWeek: 312,
    activeModules: ['AI课程生成', '智能练习', '知识库管理'],
    preparationTime: 2.5,
    correctionTime: 1.8
  });

  const [studentStats, setStudentStats] = useState<StudentUsageStats>({
    today: 128,
    thisWeek: 856,
    activeModules: ['智能练习', 'AI助手', '课程学习'],
    averageAccuracy: 78.5,
    knowledgePoints: [
      { name: 'Python基础', mastery: 85 },
      { name: '数据结构', mastery: 72 },
      { name: '算法设计', mastery: 68 },
      { name: '数据库', mastery: 91 },
      { name: '网络编程', mastery: 76 }
    ],
    errorPoints: [
      { name: '指针操作', count: 45 },
      { name: '递归算法', count: 38 },
      { name: '数据库查询', count: 32 },
      { name: '异常处理', count: 28 },
      { name: '面向对象', count: 25 }
    ]
  });

  const [efficiency, setEfficiency] = useState<TeachingEfficiency>({
    preparationTime: 2.5,
    correctionTime: 1.8,
    exerciseDesignTime: 3.2,
    courseOptimization: [
      { subject: '高等数学', passRate: 65, trend: 'down' },
      { subject: '数据结构', passRate: 78, trend: 'up' },
      { subject: 'Python编程', passRate: 82, trend: 'up' },
      { subject: '数据库原理', passRate: 71, trend: 'stable' }
    ]
  });

  // 模拟数据
  const usageTrendData = [
    { date: '07-14', teachers: 35, students: 120 },
    { date: '07-15', teachers: 42, students: 145 },
    { date: '07-16', teachers: 38, students: 132 },
    { date: '07-17', teachers: 45, students: 156 },
    { date: '07-18', teachers: 52, students: 178 },
    { date: '07-19', teachers: 48, students: 165 },
    { date: '07-20', teachers: 45, students: 128 }
  ];

  const accuracyTrendData = [
    { week: '第1周', accuracy: 72 },
    { week: '第2周', accuracy: 75 },
    { week: '第3周', accuracy: 78 },
    { week: '第4周', accuracy: 76 },
    { week: '第5周', accuracy: 79 },
    { week: '第6周', accuracy: 81 },
    { week: '第7周', accuracy: 78 }
  ];

  const moduleUsageData = [
    { name: 'AI课程生成', teachers: 28, students: 0 },
    { name: '智能练习', teachers: 35, students: 89 },
    { name: 'AI助手', teachers: 22, students: 156 },
    { name: '知识库管理', teachers: 18, students: 0 },
    { name: '课程学习', teachers: 0, students: 134 },
    { name: '在线测试', teachers: 15, students: 78 }
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  return (
    <AdminLayout fullScreen>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-8">
        {/* 标题栏 */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">智慧教育平台 - 大屏概览</h1>
            <p className="text-blue-200">实时监控教学数据与学习效果</p>
          </div>
          <div className="flex items-center space-x-4">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-32 bg-white/10 border-white/20 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="today">今日</SelectItem>
                <SelectItem value="week">本周</SelectItem>
                <SelectItem value="month">本月</SelectItem>
              </SelectContent>
            </Select>
            <div className="text-right">
              <div className="text-sm text-blue-200">最后更新</div>
              <div className="text-lg font-mono">{new Date().toLocaleTimeString()}</div>
            </div>
          </div>
        </div>

        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-4 bg-white/10 mb-8">
            <TabsTrigger value="overview" className="text-white data-[state=active]:bg-white/20">总览</TabsTrigger>
            <TabsTrigger value="teachers" className="text-white data-[state=active]:bg-white/20">教师统计</TabsTrigger>
            <TabsTrigger value="students" className="text-white data-[state=active]:bg-white/20">学生统计</TabsTrigger>
            <TabsTrigger value="efficiency" className="text-white data-[state=active]:bg-white/20">教学效率</TabsTrigger>
          </TabsList>

          {/* 总览页面 */}
          <TabsContent value="overview" className="space-y-8">
            {/* 核心指标 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0 }}
              >
                <Card className="bg-white/10 backdrop-blur-md border-white/20">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-blue-200 text-sm">教师使用次数</p>
                        <p className="text-3xl font-bold text-white">{teacherStats.today}</p>
                        <p className="text-green-400 text-sm">今日活跃</p>
                      </div>
                      <UserCheck className="w-12 h-12 text-blue-400" />
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                <Card className="bg-white/10 backdrop-blur-md border-white/20">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-blue-200 text-sm">学生使用次数</p>
                        <p className="text-3xl font-bold text-white">{studentStats.today}</p>
                        <p className="text-green-400 text-sm">今日活跃</p>
                      </div>
                      <GraduationCap className="w-12 h-12 text-green-400" />
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <Card className="bg-white/10 backdrop-blur-md border-white/20">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-blue-200 text-sm">平均正确率</p>
                        <p className="text-3xl font-bold text-white">{studentStats.averageAccuracy}%</p>
                        <p className="text-yellow-400 text-sm">学习效果</p>
                      </div>
                      <Target className="w-12 h-12 text-yellow-400" />
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <Card className="bg-white/10 backdrop-blur-md border-white/20">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-blue-200 text-sm">备课效率</p>
                        <p className="text-3xl font-bold text-white">{efficiency.preparationTime}h</p>
                        <p className="text-purple-400 text-sm">平均耗时</p>
                      </div>
                      <Timer className="w-12 h-12 text-purple-400" />
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>

            {/* 使用趋势图 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">使用趋势</CardTitle>
                  <CardDescription className="text-blue-200">教师与学生活跃度对比</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={usageTrendData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="date" stroke="rgba(255,255,255,0.7)" />
                      <YAxis stroke="rgba(255,255,255,0.7)" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: 'rgba(0,0,0,0.8)', 
                          border: '1px solid rgba(255,255,255,0.2)',
                          borderRadius: '8px'
                        }}
                      />
                      <Area type="monotone" dataKey="students" stackId="1" stroke="#10B981" fill="#10B981" fillOpacity={0.6} />
                      <Area type="monotone" dataKey="teachers" stackId="1" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.6} />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">功能模块使用分布</CardTitle>
                  <CardDescription className="text-blue-200">各功能模块的使用情况</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={moduleUsageData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="name" stroke="rgba(255,255,255,0.7)" angle={-45} textAnchor="end" height={80} />
                      <YAxis stroke="rgba(255,255,255,0.7)" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: 'rgba(0,0,0,0.8)', 
                          border: '1px solid rgba(255,255,255,0.2)',
                          borderRadius: '8px'
                        }}
                      />
                      <Bar dataKey="teachers" fill="#3B82F6" name="教师" />
                      <Bar dataKey="students" fill="#10B981" name="学生" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 教师统计页面 */}
          <TabsContent value="teachers" className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* 教师活跃板块 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <Activity className="w-5 h-5" />
                    <span>活跃板块</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {teacherStats.activeModules.map((module, index) => (
                      <div key={module} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                        <span className="text-white">{module}</span>
                        <Badge className="bg-blue-500/20 text-blue-300">
                          {Math.floor(Math.random() * 20) + 10}次
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 备课效率 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <Clock className="w-5 h-5" />
                    <span>备课效率</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-blue-200">备课耗时</span>
                        <span className="text-white">{teacherStats.preparationTime}小时</span>
                      </div>
                      <div className="w-full bg-white/10 rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full" style={{ width: '60%' }}></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-blue-200">批改耗时</span>
                        <span className="text-white">{teacherStats.correctionTime}小时</span>
                      </div>
                      <div className="w-full bg-white/10 rounded-full h-2">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* 本周统计 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <BarChart3 className="w-5 h-5" />
                    <span>本周统计</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-white mb-2">{teacherStats.thisWeek}</div>
                    <div className="text-blue-200 text-sm">总使用次数</div>
                    <div className="mt-4 flex justify-center">
                      <div className="text-green-400 flex items-center">
                        <TrendingUp className="w-4 h-4 mr-1" />
                        <span className="text-sm">+15%</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 学生统计页面 */}
          <TabsContent value="students" className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* 学习效果趋势 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">平均正确率趋势</CardTitle>
                  <CardDescription className="text-blue-200">学生学习效果变化</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={accuracyTrendData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="week" stroke="rgba(255,255,255,0.7)" />
                      <YAxis stroke="rgba(255,255,255,0.7)" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: 'rgba(0,0,0,0.8)', 
                          border: '1px solid rgba(255,255,255,0.2)',
                          borderRadius: '8px'
                        }}
                      />
                      <Line type="monotone" dataKey="accuracy" stroke="#F59E0B" strokeWidth={3} dot={{ fill: '#F59E0B', strokeWidth: 2, r: 6 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* 知识点掌握情况 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">知识点掌握情况</CardTitle>
                  <CardDescription className="text-blue-200">各知识点的掌握程度</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {studentStats.knowledgePoints.map((point, index) => (
                      <div key={point.name} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-white">{point.name}</span>
                          <span className="text-blue-200">{point.mastery}%</span>
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${point.mastery}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* 高频错误知识点 */}
            <Card className="bg-white/10 backdrop-blur-md border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center space-x-2">
                  <XCircle className="w-5 h-5 text-red-400" />
                  <span>高频错误知识点</span>
                </CardTitle>
                <CardDescription className="text-blue-200">需要重点关注的薄弱环节</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                  {studentStats.errorPoints.map((point, index) => (
                    <div key={point.name} className="text-center p-4 bg-red-500/10 rounded-lg border border-red-500/20">
                      <div className="text-2xl font-bold text-red-400 mb-2">{point.count}</div>
                      <div className="text-white text-sm">{point.name}</div>
                      <div className="text-red-300 text-xs mt-1">错误次数</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* 教学效率页面 */}
          <TabsContent value="efficiency" className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* 课程优化方向 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <Brain className="w-5 h-5" />
                    <span>课程优化方向</span>
                  </CardTitle>
                  <CardDescription className="text-blue-200">各学科通过率分析</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {efficiency.courseOptimization.map((course, index) => (
                      <div key={course.subject} className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <span className="text-white font-medium">{course.subject}</span>
                          <Badge className={`${
                            course.passRate >= 80 ? 'bg-green-500/20 text-green-300' :
                            course.passRate >= 70 ? 'bg-yellow-500/20 text-yellow-300' :
                            'bg-red-500/20 text-red-300'
                          }`}>
                            {course.passRate}%
                          </Badge>
                        </div>
                        <div className="flex items-center space-x-2">
                          {course.trend === 'up' && <TrendingUp className="w-4 h-4 text-green-400" />}
                          {course.trend === 'down' && <TrendingDown className="w-4 h-4 text-red-400" />}
                          {course.trend === 'stable' && <div className="w-4 h-4 bg-gray-400 rounded-full"></div>}
                          <span className="text-blue-200 text-sm">
                            {course.trend === 'up' ? '上升' : course.trend === 'down' ? '下降' : '稳定'}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 教学效率指数 */}
              <Card className="bg-white/10 backdrop-blur-md border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <Zap className="w-5 h-5" />
                    <span>教学效率指数</span>
                  </CardTitle>
                  <CardDescription className="text-blue-200">各环节耗时分析</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="text-center">
                      <div className="text-6xl font-bold text-yellow-400 mb-2">85</div>
                      <div className="text-blue-200">综合效率分</div>
                      <div className="text-green-400 text-sm mt-2">较上周提升 +8%</div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span className="text-blue-200">备课耗时</span>
                        <span className="text-white">{efficiency.preparationTime}h</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-blue-200">批改耗时</span>
                        <span className="text-white">{efficiency.correctionTime}h</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-blue-200">练习设计</span>
                        <span className="text-white">{efficiency.exerciseDesignTime}h</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </AdminLayout>
  );
};

export default OverviewDashboard;

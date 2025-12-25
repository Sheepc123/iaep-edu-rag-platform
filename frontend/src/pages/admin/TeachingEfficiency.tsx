import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Clock,
  TrendingUp,
  TrendingDown,
  Target,
  Award,
  AlertTriangle,
  CheckCircle,
  Timer,
  BookOpen,
  Users,
  BarChart3
} from 'lucide-react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

interface EfficiencyMetrics {
  preparationTime: number;
  correctionTime: number;
  exerciseDesignTime: number;
  courseOptimizationTime: number;
  overallEfficiency: number;
}

interface SubjectAnalysis {
  subject: string;
  passRate: number;
  trend: 'up' | 'down' | 'stable';
  avgScore: number;
  completionRate: number;
  difficultyLevel: number;
  improvementSuggestions: string[];
}

const TeachingEfficiency = () => {
  const [timeRange, setTimeRange] = useState('month');
  const [selectedSubject, setSelectedSubject] = useState('all');
  
  const [metrics, setMetrics] = useState<EfficiencyMetrics>({
    preparationTime: 2.5,
    correctionTime: 1.8,
    exerciseDesignTime: 3.2,
    courseOptimizationTime: 1.5,
    overallEfficiency: 85
  });

  const [subjectAnalysis, setSubjectAnalysis] = useState<SubjectAnalysis[]>([
    {
      subject: '高等数学',
      passRate: 65,
      trend: 'down',
      avgScore: 72.5,
      completionRate: 78,
      difficultyLevel: 8,
      improvementSuggestions: ['增加基础练习', '优化教学方法', '加强课后辅导']
    },
    {
      subject: 'Python编程',
      passRate: 82,
      trend: 'up',
      avgScore: 85.3,
      completionRate: 91,
      difficultyLevel: 6,
      improvementSuggestions: ['增加实践项目', '优化代码规范教学']
    },
    {
      subject: '数据结构',
      passRate: 78,
      trend: 'up',
      avgScore: 79.8,
      completionRate: 85,
      difficultyLevel: 7,
      improvementSuggestions: ['可视化教学', '增加算法练习']
    },
    {
      subject: '数据库原理',
      passRate: 71,
      trend: 'stable',
      avgScore: 76.2,
      completionRate: 82,
      difficultyLevel: 7,
      improvementSuggestions: ['实际案例教学', '增加SQL练习']
    }
  ]);

  // 效率趋势数据
  const efficiencyTrendData = [
    { month: '1月', preparation: 3.2, correction: 2.1, design: 3.8, optimization: 1.8 },
    { month: '2月', preparation: 3.0, correction: 2.0, design: 3.5, optimization: 1.7 },
    { month: '3月', preparation: 2.8, correction: 1.9, design: 3.3, optimization: 1.6 },
    { month: '4月', preparation: 2.6, correction: 1.8, design: 3.1, optimization: 1.5 },
    { month: '5月', preparation: 2.5, correction: 1.8, design: 3.2, optimization: 1.5 },
    { month: '6月', preparation: 2.4, correction: 1.7, design: 3.0, optimization: 1.4 }
  ];

  // 学科通过率对比
  const passRateComparisonData = subjectAnalysis.map(subject => ({
    name: subject.subject,
    passRate: subject.passRate,
    avgScore: subject.avgScore,
    completionRate: subject.completionRate
  }));

  // 雷达图数据
  const radarData = [
    { subject: '备课效率', A: 85, B: 90, fullMark: 100 },
    { subject: '批改效率', A: 88, B: 85, fullMark: 100 },
    { subject: '课程设计', A: 82, B: 88, fullMark: 100 },
    { subject: '学生反馈', A: 90, B: 92, fullMark: 100 },
    { subject: '知识传授', A: 87, B: 89, fullMark: 100 },
    { subject: '互动质量', A: 83, B: 86, fullMark: 100 }
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <div className="w-4 h-4 bg-gray-400 rounded-full"></div>;
    }
  };

  const getPassRateColor = (rate: number) => {
    if (rate >= 80) return 'text-green-600 bg-green-100';
    if (rate >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <AdminLayout>
      <div className="space-y-8">
        {/* 页面标题 */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">教学效率分析</h1>
            <p className="text-gray-600 mt-2">分析教学各环节效率与课程优化方向</p>
          </div>
          <div className="flex space-x-3">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="week">本周</SelectItem>
                <SelectItem value="month">本月</SelectItem>
                <SelectItem value="quarter">本季度</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedSubject} onValueChange={setSelectedSubject}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">所有学科</SelectItem>
                {subjectAnalysis.map(subject => (
                  <SelectItem key={subject.subject} value={subject.subject}>
                    {subject.subject}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* 效率指标卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">备课耗时</p>
                    <p className="text-2xl font-bold text-gray-900">{metrics.preparationTime}h</p>
                    <p className="text-green-600 text-sm">-0.3h vs 上月</p>
                  </div>
                  <BookOpen className="w-8 h-8 text-blue-500" />
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
                    <p className="text-sm font-medium text-gray-600">批改耗时</p>
                    <p className="text-2xl font-bold text-gray-900">{metrics.correctionTime}h</p>
                    <p className="text-green-600 text-sm">-0.2h vs 上月</p>
                  </div>
                  <CheckCircle className="w-8 h-8 text-green-500" />
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
                    <p className="text-sm font-medium text-gray-600">练习设计</p>
                    <p className="text-2xl font-bold text-gray-900">{metrics.exerciseDesignTime}h</p>
                    <p className="text-red-600 text-sm">+0.1h vs 上月</p>
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
                    <p className="text-sm font-medium text-gray-600">课程优化</p>
                    <p className="text-2xl font-bold text-gray-900">{metrics.courseOptimizationTime}h</p>
                    <p className="text-green-600 text-sm">-0.1h vs 上月</p>
                  </div>
                  <Timer className="w-8 h-8 text-orange-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">综合效率</p>
                    <p className="text-2xl font-bold text-gray-900">{metrics.overallEfficiency}</p>
                    <p className="text-green-600 text-sm">+5 vs 上月</p>
                  </div>
                  <Award className="w-8 h-8 text-yellow-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* 图表区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 效率趋势图 */}
          <Card>
            <CardHeader>
              <CardTitle>教学效率趋势</CardTitle>
              <CardDescription>各环节耗时变化趋势</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={efficiencyTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="preparation" stroke="#3B82F6" strokeWidth={2} name="备课" />
                  <Line type="monotone" dataKey="correction" stroke="#10B981" strokeWidth={2} name="批改" />
                  <Line type="monotone" dataKey="design" stroke="#F59E0B" strokeWidth={2} name="设计" />
                  <Line type="monotone" dataKey="optimization" stroke="#EF4444" strokeWidth={2} name="优化" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* 教学质量雷达图 */}
          <Card>
            <CardHeader>
              <CardTitle>教学质量评估</CardTitle>
              <CardDescription>多维度教学质量分析</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name="当前" dataKey="A" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
                  <Radar name="目标" dataKey="B" stroke="#10B981" fill="#10B981" fillOpacity={0.3} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* 学科通过率分析 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5" />
              <span>学科通过率分析</span>
            </CardTitle>
            <CardDescription>各学科通过率对比与优化建议</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* 通过率对比图 */}
              <div className="lg:col-span-2">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={passRateComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="passRate" fill="#3B82F6" name="通过率%" />
                    <Bar dataKey="avgScore" fill="#10B981" name="平均分" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* 学科详情列表 */}
              <div className="space-y-4">
                {subjectAnalysis.map((subject, index) => (
                  <motion.div
                    key={subject.subject}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{subject.subject}</h4>
                      {getTrendIcon(subject.trend)}
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">通过率:</span>
                        <Badge className={getPassRateColor(subject.passRate)}>
                          {subject.passRate}%
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">平均分:</span>
                        <span className="font-medium">{subject.avgScore}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">完成率:</span>
                        <span className="font-medium">{subject.completionRate}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">难度:</span>
                        <div className="flex">
                          {Array.from({ length: 10 }, (_, i) => (
                            <div
                              key={i}
                              className={`w-2 h-2 rounded-full mr-1 ${
                                i < subject.difficultyLevel ? 'bg-red-400' : 'bg-gray-200'
                              }`}
                            />
                          ))}
                        </div>
                      </div>
                    </div>

                    {subject.passRate < 75 && (
                      <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded">
                        <div className="flex items-center space-x-1 mb-1">
                          <AlertTriangle className="w-4 h-4 text-yellow-600" />
                          <span className="text-xs font-medium text-yellow-800">优化建议</span>
                        </div>
                        <ul className="text-xs text-yellow-700 space-y-1">
                          {subject.improvementSuggestions.map((suggestion, i) => (
                            <li key={i}>• {suggestion}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
};

export default TeachingEfficiency;

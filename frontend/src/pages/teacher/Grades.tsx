import React, { useState, useEffect } from "react";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/components/ui/use-toast";
import {
  BarChart3,
  TrendingUp,
  Users,
  BookOpen,
  Award,
  FileText,
  Download,
  Eye,
  Calendar,
  Target
} from "lucide-react";
import { GradeOverviewCards } from "@/components/grade-analysis/GradeOverviewCards";
import { GradeTrendsChart } from "@/components/grade-analysis/GradeTrendsChart";
import { SubjectAnalysisChart } from "@/components/grade-analysis/SubjectAnalysisChart";
import { RecentActivitiesList } from "@/components/grade-analysis/RecentActivitiesList";
import { ExerciseGradesList } from "@/components/grade-analysis/ExerciseGradesList";

interface GradeStats {
  average_score: number;
  average_percentage: number;
  total_students: number;
  total_exercises: number;
  total_attempts: number;
}

interface TrendData {
  date: string;
  average_score: number;
  attempt_count: number;
  pass_rate: number;
}

interface SubjectAnalysis {
  subject: string;
  average_score: number;
  attempt_count: number;
  pass_rate: number;
  excellent_rate: number;
}

interface RecentActivity {
  type: string;
  student_name: string;
  exercise_title: string;
  score: number;
  percentage: number;
  submitted_at: string;
}

interface TeacherGradeOverview {
  grade_stats: GradeStats;
  trend_data: TrendData[];
  subject_analysis: SubjectAnalysis[];
  recent_activities: RecentActivity[];
}

export const TeacherGrades: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [overviewData, setOverviewData] = useState<TeacherGradeOverview | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState("30");
  const { toast } = useToast();

  useEffect(() => {
    fetchGradeOverview();
  }, [selectedPeriod]);

  const fetchGradeOverview = async () => {
    try {
      setLoading(true);
      // TODO: 实现API调用
      // const response = await gradeAnalysisAPI.getTeacherOverview(parseInt(selectedPeriod));
      // setOverviewData(response);

      // 模拟数据
      const mockData: TeacherGradeOverview = {
        grade_stats: {
          average_score: 78.5,
          average_percentage: 78.5,
          total_students: 156,
          total_exercises: 12,
          total_attempts: 1248
        },
        trend_data: [
          { date: "2024-01-01", average_score: 75.2, attempt_count: 45, pass_rate: 82.2 },
          { date: "2024-01-02", average_score: 78.1, attempt_count: 52, pass_rate: 84.6 },
          { date: "2024-01-03", average_score: 76.8, attempt_count: 48, pass_rate: 83.3 },
          { date: "2024-01-04", average_score: 80.2, attempt_count: 55, pass_rate: 87.3 },
          { date: "2024-01-05", average_score: 79.5, attempt_count: 51, pass_rate: 86.3 }
        ],
        subject_analysis: [
          { subject: "数学", average_score: 82.3, attempt_count: 456, pass_rate: 89.5, excellent_rate: 34.2 },
          { subject: "计算机", average_score: 78.9, attempt_count: 398, pass_rate: 85.2, excellent_rate: 28.6 },
          { subject: "英语", average_score: 74.2, attempt_count: 394, pass_rate: 78.9, excellent_rate: 22.1 }
        ],
        recent_activities: [
          { type: "exercise_completed", student_name: "张三", exercise_title: "高等数学练习1", score: 85, percentage: 85, submitted_at: "2024-01-05T10:30:00Z" },
          { type: "exercise_completed", student_name: "李四", exercise_title: "计算机基础", score: 92, percentage: 92, submitted_at: "2024-01-05T09:15:00Z" },
          { type: "exercise_completed", student_name: "王五", exercise_title: "英语语法", score: 78, percentage: 78, submitted_at: "2024-01-05T08:45:00Z" }
        ]
      };
      setOverviewData(mockData);
    } catch (error) {
      console.error('获取成绩概览失败:', error);
      toast({
        title: "加载失败",
        description: "无法获取成绩数据，请稍后重试",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
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

  return (
    <TeacherLayout>
      <div className="space-y-6">
        {/* 页面标题和操作 */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">成绩分析</h1>
            <p className="text-gray-600 mt-1">查看学生成绩表现和学习分析</p>
          </div>
          <div className="flex items-center space-x-3">
            <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="7">最近7天</SelectItem>
                <SelectItem value="30">最近30天</SelectItem>
                <SelectItem value="90">最近90天</SelectItem>
                <SelectItem value="365">最近一年</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              导出报告
            </Button>
          </div>
        </div>

        {/* 概览卡片 */}
        {overviewData && (
          <GradeOverviewCards gradeStats={overviewData.grade_stats} />
        )}

        {/* 主要内容区域 */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview" className="flex items-center">
              <BarChart3 className="h-4 w-4 mr-2" />
              总体概览
            </TabsTrigger>
            <TabsTrigger value="trends" className="flex items-center">
              <TrendingUp className="h-4 w-4 mr-2" />
              趋势分析
            </TabsTrigger>
            <TabsTrigger value="subjects" className="flex items-center">
              <BookOpen className="h-4 w-4 mr-2" />
              科目分析
            </TabsTrigger>
            <TabsTrigger value="exercises" className="flex items-center">
              <FileText className="h-4 w-4 mr-2" />
              练习详情
            </TabsTrigger>
          </TabsList>

          {/* 总体概览 */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 成绩趋势图 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="h-5 w-5 mr-2" />
                    成绩趋势
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {overviewData && (
                    <GradeTrendsChart data={overviewData.trend_data} />
                  )}
                </CardContent>
              </Card>

              {/* 科目表现 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="h-5 w-5 mr-2" />
                    科目表现
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {overviewData && (
                    <SubjectAnalysisChart data={overviewData.subject_analysis} />
                  )}
                </CardContent>
              </Card>
            </div>

            {/* 最近活动 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="h-5 w-5 mr-2" />
                  最近活动
                </CardTitle>
              </CardHeader>
              <CardContent>
                {overviewData && (
                  <RecentActivitiesList activities={overviewData.recent_activities} />
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* 趋势分析 */}
          <TabsContent value="trends" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>详细趋势分析</CardTitle>
                <p className="text-sm text-gray-600">
                  查看学生成绩在时间维度上的变化趋势
                </p>
              </CardHeader>
              <CardContent>
                {overviewData && (
                  <div className="space-y-6">
                    <GradeTrendsChart
                      data={overviewData.trend_data}
                      showDetails={true}
                    />

                    {/* 趋势统计 */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">
                          {overviewData.trend_data.length}
                        </div>
                        <div className="text-sm text-gray-600">活跃天数</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">
                          {overviewData.trend_data.reduce((sum, item) => sum + item.attempt_count, 0)}
                        </div>
                        <div className="text-sm text-gray-600">总练习次数</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">
                          {(overviewData.trend_data.reduce((sum, item) => sum + item.pass_rate, 0) / overviewData.trend_data.length).toFixed(1)}%
                        </div>
                        <div className="text-sm text-gray-600">平均及格率</div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* 科目分析 */}
          <TabsContent value="subjects" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 科目对比图 */}
              <Card>
                <CardHeader>
                  <CardTitle>科目成绩对比</CardTitle>
                </CardHeader>
                <CardContent>
                  {overviewData && (
                    <SubjectAnalysisChart
                      data={overviewData.subject_analysis}
                      showDetails={true}
                    />
                  )}
                </CardContent>
              </Card>

              {/* 科目详细统计 */}
              <Card>
                <CardHeader>
                  <CardTitle>科目详细数据</CardTitle>
                </CardHeader>
                <CardContent>
                  {overviewData && (
                    <div className="space-y-4">
                      {overviewData.subject_analysis.map((subject, index) => (
                        <div key={index} className="p-4 border rounded-lg">
                          <div className="flex justify-between items-center mb-2">
                            <h4 className="font-medium">{subject.subject}</h4>
                            <Badge variant="secondary">
                              {subject.attempt_count} 次练习
                            </Badge>
                          </div>
                          <div className="grid grid-cols-3 gap-4 text-sm">
                            <div>
                              <div className="text-gray-600">平均分</div>
                              <div className="font-medium">{subject.average_score.toFixed(1)}</div>
                            </div>
                            <div>
                              <div className="text-gray-600">及格率</div>
                              <div className="font-medium">{subject.pass_rate.toFixed(1)}%</div>
                            </div>
                            <div>
                              <div className="text-gray-600">优秀率</div>
                              <div className="font-medium">{subject.excellent_rate.toFixed(1)}%</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 练习详情 */}
          <TabsContent value="exercises" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <FileText className="h-5 w-5 mr-2" />
                    练习成绩详情
                  </span>
                  <Button variant="outline" size="sm">
                    <Eye className="h-4 w-4 mr-2" />
                    查看全部
                  </Button>
                </CardTitle>
                <p className="text-sm text-gray-600">
                  点击练习可查看详细的成绩分析报告
                </p>
              </CardHeader>
              <CardContent>
                <ExerciseGradesList />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </TeacherLayout>
  );
};

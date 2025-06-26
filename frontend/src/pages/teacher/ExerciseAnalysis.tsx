import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { 
  ArrowLeft,
  Download,
  Share2,
  BarChart3,
  Users,
  Clock,
  Target,
  TrendingUp,
  FileText,
  AlertCircle,
  CheckCircle
} from "lucide-react";
import { DetailedAnalysisCharts } from "@/components/grade-analysis/DetailedAnalysisCharts";

interface ExerciseInfo {
  id: number;
  title: string;
  subject: string;
  category: string;
  difficulty: string;
  total_questions: number;
  created_at: string;
}

interface BasicStats {
  total_attempts: number;
  average_score: number;
  median_score: number;
  highest_score: number;
  lowest_score: number;
  average_percentage: number;
  standard_deviation: number;
}

interface ScoreDistribution {
  grade_distribution: {
    excellent: number;
    good: number;
    fair: number;
    poor: number;
    fail: number;
  };
  score_ranges: Array<{
    range: string;
    count: number;
    percentage: number;
  }>;
  pass_rate: number;
}

interface QuestionAnalysis {
  question_id: number;
  question_content: string;
  question_type: string;
  difficulty: string;
  accuracy_rate: number;
  total_attempts: number;
  average_time: number;
  common_mistakes: Array<{
    answer: string;
    count: number;
  }>;
}

interface StudentPerformance {
  student_id: number;
  student_name: string;
  username: string;
  score: number;
  percentage: number;
  time_spent: number;
  rank: number;
  vs_class_average: number;
  performance_level: string;
  completed_at: string;
}

interface TeachingRecommendation {
  type: string;
  title: string;
  suggestion: string;
}

interface AnalysisData {
  exercise_info: ExerciseInfo;
  basic_stats: BasicStats;
  score_distribution: ScoreDistribution;
  question_analysis: QuestionAnalysis[];
  student_performance: StudentPerformance[];
  recommendations: TeachingRecommendation[];
}

export const ExerciseAnalysis: React.FC = () => {
  const { exerciseId } = useParams<{ exerciseId: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [loading, setLoading] = useState(true);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);

  useEffect(() => {
    if (exerciseId) {
      fetchAnalysisData(parseInt(exerciseId));
    }
  }, [exerciseId]);

  const fetchAnalysisData = async (id: number) => {
    try {
      setLoading(true);
      // TODO: 实现API调用
      // const response = await gradeAnalysisAPI.getExerciseAnalysis(id);
      // setAnalysisData(response);
      
      // 模拟数据
      const mockData: AnalysisData = {
        exercise_info: {
          id: id,
          title: "高等数学基础练习",
          subject: "数学",
          category: "自主练习",
          difficulty: "medium",
          total_questions: 10,
          created_at: "2024-01-01T10:00:00Z"
        },
        basic_stats: {
          total_attempts: 45,
          average_score: 78.5,
          median_score: 80.0,
          highest_score: 95.0,
          lowest_score: 45.0,
          average_percentage: 78.5,
          standard_deviation: 12.3
        },
        score_distribution: {
          grade_distribution: {
            excellent: 8,
            good: 15,
            fair: 12,
            poor: 7,
            fail: 3
          },
          score_ranges: [
            { range: "90-100", count: 8, percentage: 17.8 },
            { range: "80-89", count: 15, percentage: 33.3 },
            { range: "70-79", count: 12, percentage: 26.7 },
            { range: "60-69", count: 7, percentage: 15.6 },
            { range: "0-59", count: 3, percentage: 6.7 }
          ],
          pass_rate: 93.3
        },
        question_analysis: [
          {
            question_id: 1,
            question_content: "函数f(x)=x²在x=2处的极限值是？",
            question_type: "multiple_choice",
            difficulty: "easy",
            accuracy_rate: 85.7,
            total_attempts: 45,
            average_time: 45,
            common_mistakes: [
              { answer: "2", count: 4 },
              { answer: "8", count: 2 }
            ]
          },
          {
            question_id: 2,
            question_content: "当x趋向于0时，sin(x)/x的极限值是____。",
            question_type: "fill_blank",
            difficulty: "medium",
            accuracy_rate: 72.3,
            total_attempts: 45,
            average_time: 68,
            common_mistakes: [
              { answer: "0", count: 8 },
              { answer: "∞", count: 4 }
            ]
          }
        ],
        student_performance: [
          {
            student_id: 1,
            student_name: "张三",
            username: "student001",
            score: 95,
            percentage: 95,
            time_spent: 1200,
            rank: 1,
            vs_class_average: 16.5,
            performance_level: "优秀",
            completed_at: "2024-01-05T10:30:00Z"
          },
          {
            student_id: 2,
            student_name: "李四",
            username: "student002",
            score: 88,
            percentage: 88,
            time_spent: 1350,
            rank: 2,
            vs_class_average: 9.5,
            performance_level: "良好",
            completed_at: "2024-01-05T11:15:00Z"
          }
        ],
        recommendations: [
          {
            type: "overall_performance",
            title: "整体表现良好",
            suggestion: "学生整体掌握情况较好，可以适当增加练习难度。"
          },
          {
            type: "difficult_questions",
            title: "发现1道难题",
            suggestion: "建议针对填空题进行专门讲解，分析常见错误原因。"
          }
        ]
      };
      setAnalysisData(mockData);
    } catch (error) {
      console.error('获取分析数据失败:', error);
      toast({
        title: "加载失败",
        description: "无法获取练习分析数据，请稍后重试",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExportReport = () => {
    // TODO: 实现报告导出功能
    toast({
      title: "导出成功",
      description: "分析报告已导出到下载文件夹",
    });
  };

  const handleShareReport = () => {
    // TODO: 实现报告分享功能
    toast({
      title: "分享链接已复制",
      description: "可以将链接分享给其他教师查看",
    });
  };

  if (loading) {
    return (
      <TeacherLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">加载分析数据中...</p>
          </div>
        </div>
      </TeacherLayout>
    );
  }

  if (!analysisData) {
    return (
      <TeacherLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">数据加载失败</h3>
            <p className="text-gray-600 mb-4">无法获取练习分析数据</p>
            <Button onClick={() => navigate(-1)}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              返回
            </Button>
          </div>
        </div>
      </TeacherLayout>
    );
  }

  return (
    <TeacherLayout>
      <div className="space-y-6">
        {/* 页面标题和操作 */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => navigate(-1)}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              返回
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {analysisData.exercise_info.title}
              </h1>
              <div className="flex items-center space-x-2 mt-1">
                <Badge variant="secondary">{analysisData.exercise_info.subject}</Badge>
                <Badge variant="outline">{analysisData.exercise_info.category}</Badge>
                <Badge variant="outline">{analysisData.exercise_info.difficulty}</Badge>
                <span className="text-sm text-gray-500">
                  {analysisData.exercise_info.total_questions} 道题目
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Button variant="outline" size="sm" onClick={handleShareReport}>
              <Share2 className="h-4 w-4 mr-2" />
              分享
            </Button>
            <Button variant="outline" size="sm" onClick={handleExportReport}>
              <Download className="h-4 w-4 mr-2" />
              导出报告
            </Button>
          </div>
        </div>

        {/* 基础统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">参与人数</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analysisData.basic_stats.total_attempts}</div>
              <p className="text-xs text-muted-foreground">
                完成练习的学生数量
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">平均分</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analysisData.basic_stats.average_score.toFixed(1)}</div>
              <p className="text-xs text-muted-foreground">
                得分率 {analysisData.basic_stats.average_percentage.toFixed(1)}%
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">及格率</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analysisData.score_distribution.pass_rate.toFixed(1)}%</div>
              <p className="text-xs text-muted-foreground">
                {analysisData.basic_stats.total_attempts - analysisData.score_distribution.grade_distribution.fail} 人及格
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">最高分</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analysisData.basic_stats.highest_score.toFixed(1)}</div>
              <p className="text-xs text-muted-foreground">
                最低分 {analysisData.basic_stats.lowest_score.toFixed(1)}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* 详细分析内容 */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">总体分析</TabsTrigger>
            <TabsTrigger value="questions">题目分析</TabsTrigger>
            <TabsTrigger value="students">学生表现</TabsTrigger>
            <TabsTrigger value="recommendations">教学建议</TabsTrigger>
          </TabsList>

          {/* 总体分析 */}
          <TabsContent value="overview" className="space-y-6">
            <DetailedAnalysisCharts
              scoreDistribution={analysisData.score_distribution}
              questionAnalysis={analysisData.question_analysis}
              studentPerformance={analysisData.student_performance}
            />
          </TabsContent>

          {/* 题目分析 */}
          <TabsContent value="questions" className="space-y-6">
            <div className="grid gap-6">
              {analysisData.question_analysis.map((question, index) => (
                <Card key={question.question_id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="space-y-2">
                        <CardTitle className="text-lg">题目 {index + 1}</CardTitle>
                        <p className="text-sm text-gray-600">{question.question_content}</p>
                        <div className="flex items-center space-x-2">
                          <Badge variant="secondary">{question.question_type}</Badge>
                          <Badge variant="outline">{question.difficulty}</Badge>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-gray-900">
                          {question.accuracy_rate.toFixed(1)}%
                        </div>
                        <div className="text-sm text-gray-500">正确率</div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <div className="text-sm text-gray-600 mb-1">答题统计</div>
                        <div className="space-y-1">
                          <div className="flex justify-between">
                            <span className="text-sm">总尝试次数</span>
                            <span className="font-medium">{question.total_attempts}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm">平均用时</span>
                            <span className="font-medium">{Math.round(question.average_time)}秒</span>
                          </div>
                        </div>
                      </div>

                      <div>
                        <div className="text-sm text-gray-600 mb-1">常见错误</div>
                        <div className="space-y-1">
                          {question.common_mistakes.slice(0, 2).map((mistake, idx) => (
                            <div key={idx} className="flex justify-between">
                              <span className="text-sm truncate">{mistake.answer}</span>
                              <span className="font-medium">{mistake.count}次</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <div className="text-sm text-gray-600 mb-1">难度评估</div>
                        <div className="space-y-1">
                          <div className={`text-sm font-medium ${
                            question.accuracy_rate >= 80 ? 'text-green-600' :
                            question.accuracy_rate >= 60 ? 'text-yellow-600' : 'text-red-600'
                          }`}>
                            {question.accuracy_rate >= 80 ? '简单' :
                             question.accuracy_rate >= 60 ? '中等' : '困难'}
                          </div>
                          <div className="text-xs text-gray-500">
                            基于正确率评估
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* 学生表现 */}
          <TabsContent value="students" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>学生成绩排名</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analysisData.student_performance.map((student, index) => (
                    <div key={student.student_id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center justify-center w-8 h-8 bg-gray-100 rounded-full">
                          <span className="text-sm font-medium">{student.rank}</span>
                        </div>
                        <div>
                          <div className="font-medium">{student.student_name}</div>
                          <div className="text-sm text-gray-500">@{student.username}</div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-6">
                        <div className="text-right">
                          <div className="font-medium">{student.score.toFixed(1)}分</div>
                          <div className="text-sm text-gray-500">{student.percentage.toFixed(1)}%</div>
                        </div>

                        <div className="text-right">
                          <div className="text-sm text-gray-600">用时</div>
                          <div className="font-medium">{Math.round(student.time_spent / 60)}分钟</div>
                        </div>

                        <Badge variant="secondary" className={
                          student.performance_level === "优秀" ? "bg-green-100 text-green-800" :
                          student.performance_level === "良好" ? "bg-blue-100 text-blue-800" :
                          student.performance_level === "中等" ? "bg-yellow-100 text-yellow-800" :
                          "bg-red-100 text-red-800"
                        }>
                          {student.performance_level}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* 教学建议 */}
          <TabsContent value="recommendations" className="space-y-6">
            <div className="grid gap-4">
              {analysisData.recommendations.map((recommendation, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <CheckCircle className="h-5 w-5 mr-2 text-green-500" />
                      {recommendation.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-700">{recommendation.suggestion}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </TeacherLayout>
  );
};

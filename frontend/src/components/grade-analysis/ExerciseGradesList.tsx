import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  Eye, 
  BarChart3, 
  Users, 
  Clock,
  Target,
  TrendingUp,
  FileText,
  Calendar
} from "lucide-react";

interface ExerciseGrade {
  id: number;
  title: string;
  subject: string;
  category: string;
  difficulty: string;
  total_attempts: number;
  completed_attempts: number;
  average_score: number;
  average_percentage: number;
  pass_rate: number;
  created_at: string;
  last_attempt_at: string;
}

export const ExerciseGradesList: React.FC = () => {
  const [exercises] = useState<ExerciseGrade[]>([
    {
      id: 1,
      title: "高等数学基础练习",
      subject: "数学",
      category: "自主练习",
      difficulty: "medium",
      total_attempts: 45,
      completed_attempts: 42,
      average_score: 78.5,
      average_percentage: 78.5,
      pass_rate: 85.7,
      created_at: "2024-01-01T10:00:00Z",
      last_attempt_at: "2024-01-05T15:30:00Z"
    },
    {
      id: 2,
      title: "线性代数矩阵运算",
      subject: "数学",
      category: "课后作业",
      difficulty: "hard",
      total_attempts: 38,
      completed_attempts: 35,
      average_score: 72.3,
      average_percentage: 72.3,
      pass_rate: 77.1,
      created_at: "2024-01-02T14:00:00Z",
      last_attempt_at: "2024-01-05T12:15:00Z"
    },
    {
      id: 3,
      title: "概率论基础概念",
      subject: "数学",
      category: "模拟考试",
      difficulty: "medium",
      total_attempts: 52,
      completed_attempts: 48,
      average_score: 82.1,
      average_percentage: 82.1,
      pass_rate: 91.7,
      created_at: "2024-01-03T09:00:00Z",
      last_attempt_at: "2024-01-05T16:45:00Z"
    },
    {
      id: 4,
      title: "计算机基础知识",
      subject: "计算机",
      category: "自主练习",
      difficulty: "easy",
      total_attempts: 67,
      completed_attempts: 63,
      average_score: 85.9,
      average_percentage: 85.9,
      pass_rate: 94.0,
      created_at: "2024-01-04T11:00:00Z",
      last_attempt_at: "2024-01-05T14:20:00Z"
    },
    {
      id: 5,
      title: "英语语法练习",
      subject: "英语",
      category: "课后作业",
      difficulty: "medium",
      total_attempts: 41,
      completed_attempts: 39,
      average_score: 74.8,
      average_percentage: 74.8,
      pass_rate: 82.1,
      created_at: "2024-01-05T08:00:00Z",
      last_attempt_at: "2024-01-05T17:10:00Z"
    }
  ]);

  // 获取难度标签样式
  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case "easy":
        return <Badge variant="secondary" className="bg-green-100 text-green-800">简单</Badge>;
      case "medium":
        return <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">中等</Badge>;
      case "hard":
        return <Badge variant="secondary" className="bg-red-100 text-red-800">困难</Badge>;
      default:
        return <Badge variant="secondary">未知</Badge>;
    }
  };

  // 获取类别标签样式
  const getCategoryBadge = (category: string) => {
    switch (category) {
      case "自主练习":
        return <Badge variant="outline" className="text-blue-600 border-blue-600">自主练习</Badge>;
      case "课后作业":
        return <Badge variant="outline" className="text-purple-600 border-purple-600">课后作业</Badge>;
      case "模拟考试":
        return <Badge variant="outline" className="text-orange-600 border-orange-600">模拟考试</Badge>;
      default:
        return <Badge variant="outline">{category}</Badge>;
    }
  };

  // 格式化日期
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return `${date.getMonth() + 1}/${date.getDate()}`;
  };

  // 处理查看详情
  const handleViewDetails = (exerciseId: number) => {
    // TODO: 导航到详细分析页面
    console.log("查看练习详情:", exerciseId);
  };

  return (
    <div className="space-y-4">
      {exercises.map((exercise) => (
        <Card key={exercise.id} className="hover:shadow-md transition-shadow">
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <CardTitle className="text-lg">{exercise.title}</CardTitle>
                <div className="flex items-center space-x-2">
                  {getCategoryBadge(exercise.category)}
                  {getDifficultyBadge(exercise.difficulty)}
                  <Badge variant="secondary" className="bg-gray-100 text-gray-700">
                    {exercise.subject}
                  </Badge>
                </div>
              </div>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleViewDetails(exercise.id)}
              >
                <Eye className="h-4 w-4 mr-2" />
                查看详情
              </Button>
            </div>
          </CardHeader>
          
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* 参与情况 */}
              <div className="space-y-2">
                <div className="flex items-center text-sm text-gray-600">
                  <Users className="h-4 w-4 mr-1" />
                  参与情况
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>完成率</span>
                    <span className="font-medium">
                      {((exercise.completed_attempts / exercise.total_attempts) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <Progress 
                    value={(exercise.completed_attempts / exercise.total_attempts) * 100} 
                    className="h-2"
                  />
                  <div className="text-xs text-gray-500">
                    {exercise.completed_attempts}/{exercise.total_attempts} 人完成
                  </div>
                </div>
              </div>

              {/* 成绩表现 */}
              <div className="space-y-2">
                <div className="flex items-center text-sm text-gray-600">
                  <BarChart3 className="h-4 w-4 mr-1" />
                  成绩表现
                </div>
                <div className="space-y-1">
                  <div className="text-lg font-bold text-gray-900">
                    {exercise.average_score.toFixed(1)}分
                  </div>
                  <div className="text-sm text-gray-600">
                    平均得分率 {exercise.average_percentage.toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* 及格率 */}
              <div className="space-y-2">
                <div className="flex items-center text-sm text-gray-600">
                  <Target className="h-4 w-4 mr-1" />
                  及格率
                </div>
                <div className="space-y-1">
                  <div className="text-lg font-bold text-gray-900">
                    {exercise.pass_rate.toFixed(1)}%
                  </div>
                  <div className={`text-sm ${
                    exercise.pass_rate >= 80 ? 'text-green-600' :
                    exercise.pass_rate >= 60 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {exercise.pass_rate >= 80 ? '表现优秀' :
                     exercise.pass_rate >= 60 ? '表现良好' : '需要改进'}
                  </div>
                </div>
              </div>

              {/* 时间信息 */}
              <div className="space-y-2">
                <div className="flex items-center text-sm text-gray-600">
                  <Calendar className="h-4 w-4 mr-1" />
                  时间信息
                </div>
                <div className="space-y-1">
                  <div className="text-sm">
                    <span className="text-gray-600">创建:</span>
                    <span className="ml-1">{formatDate(exercise.created_at)}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">最近:</span>
                    <span className="ml-1">{formatDate(exercise.last_attempt_at)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 快速操作 */}
            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span>练习ID: {exercise.id}</span>
                <span>•</span>
                <span>最后更新: {formatDate(exercise.last_attempt_at)}</span>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button variant="ghost" size="sm">
                  <FileText className="h-4 w-4 mr-1" />
                  生成报告
                </Button>
                <Button variant="ghost" size="sm">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  趋势分析
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}

      {/* 加载更多 */}
      <div className="text-center pt-4">
        <Button variant="outline">
          加载更多练习
        </Button>
      </div>
    </div>
  );
};

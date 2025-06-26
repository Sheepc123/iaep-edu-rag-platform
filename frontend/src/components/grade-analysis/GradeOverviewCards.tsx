import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Users, 
  BookOpen, 
  Target, 
  TrendingUp,
  Award,
  BarChart3
} from "lucide-react";

interface GradeStats {
  average_score: number;
  average_percentage: number;
  total_students: number;
  total_exercises: number;
  total_attempts: number;
}

interface GradeOverviewCardsProps {
  gradeStats: GradeStats;
}

export const GradeOverviewCards: React.FC<GradeOverviewCardsProps> = ({ gradeStats }) => {
  // 计算表现等级
  const getPerformanceLevel = (percentage: number) => {
    if (percentage >= 90) return { level: "优秀", color: "bg-green-500", textColor: "text-green-700" };
    if (percentage >= 80) return { level: "良好", color: "bg-blue-500", textColor: "text-blue-700" };
    if (percentage >= 70) return { level: "中等", color: "bg-yellow-500", textColor: "text-yellow-700" };
    if (percentage >= 60) return { level: "及格", color: "bg-orange-500", textColor: "text-orange-700" };
    return { level: "需改进", color: "bg-red-500", textColor: "text-red-700" };
  };

  const performance = getPerformanceLevel(gradeStats.average_percentage);

  const cards = [
    {
      title: "总学生数",
      value: gradeStats.total_students,
      icon: Users,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
      description: "参与练习的学生总数"
    },
    {
      title: "练习总数",
      value: gradeStats.total_exercises,
      icon: BookOpen,
      color: "text-green-600",
      bgColor: "bg-green-50",
      description: "已发布的练习数量"
    },
    {
      title: "练习次数",
      value: gradeStats.total_attempts,
      icon: BarChart3,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      description: "学生完成练习的总次数"
    },
    {
      title: "平均成绩",
      value: gradeStats.average_score.toFixed(1),
      icon: Award,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
      description: "所有练习的平均得分",
      suffix: "分"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <Card key={index} className="relative overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                {card.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${card.bgColor}`}>
                <Icon className={`h-4 w-4 ${card.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-baseline space-x-2">
                <div className="text-2xl font-bold text-gray-900">
                  {card.value}
                </div>
                {card.suffix && (
                  <span className="text-sm text-gray-500">{card.suffix}</span>
                )}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {card.description}
              </p>
            </CardContent>
          </Card>
        );
      })}

      {/* 表现等级卡片 */}
      <Card className="md:col-span-2 lg:col-span-4">
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="h-5 w-5 mr-2" />
            整体表现分析
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${performance.color}`}></div>
                <span className="text-sm font-medium">表现等级</span>
              </div>
              <Badge variant="secondary" className={performance.textColor}>
                {performance.level}
              </Badge>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="text-center">
                <div className="text-lg font-bold text-gray-900">
                  {gradeStats.average_percentage.toFixed(1)}%
                </div>
                <div className="text-xs text-gray-500">平均得分率</div>
              </div>
              
              <div className="text-center">
                <div className="text-lg font-bold text-gray-900">
                  {(gradeStats.total_attempts / gradeStats.total_students).toFixed(1)}
                </div>
                <div className="text-xs text-gray-500">人均练习次数</div>
              </div>
              
              <div className="text-center">
                <div className="text-lg font-bold text-gray-900">
                  {((gradeStats.total_attempts / gradeStats.total_exercises) || 0).toFixed(0)}
                </div>
                <div className="text-xs text-gray-500">平均参与人数</div>
              </div>
            </div>
          </div>
          
          {/* 进度条 */}
          <div className="mt-4">
            <div className="flex justify-between text-xs text-gray-500 mb-1">
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${performance.color}`}
                style={{ width: `${Math.min(gradeStats.average_percentage, 100)}%` }}
              ></div>
            </div>
          </div>
          
          {/* 表现建议 */}
          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <div className="text-sm">
              <span className="font-medium">建议：</span>
              {gradeStats.average_percentage >= 90 && (
                <span className="text-gray-600">
                  学生整体表现优秀，可以适当增加练习难度，挑战更高水平。
                </span>
              )}
              {gradeStats.average_percentage >= 80 && gradeStats.average_percentage < 90 && (
                <span className="text-gray-600">
                  学生表现良好，继续保持当前教学节奏，关注个别学生的提升。
                </span>
              )}
              {gradeStats.average_percentage >= 70 && gradeStats.average_percentage < 80 && (
                <span className="text-gray-600">
                  学生表现中等，建议加强基础知识讲解，增加练习量。
                </span>
              )}
              {gradeStats.average_percentage >= 60 && gradeStats.average_percentage < 70 && (
                <span className="text-gray-600">
                  学生表现需要改进，建议重点关注基础知识掌握情况。
                </span>
              )}
              {gradeStats.average_percentage < 60 && (
                <span className="text-gray-600">
                  学生表现需要重点关注，建议调整教学方法，提供更多辅导。
                </span>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

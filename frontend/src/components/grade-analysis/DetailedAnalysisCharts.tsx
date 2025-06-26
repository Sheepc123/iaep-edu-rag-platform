import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

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
}

interface StudentPerformance {
  student_id: number;
  student_name: string;
  score: number;
  percentage: number;
  time_spent: number;
  rank: number;
}

interface DetailedAnalysisChartsProps {
  scoreDistribution: ScoreDistribution;
  questionAnalysis: QuestionAnalysis[];
  studentPerformance: StudentPerformance[];
}

export const DetailedAnalysisCharts: React.FC<DetailedAnalysisChartsProps> = ({
  scoreDistribution,
  questionAnalysis,
  studentPerformance
}) => {
  // 成绩分布饼图数据
  const gradeDistributionData = [
    { name: "优秀(90+)", value: scoreDistribution.grade_distribution.excellent, color: "#10b981" },
    { name: "良好(80-89)", value: scoreDistribution.grade_distribution.good, color: "#3b82f6" },
    { name: "中等(70-79)", value: scoreDistribution.grade_distribution.fair, color: "#f59e0b" },
    { name: "及格(60-69)", value: scoreDistribution.grade_distribution.poor, color: "#ef4444" },
    { name: "不及格(<60)", value: scoreDistribution.grade_distribution.fail, color: "#6b7280" }
  ].filter(item => item.value > 0);

  // 分数段分布数据
  const scoreRangesData = scoreDistribution.score_ranges.map(range => ({
    ...range,
    displayRange: range.range.replace('-', '~')
  }));

  // 题目难度分析数据
  const questionDifficultyData = questionAnalysis.reduce((acc, question) => {
    const existing = acc.find(item => item.difficulty === question.difficulty);
    if (existing) {
      existing.count += 1;
      existing.totalAccuracy += question.accuracy_rate;
      existing.avgAccuracy = existing.totalAccuracy / existing.count;
    } else {
      acc.push({
        difficulty: question.difficulty,
        count: 1,
        totalAccuracy: question.accuracy_rate,
        avgAccuracy: question.accuracy_rate
      });
    }
    return acc;
  }, [] as Array<{ difficulty: string; count: number; totalAccuracy: number; avgAccuracy: number }>);

  // 学生成绩与时间散点图数据
  const performanceTimeData = studentPerformance.map(student => ({
    time: Math.round(student.time_spent / 60), // 转换为分钟
    score: student.percentage,
    name: student.student_name
  }));

  // 自定义工具提示
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-1">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value}${entry.unit || ''}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* 成绩分布饼图 */}
      <Card>
        <CardHeader>
          <CardTitle>成绩等级分布</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={gradeDistributionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {gradeDistributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value: any) => [`${value}人`, '人数']}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-4">
            {gradeDistributionData.map((item, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: item.color }}
                ></div>
                <span className="text-xs text-gray-600">{item.name}</span>
                <span className="text-xs font-medium">{item.value}人</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 分数段分布柱状图 */}
      <Card>
        <CardHeader>
          <CardTitle>分数段分布</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreRangesData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="displayRange" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip 
                  formatter={(value: any) => [`${value}人`, '人数']}
                  labelFormatter={(label) => `分数段: ${label}`}
                />
                <Bar 
                  dataKey="count" 
                  fill="#3b82f6"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* 题目难度分析 */}
      <Card>
        <CardHeader>
          <CardTitle>题目难度分析</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={questionDifficultyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="difficulty" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip 
                  formatter={(value: any, name: string) => [
                    name === 'avgAccuracy' ? `${value.toFixed(1)}%` : value,
                    name === 'avgAccuracy' ? '平均正确率' : '题目数量'
                  ]}
                  labelFormatter={(label) => `难度: ${label}`}
                />
                <Bar 
                  dataKey="count" 
                  fill="#10b981"
                  radius={[4, 4, 0, 0]}
                />
                <Bar 
                  dataKey="avgAccuracy" 
                  fill="#f59e0b"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center space-x-6 mt-2">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-xs text-gray-600">题目数量</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span className="text-xs text-gray-600">平均正确率</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 成绩与时间散点图 */}
      <Card>
        <CardHeader>
          <CardTitle>成绩与用时关系</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart data={performanceTimeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="time" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                  label={{ value: '用时(分钟)', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                  label={{ value: '得分率(%)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  formatter={(value: any, name: string) => [
                    name === 'score' ? `${value}%` : `${value}分钟`,
                    name === 'score' ? '得分率' : '用时'
                  ]}
                  labelFormatter={(label, payload) => 
                    payload && payload[0] ? `学生: ${payload[0].payload.name}` : ''
                  }
                />
                <Scatter 
                  dataKey="score" 
                  fill="#8b5cf6"
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 text-sm text-gray-600">
            <p>横轴表示答题用时，纵轴表示得分率。可以观察学生答题效率与成绩的关系。</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

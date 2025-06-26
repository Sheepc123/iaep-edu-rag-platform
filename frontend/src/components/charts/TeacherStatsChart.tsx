import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import {
  BarChart3,
  TrendingUp,
  Users,
  BookOpen,
  ClipboardList,
  Award,
  Target,
  Activity
} from "lucide-react";

interface TeacherStatsChartProps {
  stats: {
    total_students: number;
    total_courses: number;
    total_exercises: number;
    average_score: number;
    active_students: number;
    published_courses: number;
    published_exercises: number;
    total_enrollments: number;
  };
}

export const TeacherStatsChart: React.FC<TeacherStatsChartProps> = ({ stats }) => {
  // 计算百分比数据
  const coursePublishRate = stats.total_courses > 0 ? (stats.published_courses / stats.total_courses) * 100 : 0;
  const exercisePublishRate = stats.total_exercises > 0 ? (stats.published_exercises / stats.total_exercises) * 100 : 0;
  const studentActiveRate = stats.total_students > 0 ? (stats.active_students / stats.total_students) * 100 : 0;

  // 模拟一些趋势数据
  const weeklyData = [
    { day: '周一', students: 12, courses: 2, exercises: 3 },
    { day: '周二', students: 15, courses: 1, exercises: 5 },
    { day: '周三', students: 18, courses: 3, exercises: 2 },
    { day: '周四', students: 22, courses: 1, exercises: 4 },
    { day: '周五', students: 25, courses: 2, exercises: 6 },
    { day: '周六', students: 20, courses: 0, exercises: 3 },
    { day: '周日', students: 16, courses: 1, exercises: 2 }
  ];

  const maxStudents = Math.max(...weeklyData.map(d => d.students));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* 发布率统计 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BarChart3 className="mr-2 h-5 w-5" />
            内容发布率
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">课程发布率</span>
              <Badge variant="secondary">{coursePublishRate.toFixed(1)}%</Badge>
            </div>
            <Progress value={coursePublishRate} className="h-2" />
            <p className="text-xs text-gray-500">
              已发布 {stats.published_courses} / {stats.total_courses} 个课程
            </p>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">练习发布率</span>
              <Badge variant="secondary">{exercisePublishRate.toFixed(1)}%</Badge>
            </div>
            <Progress value={exercisePublishRate} className="h-2" />
            <p className="text-xs text-gray-500">
              已发布 {stats.published_exercises} / {stats.total_exercises} 个练习
            </p>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">学生活跃率</span>
              <Badge variant="secondary">{studentActiveRate.toFixed(1)}%</Badge>
            </div>
            <Progress value={studentActiveRate} className="h-2" />
            <p className="text-xs text-gray-500">
              活跃学生 {stats.active_students} / {stats.total_students} 人
            </p>
          </div>
        </CardContent>
      </Card>

      {/* 周活跃度趋势 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <TrendingUp className="mr-2 h-5 w-5" />
            本周活跃度趋势
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {weeklyData.map((data, index) => (
              <div key={data.day} className="flex items-center space-x-4">
                <div className="w-12 text-sm font-medium text-gray-600">
                  {data.day}
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <Users className="h-3 w-3 text-blue-500" />
                    <span className="text-xs text-gray-500">学生: {data.students}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${(data.students / maxStudents) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="flex space-x-3 text-xs text-gray-500">
                  <div className="flex items-center">
                    <BookOpen className="h-3 w-3 mr-1 text-green-500" />
                    {data.courses}
                  </div>
                  <div className="flex items-center">
                    <ClipboardList className="h-3 w-3 mr-1 text-purple-500" />
                    {data.exercises}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 教学效果分析 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Award className="mr-2 h-5 w-5" />
            教学效果分析
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {stats.average_score.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">平均成绩</div>
              <div className="text-xs text-gray-500 mt-1">
                {stats.average_score >= 80 ? '优秀' : stats.average_score >= 60 ? '良好' : '需改进'}
              </div>
            </div>
            
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {stats.total_enrollments}
              </div>
              <div className="text-sm text-gray-600">总注册数</div>
              <div className="text-xs text-gray-500 mt-1">
                累计学习人次
              </div>
            </div>

            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {((stats.published_courses + stats.published_exercises) / 2).toFixed(0)}
              </div>
              <div className="text-sm text-gray-600">内容质量</div>
              <div className="text-xs text-gray-500 mt-1">
                发布内容评分
              </div>
            </div>

            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">
                {studentActiveRate.toFixed(0)}%
              </div>
              <div className="text-sm text-gray-600">参与度</div>
              <div className="text-xs text-gray-500 mt-1">
                学生活跃比例
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 改进建议 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="mr-2 h-5 w-5" />
            改进建议
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {coursePublishRate < 80 && (
              <div className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                <BookOpen className="h-4 w-4 text-blue-500 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-blue-900">
                    增加课程发布
                  </div>
                  <div className="text-xs text-blue-700">
                    建议发布更多课程内容，提高课程发布率
                  </div>
                </div>
              </div>
            )}

            {exercisePublishRate < 80 && (
              <div className="flex items-start space-x-3 p-3 bg-purple-50 rounded-lg">
                <ClipboardList className="h-4 w-4 text-purple-500 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-purple-900">
                    增加练习内容
                  </div>
                  <div className="text-xs text-purple-700">
                    建议创建更多练习，帮助学生巩固知识
                  </div>
                </div>
              </div>
            )}

            {studentActiveRate < 70 && (
              <div className="flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg">
                <Users className="h-4 w-4 text-yellow-500 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-yellow-900">
                    提高学生参与度
                  </div>
                  <div className="text-xs text-yellow-700">
                    建议增加互动内容，提高学生学习积极性
                  </div>
                </div>
              </div>
            )}

            {stats.average_score < 70 && (
              <div className="flex items-start space-x-3 p-3 bg-red-50 rounded-lg">
                <Award className="h-4 w-4 text-red-500 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-red-900">
                    关注学习效果
                  </div>
                  <div className="text-xs text-red-700">
                    平均成绩偏低，建议调整教学方法或内容难度
                  </div>
                </div>
              </div>
            )}

            {coursePublishRate >= 80 && exercisePublishRate >= 80 && studentActiveRate >= 70 && stats.average_score >= 70 && (
              <div className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                <Activity className="h-4 w-4 text-green-500 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-green-900">
                    教学效果良好
                  </div>
                  <div className="text-xs text-green-700">
                    各项指标表现优秀，继续保持！
                  </div>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

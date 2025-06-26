import React from "react";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { 
  CheckCircle, 
  Clock, 
  User,
  BookOpen,
  Award
} from "lucide-react";

interface RecentActivity {
  type: string;
  student_name: string;
  exercise_title: string;
  score: number;
  percentage: number;
  submitted_at: string;
}

interface RecentActivitiesListProps {
  activities: RecentActivity[];
}

export const RecentActivitiesList: React.FC<RecentActivitiesListProps> = ({ activities }) => {
  // 格式化时间显示
  const formatTime = (timeString: string) => {
    const date = new Date(timeString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return "刚刚";
    if (diffInMinutes < 60) return `${diffInMinutes}分钟前`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}小时前`;
    return `${Math.floor(diffInMinutes / 1440)}天前`;
  };

  // 获取成绩等级
  const getGradeLevel = (percentage: number) => {
    if (percentage >= 90) return { level: "优秀", color: "bg-green-100 text-green-800" };
    if (percentage >= 80) return { level: "良好", color: "bg-blue-100 text-blue-800" };
    if (percentage >= 70) return { level: "中等", color: "bg-yellow-100 text-yellow-800" };
    if (percentage >= 60) return { level: "及格", color: "bg-orange-100 text-orange-800" };
    return { level: "不及格", color: "bg-red-100 text-red-800" };
  };

  // 获取学生姓名首字母
  const getInitials = (name: string) => {
    return name.charAt(0).toUpperCase();
  };

  if (!activities || activities.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-gray-500">
        <div className="text-center">
          <Clock className="h-8 w-8 mx-auto mb-2 text-gray-400" />
          <div className="text-sm">暂无最近活动</div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {activities.map((activity, index) => {
        const gradeLevel = getGradeLevel(activity.percentage);
        
        return (
          <div 
            key={index} 
            className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {/* 学生头像 */}
            <Avatar className="h-10 w-10">
              <AvatarFallback className="bg-blue-100 text-blue-600">
                {getInitials(activity.student_name)}
              </AvatarFallback>
            </Avatar>

            {/* 活动内容 */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2 mb-1">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="font-medium text-gray-900">
                  {activity.student_name}
                </span>
                <span className="text-gray-500 text-sm">完成了练习</span>
              </div>
              
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <BookOpen className="h-3 w-3" />
                <span className="truncate">{activity.exercise_title}</span>
              </div>
            </div>

            {/* 成绩信息 */}
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <div className="flex items-center space-x-2">
                  <Award className="h-4 w-4 text-gray-400" />
                  <span className="font-medium text-gray-900">
                    {activity.score.toFixed(1)}分
                  </span>
                </div>
                <div className="text-xs text-gray-500">
                  {activity.percentage.toFixed(1)}%
                </div>
              </div>
              
              <Badge variant="secondary" className={gradeLevel.color}>
                {gradeLevel.level}
              </Badge>
            </div>

            {/* 时间 */}
            <div className="text-xs text-gray-500 min-w-0">
              {formatTime(activity.submitted_at)}
            </div>
          </div>
        );
      })}

      {/* 查看更多 */}
      {activities.length >= 5 && (
        <div className="text-center pt-4 border-t border-gray-200">
          <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
            查看更多活动
          </button>
        </div>
      )}
    </div>
  );
};

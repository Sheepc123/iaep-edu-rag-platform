import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from "recharts";

interface TrendData {
  date: string;
  average_score: number;
  attempt_count: number;
  pass_rate: number;
}

interface GradeTrendsChartProps {
  data: TrendData[];
  showDetails?: boolean;
}

export const GradeTrendsChart: React.FC<GradeTrendsChartProps> = ({ 
  data, 
  showDetails = false 
}) => {
  // 格式化日期显示
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return `${date.getMonth() + 1}/${date.getDate()}`;
  };

  // 处理数据，添加格式化的日期
  const chartData = data.map(item => ({
    ...item,
    formattedDate: formatDate(item.date),
    displayScore: item.average_score.toFixed(1),
    displayPassRate: item.pass_rate.toFixed(1)
  }));

  // 自定义工具提示
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-2">{`日期: ${label}`}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name === 'average_score' && `平均分: ${entry.value.toFixed(1)}`}
              {entry.name === 'pass_rate' && `及格率: ${entry.value.toFixed(1)}%`}
              {entry.name === 'attempt_count' && `练习次数: ${entry.value}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        <div className="text-center">
          <div className="text-lg font-medium">暂无数据</div>
          <div className="text-sm">还没有足够的数据来显示趋势</div>
        </div>
      </div>
    );
  }

  if (showDetails) {
    return (
      <div className="space-y-6">
        {/* 成绩趋势 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">成绩变化趋势</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="formattedDate" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="average_score"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.1}
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 及格率趋势 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">及格率变化趋势</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="formattedDate" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="pass_rate"
                  stroke="#10b981"
                  strokeWidth={2}
                  dot={{ fill: "#10b981", strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, stroke: "#10b981", strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 练习活跃度 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">练习活跃度</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="formattedDate" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="attempt_count"
                  stroke="#8b5cf6"
                  fill="#8b5cf6"
                  fillOpacity={0.2}
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    );
  }

  // 简化版本 - 只显示成绩趋势
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="formattedDate" 
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="average_score"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={{ fill: "#3b82f6", strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: "#3b82f6", strokeWidth: 2 }}
          />
          <Line
            type="monotone"
            dataKey="pass_rate"
            stroke="#10b981"
            strokeWidth={2}
            dot={{ fill: "#10b981", strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: "#10b981", strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      {/* 图例 */}
      <div className="flex justify-center space-x-6 mt-2">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
          <span className="text-xs text-gray-600">平均分</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-xs text-gray-600">及格率</span>
        </div>
      </div>
    </div>
  );
};

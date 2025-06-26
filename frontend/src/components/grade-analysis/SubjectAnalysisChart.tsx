import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from "recharts";

interface SubjectAnalysis {
  subject: string;
  average_score: number;
  attempt_count: number;
  pass_rate: number;
  excellent_rate: number;
}

interface SubjectAnalysisChartProps {
  data: SubjectAnalysis[];
  showDetails?: boolean;
}

export const SubjectAnalysisChart: React.FC<SubjectAnalysisChartProps> = ({ 
  data, 
  showDetails = false 
}) => {
  // 自定义工具提示
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-2">{`科目: ${label}`}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.dataKey === 'average_score' && `平均分: ${entry.value.toFixed(1)}`}
              {entry.dataKey === 'pass_rate' && `及格率: ${entry.value.toFixed(1)}%`}
              {entry.dataKey === 'excellent_rate' && `优秀率: ${entry.value.toFixed(1)}%`}
              {entry.dataKey === 'attempt_count' && `练习次数: ${entry.value}`}
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
          <div className="text-sm">还没有科目数据</div>
        </div>
      </div>
    );
  }

  if (showDetails) {
    return (
      <div className="space-y-6">
        {/* 科目成绩对比 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">科目平均分对比</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="subject" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar 
                  dataKey="average_score" 
                  fill="#3b82f6"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 及格率和优秀率对比 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">及格率与优秀率对比</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="subject" 
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <YAxis 
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                  stroke="#666"
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar 
                  dataKey="pass_rate" 
                  fill="#10b981"
                  radius={[4, 4, 0, 0]}
                />
                <Bar 
                  dataKey="excellent_rate" 
                  fill="#f59e0b"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center space-x-6 mt-2">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-xs text-gray-600">及格率</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span className="text-xs text-gray-600">优秀率</span>
            </div>
          </div>
        </div>

        {/* 雷达图 - 综合表现 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">科目综合表现雷达图</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={data}>
                <PolarGrid stroke="#f0f0f0" />
                <PolarAngleAxis 
                  dataKey="subject" 
                  tick={{ fontSize: 12 }}
                />
                <PolarRadiusAxis 
                  domain={[0, 100]} 
                  tick={{ fontSize: 10 }}
                  tickCount={5}
                />
                <Radar
                  name="平均分"
                  dataKey="average_score"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.1}
                  strokeWidth={2}
                />
                <Radar
                  name="及格率"
                  dataKey="pass_rate"
                  stroke="#10b981"
                  fill="#10b981"
                  fillOpacity={0.1}
                  strokeWidth={2}
                />
                <Tooltip content={<CustomTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
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
      </div>
    );
  }

  // 简化版本 - 只显示平均分对比
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="subject" 
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="average_score" 
            fill="#3b82f6"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
      
      {/* 简单统计 */}
      <div className="mt-4 grid grid-cols-3 gap-4 text-center">
        <div>
          <div className="text-lg font-bold text-gray-900">
            {data.length}
          </div>
          <div className="text-xs text-gray-500">科目数量</div>
        </div>
        <div>
          <div className="text-lg font-bold text-gray-900">
            {(data.reduce((sum, item) => sum + item.average_score, 0) / data.length).toFixed(1)}
          </div>
          <div className="text-xs text-gray-500">整体平均分</div>
        </div>
        <div>
          <div className="text-lg font-bold text-gray-900">
            {(data.reduce((sum, item) => sum + item.pass_rate, 0) / data.length).toFixed(1)}%
          </div>
          <div className="text-xs text-gray-500">整体及格率</div>
        </div>
      </div>
    </div>
  );
};

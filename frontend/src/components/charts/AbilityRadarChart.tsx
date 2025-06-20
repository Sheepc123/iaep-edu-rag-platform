"use client";

import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts';

const data = [
  { subject: '计算能力', A: 105, fullMark: 150 },
  { subject: '逻辑思维', A: 130, fullMark: 150 },
  { subject: '空间想象', A: 95, fullMark: 150 },
  { subject: '语言表达', A: 110, fullMark: 150 },
  { subject: '数据分析', A: 85, fullMark: 150 },
  { subject: '知识应用', A: 125, fullMark: 150 },
];

export const AbilityRadarChart = () => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
        <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#8884d8" stopOpacity={0.2}/>
            </linearGradient>
        </defs>
        <PolarGrid stroke="#4A5568" />
        <PolarAngleAxis dataKey="subject" tick={{ fill: '#A0AEC0', fontSize: 14 }} />
        <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
        <Radar name="能力评估" dataKey="A" stroke="#8884d8" fill="url(#colorUv)" fillOpacity={0.6} />
        <Legend />
      </RadarChart>
    </ResponsiveContainer>
  );
}; 
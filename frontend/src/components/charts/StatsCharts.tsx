"use client";

import React from 'react';
import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer, Legend } from 'recharts';

const data = [
    { name: '今日学习', value: 45, total: 120, fill: '#8884d8' },
    { name: '任务完成', value: 80, total: 100, fill: '#83a6ed' },
    { name: '知识掌握', value: 75, total: 100, fill: '#82ca9d' },
];

const CircleStat = ({ item }: { item: typeof data[0] }) => {
    const percentage = Math.round((item.value / item.total) * 100);
    return (
        <div className="flex flex-col items-center">
            <ResponsiveContainer width={120} height={120}>
                <RadialBarChart
                    innerRadius="70%"
                    outerRadius="90%"
                    barSize={10}
                    data={[{...item, value: 100}, { ...item }]}
                    startAngle={90}
                    endAngle={-270}
                >
                    <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                    <RadialBar
                        background
                        dataKey="value"
                        cornerRadius={10}
                        angleAxisId={0}
                        data={[{ value: item.total, fill: '#333' }]}
                    />
                    <RadialBar
                        dataKey="value"
                        cornerRadius={10}
                        angleAxisId={0}
                        data={[{ value: item.value, fill: item.fill }]}
                    />
                    <text
                        x="50%"
                        y="50%"
                        textAnchor="middle"
                        dominantBaseline="middle"
                        className="text-2xl font-bold fill-white"
                    >
                        {`${percentage}%`}
                    </text>
                </RadialBarChart>
            </ResponsiveContainer>
            <p className="mt-2 text-sm text-gray-400">{item.name}</p>
        </div>
    )
}


export const StatsCharts = () => {
    return (
        <div className="flex justify-around items-center h-full w-full">
            {data.map(item => <CircleStat key={item.name} item={item} />)}
        </div>
    );
}; 
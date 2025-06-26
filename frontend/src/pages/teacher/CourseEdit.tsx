import React from "react";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const TeacherCourseEdit: React.FC = () => {
  return (
    <TeacherLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">编辑课程</h1>
        <Card>
          <CardHeader>
            <CardTitle>编辑课程信息</CardTitle>
          </CardHeader>
          <CardContent>
            <p>此页面正在开发中...</p>
          </CardContent>
        </Card>
      </div>
    </TeacherLayout>
  );
};

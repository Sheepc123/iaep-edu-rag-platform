"""
成绩分析相关的数据模式
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BasicStatsResponse(BaseModel):
    """基础统计响应模型"""
    total_attempts: int = Field(..., description="总尝试次数")
    average_score: float = Field(..., description="平均分")
    median_score: float = Field(..., description="中位数")
    highest_score: float = Field(..., description="最高分")
    lowest_score: float = Field(..., description="最低分")
    average_percentage: float = Field(..., description="平均得分率")
    standard_deviation: float = Field(..., description="标准差")


class GradeDistribution(BaseModel):
    """成绩分布模型"""
    excellent: int = Field(..., description="优秀人数(90+)")
    good: int = Field(..., description="良好人数(80-89)")
    fair: int = Field(..., description="中等人数(70-79)")
    poor: int = Field(..., description="及格人数(60-69)")
    fail: int = Field(..., description="不及格人数(<60)")


class GradeDistributionPercentage(BaseModel):
    """成绩分布百分比模型"""
    excellent: float = Field(..., description="优秀比例")
    good: float = Field(..., description="良好比例")
    fair: float = Field(..., description="中等比例")
    poor: float = Field(..., description="及格比例")
    fail: float = Field(..., description="不及格比例")


class ScoreRange(BaseModel):
    """分数段模型"""
    range: str = Field(..., description="分数段")
    count: int = Field(..., description="人数")
    percentage: float = Field(..., description="百分比")


class ScoreDistributionResponse(BaseModel):
    """分数分布响应模型"""
    grade_distribution: GradeDistribution
    grade_distribution_percentage: GradeDistributionPercentage
    score_ranges: List[ScoreRange]
    pass_rate: float = Field(..., description="及格率")


class CommonMistake(BaseModel):
    """常见错误模型"""
    answer: str = Field(..., description="错误答案")
    count: int = Field(..., description="出现次数")


class QuestionAnalysis(BaseModel):
    """题目分析模型"""
    question_id: int = Field(..., description="题目ID")
    question_content: str = Field(..., description="题目内容")
    question_type: str = Field(..., description="题目类型")
    difficulty: str = Field(..., description="难度")
    points: int = Field(..., description="分值")
    total_attempts: int = Field(..., description="总尝试次数")
    correct_attempts: int = Field(..., description="正确次数")
    accuracy_rate: float = Field(..., description="正确率")
    common_mistakes: List[CommonMistake] = Field(..., description="常见错误")
    average_time: float = Field(..., description="平均用时")


class TimeRange(BaseModel):
    """时间段模型"""
    range: str = Field(..., description="时间段")
    count: int = Field(..., description="人数")
    percentage: float = Field(..., description="百分比")


class TimeAnalysisResponse(BaseModel):
    """时间分析响应模型"""
    average_time: float = Field(..., description="平均用时")
    median_time: float = Field(..., description="中位用时")
    min_time: float = Field(..., description="最短用时")
    max_time: float = Field(..., description="最长用时")
    time_distribution: List[TimeRange] = Field(..., description="时间分布")


class StudentPerformanceResponse(BaseModel):
    """学生表现响应模型"""
    student_id: int = Field(..., description="学生ID")
    student_name: str = Field(..., description="学生姓名")
    username: str = Field(..., description="用户名")
    score: float = Field(..., description="得分")
    percentage: float = Field(..., description="得分率")
    time_spent: int = Field(..., description="用时(秒)")
    rank: int = Field(..., description="排名")
    vs_class_average: float = Field(..., description="与班级平均分对比")
    performance_level: str = Field(..., description="表现等级")
    completed_at: Optional[str] = Field(None, description="完成时间")


class GradeAnalysisResponse(BaseModel):
    """成绩分析响应模型"""
    basic_stats: BasicStatsResponse
    score_distribution: ScoreDistributionResponse
    question_analysis: List[QuestionAnalysis]
    time_analysis: TimeAnalysisResponse
    student_performance: List[StudentPerformanceResponse]


class GradeStats(BaseModel):
    """成绩统计模型"""
    average_score: float = Field(..., description="平均分")
    average_percentage: float = Field(..., description="平均得分率")
    total_students: int = Field(..., description="总学生数")
    total_exercises: int = Field(..., description="总练习数")
    total_attempts: int = Field(..., description="总尝试次数")


class TrendData(BaseModel):
    """趋势数据模型"""
    date: str = Field(..., description="日期")
    average_score: float = Field(..., description="平均分")
    attempt_count: int = Field(..., description="尝试次数")
    pass_rate: float = Field(..., description="及格率")


class SubjectAnalysis(BaseModel):
    """科目分析模型"""
    subject: str = Field(..., description="科目")
    average_score: float = Field(..., description="平均分")
    attempt_count: int = Field(..., description="尝试次数")
    pass_rate: float = Field(..., description="及格率")
    excellent_rate: float = Field(..., description="优秀率")


class RecentActivity(BaseModel):
    """最近活动模型"""
    type: str = Field(..., description="活动类型")
    student_name: str = Field(..., description="学生姓名")
    exercise_title: str = Field(..., description="练习标题")
    score: float = Field(..., description="得分")
    percentage: float = Field(..., description="得分率")
    submitted_at: Optional[str] = Field(None, description="提交时间")


class TeacherGradeOverviewResponse(BaseModel):
    """教师成绩概览响应模型"""
    grade_stats: GradeStats
    trend_data: List[TrendData]
    subject_analysis: List[SubjectAnalysis]
    recent_activities: List[RecentActivity]


class ExerciseInfo(BaseModel):
    """练习信息模型"""
    id: int = Field(..., description="练习ID")
    title: str = Field(..., description="练习标题")
    subject: str = Field(..., description="科目")
    category: str = Field(..., description="类别")
    difficulty: str = Field(..., description="难度")
    total_questions: int = Field(..., description="总题数")


class TeachingRecommendation(BaseModel):
    """教学建议模型"""
    type: str = Field(..., description="建议类型")
    title: str = Field(..., description="建议标题")
    suggestion: str = Field(..., description="具体建议")


class ClassReportResponse(BaseModel):
    """班级报告响应模型"""
    exercise_info: ExerciseInfo
    analysis_result: GradeAnalysisResponse
    generated_at: str = Field(..., description="生成时间")
    recommendations: List[TeachingRecommendation] = Field(..., description="教学建议")


class GradeStatsSummary(BaseModel):
    """成绩统计摘要模型"""
    total_students: int = Field(..., description="总学生数")
    total_exercises: int = Field(..., description="总练习数")
    total_attempts: int = Field(..., description="总尝试次数")
    average_score: float = Field(..., description="平均分")
    average_percentage: float = Field(..., description="平均得分率")
    recent_activities_count: int = Field(..., description="最近活动数")
    subject_count: int = Field(..., description="科目数")
    trend_days: int = Field(..., description="趋势天数")
    performance_level: str = Field(..., description="表现等级")
    performance_color: str = Field(..., description="表现颜色")


class GradeStatsSummaryResponse(BaseModel):
    """成绩统计摘要响应模型"""
    summary: GradeStatsSummary
    recent_activities: List[RecentActivity]
    top_subjects: List[SubjectAnalysis]


class GradeTrendsResponse(BaseModel):
    """成绩趋势响应模型"""
    trend_data: List[TrendData]
    period: str = Field(..., description="统计周期")
    data_points: int = Field(..., description="数据点数量")

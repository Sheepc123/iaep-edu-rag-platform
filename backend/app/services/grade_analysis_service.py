"""
成绩分析服务
"""
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from datetime import datetime, timedelta
import json
import statistics
from collections import defaultdict, Counter

from ..models.exercise import (
    Exercise, ExerciseAttempt, StudentAnswer, Question,
    GradeAnalysis, StudentPerformance, ClassGradeReport
)
from ..models.user import User, StudentProfile
from ..models.course import CourseEnrollment


class GradeAnalysisService:
    """成绩分析服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_exercise_grades(self, exercise_id: int, teacher_id: int) -> Dict[str, Any]:
        """分析练习成绩"""
        # 获取练习信息
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise ValueError("练习不存在")
        
        # 获取所有完成的尝试
        attempts = self.db.query(ExerciseAttempt).filter(
            and_(
                ExerciseAttempt.exercise_id == exercise_id,
                ExerciseAttempt.is_submitted == True
            )
        ).all()
        
        if not attempts:
            return self._empty_analysis_result()
        
        # 基础统计
        scores = [attempt.score for attempt in attempts]
        percentages = [(attempt.score / attempt.max_score * 100) for attempt in attempts]
        
        basic_stats = {
            "total_attempts": len(attempts),
            "average_score": statistics.mean(scores),
            "median_score": statistics.median(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "average_percentage": statistics.mean(percentages),
            "standard_deviation": statistics.stdev(scores) if len(scores) > 1 else 0
        }
        
        # 分数分布分析
        score_distribution = self._analyze_score_distribution(percentages)
        
        # 题目分析
        question_analysis = self._analyze_questions(exercise_id, attempts)
        
        # 时间分析
        time_analysis = self._analyze_time_spent(attempts)
        
        # 学生表现分析
        student_performance = self._analyze_student_performance(attempts, basic_stats["average_score"])
        
        # 保存分析结果
        self._save_grade_analysis(exercise_id, teacher_id, {
            **basic_stats,
            "score_distribution": score_distribution,
            "question_analysis": question_analysis,
            "time_analysis": time_analysis
        })
        
        return {
            "basic_stats": basic_stats,
            "score_distribution": score_distribution,
            "question_analysis": question_analysis,
            "time_analysis": time_analysis,
            "student_performance": student_performance
        }
    
    def _analyze_score_distribution(self, percentages: List[float]) -> Dict[str, Any]:
        """分析分数分布"""
        distribution = {
            "excellent": len([p for p in percentages if p >= 90]),  # 优秀
            "good": len([p for p in percentages if 80 <= p < 90]),  # 良好
            "fair": len([p for p in percentages if 70 <= p < 80]),  # 中等
            "poor": len([p for p in percentages if 60 <= p < 70]),  # 及格
            "fail": len([p for p in percentages if p < 60])         # 不及格
        }
        
        total = len(percentages)
        distribution_percentage = {
            key: (count / total * 100) if total > 0 else 0
            for key, count in distribution.items()
        }
        
        # 分数段详细分布
        score_ranges = []
        for i in range(0, 101, 10):
            range_count = len([p for p in percentages if i <= p < i + 10])
            score_ranges.append({
                "range": f"{i}-{i+9}",
                "count": range_count,
                "percentage": (range_count / total * 100) if total > 0 else 0
            })
        
        return {
            "grade_distribution": distribution,
            "grade_distribution_percentage": distribution_percentage,
            "score_ranges": score_ranges,
            "pass_rate": ((total - distribution["fail"]) / total * 100) if total > 0 else 0
        }
    
    def _analyze_questions(self, exercise_id: int, attempts: List[ExerciseAttempt]) -> List[Dict[str, Any]]:
        """分析题目表现"""
        # 获取所有题目
        questions = self.db.query(Question).filter(Question.exercise_id == exercise_id).all()
        
        question_stats = []
        for question in questions:
            # 获取该题目的所有答案
            answers = self.db.query(StudentAnswer).filter(
                StudentAnswer.question_id == question.id
            ).all()
            
            if not answers:
                continue
            
            correct_count = len([a for a in answers if a.is_correct])
            total_count = len(answers)
            accuracy_rate = (correct_count / total_count * 100) if total_count > 0 else 0
            
            # 分析常见错误答案
            wrong_answers = [a.answer_content for a in answers if not a.is_correct]
            common_mistakes = Counter(wrong_answers).most_common(3)
            
            question_stats.append({
                "question_id": question.id,
                "question_content": question.content[:100] + "..." if len(question.content) > 100 else question.content,
                "question_type": question.question_type,
                "difficulty": question.difficulty,
                "points": question.points,
                "total_attempts": total_count,
                "correct_attempts": correct_count,
                "accuracy_rate": accuracy_rate,
                "common_mistakes": [{"answer": mistake[0], "count": mistake[1]} for mistake in common_mistakes],
                "average_time": statistics.mean([a.time_spent for a in answers if a.time_spent > 0]) if answers else 0
            })
        
        # 按准确率排序，找出最难和最容易的题目
        question_stats.sort(key=lambda x: x["accuracy_rate"])
        
        return question_stats
    
    def _analyze_time_spent(self, attempts: List[ExerciseAttempt]) -> Dict[str, Any]:
        """分析答题时间"""
        times = [attempt.time_spent for attempt in attempts if attempt.time_spent > 0]
        
        if not times:
            return {"average_time": 0, "time_distribution": []}
        
        time_stats = {
            "average_time": statistics.mean(times),
            "median_time": statistics.median(times),
            "min_time": min(times),
            "max_time": max(times)
        }
        
        # 时间分布
        time_ranges = [
            {"range": "0-5分钟", "count": len([t for t in times if t <= 300])},
            {"range": "5-10分钟", "count": len([t for t in times if 300 < t <= 600])},
            {"range": "10-20分钟", "count": len([t for t in times if 600 < t <= 1200])},
            {"range": "20-30分钟", "count": len([t for t in times if 1200 < t <= 1800])},
            {"range": "30分钟以上", "count": len([t for t in times if t > 1800])}
        ]
        
        total = len(times)
        for range_data in time_ranges:
            range_data["percentage"] = (range_data["count"] / total * 100) if total > 0 else 0
        
        return {
            **time_stats,
            "time_distribution": time_ranges
        }
    
    def _analyze_student_performance(self, attempts: List[ExerciseAttempt], class_average: float) -> List[Dict[str, Any]]:
        """分析学生个人表现"""
        performance_list = []
        
        for attempt in attempts:
            # 获取学生信息
            student = self.db.query(User).filter(User.id == attempt.student_id).first()
            if not student:
                continue
            
            percentage = (attempt.score / attempt.max_score * 100) if attempt.max_score > 0 else 0
            
            # 计算排名（简化版本）
            better_scores = len([a for a in attempts if a.score > attempt.score])
            rank = better_scores + 1
            
            # 与班级平均分对比
            vs_average = attempt.score - class_average
            
            performance_list.append({
                "student_id": student.id,
                "student_name": student.full_name,
                "username": student.username,
                "score": attempt.score,
                "percentage": percentage,
                "time_spent": attempt.time_spent,
                "rank": rank,
                "vs_class_average": vs_average,
                "performance_level": self._get_performance_level(percentage),
                "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None
            })
        
        # 按分数排序
        performance_list.sort(key=lambda x: x["score"], reverse=True)
        
        return performance_list
    
    def _get_performance_level(self, percentage: float) -> str:
        """获取表现等级"""
        if percentage >= 90:
            return "优秀"
        elif percentage >= 80:
            return "良好"
        elif percentage >= 70:
            return "中等"
        elif percentage >= 60:
            return "及格"
        else:
            return "不及格"
    
    def _save_grade_analysis(self, exercise_id: int, teacher_id: int, analysis_data: Dict[str, Any]):
        """保存分析结果到数据库"""
        # 检查是否已存在分析记录
        existing_analysis = self.db.query(GradeAnalysis).filter(
            and_(
                GradeAnalysis.exercise_id == exercise_id,
                GradeAnalysis.teacher_id == teacher_id
            )
        ).first()
        
        if existing_analysis:
            # 更新现有记录
            existing_analysis.total_attempts = analysis_data["total_attempts"]
            existing_analysis.average_score = analysis_data["average_score"]
            existing_analysis.highest_score = analysis_data["highest_score"]
            existing_analysis.lowest_score = analysis_data["lowest_score"]
            existing_analysis.score_distribution = analysis_data["score_distribution"]
            existing_analysis.knowledge_point_stats = analysis_data["question_analysis"]
            existing_analysis.average_time = int(analysis_data["time_analysis"]["average_time"])
            existing_analysis.time_distribution = analysis_data["time_analysis"]
            existing_analysis.updated_at = datetime.utcnow()
        else:
            # 创建新记录
            analysis = GradeAnalysis(
                exercise_id=exercise_id,
                teacher_id=teacher_id,
                total_attempts=analysis_data["total_attempts"],
                completed_attempts=analysis_data["total_attempts"],
                average_score=analysis_data["average_score"],
                highest_score=analysis_data["highest_score"],
                lowest_score=analysis_data["lowest_score"],
                score_distribution=analysis_data["score_distribution"],
                knowledge_point_stats=analysis_data["question_analysis"],
                average_time=int(analysis_data["time_analysis"]["average_time"]),
                time_distribution=analysis_data["time_analysis"]
            )
            self.db.add(analysis)
        
        self.db.commit()
    
    def _empty_analysis_result(self) -> Dict[str, Any]:
        """返回空的分析结果"""
        return {
            "basic_stats": {
                "total_attempts": 0,
                "average_score": 0,
                "median_score": 0,
                "highest_score": 0,
                "lowest_score": 0,
                "average_percentage": 0,
                "standard_deviation": 0
            },
            "score_distribution": {
                "grade_distribution": {"excellent": 0, "good": 0, "fair": 0, "poor": 0, "fail": 0},
                "grade_distribution_percentage": {"excellent": 0, "good": 0, "fair": 0, "poor": 0, "fail": 0},
                "score_ranges": [],
                "pass_rate": 0
            },
            "question_analysis": [],
            "time_analysis": {"average_time": 0, "time_distribution": []},
            "student_performance": []
        }

    def get_teacher_grade_overview(self, teacher_id: int, days: int = 30) -> Dict[str, Any]:
        """获取教师成绩概览"""
        # 获取教师的所有练习
        exercises = self.db.query(Exercise).filter(Exercise.created_by == teacher_id).all()
        exercise_ids = [e.id for e in exercises]

        if not exercise_ids:
            return self._empty_teacher_overview()

        # 获取最近指定天数的尝试记录
        since_date = datetime.utcnow() - timedelta(days=days)
        recent_attempts = self.db.query(ExerciseAttempt).filter(
            and_(
                ExerciseAttempt.exercise_id.in_(exercise_ids),
                ExerciseAttempt.is_submitted == True,
                ExerciseAttempt.submitted_at >= since_date
            )
        ).all()

        # 基础统计
        total_students = len(set([attempt.student_id for attempt in recent_attempts]))
        total_exercises = len(exercise_ids)
        total_attempts = len(recent_attempts)

        if not recent_attempts:
            return self._empty_teacher_overview()

        # 成绩统计
        scores = [attempt.score for attempt in recent_attempts]
        percentages = [(attempt.score / attempt.max_score * 100) for attempt in recent_attempts]

        grade_stats = {
            "average_score": statistics.mean(scores),
            "average_percentage": statistics.mean(percentages),
            "total_students": total_students,
            "total_exercises": total_exercises,
            "total_attempts": total_attempts
        }

        # 趋势分析
        trend_data = self._analyze_grade_trends(recent_attempts, days)

        # 科目分析
        subject_analysis = self._analyze_by_subject(exercise_ids, recent_attempts)

        # 最近活动
        recent_activities = self._get_recent_activities(teacher_id, exercise_ids)

        return {
            "grade_stats": grade_stats,
            "trend_data": trend_data,
            "subject_analysis": subject_analysis,
            "recent_activities": recent_activities
        }

    def _analyze_grade_trends(self, attempts: List[ExerciseAttempt], days: int) -> List[Dict[str, Any]]:
        """分析成绩趋势"""
        # 按日期分组
        daily_stats = defaultdict(list)

        for attempt in attempts:
            if attempt.submitted_at:
                date_key = attempt.submitted_at.date().isoformat()
                percentage = (attempt.score / attempt.max_score * 100) if attempt.max_score > 0 else 0
                daily_stats[date_key].append(percentage)

        # 生成趋势数据
        trend_data = []
        for date_str, scores in daily_stats.items():
            trend_data.append({
                "date": date_str,
                "average_score": statistics.mean(scores),
                "attempt_count": len(scores),
                "pass_rate": len([s for s in scores if s >= 60]) / len(scores) * 100
            })

        # 按日期排序
        trend_data.sort(key=lambda x: x["date"])

        return trend_data

    def _analyze_by_subject(self, exercise_ids: List[int], attempts: List[ExerciseAttempt]) -> List[Dict[str, Any]]:
        """按科目分析成绩"""
        # 获取练习的科目信息
        exercises = self.db.query(Exercise).filter(Exercise.id.in_(exercise_ids)).all()
        exercise_subjects = {e.id: e.subject for e in exercises}

        # 按科目分组统计
        subject_stats = defaultdict(list)

        for attempt in attempts:
            subject = exercise_subjects.get(attempt.exercise_id, "未分类")
            percentage = (attempt.score / attempt.max_score * 100) if attempt.max_score > 0 else 0
            subject_stats[subject].append(percentage)

        # 生成科目分析数据
        subject_analysis = []
        for subject, scores in subject_stats.items():
            if scores:
                subject_analysis.append({
                    "subject": subject,
                    "average_score": statistics.mean(scores),
                    "attempt_count": len(scores),
                    "pass_rate": len([s for s in scores if s >= 60]) / len(scores) * 100,
                    "excellent_rate": len([s for s in scores if s >= 90]) / len(scores) * 100
                })

        # 按平均分排序
        subject_analysis.sort(key=lambda x: x["average_score"], reverse=True)

        return subject_analysis

    def _get_recent_activities(self, teacher_id: int, exercise_ids: List[int]) -> List[Dict[str, Any]]:
        """获取最近活动"""
        # 获取最近的练习尝试
        recent_attempts = self.db.query(ExerciseAttempt).filter(
            and_(
                ExerciseAttempt.exercise_id.in_(exercise_ids),
                ExerciseAttempt.is_submitted == True
            )
        ).order_by(desc(ExerciseAttempt.submitted_at)).limit(10).all()

        activities = []
        for attempt in recent_attempts:
            # 获取学生和练习信息
            student = self.db.query(User).filter(User.id == attempt.student_id).first()
            exercise = self.db.query(Exercise).filter(Exercise.id == attempt.exercise_id).first()

            if student and exercise:
                percentage = (attempt.score / attempt.max_score * 100) if attempt.max_score > 0 else 0
                activities.append({
                    "type": "exercise_completed",
                    "student_name": student.full_name,
                    "exercise_title": exercise.title,
                    "score": attempt.score,
                    "percentage": percentage,
                    "submitted_at": attempt.submitted_at.isoformat() if attempt.submitted_at else None
                })

        return activities

    def _empty_teacher_overview(self) -> Dict[str, Any]:
        """返回空的教师概览"""
        return {
            "grade_stats": {
                "average_score": 0,
                "average_percentage": 0,
                "total_students": 0,
                "total_exercises": 0,
                "total_attempts": 0
            },
            "trend_data": [],
            "subject_analysis": [],
            "recent_activities": []
        }

    def generate_class_report(self, exercise_id: int, teacher_id: int) -> Dict[str, Any]:
        """生成班级成绩报告"""
        # 先进行成绩分析
        analysis_result = self.analyze_exercise_grades(exercise_id, teacher_id)

        # 获取练习信息
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise ValueError("练习不存在")

        # 生成报告数据
        report_data = {
            "exercise_info": {
                "id": exercise.id,
                "title": exercise.title,
                "subject": exercise.subject,
                "category": exercise.category,
                "difficulty": exercise.difficulty,
                "total_questions": exercise.total_questions
            },
            "analysis_result": analysis_result,
            "generated_at": datetime.utcnow().isoformat(),
            "recommendations": self._generate_teaching_recommendations(analysis_result)
        }

        # 保存报告到数据库
        self._save_class_report(exercise_id, teacher_id, report_data)

        return report_data

    def _generate_teaching_recommendations(self, analysis_result: Dict[str, Any]) -> List[Dict[str, str]]:
        """生成教学建议"""
        recommendations = []

        # 基于整体成绩给出建议
        avg_percentage = analysis_result["basic_stats"]["average_percentage"]
        pass_rate = analysis_result["score_distribution"]["pass_rate"]

        if avg_percentage < 60:
            recommendations.append({
                "type": "overall_performance",
                "title": "整体成绩偏低",
                "suggestion": "建议重新讲解相关知识点，增加练习量，并提供个别辅导。"
            })
        elif avg_percentage >= 90:
            recommendations.append({
                "type": "overall_performance",
                "title": "整体成绩优秀",
                "suggestion": "可以适当增加题目难度，挑战学生的更高水平。"
            })

        if pass_rate < 70:
            recommendations.append({
                "type": "pass_rate",
                "title": "及格率偏低",
                "suggestion": "需要关注基础知识的掌握情况，建议进行补救教学。"
            })

        # 基于题目分析给出建议
        question_analysis = analysis_result["question_analysis"]
        if question_analysis:
            difficult_questions = [q for q in question_analysis if q["accuracy_rate"] < 50]
            if difficult_questions:
                recommendations.append({
                    "type": "difficult_questions",
                    "title": f"发现{len(difficult_questions)}道难题",
                    "suggestion": "建议针对这些题目进行专门讲解，分析常见错误原因。"
                })

        return recommendations

    def _save_class_report(self, exercise_id: int, teacher_id: int, report_data: Dict[str, Any]):
        """保存班级报告"""
        analysis_result = report_data["analysis_result"]
        basic_stats = analysis_result["basic_stats"]
        score_dist = analysis_result["score_distribution"]["grade_distribution"]

        # 检查是否已存在报告
        existing_report = self.db.query(ClassGradeReport).filter(
            and_(
                ClassGradeReport.exercise_id == exercise_id,
                ClassGradeReport.teacher_id == teacher_id
            )
        ).first()

        if existing_report:
            # 更新现有报告
            existing_report.total_students = basic_stats["total_attempts"]
            existing_report.participated_students = basic_stats["total_attempts"]
            existing_report.participation_rate = 100.0  # 简化处理
            existing_report.class_average = basic_stats["average_score"]
            existing_report.median_score = basic_stats["median_score"]
            existing_report.standard_deviation = basic_stats["standard_deviation"]
            existing_report.excellent_count = score_dist["excellent"]
            existing_report.good_count = score_dist["good"]
            existing_report.fair_count = score_dist["fair"]
            existing_report.poor_count = score_dist["poor"]
            existing_report.fail_count = score_dist["fail"]
            existing_report.question_analysis = analysis_result["question_analysis"]
            existing_report.recommendations = report_data["recommendations"]
            existing_report.updated_at = datetime.utcnow()
        else:
            # 创建新报告
            report = ClassGradeReport(
                exercise_id=exercise_id,
                teacher_id=teacher_id,
                report_title=f"{report_data['exercise_info']['title']} - 成绩分析报告",
                report_type=report_data['exercise_info']['category'],
                total_students=basic_stats["total_attempts"],
                participated_students=basic_stats["total_attempts"],
                participation_rate=100.0,
                class_average=basic_stats["average_score"],
                median_score=basic_stats["median_score"],
                standard_deviation=basic_stats["standard_deviation"],
                excellent_count=score_dist["excellent"],
                good_count=score_dist["good"],
                fair_count=score_dist["fair"],
                poor_count=score_dist["poor"],
                fail_count=score_dist["fail"],
                question_analysis=analysis_result["question_analysis"],
                recommendations=report_data["recommendations"]
            )
            self.db.add(report)

        self.db.commit()

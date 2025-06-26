"""
成绩导出服务
"""
import io
import json
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session

from ..models.exercise import Exercise, ExerciseAttempt, StudentAnswer, Question
from ..models.user import User
from .grade_analysis_service import GradeAnalysisService


class GradeExportService:
    """成绩导出服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.grade_service = GradeAnalysisService(db)
    
    def export_exercise_grades_to_excel(self, exercise_id: int, teacher_id: int) -> bytes:
        """导出练习成绩到Excel"""
        # 获取分析数据
        analysis_data = self.grade_service.analyze_exercise_grades(exercise_id, teacher_id)
        
        # 获取练习信息
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            raise ValueError("练习不存在")
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 工作表1: 基础统计
            basic_stats_df = pd.DataFrame([analysis_data["basic_stats"]])
            basic_stats_df.to_excel(writer, sheet_name='基础统计', index=False)
            
            # 工作表2: 学生成绩详情
            students_data = []
            for student in analysis_data["student_performance"]:
                students_data.append({
                    "排名": student["rank"],
                    "学生姓名": student["student_name"],
                    "用户名": student["username"],
                    "得分": student["score"],
                    "得分率(%)": student["percentage"],
                    "用时(分钟)": round(student["time_spent"] / 60, 1),
                    "与平均分差值": student["vs_class_average"],
                    "表现等级": student["performance_level"],
                    "完成时间": student["completed_at"]
                })
            
            students_df = pd.DataFrame(students_data)
            students_df.to_excel(writer, sheet_name='学生成绩', index=False)
            
            # 工作表3: 题目分析
            questions_data = []
            for question in analysis_data["question_analysis"]:
                questions_data.append({
                    "题目ID": question["question_id"],
                    "题目内容": question["question_content"][:50] + "..." if len(question["question_content"]) > 50 else question["question_content"],
                    "题目类型": question["question_type"],
                    "难度": question["difficulty"],
                    "分值": question["points"],
                    "总尝试次数": question["total_attempts"],
                    "正确次数": question["correct_attempts"],
                    "正确率(%)": question["accuracy_rate"],
                    "平均用时(秒)": question["average_time"]
                })
            
            questions_df = pd.DataFrame(questions_data)
            questions_df.to_excel(writer, sheet_name='题目分析', index=False)
            
            # 工作表4: 分数分布
            score_dist = analysis_data["score_distribution"]
            distribution_data = [
                {"等级": "优秀(90+)", "人数": score_dist["grade_distribution"]["excellent"], "比例(%)": score_dist["grade_distribution_percentage"]["excellent"]},
                {"等级": "良好(80-89)", "人数": score_dist["grade_distribution"]["good"], "比例(%)": score_dist["grade_distribution_percentage"]["good"]},
                {"等级": "中等(70-79)", "人数": score_dist["grade_distribution"]["fair"], "比例(%)": score_dist["grade_distribution_percentage"]["fair"]},
                {"等级": "及格(60-69)", "人数": score_dist["grade_distribution"]["poor"], "比例(%)": score_dist["grade_distribution_percentage"]["poor"]},
                {"等级": "不及格(<60)", "人数": score_dist["grade_distribution"]["fail"], "比例(%)": score_dist["grade_distribution_percentage"]["fail"]}
            ]
            
            distribution_df = pd.DataFrame(distribution_data)
            distribution_df.to_excel(writer, sheet_name='分数分布', index=False)
            
            # 工作表5: 练习信息
            exercise_info = {
                "练习ID": exercise.id,
                "练习标题": exercise.title,
                "科目": exercise.subject,
                "类别": exercise.category,
                "难度": exercise.difficulty,
                "总题数": exercise.total_questions,
                "创建时间": exercise.created_at.strftime("%Y-%m-%d %H:%M:%S") if exercise.created_at else "",
                "导出时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "导出教师": teacher_id
            }
            
            exercise_df = pd.DataFrame([exercise_info])
            exercise_df.to_excel(writer, sheet_name='练习信息', index=False)
        
        output.seek(0)
        return output.getvalue()
    
    def export_teacher_overview_to_excel(self, teacher_id: int, days: int = 30) -> bytes:
        """导出教师概览数据到Excel"""
        # 获取概览数据
        overview_data = self.grade_service.get_teacher_grade_overview(teacher_id, days)
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 工作表1: 成绩统计
            grade_stats_df = pd.DataFrame([overview_data["grade_stats"]])
            grade_stats_df.to_excel(writer, sheet_name='成绩统计', index=False)
            
            # 工作表2: 趋势数据
            trend_df = pd.DataFrame(overview_data["trend_data"])
            trend_df.to_excel(writer, sheet_name='趋势数据', index=False)
            
            # 工作表3: 科目分析
            subject_df = pd.DataFrame(overview_data["subject_analysis"])
            subject_df.to_excel(writer, sheet_name='科目分析', index=False)
            
            # 工作表4: 最近活动
            activities_data = []
            for activity in overview_data["recent_activities"]:
                activities_data.append({
                    "活动类型": activity["type"],
                    "学生姓名": activity["student_name"],
                    "练习标题": activity["exercise_title"],
                    "得分": activity["score"],
                    "得分率(%)": activity["percentage"],
                    "提交时间": activity["submitted_at"]
                })
            
            activities_df = pd.DataFrame(activities_data)
            activities_df.to_excel(writer, sheet_name='最近活动', index=False)
            
            # 工作表5: 导出信息
            export_info = {
                "教师ID": teacher_id,
                "统计天数": days,
                "导出时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "数据范围": f"最近{days}天"
            }
            
            export_df = pd.DataFrame([export_info])
            export_df.to_excel(writer, sheet_name='导出信息', index=False)
        
        output.seek(0)
        return output.getvalue()
    
    def export_class_report_to_excel(self, exercise_id: int, teacher_id: int) -> bytes:
        """导出班级报告到Excel"""
        # 生成班级报告
        report_data = self.grade_service.generate_class_report(exercise_id, teacher_id)
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 工作表1: 报告摘要
            exercise_info = report_data["exercise_info"]
            summary_data = {
                "练习标题": exercise_info["title"],
                "科目": exercise_info["subject"],
                "类别": exercise_info["category"],
                "难度": exercise_info["difficulty"],
                "总题数": exercise_info["total_questions"],
                "生成时间": report_data["generated_at"]
            }
            
            summary_df = pd.DataFrame([summary_data])
            summary_df.to_excel(writer, sheet_name='报告摘要', index=False)
            
            # 工作表2: 基础统计
            basic_stats = report_data["analysis_result"]["basic_stats"]
            stats_df = pd.DataFrame([basic_stats])
            stats_df.to_excel(writer, sheet_name='基础统计', index=False)
            
            # 工作表3: 学生表现
            students_data = []
            for student in report_data["analysis_result"]["student_performance"]:
                students_data.append({
                    "排名": student["rank"],
                    "学生姓名": student["student_name"],
                    "得分": student["score"],
                    "得分率(%)": student["percentage"],
                    "用时(分钟)": round(student["time_spent"] / 60, 1),
                    "表现等级": student["performance_level"]
                })
            
            students_df = pd.DataFrame(students_data)
            students_df.to_excel(writer, sheet_name='学生表现', index=False)
            
            # 工作表4: 题目分析
            questions_data = []
            for question in report_data["analysis_result"]["question_analysis"]:
                questions_data.append({
                    "题目ID": question["question_id"],
                    "题目类型": question["question_type"],
                    "难度": question["difficulty"],
                    "正确率(%)": question["accuracy_rate"],
                    "总尝试次数": question["total_attempts"],
                    "平均用时(秒)": question["average_time"]
                })
            
            questions_df = pd.DataFrame(questions_data)
            questions_df.to_excel(writer, sheet_name='题目分析', index=False)
            
            # 工作表5: 教学建议
            recommendations_data = []
            for rec in report_data["recommendations"]:
                recommendations_data.append({
                    "建议类型": rec["type"],
                    "建议标题": rec["title"],
                    "具体建议": rec["suggestion"]
                })
            
            recommendations_df = pd.DataFrame(recommendations_data)
            recommendations_df.to_excel(writer, sheet_name='教学建议', index=False)
        
        output.seek(0)
        return output.getvalue()
    
    def export_student_answers_to_excel(self, exercise_id: int, teacher_id: int) -> bytes:
        """导出学生答题详情到Excel"""
        # 验证权限
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise or exercise.created_by != teacher_id:
            raise ValueError("无权限访问此练习")
        
        # 获取所有答题记录
        attempts = self.db.query(ExerciseAttempt).filter(
            ExerciseAttempt.exercise_id == exercise_id,
            ExerciseAttempt.is_submitted == True
        ).all()
        
        # 获取题目信息
        questions = self.db.query(Question).filter(Question.exercise_id == exercise_id).all()
        question_map = {q.id: q for q in questions}
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 为每个学生创建一个工作表
            for attempt in attempts:
                # 获取学生信息
                student = self.db.query(User).filter(User.id == attempt.student_id).first()
                if not student:
                    continue
                
                # 获取学生的答案
                answers = self.db.query(StudentAnswer).filter(
                    StudentAnswer.attempt_id == attempt.id
                ).all()
                
                # 准备答案数据
                answers_data = []
                for answer in answers:
                    question = question_map.get(answer.question_id)
                    if question:
                        answers_data.append({
                            "题目序号": question.order_num,
                            "题目内容": question.content[:100] + "..." if len(question.content) > 100 else question.content,
                            "题目类型": question.question_type,
                            "正确答案": question.correct_answer,
                            "学生答案": answer.answer_content,
                            "是否正确": "正确" if answer.is_correct else "错误",
                            "得分": answer.score,
                            "用时(秒)": answer.time_spent,
                            "答题时间": answer.answered_at.strftime("%Y-%m-%d %H:%M:%S") if answer.answered_at else ""
                        })
                
                # 创建DataFrame并写入工作表
                if answers_data:
                    answers_df = pd.DataFrame(answers_data)
                    sheet_name = f"{student.full_name}({student.username})"[:31]  # Excel工作表名称限制
                    answers_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 创建汇总工作表
            summary_data = []
            for attempt in attempts:
                student = self.db.query(User).filter(User.id == attempt.student_id).first()
                if student:
                    summary_data.append({
                        "学生姓名": student.full_name,
                        "用户名": student.username,
                        "总分": attempt.score,
                        "满分": attempt.max_score,
                        "得分率(%)": (attempt.score / attempt.max_score * 100) if attempt.max_score > 0 else 0,
                        "用时(分钟)": round(attempt.time_spent / 60, 1),
                        "开始时间": attempt.started_at.strftime("%Y-%m-%d %H:%M:%S") if attempt.started_at else "",
                        "完成时间": attempt.completed_at.strftime("%Y-%m-%d %H:%M:%S") if attempt.completed_at else ""
                    })
            
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='成绩汇总', index=False)
        
        output.seek(0)
        return output.getvalue()

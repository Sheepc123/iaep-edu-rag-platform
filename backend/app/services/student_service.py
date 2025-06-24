"""
学生档案服务层
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import json

from ..models.user import User, StudentProfile
from ..schemas.auth import StudentProfileCreate, StudentProfileUpdate


class StudentService:
    """学生服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_student_profile(self, user_id: int) -> Optional[StudentProfile]:
        """获取学生档案"""
        return self.db.query(StudentProfile).filter(
            StudentProfile.user_id == user_id
        ).first()
    
    def create_student_profile(self, user_id: int, profile_data: StudentProfileCreate) -> StudentProfile:
        """创建学生档案"""
        # 检查用户是否存在且为学生角色
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只有学生用户可以创建学生档案"
            )
        
        # 检查是否已有档案
        existing_profile = self.get_student_profile(user_id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学生档案已存在"
            )
        
        # 检查学号是否重复
        if profile_data.student_id:
            existing_student = self.db.query(StudentProfile).filter(
                StudentProfile.student_id == profile_data.student_id
            ).first()
            if existing_student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="学号已存在"
                )
        
        # 创建学生档案
        profile = StudentProfile(
            user_id=user_id,
            **profile_data.dict(exclude_unset=True)
        )
        
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        
        return profile
    
    def update_student_profile(self, user_id: int, profile_data: StudentProfileUpdate) -> StudentProfile:
        """更新学生档案"""
        profile = self.get_student_profile(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生档案不存在"
            )
        
        # 检查学号是否重复（如果要更新学号）
        if profile_data.student_id and profile_data.student_id != profile.student_id:
            existing_student = self.db.query(StudentProfile).filter(
                StudentProfile.student_id == profile_data.student_id,
                StudentProfile.id != profile.id
            ).first()
            if existing_student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="学号已存在"
                )
        
        # 更新档案信息
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        self.db.commit()
        self.db.refresh(profile)
        
        return profile
    
    def update_learning_stats(self, user_id: int, stats_data: dict):
        """更新学习统计数据"""
        profile = self.get_student_profile(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生档案不存在"
            )
        
        # 更新统计数据
        if 'study_time' in stats_data:
            profile.total_study_time += stats_data['study_time']
        
        if 'exercises' in stats_data:
            profile.total_exercises += stats_data['exercises']
        
        if 'correct_exercises' in stats_data:
            profile.correct_exercises += stats_data['correct_exercises']
        
        if 'courses' in stats_data:
            profile.total_courses += stats_data['courses']
        
        if 'completed_courses' in stats_data:
            profile.completed_courses += stats_data['completed_courses']
        
        self.db.commit()
        self.db.refresh(profile)
        
        return profile
    
    def set_learning_preferences(self, user_id: int, preferences: dict):
        """设置学习偏好"""
        profile = self.get_student_profile(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生档案不存在"
            )
        
        # 更新偏好设置
        if 'subjects' in preferences:
            profile.preferred_subjects = json.dumps(preferences['subjects'], ensure_ascii=False)
        
        if 'goals' in preferences:
            profile.learning_goals = preferences['goals']
        
        self.db.commit()
        self.db.refresh(profile)
        
        return profile
    
    def get_learning_preferences(self, user_id: int) -> dict:
        """获取学习偏好"""
        profile = self.get_student_profile(user_id)
        if not profile:
            return {}
        
        preferences = {}
        
        if profile.preferred_subjects:
            try:
                preferences['subjects'] = json.loads(profile.preferred_subjects)
            except json.JSONDecodeError:
                preferences['subjects'] = []
        else:
            preferences['subjects'] = []
        
        preferences['goals'] = profile.learning_goals or ""
        
        return preferences
    
    def get_learning_stats(self, user_id: int) -> dict:
        """获取学习统计数据"""
        profile = self.get_student_profile(user_id)
        if not profile:
            return {
                'total_study_time': 0,
                'total_exercises': 0,
                'correct_exercises': 0,
                'accuracy_rate': 0.0,
                'total_courses': 0,
                'completed_courses': 0,
                'completion_rate': 0.0
            }
        
        # 计算正确率
        accuracy_rate = 0.0
        if profile.total_exercises > 0:
            accuracy_rate = (profile.correct_exercises / profile.total_exercises) * 100
        
        # 计算完成率
        completion_rate = 0.0
        if profile.total_courses > 0:
            completion_rate = (profile.completed_courses / profile.total_courses) * 100
        
        return {
            'total_study_time': profile.total_study_time,
            'total_exercises': profile.total_exercises,
            'correct_exercises': profile.correct_exercises,
            'accuracy_rate': round(accuracy_rate, 2),
            'total_courses': profile.total_courses,
            'completed_courses': profile.completed_courses,
            'completion_rate': round(completion_rate, 2)
        }
    
    def get_student_list(self, skip: int = 0, limit: int = 100) -> list:
        """获取学生列表（管理员功能）"""
        students = self.db.query(StudentProfile).join(User).filter(
            User.role == "student",
            User.is_active == True
        ).offset(skip).limit(limit).all()
        
        return students
    
    def search_students(self, query: str, skip: int = 0, limit: int = 100) -> list:
        """搜索学生（管理员功能）"""
        students = self.db.query(StudentProfile).join(User).filter(
            User.role == "student",
            User.is_active == True,
            (User.full_name.contains(query) | 
             User.username.contains(query) |
             StudentProfile.student_id.contains(query) |
             StudentProfile.school.contains(query))
        ).offset(skip).limit(limit).all()
        
        return students

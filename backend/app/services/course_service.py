"""
课程管理服务层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from fastapi import HTTPException, status
from typing import Optional, List, Tuple
from datetime import datetime
import json

from ..models.course import Course, Lesson, CourseEnrollment, LessonProgress, StudyPlan
from ..models.user import User
from ..schemas.course import (
    CourseCreate, CourseUpdate, LessonCreate, LessonUpdate,
    CourseListQuery, LessonProgressUpdate, CourseRatingCreate,
    StudyPlanCreate
)


class CourseService:
    """课程服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_course(self, course_data: CourseCreate, instructor_id: int) -> Course:
        """创建课程"""
        # 获取教师信息
        instructor = self.db.query(User).filter(User.id == instructor_id).first()
        if not instructor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="教师不存在"
            )
        
        # 创建课程
        course = Course(
            title=course_data.title,
            description=course_data.description,
            category=course_data.category,
            difficulty=course_data.difficulty.value,
            duration=course_data.duration,
            cover_image=course_data.cover_image,
            instructor_id=instructor_id,
            instructor_name=instructor.full_name,
            is_published=course_data.is_published
        )
        
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        
        return course

    def get_teacher_courses(
        self,
        teacher_id: int,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_published: Optional[bool] = None
    ) -> Tuple[List[Course], int]:
        """获取教师的课程列表"""
        query = self.db.query(Course).filter(Course.instructor_id == teacher_id)

        # 搜索过滤
        if search:
            query = query.filter(
                or_(
                    Course.title.contains(search),
                    Course.description.contains(search)
                )
            )

        # 分类过滤
        if category:
            query = query.filter(Course.category == category)

        # 发布状态过滤
        if is_published is not None:
            query = query.filter(Course.is_published == is_published)

        # 获取总数
        total = query.count()

        # 分页和排序
        courses = query.order_by(desc(Course.updated_at)).offset(skip).limit(limit).all()

        return courses, total

    def get_teacher_course_detail(self, course_id: int, teacher_id: int) -> Course:
        """获取教师课程详情"""
        course = self.db.query(Course).filter(
            and_(
                Course.id == course_id,
                Course.instructor_id == teacher_id
            )
        ).first()

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课程不存在或您没有权限访问"
            )

        return course

    def update_teacher_course(
        self,
        course_id: int,
        teacher_id: int,
        course_data: CourseUpdate
    ) -> Course:
        """更新教师课程"""
        course = self.get_teacher_course_detail(course_id, teacher_id)

        # 更新课程信息
        for field, value in course_data.dict(exclude_unset=True).items():
            if field == "difficulty" and value:
                setattr(course, field, value.value)
            else:
                setattr(course, field, value)

        course.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(course)

        return course

    def delete_teacher_course(self, course_id: int, teacher_id: int) -> bool:
        """删除教师课程"""
        course = self.get_teacher_course_detail(course_id, teacher_id)

        # 检查是否有学生已注册
        enrollment_count = self.db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).count()

        if enrollment_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="已有学生注册此课程，无法删除"
            )

        # 删除相关的课时
        self.db.query(Lesson).filter(Lesson.course_id == course_id).delete()

        # 删除课程
        self.db.delete(course)
        self.db.commit()

        return True

    def toggle_course_publish(self, course_id: int, teacher_id: int) -> Course:
        """切换课程发布状态"""
        course = self.get_teacher_course_detail(course_id, teacher_id)

        # 如果要发布课程，检查是否满足发布条件
        if not course.is_published:
            # 检查是否有课时
            lesson_count = self.db.query(Lesson).filter(Lesson.course_id == course_id).count()
            if lesson_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="课程至少需要包含一个课时才能发布"
                )

        course.is_published = not course.is_published
        course.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(course)

        return course

    def get_teacher_course_statistics(self, teacher_id: int) -> dict:
        """获取教师课程统计信息"""
        # 总课程数
        total_courses = self.db.query(Course).filter(Course.instructor_id == teacher_id).count()

        # 已发布课程数
        published_courses = self.db.query(Course).filter(
            and_(
                Course.instructor_id == teacher_id,
                Course.is_published == True
            )
        ).count()

        # 总学员数
        total_students = self.db.query(func.count(CourseEnrollment.id)).join(
            Course, CourseEnrollment.course_id == Course.id
        ).filter(Course.instructor_id == teacher_id).scalar() or 0

        # 平均评分
        avg_rating = self.db.query(func.avg(Course.rating)).filter(
            and_(
                Course.instructor_id == teacher_id,
                Course.rating_count > 0
            )
        ).scalar() or 0.0

        return {
            "total_courses": total_courses,
            "published_courses": published_courses,
            "draft_courses": total_courses - published_courses,
            "total_students": total_students,
            "average_rating": round(float(avg_rating), 1) if avg_rating else 0.0
        }
    
    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """根据ID获取课程"""
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def update_course(self, course_id: int, course_data: CourseUpdate, instructor_id: int) -> Course:
        """更新课程"""
        course = self.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课程不存在"
            )
        
        # 检查权限（只有课程创建者或管理员可以修改）
        if course.instructor_id != instructor_id:
            # 这里可以添加管理员权限检查
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此课程"
            )
        
        # 更新课程信息
        update_data = course_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "difficulty" and value:
                setattr(course, field, value.value)
            else:
                setattr(course, field, value)
        
        self.db.commit()
        self.db.refresh(course)
        
        return course
    
    def delete_course(self, course_id: int, instructor_id: int) -> bool:
        """删除课程"""
        course = self.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课程不存在"
            )
        
        # 检查权限
        if course.instructor_id != instructor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此课程"
            )
        
        # 检查是否有学生注册
        enrollment_count = self.db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).count()
        
        if enrollment_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="课程已有学生注册，无法删除"
            )
        
        # 删除相关课时
        self.db.query(Lesson).filter(Lesson.course_id == course_id).delete()
        
        # 删除课程
        self.db.delete(course)
        self.db.commit()
        
        return True
    
    def get_courses(self, query: CourseListQuery, user_id: Optional[int] = None) -> Tuple[List[Course], int]:
        """获取课程列表"""
        # 构建查询
        db_query = self.db.query(Course).filter(Course.is_active == True)
        
        # 应用过滤条件
        if query.category:
            db_query = db_query.filter(Course.category == query.category)
        
        if query.difficulty:
            # 处理difficulty参数，支持字符串和枚举类型
            difficulty_value = query.difficulty.value if hasattr(query.difficulty, 'value') else query.difficulty
            db_query = db_query.filter(Course.difficulty == difficulty_value)
        
        if query.instructor_id:
            db_query = db_query.filter(Course.instructor_id == query.instructor_id)
        
        if query.is_published is not None:
            db_query = db_query.filter(Course.is_published == query.is_published)
        
        if query.search:
            search_term = f"%{query.search}%"
            db_query = db_query.filter(
                or_(
                    Course.title.contains(query.search),
                    Course.description.contains(query.search),
                    Course.instructor_name.contains(query.search)
                )
            )
        
        # 获取总数
        total = db_query.count()
        
        # 应用排序
        if query.sort_by == "rating":
            order_func = desc if query.sort_order == "desc" else asc
            db_query = db_query.order_by(order_func(Course.rating))
        elif query.sort_by == "enrolled_students":
            order_func = desc if query.sort_order == "desc" else asc
            db_query = db_query.order_by(order_func(Course.enrolled_students))
        else:  # 默认按创建时间排序
            order_func = desc if query.sort_order == "desc" else asc
            db_query = db_query.order_by(order_func(Course.created_at))
        
        # 应用分页
        courses = db_query.offset(query.skip).limit(query.limit).all()

        # 如果提供了用户ID，添加注册状态信息
        if user_id:
            # 获取用户的所有注册记录
            enrollments = self.db.query(CourseEnrollment).filter(
                and_(
                    CourseEnrollment.student_id == user_id,
                    CourseEnrollment.is_active == True
                )
            ).all()

            # 创建课程ID到注册记录的映射
            enrollment_map = {e.course_id: e for e in enrollments}

            # 为每个课程添加注册状态
            for course in courses:
                enrollment = enrollment_map.get(course.id)
                course.is_enrolled = enrollment is not None
                course.enrollment_id = enrollment.id if enrollment else None
        else:
            # 未登录用户，所有课程都标记为未注册
            for course in courses:
                course.is_enrolled = False
                course.enrollment_id = None

        return courses, total
    
    def enroll_course(self, course_id: int, student_id: int) -> CourseEnrollment:
        """学生注册课程"""
        # 检查课程是否存在
        course = self.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课程不存在"
            )
        
        if not course.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="课程未发布，无法注册"
            )
        
        # 检查是否已经注册
        existing_enrollment = self.db.query(CourseEnrollment).filter(
            and_(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.student_id == student_id
            )
        ).first()
        
        if existing_enrollment:
            if existing_enrollment.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="已经注册过此课程"
                )
            else:
                # 重新激活注册
                existing_enrollment.is_active = True
                self.db.commit()
                return existing_enrollment
        
        # 创建新的注册记录
        enrollment = CourseEnrollment(
            course_id=course_id,
            student_id=student_id,
            total_study_time=0,
            progress_percentage=0.0,
            completed_lessons=0,
            is_completed=False,
            is_active=True
        )
        
        self.db.add(enrollment)
        
        # 更新课程注册人数
        course.enrolled_students += 1
        
        self.db.commit()
        self.db.refresh(enrollment)
        
        return enrollment
    
    def get_student_enrollments(self, student_id: int) -> List[CourseEnrollment]:
        """获取学生的课程注册列表"""
        from sqlalchemy.orm import joinedload

        return self.db.query(CourseEnrollment).options(
            joinedload(CourseEnrollment.course)
        ).filter(
            and_(
                CourseEnrollment.student_id == student_id,
                CourseEnrollment.is_active == True
            )
        ).all()
    
    def get_course_enrollment(self, course_id: int, student_id: int) -> Optional[CourseEnrollment]:
        """获取学生的课程注册信息"""
        return self.db.query(CourseEnrollment).filter(
            and_(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.student_id == student_id,
                CourseEnrollment.is_active == True
            )
        ).first()
    
    def update_course_progress(self, course_id: int, student_id: int):
        """更新课程学习进度"""
        enrollment = self.get_course_enrollment(course_id, student_id)
        if not enrollment:
            return
        
        # 获取课程总课时数
        total_lessons = self.db.query(Lesson).filter(
            and_(
                Lesson.course_id == course_id,
                Lesson.is_published == True
            )
        ).count()
        
        if total_lessons == 0:
            return
        
        # 获取已完成课时数
        completed_lessons = self.db.query(LessonProgress).filter(
            and_(
                LessonProgress.student_id == student_id,
                LessonProgress.is_completed == True
            )
        ).join(Lesson).filter(Lesson.course_id == course_id).count()
        
        # 计算进度百分比
        progress_percentage = (completed_lessons / total_lessons) * 100
        
        # 更新注册信息
        enrollment.completed_lessons = completed_lessons
        enrollment.progress_percentage = progress_percentage
        enrollment.is_completed = progress_percentage >= 100
        enrollment.last_accessed = datetime.utcnow()
        
        if enrollment.is_completed and not enrollment.completed_at:
            enrollment.completed_at = datetime.utcnow()
        
        self.db.commit()
    
    def rate_course(self, course_id: int, student_id: int, rating_data: CourseRatingCreate):
        """课程评分"""
        # 检查是否已注册课程
        enrollment = self.get_course_enrollment(course_id, student_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您尚未注册此课程"
            )
        
        # 更新注册记录中的评分
        enrollment.rating = rating_data.rating
        enrollment.review = rating_data.review
        
        # 重新计算课程平均评分
        course = self.get_course_by_id(course_id)
        if course:
            # 获取所有评分
            ratings = self.db.query(CourseEnrollment.rating).filter(
                and_(
                    CourseEnrollment.course_id == course_id,
                    CourseEnrollment.rating.isnot(None)
                )
            ).all()
            
            if ratings:
                total_rating = sum(r[0] for r in ratings)
                course.rating = total_rating / len(ratings)
                course.rating_count = len(ratings)
            
        self.db.commit()
    
    def get_course_statistics(self, instructor_id: Optional[int] = None) -> dict:
        """获取课程统计信息"""
        query = self.db.query(Course)
        
        if instructor_id:
            query = query.filter(Course.instructor_id == instructor_id)
        
        total_courses = query.count()
        published_courses = query.filter(Course.is_published == True).count()
        
        # 获取总学生数（去重）
        total_students = self.db.query(CourseEnrollment.student_id).distinct().count()
        
        # 获取总课时数
        total_lessons = self.db.query(Lesson).count()
        
        # 计算平均评分
        avg_rating = self.db.query(func.avg(Course.rating)).scalar() or 0.0
        
        # 计算完成率
        total_enrollments = self.db.query(CourseEnrollment).count()
        completed_enrollments = self.db.query(CourseEnrollment).filter(
            CourseEnrollment.is_completed == True
        ).count()
        
        completion_rate = 0.0
        if total_enrollments > 0:
            completion_rate = (completed_enrollments / total_enrollments) * 100
        
        return {
            "total_courses": total_courses,
            "published_courses": published_courses,
            "total_students": total_students,
            "total_lessons": total_lessons,
            "average_rating": round(avg_rating, 2),
            "completion_rate": round(completion_rate, 2)
        }


class LessonService:
    """课时服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_lesson(self, course_id: int, lesson_data: LessonCreate, instructor_id: int) -> Lesson:
        """创建课时"""
        # 检查课程是否存在且有权限
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课程不存在"
            )

        if course.instructor_id != instructor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权在此课程中创建课时"
            )

        # 检查课时顺序是否重复
        existing_lesson = self.db.query(Lesson).filter(
            and_(
                Lesson.course_id == course_id,
                Lesson.lesson_order == lesson_data.lesson_order
            )
        ).first()

        if existing_lesson:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="课时顺序已存在"
            )

        # 创建课时
        lesson = Lesson(
            course_id=course_id,
            title=lesson_data.title,
            description=lesson_data.description,
            content=lesson_data.content,
            lesson_order=lesson_data.lesson_order,
            duration=lesson_data.duration,
            lesson_type=lesson_data.lesson_type.value,
            video_url=lesson_data.video_url,
            materials=lesson_data.materials,
            is_published=lesson_data.is_published,
            is_free=lesson_data.is_free
        )

        self.db.add(lesson)

        # 更新课程总课时数
        course.total_lessons = self.db.query(Lesson).filter(
            Lesson.course_id == course_id
        ).count() + 1

        self.db.commit()
        self.db.refresh(lesson)

        return lesson

    def get_lesson_by_id(self, lesson_id: int) -> Optional[Lesson]:
        """根据ID获取课时"""
        return self.db.query(Lesson).filter(Lesson.id == lesson_id).first()

    def get_course_lessons(self, course_id: int, include_unpublished: bool = False) -> List[Lesson]:
        """获取课程的所有课时"""
        query = self.db.query(Lesson).filter(Lesson.course_id == course_id)

        if not include_unpublished:
            query = query.filter(Lesson.is_published == True)

        return query.order_by(Lesson.lesson_order).all()

    def update_lesson(self, lesson_id: int, lesson_data: LessonUpdate, instructor_id: int) -> Lesson:
        """更新课时"""
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课时不存在"
            )

        # 检查权限
        course = self.db.query(Course).filter(Course.id == lesson.course_id).first()
        if not course or course.instructor_id != instructor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此课时"
            )

        # 检查课时顺序是否重复（如果要更新顺序）
        if lesson_data.lesson_order and lesson_data.lesson_order != lesson.lesson_order:
            existing_lesson = self.db.query(Lesson).filter(
                and_(
                    Lesson.course_id == lesson.course_id,
                    Lesson.lesson_order == lesson_data.lesson_order,
                    Lesson.id != lesson_id
                )
            ).first()

            if existing_lesson:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="课时顺序已存在"
                )

        # 更新课时信息
        update_data = lesson_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "lesson_type" and value:
                setattr(lesson, field, value.value)
            else:
                setattr(lesson, field, value)

        self.db.commit()
        self.db.refresh(lesson)

        return lesson

    def delete_lesson(self, lesson_id: int, instructor_id: int) -> bool:
        """删除课时"""
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课时不存在"
            )

        # 检查权限
        course = self.db.query(Course).filter(Course.id == lesson.course_id).first()
        if not course or course.instructor_id != instructor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此课时"
            )

        # 删除相关的学习进度记录
        self.db.query(LessonProgress).filter(
            LessonProgress.lesson_id == lesson_id
        ).delete()

        # 删除课时
        self.db.delete(lesson)

        # 更新课程总课时数
        course.total_lessons = self.db.query(Lesson).filter(
            Lesson.course_id == lesson.course_id
        ).count() - 1

        self.db.commit()

        return True

    def update_lesson_progress(self, lesson_id: int, student_id: int,
                             progress_data: LessonProgressUpdate) -> LessonProgress:
        """更新课时学习进度"""
        # 检查课时是否存在
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="课时不存在"
            )

        # 检查学生是否注册了该课程
        course_service = CourseService(self.db)
        enrollment = course_service.get_course_enrollment(lesson.course_id, student_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您尚未注册此课程"
            )

        # 获取或创建学习进度记录
        progress = self.db.query(LessonProgress).filter(
            and_(
                LessonProgress.lesson_id == lesson_id,
                LessonProgress.student_id == student_id
            )
        ).first()

        if not progress:
            progress = LessonProgress(
                lesson_id=lesson_id,
                student_id=student_id,
                progress_percentage=0.0,
                watch_time=0,
                is_completed=False
            )
            self.db.add(progress)

        # 更新进度信息
        progress.progress_percentage = progress_data.progress_percentage
        if progress_data.watch_time is not None:
            progress.watch_time = progress_data.watch_time
        progress.is_completed = progress_data.is_completed
        if progress_data.notes:
            progress.notes = progress_data.notes
        progress.last_accessed = datetime.utcnow()

        if progress_data.is_completed and not progress.completed_at:
            progress.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(progress)

        # 更新课程整体进度
        course_service.update_course_progress(lesson.course_id, student_id)

        return progress

    def get_lesson_progress(self, lesson_id: int, student_id: int) -> Optional[LessonProgress]:
        """获取课时学习进度"""
        return self.db.query(LessonProgress).filter(
            and_(
                LessonProgress.lesson_id == lesson_id,
                LessonProgress.student_id == student_id
            )
        ).first()

    def get_student_lesson_progresses(self, course_id: int, student_id: int) -> List[LessonProgress]:
        """获取学生在某课程中的所有课时进度"""
        return self.db.query(LessonProgress).join(Lesson).filter(
            and_(
                Lesson.course_id == course_id,
                LessonProgress.student_id == student_id
            )
        ).order_by(Lesson.lesson_order).all()

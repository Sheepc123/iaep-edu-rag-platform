"""
用户管理API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from ....core.database import get_db
from ....schemas.auth import (
    UserUpdate, UserInfo, StudentProfileCreate, StudentProfileUpdate,
    StudentProfileResponse, TeacherProfileCreate, TeacherProfileUpdate,
    TeacherProfileResponse, AuthResponse
)
from ....services.auth_service import AuthService
from ....services.student_service import StudentService
from ....models.user import User
from ...dependencies import (
    get_current_active_user, get_current_student, get_current_teacher, get_current_admin,
    get_auth_service, get_pagination_params
)


router = APIRouter()


@router.get("/profile", response_model=UserInfo, summary="获取用户资料")
async def get_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """获取当前用户的详细资料"""
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        avatar=current_user.avatar,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.put("/profile", response_model=UserInfo, summary="更新用户资料")
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    更新用户基本资料
    
    - **full_name**: 真实姓名
    - **phone**: 手机号码
    - **avatar**: 头像URL
    """
    try:
        updated_user = auth_service.update_user_info(current_user.id, user_data)
        
        return UserInfo(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            full_name=updated_user.full_name,
            phone=updated_user.phone,
            avatar=updated_user.avatar,
            role=updated_user.role,
            is_active=updated_user.is_active,
            is_verified=updated_user.is_verified,
            created_at=updated_user.created_at,
            last_login=updated_user.last_login
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户资料失败"
        )


@router.get("/student-profile", response_model=StudentProfileResponse, summary="获取学生档案")
async def get_student_profile(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前学生的详细档案"""
    try:
        student_service = StudentService(db)
        profile = student_service.get_student_profile(current_user.id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生档案不存在"
            )
        
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学生档案失败"
        )


@router.post("/student-profile", response_model=StudentProfileResponse, summary="创建学生档案")
async def create_student_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    创建学生档案
    
    - **student_id**: 学号
    - **school**: 学校
    - **college**: 学院
    - **major**: 专业
    - **grade**: 年级
    - **class_name**: 班级
    """
    try:
        student_service = StudentService(db)
        profile = student_service.create_student_profile(current_user.id, profile_data)
        
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建学生档案失败"
        )


@router.put("/student-profile", response_model=StudentProfileResponse, summary="更新学生档案")
async def update_student_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    更新学生档案
    
    - **student_id**: 学号
    - **school**: 学校
    - **college**: 学院
    - **major**: 专业
    - **grade**: 年级
    - **class_name**: 班级
    - **preferred_subjects**: 偏好科目
    - **learning_goals**: 学习目标
    """
    try:
        student_service = StudentService(db)
        profile = student_service.update_student_profile(current_user.id, profile_data)
        
        return profile
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新学生档案失败"
        )


@router.get("/learning-stats", response_model=dict, summary="获取学习统计")
async def get_learning_stats(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取学生学习统计数据"""
    try:
        student_service = StudentService(db)
        stats = student_service.get_learning_stats(current_user.id)
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学习统计失败"
        )


@router.get("/learning-preferences", response_model=dict, summary="获取学习偏好")
async def get_learning_preferences(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """获取学生学习偏好设置"""
    try:
        student_service = StudentService(db)
        preferences = student_service.get_learning_preferences(current_user.id)
        
        return {
            "success": True,
            "data": preferences
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学习偏好失败"
        )


@router.post("/learning-preferences", response_model=AuthResponse, summary="设置学习偏好")
async def set_learning_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Any:
    """
    设置学生学习偏好
    
    - **subjects**: 偏好科目列表
    - **goals**: 学习目标
    """
    try:
        student_service = StudentService(db)
        student_service.set_learning_preferences(current_user.id, preferences)
        
        return AuthResponse(
            success=True,
            message="学习偏好设置成功"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="设置学习偏好失败"
        )


# 管理员功能
@router.get("/list", response_model=List[UserInfo], summary="获取用户列表")
async def get_user_list(
    pagination: dict = Depends(get_pagination_params),
    current_user: User = Depends(get_current_admin),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """获取用户列表（管理员功能）"""
    try:
        # 这里需要在AuthService中添加获取用户列表的方法
        # users = auth_service.get_user_list(pagination["skip"], pagination["limit"])
        # 暂时返回空列表
        return []
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表失败"
        )


@router.get("/{user_id}", response_model=UserInfo, summary="获取指定用户信息")
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """获取指定用户的详细信息"""
    try:
        # 权限检查：管理员可以访问所有用户数据，普通用户只能访问自己的数据
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问其他用户的数据"
            )

        user = auth_service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            avatar=user.avatar,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )


@router.get("/teacher-profile", response_model=TeacherProfileResponse, summary="获取教师档案")
async def get_teacher_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前教师的详细档案"""
    try:
        # 检查用户是否为教师
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有教师可以访问教师档案"
            )

        # 获取教师档案
        from ....models.user import TeacherProfile
        teacher_profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == current_user.id).first()

        if not teacher_profile:
            # 如果没有教师档案，创建一个默认的
            from ....models.user import TeacherProfile
            teacher_profile = TeacherProfile(
                user_id=current_user.id,
                teacher_id=f"T{current_user.id:06d}",
                department="",
                title="",
                specialization="",
                total_courses=0,
                total_students=0,
                teaching_years=0,
                rating=0.0,
                bio=""
            )
            db.add(teacher_profile)
            db.commit()
            db.refresh(teacher_profile)

        return teacher_profile

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取教师档案失败"
        )


@router.put("/teacher-profile", response_model=TeacherProfileResponse, summary="更新教师档案")
async def update_teacher_profile(
    profile_data: TeacherProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """更新教师档案信息"""
    try:
        # 检查用户是否为教师
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有教师可以更新教师档案"
            )

        # 获取教师档案
        from ....models.user import TeacherProfile
        teacher_profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == current_user.id).first()

        if not teacher_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="教师档案不存在"
            )

        # 更新档案信息
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(teacher_profile, field, value)

        db.commit()
        db.refresh(teacher_profile)

        return teacher_profile

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新教师档案失败"
        )


# 教师功能：学生管理
@router.get("/students", response_model=dict, summary="获取学生列表")
async def get_students_list(
    course_id: int = None,
    skip: int = 0,
    limit: int = 20,
    search: str = None,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取学生列表（教师功能）

    - **course_id**: 可选，筛选特定课程的学生
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数
    - **search**: 搜索关键词（姓名、邮箱、学号）
    """
    try:
        from ....models.course import CourseEnrollment
        from ....models.user import StudentProfile

        # 构建查询
        query = db.query(User).join(StudentProfile, User.id == StudentProfile.user_id)

        # 如果指定了课程ID，只返回该课程的学生
        if course_id:
            # 验证教师是否有权限查看该课程的学生
            from ....models.course import Course
            course = db.query(Course).filter(
                Course.id == course_id,
                Course.instructor_id == current_user.id
            ).first()

            if not course:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限查看该课程的学生"
                )

            # 只返回注册了该课程的学生
            query = query.join(CourseEnrollment, User.id == CourseEnrollment.student_id).filter(
                CourseEnrollment.course_id == course_id
            )
        else:
            # 返回所有注册了教师课程的学生
            teacher_courses = db.query(Course.id).filter(Course.instructor_id == current_user.id).subquery()
            query = query.join(CourseEnrollment, User.id == CourseEnrollment.student_id).filter(
                CourseEnrollment.course_id.in_(teacher_courses)
            ).distinct()

        # 搜索过滤
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.full_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.username.ilike(search_pattern),
                    StudentProfile.student_id.ilike(search_pattern)
                )
            )

        # 获取总数
        total = query.count()

        # 分页查询
        students = query.offset(skip).limit(limit).all()

        # 构建返回数据
        student_list = []
        for student in students:
            student_profile = student.student_profile

            # 获取学生的课程注册信息
            enrollments = db.query(CourseEnrollment).join(Course).filter(
                CourseEnrollment.student_id == student.id,
                Course.instructor_id == current_user.id
            ).all()

            student_info = {
                "id": student.id,
                "username": student.username,
                "full_name": student.full_name,
                "email": student.email,
                "avatar": getattr(student, 'avatar', None),
                "student_id": student_profile.student_id if student_profile else None,
                "school": student_profile.school if student_profile else None,
                "college": student_profile.college if student_profile else None,
                "major": student_profile.major if student_profile else None,
                "grade": student_profile.grade if student_profile else None,
                "class_name": student_profile.class_name if student_profile else None,
                "total_courses": len(enrollments),
                "total_study_time": sum(e.total_study_time for e in enrollments),
                "average_progress": sum(e.progress_percentage for e in enrollments) / len(enrollments) if enrollments else 0,
                "last_active": max(e.last_accessed for e in enrollments if e.last_accessed) if enrollments else None,
                "created_at": student.created_at.isoformat() if student.created_at else None
            }
            student_list.append(student_info)

        return {
            "students": student_list,
            "total": total,
            "skip": skip,
            "limit": limit
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学生列表失败"
        )


@router.get("/students/{student_id}", response_model=dict, summary="获取学生详细信息")
async def get_student_detail(
    student_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
) -> Any:
    """
    获取学生详细信息（教师功能）

    - **student_id**: 学生ID
    """
    try:
        from ....models.course import CourseEnrollment, Course
        from ....models.user import StudentProfile
        from ....models.exercise import ExerciseAttempt

        # 获取学生基本信息
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生不存在"
            )

        # 验证教师是否有权限查看该学生（学生必须注册了教师的课程）
        teacher_courses = db.query(Course.id).filter(Course.instructor_id == current_user.id).subquery()
        enrollment_exists = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id == student_id,
            CourseEnrollment.course_id.in_(teacher_courses)
        ).first()

        if not enrollment_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限查看该学生信息"
            )

        # 获取学生档案
        student_profile = student.student_profile

        # 获取学生在教师课程中的注册信息
        enrollments = db.query(CourseEnrollment).join(Course).filter(
            CourseEnrollment.student_id == student_id,
            Course.instructor_id == current_user.id
        ).all()

        # 获取学生的练习记录
        exercise_attempts = db.query(ExerciseAttempt).join(
            Course, ExerciseAttempt.exercise_id == Course.id  # 这里需要根据实际的练习模型调整
        ).filter(
            ExerciseAttempt.student_id == student_id,
            Course.instructor_id == current_user.id
        ).limit(10).all()

        # 构建课程注册信息
        enrollment_list = []
        for enrollment in enrollments:
            course = enrollment.course
            enrollment_info = {
                "id": enrollment.id,
                "course_id": course.id,
                "course_title": course.title,
                "course_category": course.category,
                "progress_percentage": enrollment.progress_percentage,
                "completed_lessons": enrollment.completed_lessons,
                "total_study_time": enrollment.total_study_time,
                "rating": enrollment.rating,
                "enrolled_at": enrollment.enrolled_at.isoformat() if enrollment.enrolled_at else None,
                "last_accessed": enrollment.last_accessed.isoformat() if enrollment.last_accessed else None,
                "is_completed": enrollment.is_completed
            }
            enrollment_list.append(enrollment_info)

        # 构建练习记录信息
        attempt_list = []
        for attempt in exercise_attempts:
            attempt_info = {
                "id": attempt.id,
                "exercise_id": attempt.exercise_id,
                "score": attempt.score,
                "total_points": attempt.total_points,
                "percentage": attempt.percentage,
                "time_spent": attempt.time_spent,
                "is_completed": attempt.is_completed,
                "submitted_at": attempt.submitted_at.isoformat() if attempt.submitted_at else None
            }
            attempt_list.append(attempt_info)

        # 计算学习统计
        total_courses = len(enrollments)
        total_study_time = sum(e.total_study_time for e in enrollments)
        average_progress = sum(e.progress_percentage for e in enrollments) / total_courses if total_courses > 0 else 0
        completed_courses = sum(1 for e in enrollments if e.is_completed)

        # 构建返回数据
        student_detail = {
            "id": student.id,
            "username": student.username,
            "full_name": student.full_name,
            "email": student.email,
            "avatar": getattr(student, 'avatar', None),
            "created_at": student.created_at.isoformat() if student.created_at else None,
            "last_login": getattr(student, 'last_login', None),

            # 学生档案信息
            "profile": {
                "student_id": student_profile.student_id if student_profile else None,
                "school": student_profile.school if student_profile else None,
                "college": student_profile.college if student_profile else None,
                "major": student_profile.major if student_profile else None,
                "grade": student_profile.grade if student_profile else None,
                "class_name": student_profile.class_name if student_profile else None,
                "preferred_subjects": student_profile.preferred_subjects if student_profile else None,
                "learning_goals": student_profile.learning_goals if student_profile else None
            },

            # 学习统计
            "statistics": {
                "total_courses": total_courses,
                "completed_courses": completed_courses,
                "total_study_time": total_study_time,
                "average_progress": round(average_progress, 2),
                "total_exercises": len(attempt_list),
                "average_score": sum(a.percentage for a in exercise_attempts) / len(exercise_attempts) if exercise_attempts else 0
            },

            # 课程注册信息
            "enrollments": enrollment_list,

            # 练习记录
            "exercise_attempts": attempt_list
        }

        return student_detail

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取学生详细信息失败"
        )

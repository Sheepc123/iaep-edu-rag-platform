# 教师端课程管理后端逻辑实现

## 📋 功能概述

为教师端实现了完整的课程管理后端逻辑，包括课程创建、编辑、发布、删除等功能，确保教师可以完全管理自己的课程内容。

## ✅ 已完成功能

### 1. 前端页面

#### 课程管理页面 (`TeacherCourseManagement.tsx`)
- **功能特性**:
  - 课程列表展示（网格布局）
  - 搜索和过滤功能（按分类、状态）
  - 课程统计卡片（总数、已发布、学员数、平均评分）
  - 课程操作（查看、编辑、发布/取消发布、删除）
  - 响应式设计和动画效果

- **核心组件**:
  ```typescript
  // 课程过滤
  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === "all" || course.category === filterCategory;
    const matchesStatus = filterStatus === "all" || 
                         (filterStatus === "published" && course.isPublished);
    return matchesSearch && matchesCategory && matchesStatus;
  });
  ```

#### 课程创建页面 (`TeacherCourseCreate.tsx`)
- **功能特性**:
  - 三步式创建流程（基本信息、课程内容、发布设置）
  - 课时管理（添加、编辑、删除课时）
  - 实时预览和验证
  - 发布前检查清单

- **核心功能**:
  ```typescript
  // 课时管理
  const handleSaveLesson = () => {
    const lessonWithId = { ...currentLesson, id: currentLesson.id || Date.now().toString() };
    
    if (editingLessonIndex !== null) {
      const updatedLessons = [...courseData.lessons];
      updatedLessons[editingLessonIndex] = lessonWithId;
      setCourseData(prev => ({ ...prev, lessons: updatedLessons }));
    } else {
      setCourseData(prev => ({ ...prev, lessons: [...prev.lessons, lessonWithId] }));
    }
  };
  ```

#### 课程详情页面 (`TeacherCourseDetail.tsx`)
- **功能特性**:
  - 与学生端完全相同的界面
  - 教师专用操作按钮（编辑、数据分析、设置）
  - 课程统计信息
  - 课时列表和资料管理

### 2. 后端服务层

#### 课程服务扩展 (`CourseService`)

##### 教师课程列表
```python
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
    
    # 搜索和过滤逻辑
    if search:
        query = query.filter(or_(Course.title.contains(search), Course.description.contains(search)))
    if category:
        query = query.filter(Course.category == category)
    if is_published is not None:
        query = query.filter(Course.is_published == is_published)
    
    total = query.count()
    courses = query.order_by(desc(Course.updated_at)).offset(skip).limit(limit).all()
    
    return courses, total
```

##### 课程权限验证
```python
def get_teacher_course_detail(self, course_id: int, teacher_id: int) -> Course:
    """获取教师课程详情"""
    course = self.db.query(Course).filter(
        and_(Course.id == course_id, Course.instructor_id == teacher_id)
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在或您没有权限访问"
        )
    
    return course
```

##### 课程发布管理
```python
def toggle_course_publish(self, course_id: int, teacher_id: int) -> Course:
    """切换课程发布状态"""
    course = self.get_teacher_course_detail(course_id, teacher_id)
    
    # 发布前检查
    if not course.is_published:
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
```

##### 统计信息
```python
def get_teacher_course_statistics(self, teacher_id: int) -> dict:
    """获取教师课程统计信息"""
    total_courses = self.db.query(Course).filter(Course.instructor_id == teacher_id).count()
    published_courses = self.db.query(Course).filter(
        and_(Course.instructor_id == teacher_id, Course.is_published == True)
    ).count()
    
    total_students = self.db.query(func.count(CourseEnrollment.id)).join(
        Course, CourseEnrollment.course_id == Course.id
    ).filter(Course.instructor_id == teacher_id).scalar() or 0
    
    avg_rating = self.db.query(func.avg(Course.rating)).filter(
        and_(Course.instructor_id == teacher_id, Course.rating_count > 0)
    ).scalar() or 0.0
    
    return {
        "total_courses": total_courses,
        "published_courses": published_courses,
        "draft_courses": total_courses - published_courses,
        "total_students": total_students,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0.0
    }
```

### 3. API端点

#### 教师专用API端点 (`/api/v1/courses/teacher/`)

```python
# 获取教师课程列表
@router.get("/teacher/courses", response_model=List[CourseResponse])
async def get_teacher_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    is_published: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)

# 创建课程
@router.post("/teacher/courses", response_model=CourseResponse)
async def create_teacher_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)

# 获取课程详情
@router.get("/teacher/courses/{course_id}", response_model=CourseResponse)
async def get_teacher_course_detail(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)

# 更新课程
@router.put("/teacher/courses/{course_id}", response_model=CourseResponse)
async def update_teacher_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)

# 删除课程
@router.delete("/teacher/courses/{course_id}", response_model=dict)
async def delete_teacher_course(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)

# 切换发布状态
@router.post("/teacher/courses/{course_id}/toggle-publish", response_model=CourseResponse)
async def toggle_course_publish(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)

# 获取统计信息
@router.get("/teacher/statistics", response_model=dict)
async def get_teacher_course_statistics(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
)
```

### 4. 路由配置

#### 前端路由更新 (`App.tsx`)
```typescript
// 教师端路由
<Route path="/teacher/courses" element={<TeacherCourseManagement />} />
<Route path="/teacher/courses/create" element={<TeacherCourseCreate />} />
<Route path="/teacher/courses/:courseId" element={<TeacherCourseDetail />} />
<Route path="/teacher/courses/:courseId/edit" element={<TeacherCourseEdit />} />
```

#### 导航菜单 (`TeacherLayout.tsx`)
```typescript
const navItems = [
  { icon: <LayoutDashboard size={20} />, label: "教学中心", path: "/teacher/dashboard" },
  { icon: <BookOpen size={20} />, label: "课程管理", path: "/teacher/courses" },
  // ... 其他菜单项
];
```

## 🔧 技术实现细节

### 1. 权限控制
- **教师身份验证**: 使用 `get_current_teacher` 依赖确保只有教师可以访问
- **课程所有权验证**: 教师只能操作自己创建的课程
- **操作权限检查**: 删除课程前检查是否有学生注册

### 2. 数据验证
- **发布前检查**: 课程必须包含至少一个课时才能发布
- **输入验证**: 使用Pydantic模型验证所有输入数据
- **业务逻辑验证**: 防止删除已有学生注册的课程

### 3. 错误处理
- **统一异常处理**: 所有API端点都有完整的异常处理
- **详细错误信息**: 提供具体的错误描述帮助调试
- **日志记录**: 记录所有重要操作和错误信息

### 4. 性能优化
- **分页查询**: 支持分页获取课程列表
- **索引优化**: 在常用查询字段上建立索引
- **懒加载**: 按需加载课程详细信息

## 🎯 功能流程

### 1. 课程创建流程
1. 教师填写基本信息（标题、描述、分类、难度）
2. 添加课程内容（课时列表）
3. 配置发布设置
4. 系统验证完整性
5. 保存为草稿或直接发布

### 2. 课程发布流程
1. 检查课程完整性（至少一个课时）
2. 更新发布状态
3. 学生可在课程中心看到
4. 记录操作日志

### 3. 课程管理流程
1. 教师查看课程列表
2. 使用搜索和过滤功能
3. 执行各种操作（编辑、发布、删除）
4. 查看统计信息

## 📊 数据流向

```
前端页面 → API端点 → 服务层 → 数据库
    ↓         ↓        ↓        ↓
用户操作 → 权限验证 → 业务逻辑 → 数据持久化
    ↓         ↓        ↓        ↓
界面更新 ← 响应数据 ← 处理结果 ← 数据返回
```

## 🚀 使用方式

### 1. 教师创建课程
1. 登录教师账号
2. 进入"课程管理"页面
3. 点击"创建新课程"
4. 按步骤填写课程信息
5. 添加课时内容
6. 发布课程

### 2. 课程管理操作
1. 在课程列表中查看所有课程
2. 使用搜索框查找特定课程
3. 使用过滤器筛选课程
4. 点击操作按钮进行管理

### 3. 学生查看课程
1. 教师发布课程后
2. 学生可在课程中心看到
3. 学生可以注册和学习课程

## 🔄 后续优化建议

### 1. 功能增强
- **批量操作**: 支持批量发布/取消发布课程
- **课程模板**: 提供课程创建模板
- **版本管理**: 支持课程版本控制
- **协作功能**: 支持多教师协作编辑

### 2. 性能优化
- **缓存机制**: 缓存热门课程数据
- **CDN支持**: 课程封面和视频使用CDN
- **数据库优化**: 优化复杂查询性能

### 3. 用户体验
- **拖拽排序**: 支持课时拖拽排序
- **自动保存**: 编辑时自动保存草稿
- **富文本编辑**: 支持更丰富的内容编辑

## 📝 注意事项

1. **权限安全**: 确保教师只能操作自己的课程
2. **数据完整性**: 删除课程时检查关联数据
3. **并发控制**: 防止多人同时编辑同一课程
4. **备份恢复**: 重要操作前进行数据备份
5. **审核机制**: 可考虑添加课程发布审核流程

## 🎉 总结

成功实现了教师端完整的课程管理功能，包括：

- ✅ 完整的前端界面（管理、创建、详情页面）
- ✅ 完善的后端服务（CRUD操作、权限控制）
- ✅ 安全的API端点（身份验证、数据验证）
- ✅ 灵活的路由配置（支持所有操作）

教师现在可以：
- 创建和管理自己的课程
- 添加和编辑课程内容
- 发布课程供学生学习
- 查看课程统计数据

学生可以：
- 在课程中心看到教师发布的课程
- 注册和学习感兴趣的课程
- 享受与教师端一致的课程详情体验

这为构建完整的在线教育平台奠定了坚实的基础。

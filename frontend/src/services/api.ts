/**
 * API服务 - 后端通信接口
 */

// API基础配置
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// 请求配置
const defaultHeaders = {
  'Content-Type': 'application/json',
};

// 获取认证头
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return token ? { ...defaultHeaders, Authorization: `Bearer ${token}` } : defaultHeaders;
};

// 通用请求函数
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  // 合并默认headers和传入的headers，确保认证token被包含
  const mergedHeaders = {
    ...defaultHeaders,
    ...options.headers
  };

  const config: RequestInit = {
    ...options,
    headers: mergedHeaders,
  };

  try {
    const response = await fetch(url, config);

    // 如果是401错误，尝试刷新token
    if (response.status === 401 && tokenManager.getRefreshToken()) {
      console.log('收到401错误，尝试刷新token...');
      try {
        const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: defaultHeaders,
          body: JSON.stringify({ refresh_token: tokenManager.getRefreshToken() })
        });

        if (refreshResponse.ok) {
          const refreshData = await refreshResponse.json();
          tokenManager.saveTokens(refreshData.data.access_token, refreshData.data.refresh_token);
          console.log('Token刷新成功，重试原请求...');

          // 更新请求头中的token并重试
          const newConfig = {
            ...config,
            headers: {
              ...config.headers,
              Authorization: `Bearer ${refreshData.data.access_token}`
            }
          };

          const retryResponse = await fetch(url, newConfig);
          const retryData = await retryResponse.json();

          if (!retryResponse.ok) {
            throw new Error(retryData.detail || `HTTP error! status: ${retryResponse.status}`);
          }

          return retryData;
        } else {
          console.log('Token刷新失败，清除本地token');
          tokenManager.clearTokens();
          throw new Error('认证已过期，请重新登录');
        }
      } catch (refreshError) {
        console.error('Token刷新失败:', refreshError);
        tokenManager.clearTokens();
        throw new Error('认证已过期，请重新登录');
      }
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// 认证相关接口
export interface LoginRequest {
  username: string;
  password: string;
  remember_me?: boolean;
  device_info?: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user_info: {
    id: number;
    username: string;
    email: string;
    full_name: string;
    phone?: string;
    avatar?: string;
    role: string;
    is_active: boolean;
    is_verified: boolean;
    created_at: string;
    last_login?: string;
  };
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  role: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data?: any;
}

// 认证API
export const authAPI = {
  // 用户登录
  async login(data: LoginRequest): Promise<LoginResponse> {
    return apiRequest<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        device_info: data.device_info || navigator.userAgent,
      }),
    });
  },

  // 用户注册
  async register(data: RegisterRequest): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // 刷新令牌
  async refreshToken(refreshToken: string): Promise<any> {
    return apiRequest('/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
  },

  // 获取当前用户信息
  async getCurrentUser(): Promise<LoginResponse['user_info']> {
    return apiRequest('/auth/me', {
      headers: getAuthHeaders(),
    });
  },

  // 用户登出
  async logout(): Promise<AuthResponse> {
    const refreshToken = localStorage.getItem('refresh_token');
    return apiRequest<AuthResponse>('/auth/logout', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: refreshToken ? JSON.stringify({ refresh_token: refreshToken }) : undefined,
    });
  },

  // 修改密码
  async changePassword(data: {
    current_password: string;
    new_password: string;
    confirm_password: string;
  }): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/auth/change-password', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 验证令牌
  async verifyToken(): Promise<any> {
    return apiRequest('/auth/verify-token', {
      headers: getAuthHeaders(),
    });
  },
};

// 用户管理API
export const userAPI = {
  // 获取用户资料
  async getProfile(): Promise<LoginResponse['user_info']> {
    return apiRequest('/users/profile', {
      headers: getAuthHeaders(),
    });
  },

  // 更新用户资料
  async updateProfile(data: {
    full_name?: string;
    phone?: string;
    avatar?: string;
  }): Promise<LoginResponse['user_info']> {
    return apiRequest('/users/profile', {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 获取学生档案
  async getStudentProfile(): Promise<any> {
    return apiRequest('/users/student-profile', {
      headers: getAuthHeaders(),
    });
  },

  // 更新学生档案
  async updateStudentProfile(data: any): Promise<any> {
    return apiRequest('/users/student-profile', {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 获取学习统计
  async getLearningStats(): Promise<any> {
    return apiRequest('/users/learning-stats', {
      headers: getAuthHeaders(),
    });
  },

  // 获取学习偏好
  async getLearningPreferences(): Promise<any> {
    return apiRequest('/users/learning-preferences', {
      headers: getAuthHeaders(),
    });
  },

  // 设置学习偏好
  async setLearningPreferences(data: any): Promise<AuthResponse> {
    return apiRequest('/users/learning-preferences', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 修改密码
  async changePassword(data: {
    current_password: string;
    new_password: string;
    confirm_password: string;
  }): Promise<{ success: boolean; message: string }> {
    return apiRequest('/auth/change-password', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 获取教师档案
  async getTeacherProfile(): Promise<{
    id: number;
    user_id: number;
    teacher_id?: string;
    department?: string;
    title?: string;
    specialization?: string;
    total_courses: number;
    total_students: number;
    teaching_years: number;
    rating: number;
    bio?: string;
    created_at: string;
    updated_at?: string;
  }> {
    return apiRequest('/users/teacher-profile', {
      headers: getAuthHeaders(),
    });
  },

  // 更新教师档案
  async updateTeacherProfile(data: {
    teacher_id?: string;
    department?: string;
    title?: string;
    specialization?: string;
    teaching_years?: number;
    bio?: string;
  }): Promise<{
    id: number;
    user_id: number;
    teacher_id?: string;
    department?: string;
    title?: string;
    specialization?: string;
    total_courses: number;
    total_students: number;
    teaching_years: number;
    rating: number;
    bio?: string;
    created_at: string;
    updated_at?: string;
  }> {
    return apiRequest('/users/teacher-profile', {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },
};

// 令牌管理工具
export const tokenManager = {
  // 保存令牌
  saveTokens(accessToken: string, refreshToken: string) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  },

  // 获取访问令牌
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  },

  // 获取刷新令牌
  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  },

  // 清除令牌
  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token'); // 清除旧的token
  },

  // 检查是否已登录
  isLoggedIn(): boolean {
    return !!this.getAccessToken();
  },
};

// 课程管理API
export interface Course {
  id: number;
  title: string;
  description?: string;
  cover_image?: string;
  category?: string;
  difficulty: string;
  duration?: number;
  total_lessons: number;
  instructor_id: number;
  instructor_name: string;
  enrolled_students: number;
  rating: number;
  rating_count: number;
  is_active: boolean;
  is_published: boolean;
  created_at: string;
  updated_at?: string;
  is_enrolled?: boolean;
  enrollment_id?: number;
}

export interface Lesson {
  id: number;
  course_id: number;
  title: string;
  description?: string;
  content?: string;
  lesson_order: number;
  duration?: number;
  lesson_type: string;
  video_url?: string;
  materials?: string;
  is_published: boolean;
  is_free: boolean;
  created_at: string;
  updated_at?: string;
}

export interface CourseEnrollment {
  id: number;
  course_id: number;
  student_id: number;
  progress_percentage: number;
  completed_lessons: number;
  total_study_time: number;
  rating?: number;
  review?: string;
  is_completed: boolean;
  enrolled_at: string;
  completed_at?: string;
  last_accessed?: string;
  course?: Course; // 可选的课程详情
}

export interface LessonProgress {
  id: number;
  lesson_id: number;
  student_id: number;
  progress_percentage: number;
  watch_time: number;
  is_completed: boolean;
  notes?: string;
  started_at: string;
  completed_at?: string;
  last_accessed: string;
}

export const courseAPI = {
  // 获取课程列表
  async getCourses(params?: {
    category?: string;
    difficulty?: string;
    instructor_id?: number;
    search?: string;
    is_published?: boolean;
    skip?: number;
    limit?: number;
    sort_by?: string;
    sort_order?: string;
  }): Promise<{
    courses: Course[];
    total: number;
    skip: number;
    limit: number;
    has_more: boolean;
  }> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }

    return apiRequest(`/courses/?${queryParams.toString()}`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取课程详情
  async getCourse(courseId: number): Promise<Course> {
    return apiRequest(`/courses/${courseId}`, {
      headers: getAuthHeaders(),
    });
  },

  // 注册课程
  async enrollCourse(courseId: number): Promise<CourseEnrollment> {
    return apiRequest(`/courses/${courseId}/enroll`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
  },

  // 获取我的课程
  async getMyCourses(): Promise<CourseEnrollment[]> {
    return apiRequest('/courses/my-courses', {
      headers: getAuthHeaders(),
    });
  },

  // 获取课程注册信息
  async getCourseEnrollment(courseId: number): Promise<CourseEnrollment> {
    return apiRequest(`/courses/${courseId}/enrollment`, {
      headers: getAuthHeaders(),
    });
  },

  // 课程评分
  async rateCourse(courseId: number, data: {
    rating: number;
    review?: string;
  }): Promise<AuthResponse> {
    return apiRequest(`/courses/${courseId}/rate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 获取课程课时列表
  async getCourseLessons(courseId: number, includeUnpublished = false): Promise<Lesson[]> {
    return apiRequest(`/courses/${courseId}/lessons?include_unpublished=${includeUnpublished}`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取课时详情
  async getLesson(lessonId: number): Promise<Lesson> {
    return apiRequest(`/courses/lessons/${lessonId}`, {
      headers: getAuthHeaders(),
    });
  },

  // 更新课时学习进度
  async updateLessonProgress(lessonId: number, data: {
    progress_percentage: number;
    watch_time?: number;
    is_completed: boolean;
    notes?: string;
  }): Promise<LessonProgress> {
    return apiRequest(`/courses/lessons/${lessonId}/progress`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 获取课时学习进度
  async getLessonProgress(lessonId: number): Promise<LessonProgress> {
    return apiRequest(`/courses/lessons/${lessonId}/progress`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取课程学习进度
  async getCourseProgress(courseId: number): Promise<LessonProgress[]> {
    return apiRequest(`/courses/${courseId}/progress`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取课程练习
  async getCourseExercises(courseId: number): Promise<{exercises: Exercise[]}> {
    return apiRequest(`/courses/${courseId}/exercises`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取课程统计信息
  async getCourseStatistics(): Promise<{
    total_courses: number;
    published_courses: number;
    total_students: number;
    total_lessons: number;
    average_rating: number;
    completion_rate: number;
  }> {
    return apiRequest('/courses/statistics', {
      headers: getAuthHeaders(),
    });
  },
};

// AI助手API
export interface AIMessage {
  id: number;
  conversation_id: number;
  content: string;
  sender: 'user' | 'ai';
  message_type: 'text' | 'image' | 'code' | 'suggestion';
  model_used?: string;
  tokens_used?: number;
  response_time?: number;
  created_at: string;
}

export interface AIConversation {
  id: number;
  title: string;
  context?: string;
  message_count: number;
  total_tokens: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  last_message_at?: string;
}

export interface AIMessageRequest {
  content: string;
  conversation_id?: number;
  message_type?: 'text' | 'image' | 'code' | 'suggestion';
  context?: any;
}

export interface AIConversationRequest {
  title?: string;
  context?: string;
}

// AI题目生成相关接口
export interface GeneratedQuestion {
  question_text: string;
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  options?: string[];
  correct_answer: string;
  explanation: string;
  points: number;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface QuestionGenerationRequest {
  subject: string;
  topic: string;
  difficulty: 'easy' | 'medium' | 'hard';
  question_count: number;
  question_types: string[];
  additional_requirements?: string;
}

export interface QuestionGenerationResponse {
  questions: GeneratedQuestion[];
}



export const aiAPI = {
  // 创建新对话
  async createConversation(data: AIConversationRequest): Promise<AIConversation> {
    return apiRequest<AIConversation>('/ai/conversations', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 获取对话列表
  async getConversations(): Promise<AIConversation[]> {
    return apiRequest<AIConversation[]>('/ai/conversations', {
      headers: getAuthHeaders(),
    });
  },

  // 获取对话消息
  async getConversationMessages(conversationId: string): Promise<AIMessage[]> {
    return apiRequest<AIMessage[]>(`/ai/conversations/${conversationId}/messages`, {
      headers: getAuthHeaders(),
    });
  },

  // 发送消息
  async sendMessage(data: AIMessageRequest): Promise<AIMessage> {
    return apiRequest<AIMessage>('/ai/messages', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 删除对话
  async deleteConversation(conversationId: string): Promise<{ message: string }> {
    return apiRequest<{ message: string }>(`/ai/conversations/${conversationId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
  },

  // 获取快速操作
  async getQuickActions(): Promise<{ quick_actions: any[] }> {
    return apiRequest<{ quick_actions: any[] }>('/ai/quick-actions', {
      headers: getAuthHeaders(),
    });
  },

  // AI服务健康检查
  async healthCheck(): Promise<any> {
    return apiRequest('/ai/health', {
      headers: getAuthHeaders(),
    });
  },

  // AI生成题目
  async generateQuestions(data: QuestionGenerationRequest): Promise<QuestionGenerationResponse> {
    return apiRequest<QuestionGenerationResponse>('/ai/generate-questions', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },
};

// 练习系统API
export interface Exercise {
  id: number;
  title: string;
  description?: string;
  category: string;
  subject: string;
  difficulty: 'easy' | 'medium' | 'hard';
  time_limit?: number;
  course_id?: number;
  total_questions: number;
  total_attempts: number;
  average_score: number;
  is_published: boolean;
  is_active: boolean;
  created_by: number;
  created_at: string;
  updated_at?: string;
}

export interface ExerciseDetail extends Exercise {
  questions: Question[];
}

export interface Question {
  id: number;
  exercise_id: number;
  title?: string;
  content: string;
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  options?: string[];
  correct_answer: string;
  explanation?: string;
  points: number;
  difficulty: 'easy' | 'medium' | 'hard';
  subject?: string;
  tags?: string[];
  total_attempts: number;
  correct_attempts: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ExerciseCreateRequest {
  title: string;
  description?: string;
  category: string;
  subject: string;
  difficulty: 'easy' | 'medium' | 'hard';
  time_limit?: number;
  course_id?: number;
  is_published?: boolean;
}

export interface ExerciseUpdateRequest {
  title?: string;
  description?: string;
  category?: string;
  subject?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  time_limit?: number;
  is_active?: boolean;
  is_published?: boolean;
}

export interface QuestionCreateRequest {
  content: string;  // 后端期望的字段名
  question_type: 'multiple_choice' | 'fill_blank' | 'essay';
  options?: string[];
  correct_answer: string;
  explanation?: string;
  points: number;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface QuestionUpdateRequest {
  question_text?: string;
  question_type?: 'multiple_choice' | 'fill_blank' | 'essay';
  options?: string[];
  correct_answer?: string;
  explanation?: string;
  points?: number;
  difficulty?: 'easy' | 'medium' | 'hard';
  question_order?: number;
  is_active?: boolean;
}

export interface ExerciseListQuery {
  category?: string;
  subject?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  is_published?: boolean;
  page?: number;
  page_size?: number;
}

export interface ExerciseAttempt {
  id: number;
  exercise_id: number;
  student_id: number;
  score: number;
  total_points: number;
  percentage: number;
  time_spent: number;
  is_completed: boolean;
  started_at: string;
  completed_at?: string;
  answers: any[];
}

export const exerciseAPI = {
  // 获取练习列表
  async getExercises(params?: {
    course_id?: number;
    instructor_id?: number;
    difficulty?: string;
    is_published?: boolean;
    skip?: number;
    limit?: number;
  }): Promise<{
    exercises: Exercise[];
    total: number;
    skip: number;
    limit: number;
  }> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }

    return apiRequest(`/exercises/?${queryParams.toString()}`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取练习详情
  async getExercise(exerciseId: number): Promise<Exercise> {
    return apiRequest(`/exercises/${exerciseId}`, {
      headers: getAuthHeaders(),
    });
  },

  // 创建练习
  async createExercise(data: ExerciseCreateRequest): Promise<Exercise> {
    return apiRequest('/exercises/', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 更新练习
  async updateExercise(exerciseId: number, data: ExerciseUpdateRequest): Promise<Exercise> {
    return apiRequest(`/exercises/${exerciseId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 删除练习
  async deleteExercise(exerciseId: number): Promise<{ message: string }> {
    return apiRequest(`/exercises/${exerciseId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
  },

  // 获取练习题目
  async getExerciseQuestions(exerciseId: number): Promise<Question[]> {
    return apiRequest(`/exercises/${exerciseId}/questions`, {
      headers: getAuthHeaders(),
    });
  },

  // 添加题目
  async addQuestion(exerciseId: number, data: QuestionCreateRequest): Promise<Question> {
    return apiRequest(`/exercises/${exerciseId}/questions`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 更新题目
  async updateQuestion(questionId: number, data: QuestionUpdateRequest): Promise<Question> {
    return apiRequest(`/exercises/questions/${questionId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 删除题目
  async deleteQuestion(questionId: number): Promise<{ message: string }> {
    return apiRequest(`/exercises/questions/${questionId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
  },

  // 获取练习统计
  async getExerciseStatistics(exerciseId: number): Promise<{
    total_attempts: number;
    completed_attempts: number;
    average_score: number;
    average_time: number;
    pass_rate: number;
  }> {
    return apiRequest(`/exercises/${exerciseId}/statistics`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取练习结果
  async getExerciseResults(exerciseId: number): Promise<ExerciseAttempt[]> {
    return apiRequest(`/exercises/${exerciseId}/results`, {
      headers: getAuthHeaders(),
    });
  },

  // 开始练习
  async startExercise(exerciseId: number): Promise<ExerciseAttempt> {
    return apiRequest(`/exercises/${exerciseId}/start`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
  },

  // 获取练习详情（包含题目）
  async getExerciseDetail(exerciseId: number): Promise<ExerciseDetail> {
    return apiRequest(`/exercises/${exerciseId}`, {
      headers: getAuthHeaders(),
    });
  },

  // 提交练习答案
  async submitExercise(submitData: {
    attempt_id: number;
    answers: Array<{
      question_id: number;
      answer_content: string;
      time_spent?: number;
    }>;
  }): Promise<{
    attempt_id: number;
    total_questions: number;
    answered_questions: number;
    correct_answers: number;
    score: number;
    max_score: number;
    accuracy_rate: number;
    time_spent: number;
    submitted_at: string;
  }> {
    return apiRequest('/exercises/submit-exercise', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(submitData),
    });
  },

  // 获取练习尝试结果
  async getExerciseAttempt(attemptId: number): Promise<{
    id: number;
    exercise_id: number;
    student_id: number;
    total_questions: number;
    answered_questions: number;
    correct_answers: number;
    score: number;
    max_score: number;
    accuracy_rate: number;
    time_spent: number;
    is_completed: boolean;
    is_submitted: boolean;
    started_at: string;
    submitted_at?: string;
    exercise: Exercise;
    answers: Array<{
      id: number;
      question_id: number;
      answer: string;
      is_correct: boolean;
      points_earned: number;
      time_spent: number;
      question: Question;
    }>;
  }> {
    return apiRequest(`/exercises/attempts/${attemptId}`, {
      headers: getAuthHeaders(),
    });
  },
};



// 教师端专用API
export interface TeacherStats {
  total_students: number;
  total_courses: number;
  total_exercises: number;
  average_score: number;
  active_students: number;
  published_courses: number;
  published_exercises: number;
  total_enrollments: number;
}

export interface StudentInfo {
  id: number;
  username: string;
  full_name: string;
  email: string;
  avatar?: string;
  enrolled_courses: number;
  completed_exercises: number;
  average_score: number;
  total_study_time: number;
  last_active: string;
  created_at: string;
}

export interface TeacherActivity {
  id: number;
  type: string;
  title: string;
  description: string;
  created_at: string;
  related_id?: number;
  related_type?: string;
}

export const teacherAPI = {
  // 获取教师统计数据
  async getStats(): Promise<TeacherStats> {
    const courseStats = await apiRequest('/courses/statistics', {
      headers: getAuthHeaders(),
    });

    // 转换后端返回的数据格式到前端期望的格式
    return {
      total_students: courseStats.total_students || 0,
      total_courses: courseStats.total_courses || 0,
      total_exercises: 0, // 需要从练习API获取
      average_score: courseStats.average_rating || 0,
      active_students: courseStats.total_students || 0,
      published_courses: courseStats.published_courses || 0,
      published_exercises: 0, // 需要从练习API获取
      total_enrollments: courseStats.total_students || 0
    };
  },

  // 获取教师的学生列表
  async getStudents(params?: {
    course_id?: number;
    skip?: number;
    limit?: number;
    search?: string;
  }): Promise<{
    students: StudentInfo[];
    total: number;
    skip: number;
    limit: number;
  }> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }

    return apiRequest(`/users/students?${queryParams.toString()}`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取学生详细信息
  async getStudentDetail(studentId: number): Promise<StudentInfo & {
    enrollments: CourseEnrollment[];
    exercise_attempts: ExerciseAttempt[];
    learning_progress: any[];
  }> {
    return apiRequest(`/users/students/${studentId}`, {
      headers: getAuthHeaders(),
    });
  },

  // 获取最近活动
  async getRecentActivities(limit = 10): Promise<TeacherActivity[]> {
    // 暂时返回模拟数据，后续需要后端支持
    return [
      {
        id: 1,
        type: 'course_created',
        title: '创建了新课程',
        description: '《React 基础教程》课程已创建',
        created_at: new Date().toISOString(),
        related_id: 1,
        related_type: 'course'
      },
      {
        id: 2,
        type: 'exercise_created',
        title: '创建了新练习',
        description: '《JavaScript 基础练习》已发布',
        created_at: new Date(Date.now() - 3600000).toISOString(),
        related_id: 1,
        related_type: 'exercise'
      },
      {
        id: 3,
        type: 'student_enrolled',
        title: '新学生注册',
        description: '学生张三注册了《React 基础教程》',
        created_at: new Date(Date.now() - 7200000).toISOString(),
        related_id: 1,
        related_type: 'enrollment'
      }
    ];
  },

  // 获取教师练习统计
  async getExerciseStats(): Promise<{
    total_exercises: number;
    published_exercises: number;
    total_attempts: number;
    average_score: number;
  }> {
    try {
      const exercises = await exerciseAPI.getExercises({ limit: 1000 });
      const publishedCount = exercises.exercises.filter(ex => ex.is_published).length;

      return {
        total_exercises: exercises.total,
        published_exercises: publishedCount,
        total_attempts: 0, // 需要后端支持
        average_score: 0 // 需要后端支持
      };
    } catch (error) {
      console.error('获取练习统计失败:', error);
      return {
        total_exercises: 0,
        published_exercises: 0,
        total_attempts: 0,
        average_score: 0
      };
    }
  },

  // 获取综合统计数据
  async getComprehensiveStats(): Promise<TeacherStats> {
    try {
      const [courseStats, exerciseStats] = await Promise.all([
        this.getStats(),
        this.getExerciseStats()
      ]);

      return {
        ...courseStats,
        total_exercises: exerciseStats.total_exercises,
        published_exercises: exerciseStats.published_exercises
      };
    } catch (error) {
      console.error('获取综合统计失败:', error);
      throw error;
    }
  },

  // 获取教师课程列表
  async getCourses(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    category?: string;
    is_published?: boolean;
  }): Promise<{
    courses: Course[];
    total: number;
    skip: number;
    limit: number;
  }> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }

    return apiRequest(`/courses/teacher/courses?${queryParams.toString()}`, {
      headers: getAuthHeaders(),
    });
  },

  // 创建课程
  async createCourse(data: {
    title: string;
    description?: string;
    category?: string;
    difficulty: string;
    duration?: number;
    cover_image?: string;
    is_published?: boolean;
  }): Promise<Course> {
    return apiRequest('/courses/', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 更新课程
  async updateCourse(courseId: number, data: Partial<Course>): Promise<Course> {
    return apiRequest(`/courses/${courseId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 删除课程
  async deleteCourse(courseId: number): Promise<{ message: string }> {
    return apiRequest(`/courses/${courseId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
  },

  // 创建课时
  async createLesson(courseId: number, data: {
    title: string;
    description?: string;
    content?: string;
    lesson_order: number;
    duration?: number;
    lesson_type: string;
    video_url?: string;
    materials?: string;
    is_published?: boolean;
    is_free?: boolean;
  }): Promise<Lesson> {
    return apiRequest(`/courses/${courseId}/lessons`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 更新课时
  async updateLesson(lessonId: number, data: Partial<Lesson>): Promise<Lesson> {
    return apiRequest(`/courses/lessons/${lessonId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  // 删除课时
  async deleteLesson(lessonId: number): Promise<{ message: string }> {
    return apiRequest(`/courses/lessons/${lessonId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
  },
};

// 健康检查
export const healthAPI = {
  async check(): Promise<any> {
    const response = await fetch('http://127.0.0.1:8000/health');
    return response.json();
  },
};

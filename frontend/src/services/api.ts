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
  
  const config: RequestInit = {
    headers: defaultHeaders,
    ...options,
  };

  try {
    const response = await fetch(url, config);
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

// 健康检查
export const healthAPI = {
  async check(): Promise<any> {
    const response = await fetch('http://127.0.0.1:8000/health');
    return response.json();
  },
};

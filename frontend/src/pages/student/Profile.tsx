import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  User,
  Mail,
  Phone,
  School,
  GraduationCap,
  Lock,
  Edit3,
  Save,
  X,
  Eye,
  EyeOff,
  CheckCircle,
  AlertCircle,
  BookOpen,
  Clock,
  Star,
  Users,
  PlayCircle
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import StudentLayout from "@/components/layouts/StudentLayout";
import { courseAPI, userAPI, authAPI, CourseEnrollment } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";
import { AvatarUpload } from "@/components/ui/avatar-upload";

interface UserProfile {
  name: string;
  email: string;
  phone: string;
  school: string;
  college: string;
  studentId: string;
  avatar: string;
}

interface PasswordForm {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

interface EnrolledCourse {
  id: number;
  title: string;
  description: string;
  cover_image: string;
  category: string;
  difficulty: string;
  instructor_name: string;
  total_lessons: number;
  duration: number;
  rating: number;
  enrolled_at: string;
}

export const Profile = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  // 用户信息状态
  const [profile, setProfile] = useState<UserProfile>({
    name: "",
    email: "",
    phone: "",
    school: "",
    college: "",
    studentId: "",
    avatar: "https://i.pravatar.cc/120"
  });
  const [profileLoading, setProfileLoading] = useState(true);

  // 我的课程状态
  const [enrolledCourses, setEnrolledCourses] = useState<EnrolledCourse[]>([]);
  const [coursesLoading, setCoursesLoading] = useState(true);

  // 编辑状态
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState<UserProfile>(profile);

  // 密码修改状态
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [passwordForm, setPasswordForm] = useState<PasswordForm>({
    currentPassword: "",
    newPassword: "",
    confirmPassword: ""
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });

  // 保存状态
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  // 标签页状态
  const [activeTab, setActiveTab] = useState("profile");
  const [hasLoadedCourses, setHasLoadedCourses] = useState(false);

  // 加载用户数据
  const fetchUserProfile = async () => {
    try {
      setProfileLoading(true);

      // 获取用户基本信息
      const userInfo = await userAPI.getProfile();

      // 获取学生档案
      let studentProfile = null;
      try {
        studentProfile = await userAPI.getStudentProfile();
      } catch (error) {
        console.log('学生档案不存在，将使用默认值');
      }

      // 合并数据
      const profileData: UserProfile = {
        name: userInfo.full_name || userInfo.username || "",
        email: userInfo.email || "",
        phone: userInfo.phone || "",
        school: studentProfile?.school || "",
        college: studentProfile?.college || "",
        studentId: studentProfile?.student_id || "",
        avatar: userInfo.avatar || "https://i.pravatar.cc/120"
      };

      setProfile(profileData);
      setEditForm(profileData);

    } catch (error: any) {
      console.error('加载用户数据失败:', error);
      toast({
        title: "加载失败",
        description: "无法加载用户数据，请刷新页面重试",
        variant: "destructive",
      });
    } finally {
      setProfileLoading(false);
    }
  };

  // 页面加载时获取用户数据
  useEffect(() => {
    fetchUserProfile();
  }, []);

  // 处理头像更新
  const handleAvatarChange = (newAvatarUrl: string) => {
    const updatedProfile = { ...profile, avatar: newAvatarUrl };
    setProfile(updatedProfile);
    setEditForm(updatedProfile);
  };

  // 获取已注册课程
  const fetchEnrolledCourses = async () => {
    try {
      setCoursesLoading(true);
      const enrollments = await courseAPI.getMyCourses();

      // 转换数据格式，将CourseEnrollment转换为EnrolledCourse
      const courses: EnrolledCourse[] = enrollments.map((enrollment: CourseEnrollment) => ({
        id: enrollment.course_id,
        title: enrollment.course?.title || '未知课程',
        description: enrollment.course?.description || '',
        cover_image: enrollment.course?.cover_image || '',
        category: enrollment.course?.category || '',
        difficulty: enrollment.course?.difficulty || 'medium',
        instructor_name: enrollment.course?.instructor_name || '',
        total_lessons: enrollment.course?.total_lessons || 0,
        duration: enrollment.course?.duration || 0,
        rating: enrollment.course?.rating || 0,
        enrolled_at: enrollment.enrolled_at
      }));

      setEnrolledCourses(courses);
    } catch (error) {
      console.error('获取已注册课程失败:', error);
      // 设置空的课程列表，避免显示错误提示
      setEnrolledCourses([]);
      // 只在用户主动查看课程时才显示错误提示
      if (activeTab === "courses") {
        toast({
          title: "加载课程数据失败",
          description: "暂时无法获取课程信息，请稍后重试",
          variant: "destructive",
        });
      }
    } finally {
      setCoursesLoading(false);
    }
  };

  // 处理标签页切换
  const handleTabChange = (value: string) => {
    setActiveTab(value);
    // 只有在切换到课程标签页且还没有加载过课程数据时才获取
    if (value === "courses" && !hasLoadedCourses) {
      fetchEnrolledCourses();
      setHasLoadedCourses(true);
    }
  };

  // 只在需要时获取课程数据，而不是页面加载时就获取
  // useEffect(() => {
  //   fetchEnrolledCourses();
  // }, []);

  // 动画配置
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring" as const,
        stiffness: 100,
        damping: 15
      }
    }
  };

  // 保存个人信息
  const handleSaveProfile = async () => {
    setIsSaving(true);
    try {
      // 调用真实API更新用户基本信息
      const updatedUser = await userAPI.updateProfile({
        full_name: editForm.name,
        phone: editForm.phone,
        avatar: editForm.avatar
      });

      // 调用真实API更新学生档案
      await userAPI.updateStudentProfile({
        school: editForm.school,
        college: editForm.college,
        student_id: editForm.studentId
      });

      // 更新本地状态
      setProfile(editForm);
      setIsEditing(false);
      setSaveMessage({ type: 'success', text: '个人信息更新成功！' });

      // 触发自定义事件通知其他组件用户信息已更新
      window.dispatchEvent(new CustomEvent('userProfileUpdated', {
        detail: { full_name: editForm.name }
      }));

      toast({
        title: "保存成功",
        description: "个人信息已更新",
      });
    } catch (error: any) {
      console.error('更新个人信息失败:', error);
      const errorMessage = error?.detail || error?.message || '更新失败，请稍后重试';
      setSaveMessage({ type: 'error', text: errorMessage });

      toast({
        title: "保存失败",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
      setTimeout(() => setSaveMessage(null), 3000);
    }
  };

  // 取消编辑
  const handleCancelEdit = () => {
    setEditForm(profile);
    setIsEditing(false);
  };

  // 修改密码
  const handleChangePassword = async () => {
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setSaveMessage({ type: 'error', text: '新密码与确认密码不匹配！' });
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      setSaveMessage({ type: 'error', text: '新密码长度至少6位！' });
      return;
    }

    setIsSaving(true);
    try {
      // 调用真实API修改密码
      await authAPI.changePassword({
        current_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword,
        confirm_password: passwordForm.confirmPassword
      });

      setPasswordForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
      setShowPasswordForm(false);
      setSaveMessage({ type: 'success', text: '密码修改成功！请重新登录。' });

      toast({
        title: "密码修改成功",
        description: "密码已更新，请重新登录",
      });

      // 3秒后跳转到登录页面
      setTimeout(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }, 3000);

    } catch (error: any) {
      console.error('修改密码失败:', error);
      const errorMessage = error?.detail || error?.message || '密码修改失败，请检查当前密码是否正确';
      setSaveMessage({ type: 'error', text: errorMessage });

      toast({
        title: "密码修改失败",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
      setTimeout(() => setSaveMessage(null), 3000);
    }
  };

  return (
    <StudentLayout>
      <motion.div
        className="space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* 页面标题 */}
        <motion.div variants={cardVariants}>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">个人中心</h1>
              <p className="text-gray-600 mt-2">管理您的个人信息和学习课程</p>
            </div>
            <Badge variant="outline" className="px-4 py-2">
              学生账户
            </Badge>
          </div>
        </motion.div>

        {/* 保存消息提示 */}
        {saveMessage && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`flex items-center space-x-2 p-4 rounded-lg ${
              saveMessage.type === 'success' 
                ? 'bg-green-50 text-green-700 border border-green-200' 
                : 'bg-red-50 text-red-700 border border-red-200'
            }`}
          >
            {saveMessage.type === 'success' ? (
              <CheckCircle className="w-5 h-5" />
            ) : (
              <AlertCircle className="w-5 h-5" />
            )}
            <span>{saveMessage.text}</span>
          </motion.div>
        )}

        {/* 标签页导航 */}
        <motion.div variants={cardVariants}>
          <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="profile" className="flex items-center gap-2">
                <User className="w-4 h-4" />
                个人信息
              </TabsTrigger>
              <TabsTrigger value="courses" className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                我的课程
              </TabsTrigger>
            </TabsList>

            {/* 个人信息标签页 */}
            <TabsContent value="profile" className="mt-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* 左侧：头像和基本信息 */}
                <motion.div className="lg:col-span-1" variants={cardVariants}>
            <Card className="border-0 shadow-lg">
              <CardContent className="p-8 text-center">
                <div className="mb-6">
                  <AvatarUpload
                    currentAvatar={profile.avatar}
                    onAvatarChange={handleAvatarChange}
                    size="md"
                    disabled={profileLoading}
                  />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">{profile.name}</h2>
                <p className="text-gray-600 mb-1">学号：{profile.studentId}</p>
                <p className="text-gray-600">{profile.school}</p>
                <div className="mt-6 space-y-2">
                  <Badge className="bg-blue-100 text-blue-700 px-3 py-1">
                    在读学生
                  </Badge>
                  <Badge className="bg-green-100 text-green-700 px-3 py-1">
                    账户正常
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* 右侧：详细信息 */}
          <motion.div className="lg:col-span-2 space-y-6" variants={cardVariants}>
            {/* 个人信息卡片 */}
            <Card className="border-0 shadow-lg">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-xl font-bold flex items-center gap-2">
                    <User className="w-5 h-5 text-blue-600" />
                    个人信息
                  </CardTitle>
                  {!isEditing ? (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setIsEditing(true)}
                      className="flex items-center gap-2"
                    >
                      <Edit3 className="w-4 h-4" />
                      编辑
                    </Button>
                  ) : (
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleCancelEdit}
                        className="flex items-center gap-2"
                      >
                        <X className="w-4 h-4" />
                        取消
                      </Button>
                      <Button
                        size="sm"
                        onClick={handleSaveProfile}
                        disabled={isSaving}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
                      >
                        <Save className="w-4 h-4" />
                        {isSaving ? '保存中...' : '保存'}
                      </Button>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                {profileLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                    <span className="ml-2 text-gray-600">加载中...</span>
                  </div>
                ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* 姓名 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      姓名
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={editForm.name}
                        onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.name}</p>
                    )}
                  </div>

                  {/* 邮箱 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Mail className="w-4 h-4 inline mr-1" />
                      邮箱
                    </label>
                    {isEditing ? (
                      <input
                        type="email"
                        value={editForm.email}
                        onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.email}</p>
                    )}
                  </div>

                  {/* 电话 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Phone className="w-4 h-4 inline mr-1" />
                      电话
                    </label>
                    {isEditing ? (
                      <input
                        type="tel"
                        value={editForm.phone}
                        onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.phone}</p>
                    )}
                  </div>

                  {/* 学校 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <School className="w-4 h-4 inline mr-1" />
                      学校
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={editForm.school}
                        onChange={(e) => setEditForm({ ...editForm, school: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.school}</p>
                    )}
                  </div>

                  {/* 学院 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <GraduationCap className="w-4 h-4 inline mr-1" />
                      学院
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={editForm.college}
                        onChange={(e) => setEditForm({ ...editForm, college: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.college}</p>
                    )}
                  </div>
                </div>
                )}
              </CardContent>
            </Card>

            {/* 密码修改卡片 */}
            <Card className="border-0 shadow-lg">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-xl font-bold flex items-center gap-2">
                    <Lock className="w-5 h-5 text-blue-600" />
                    账户安全
                  </CardTitle>
                  {!showPasswordForm && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setShowPasswordForm(true)}
                      className="flex items-center gap-2"
                    >
                      <Lock className="w-4 h-4" />
                      修改密码
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {!showPasswordForm ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h4 className="font-medium text-gray-900">登录密码</h4>
                        <p className="text-sm text-gray-600">上次修改：2024年5月15日</p>
                      </div>
                      <Badge className="bg-green-100 text-green-700">
                        安全
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h4 className="font-medium text-gray-900">两步验证</h4>
                        <p className="text-sm text-gray-600">通过手机短信验证登录</p>
                      </div>
                      <Badge className="bg-yellow-100 text-yellow-700">
                        未启用
                      </Badge>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 gap-6">
                      {/* 当前密码 */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          当前密码
                        </label>
                        <div className="relative">
                          <input
                            type={showPasswords.current ? "text" : "password"}
                            value={passwordForm.currentPassword}
                            onChange={(e) => setPasswordForm({ ...passwordForm, currentPassword: e.target.value })}
                            className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="请输入当前密码"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPasswords({ ...showPasswords, current: !showPasswords.current })}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                          >
                            {showPasswords.current ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </div>
                      </div>

                      {/* 新密码 */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          新密码
                        </label>
                        <div className="relative">
                          <input
                            type={showPasswords.new ? "text" : "password"}
                            value={passwordForm.newPassword}
                            onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
                            className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="请输入新密码（至少6位）"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPasswords({ ...showPasswords, new: !showPasswords.new })}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                          >
                            {showPasswords.new ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </div>
                      </div>

                      {/* 确认新密码 */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          确认新密码
                        </label>
                        <div className="relative">
                          <input
                            type={showPasswords.confirm ? "text" : "password"}
                            value={passwordForm.confirmPassword}
                            onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
                            className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="请再次输入新密码"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPasswords({ ...showPasswords, confirm: !showPasswords.confirm })}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                          >
                            {showPasswords.confirm ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* 密码强度提示 */}
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h4 className="text-sm font-medium text-blue-900 mb-2">密码安全建议：</h4>
                      <ul className="text-xs text-blue-700 space-y-1">
                        <li>• 密码长度至少6位字符</li>
                        <li>• 包含大小写字母、数字和特殊字符</li>
                        <li>• 不要使用生日、姓名等个人信息</li>
                        <li>• 定期更换密码以保证账户安全</li>
                      </ul>
                    </div>

                    {/* 操作按钮 */}
                    <div className="flex space-x-3">
                      <Button
                        onClick={handleChangePassword}
                        disabled={isSaving || !passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
                      >
                        <Save className="w-4 h-4" />
                        {isSaving ? '修改中...' : '确认修改'}
                      </Button>
                      <Button
                        variant="outline"
                        onClick={() => {
                          setShowPasswordForm(false);
                          setPasswordForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
                        }}
                        className="flex items-center gap-2"
                      >
                        <X className="w-4 h-4" />
                        取消
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </TabsContent>

      {/* 我的课程标签页 */}
      <TabsContent value="courses" className="mt-6">
        <motion.div variants={cardVariants}>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl font-bold flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-600" />
                我的课程
                <Badge variant="secondary" className="ml-2">
                  {enrolledCourses.length} 门课程
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {coursesLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-2 text-gray-600">加载中...</span>
                </div>
              ) : enrolledCourses.length === 0 ? (
                <div className="text-center py-12">
                  <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">暂无已注册课程</h3>
                  <p className="text-gray-600 mb-6">您还没有注册任何课程，快去课程中心看看吧！</p>
                  <Button
                    onClick={() => navigate('/student/courses')}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    <BookOpen className="w-4 h-4 mr-2" />
                    浏览课程
                  </Button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {enrolledCourses.map((course) => (
                    <motion.div
                      key={course.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className="group cursor-pointer"
                      onClick={() => navigate(`/student/courses/${course.id}`)}
                    >
                      <Card className="h-full border-0 shadow-md hover:shadow-lg transition-all duration-300 group-hover:scale-105">
                        <div className="relative">
                          <img
                            src={course.cover_image || "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=200&fit=crop"}
                            alt={course.title}
                            className="w-full h-48 object-cover rounded-t-lg"
                          />
                          <div className="absolute top-3 left-3">
                            <Badge
                              className={`${
                                course.difficulty === 'easy' ? 'bg-green-100 text-green-700' :
                                course.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                                'bg-red-100 text-red-700'
                              }`}
                            >
                              {course.difficulty === 'easy' ? '初级' :
                               course.difficulty === 'medium' ? '中级' : '高级'}
                            </Badge>
                          </div>
                          <div className="absolute top-3 right-3">
                            <div className="bg-black bg-opacity-50 text-white px-2 py-1 rounded text-xs flex items-center gap-1">
                              <PlayCircle className="w-3 h-3" />
                              {course.total_lessons} 课时
                            </div>
                          </div>
                        </div>
                        <CardContent className="p-4">
                          <div className="mb-2">
                            <Badge variant="outline" className="text-xs">
                              {course.category}
                            </Badge>
                          </div>
                          <h3 className="font-semibold text-lg mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
                            {course.title}
                          </h3>
                          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                            {course.description}
                          </p>
                          <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                            <div className="flex items-center gap-1">
                              <User className="w-4 h-4" />
                              {course.instructor_name}
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              {Math.round(course.duration / 60)}小时
                            </div>
                          </div>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-1">
                              <Star className="w-4 h-4 text-yellow-400 fill-current" />
                              <span className="text-sm font-medium">{course.rating}</span>
                            </div>
                            <div className="text-xs text-gray-500">
                              注册于 {new Date(course.enrolled_at).toLocaleDateString()}
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </TabsContent>
    </Tabs>
  </motion.div>
      </motion.div>
    </StudentLayout>
  );
};

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
  PlayCircle,
  Award,
  Briefcase
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import { teacherAPI, userAPI, Course } from "@/services/api";
import { useToast } from "@/components/ui/use-toast";

interface TeacherProfile {
  name: string;
  email: string;
  phone: string;
  school: string;
  department: string;
  teacherId: string;
  title: string;
  specialization: string;
  avatar: string;
  bio: string;
}

interface PasswordForm {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

interface TeacherCourse {
  id: number;
  title: string;
  description: string;
  cover_image: string;
  category: string;
  difficulty: string;
  total_lessons: number;
  duration: number;
  rating: number;
  total_students: number;
  is_published: boolean;
  created_at: string;
}

export const TeacherProfile = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  // 用户信息状态
  const [profile, setProfile] = useState<TeacherProfile>({
    name: "王老师",
    email: "wang.teacher@example.com",
    phone: "138****8888",
    school: "清华大学",
    department: "计算机科学与技术学院",
    teacherId: "T2021001",
    title: "副教授",
    specialization: "人工智能、机器学习",
    avatar: "https://ui-avatars.com/api/?name=Teacher&background=3b82f6&color=fff&size=120",
    bio: "专注于人工智能和机器学习领域的教学与研究，拥有10年教学经验。"
  });

  // 我的课程状态
  const [teacherCourses, setTeacherCourses] = useState<TeacherCourse[]>([]);
  const [coursesLoading, setCoursesLoading] = useState(true);

  // 编辑状态
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState<TeacherProfile>(profile);

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

  // 获取教师课程
  const fetchTeacherCourses = async () => {
    try {
      setCoursesLoading(true);
      const response = await teacherAPI.getCourses();

      // 转换数据格式
      const courses: TeacherCourse[] = response.courses.map((course: Course) => ({
        id: course.id,
        title: course.title,
        description: course.description || '',
        cover_image: course.cover_image || '',
        category: course.category || '',
        difficulty: course.difficulty || 'medium',
        total_lessons: course.total_lessons || 0,
        duration: course.duration || 0,
        rating: course.rating || 0,
        total_students: course.total_students || 0,
        is_published: course.is_published || false,
        created_at: course.created_at
      }));

      setTeacherCourses(courses);
    } catch (error) {
      console.error('获取教师课程失败:', error);
      setTeacherCourses([]);
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
    if (value === "courses" && !hasLoadedCourses) {
      fetchTeacherCourses();
      setHasLoadedCourses(true);
    }
  };

  // 获取用户信息
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const userInfo = await userAPI.getProfile();

        // 获取教师档案信息
        let teacherProfile = null;
        try {
          teacherProfile = await userAPI.getTeacherProfile();
        } catch (error) {
          console.log('获取教师档案失败，使用默认信息');
        }

        const userName = userInfo.full_name || "教师";
        const profileData = {
          name: userName,
          email: userInfo.email,
          phone: userInfo.phone || "",
          school: "清华大学",
          department: teacherProfile?.department || "计算机科学与技术学院",
          teacherId: teacherProfile?.teacher_id || `T${userInfo.id.toString().padStart(6, '0')}`,
          title: teacherProfile?.title || "讲师",
          specialization: teacherProfile?.specialization || "计算机科学",
          avatar: userInfo.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(userName)}&background=3b82f6&color=fff&size=120`,
          bio: teacherProfile?.bio || "暂无个人简介"
        };

        setProfile(profileData);
        setEditForm(profileData);
      } catch (error) {
        console.error('获取用户信息失败:', error);
        toast({
          title: "加载失败",
          description: "无法获取用户信息，请刷新页面重试",
          variant: "destructive",
        });
      }
    };

    fetchUserProfile();
  }, []);

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
        stiffness: 300,
        damping: 30
      }
    }
  };

  // 保存个人信息
  const handleSaveProfile = async () => {
    setIsSaving(true);
    try {
      // 同时更新用户基本信息和教师档案
      await Promise.all([
        userAPI.updateProfile({
          full_name: editForm.name,
          phone: editForm.phone,
          avatar: editForm.avatar,
        }),
        userAPI.updateTeacherProfile({
          teacher_id: editForm.teacherId,
          department: editForm.department,
          title: editForm.title,
          specialization: editForm.specialization,
          bio: editForm.bio,
        })
      ]);

      setProfile(editForm);
      setIsEditing(false);
      setSaveMessage({ type: 'success', text: '个人信息更新成功！' });

      toast({
        title: "更新成功",
        description: "个人信息已成功更新",
      });
    } catch (error) {
      console.error('更新个人信息失败:', error);
      setSaveMessage({ type: 'error', text: '更新失败，请稍后重试。' });

      toast({
        title: "更新失败",
        description: "个人信息更新失败，请稍后重试",
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
    setSaveMessage(null);
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
      // 调用API修改密码
      await userAPI.changePassword({
        current_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword,
        confirm_password: passwordForm.confirmPassword,
      });

      setPasswordForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
      setShowPasswordForm(false);
      setSaveMessage({ type: 'success', text: '密码修改成功！' });

      toast({
        title: "密码修改成功",
        description: "您的密码已成功修改",
      });
    } catch (error) {
      console.error('密码修改失败:', error);
      setSaveMessage({ type: 'error', text: '密码修改失败，请检查当前密码是否正确。' });

      toast({
        title: "密码修改失败",
        description: "请检查当前密码是否正确",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
      setTimeout(() => setSaveMessage(null), 3000);
    }
  };

  return (
    <TeacherLayout>
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
              <p className="text-gray-600 mt-2">管理您的个人信息和教学课程</p>
            </div>
            <Badge variant="outline" className="px-4 py-2">
              教师账户
            </Badge>
          </div>
        </motion.div>

        {/* 保存状态提示 */}
        {saveMessage && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`flex items-center gap-2 p-4 rounded-lg ${
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
                <div className="relative inline-block mb-6">
                  <img
                    src={profile.avatar}
                    alt="头像"
                    className="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg"
                  />
                  {isEditing && (
                    <button className="absolute bottom-0 right-0 bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 transition-colors">
                      <Edit3 className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">{profile.name}</h2>
                <p className="text-gray-600 mb-1">工号：{profile.teacherId}</p>
                <p className="text-gray-600 mb-1">{profile.title}</p>
                <p className="text-gray-600">{profile.school}</p>
                <div className="mt-6 space-y-2">
                  <Badge className="bg-blue-100 text-blue-700 px-3 py-1 flex items-center gap-1">
                    <Award className="w-3 h-3" />
                    {profile.title}
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
                      onClick={() => setIsEditing(true)}
                      variant="outline"
                      size="sm"
                      className="flex items-center gap-2"
                    >
                      <Edit3 className="w-4 h-4" />
                      编辑
                    </Button>
                  ) : (
                    <div className="flex gap-2">
                      <Button
                        onClick={handleSaveProfile}
                        disabled={isSaving}
                        size="sm"
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
                      >
                        {isSaving ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        ) : (
                          <Save className="w-4 h-4" />
                        )}
                        保存
                      </Button>
                      <Button
                        onClick={handleCancelEdit}
                        variant="outline"
                        size="sm"
                        className="flex items-center gap-2"
                      >
                        <X className="w-4 h-4" />
                        取消
                      </Button>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* 姓名 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <User className="w-4 h-4 inline mr-1" />
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
                    <p className="text-gray-900 py-2">{profile.email}</p>
                    <p className="text-xs text-gray-500">邮箱不可修改</p>
                  </div>

                  {/* 手机号 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Phone className="w-4 h-4 inline mr-1" />
                      手机号
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

                  {/* 部门 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <GraduationCap className="w-4 h-4 inline mr-1" />
                      部门
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={editForm.department}
                        onChange={(e) => setEditForm({ ...editForm, department: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.department}</p>
                    )}
                  </div>

                  {/* 职称 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Award className="w-4 h-4 inline mr-1" />
                      职称
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={editForm.title}
                        onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.title}</p>
                    )}
                  </div>

                  {/* 专业领域 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Briefcase className="w-4 h-4 inline mr-1" />
                      专业领域
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={editForm.specialization}
                        onChange={(e) => setEditForm({ ...editForm, specialization: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.specialization}</p>
                    )}
                  </div>

                  {/* 个人简介 */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <User className="w-4 h-4 inline mr-1" />
                      个人简介
                    </label>
                    {isEditing ? (
                      <textarea
                        value={editForm.bio}
                        onChange={(e) => setEditForm({ ...editForm, bio: e.target.value })}
                        rows={3}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="请输入个人简介..."
                      />
                    ) : (
                      <p className="text-gray-900 py-2">{profile.bio || "暂无个人简介"}</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 密码修改卡片 */}
            <Card className="border-0 shadow-lg">
              <CardHeader className="pb-4">
                <CardTitle className="text-xl font-bold flex items-center gap-2">
                  <Lock className="w-5 h-5 text-blue-600" />
                  密码管理
                </CardTitle>
              </CardHeader>
              <CardContent>
                {!showPasswordForm ? (
                  <div className="text-center py-6">
                    <Lock className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">为了账户安全，建议定期更换密码</p>
                    <Button
                      onClick={() => setShowPasswordForm(true)}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      修改密码
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
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

                    {/* 操作按钮 */}
                    <div className="flex gap-3 pt-4">
                      <Button
                        onClick={handleChangePassword}
                        disabled={isSaving || !passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword}
                        className="flex-1 bg-blue-600 hover:bg-blue-700"
                      >
                        {isSaving ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        ) : (
                          "确认修改"
                        )}
                      </Button>
                      <Button
                        onClick={() => {
                          setShowPasswordForm(false);
                          setPasswordForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
                          setSaveMessage(null);
                        }}
                        variant="outline"
                        className="flex-1"
                      >
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
                  {teacherCourses.length} 门课程
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {coursesLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-2 text-gray-600">加载中...</span>
                </div>
              ) : teacherCourses.length === 0 ? (
                <div className="text-center py-12">
                  <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">暂无创建课程</h3>
                  <p className="text-gray-600 mb-6">您还没有创建任何课程，快去创建第一门课程吧！</p>
                  <Button
                    onClick={() => navigate('/teacher/courses/create')}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    <BookOpen className="w-4 h-4 mr-2" />
                    创建课程
                  </Button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {teacherCourses.map((course) => (
                    <motion.div
                      key={course.id}
                      className="group cursor-pointer"
                      onClick={() => navigate(`/teacher/courses/${course.id}`)}
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
                            <Badge
                              className={`${
                                course.is_published
                                  ? 'bg-green-500 text-white'
                                  : 'bg-gray-500 text-white'
                              }`}
                            >
                              {course.is_published ? '已发布' : '草稿'}
                            </Badge>
                          </div>
                          <div className="absolute bottom-3 right-3">
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
                              <Users className="w-4 h-4" />
                              {course.total_students} 学生
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
                              创建于 {new Date(course.created_at).toLocaleDateString()}
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
    </TeacherLayout>
  );
};

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/layouts/AdminLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';
import {
  Users as UsersIcon,
  Search,
  Plus,
  Edit,
  Trash2,
  Eye,
  EyeOff,
  Filter,
  Download,
  UserCheck,
  UserX,
  Mail,
  Phone,
  Calendar
} from 'lucide-react';
import { motion } from 'framer-motion';
import { adminAPI } from '@/services/api';

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  phone?: string;
  role: 'student' | 'teacher' | 'admin';
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
  avatar?: string;
}

interface PasswordChangeData {
  new_password: string;
  confirm_password: string;
}

interface CreateUserData {
  username: string;
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  role: 'student' | 'teacher';
}

const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [showPasswordDialog, setShowPasswordDialog] = useState(false);
  const [showUserDetailDialog, setShowUserDetailDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [passwordChangeData, setPasswordChangeData] = useState<PasswordChangeData>({
    new_password: '',
    confirm_password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [createUserData, setCreateUserData] = useState<CreateUserData>({
    username: '',
    email: '',
    password: '',
    full_name: '',
    phone: '',
    role: 'student'
  });
  const { toast } = useToast();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await adminAPI.getUsers({
        page: 1,
        size: 100,
        role: roleFilter === 'all' ? undefined : roleFilter,
        is_active: statusFilter === 'all' ? undefined : statusFilter === 'active'
      });
      setUsers(response.users);

    } catch (error) {
      console.error('获取用户列表失败:', error);
      // 如果API调用失败，使用模拟数据作为后备
      setUsers([
        {
          id: 1,
          username: 'student001',
          email: 'student001@example.com',
          full_name: '张同学',
          phone: '13800138001',
          role: 'student',
          is_active: true,
          is_verified: true,
          created_at: '2024-01-15T10:30:00Z',
          last_login: '2024-07-20T08:15:00Z'
        },
        {
          id: 2,
          username: 'teacher001',
          email: 'teacher001@example.com',
          full_name: '李老师',
          phone: '13800138002',
          role: 'teacher',
          is_active: true,
          is_verified: true,
          created_at: '2024-01-10T09:00:00Z',
          last_login: '2024-07-20T09:30:00Z'
        },
        {
          id: 3,
          username: 'student002',
          email: 'student002@example.com',
          full_name: '王同学',
          role: 'student',
          is_active: false,
          is_verified: false,
          created_at: '2024-07-18T14:20:00Z'
        }
      ]);

      toast({
        title: "获取用户列表失败",
        description: "使用模拟数据，请检查网络连接",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async () => {
    // 表单验证
    if (!createUserData.username || !createUserData.email || !createUserData.password || !createUserData.full_name) {
      toast({
        title: "表单验证失败",
        description: "请填写所有必填字段",
        variant: "destructive",
      });
      return;
    }

    // 邮箱格式验证
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(createUserData.email)) {
      toast({
        title: "邮箱格式错误",
        description: "请输入有效的邮箱地址",
        variant: "destructive",
      });
      return;
    }

    // 密码长度验证
    if (createUserData.password.length < 6) {
      toast({
        title: "密码太短",
        description: "密码至少需要6个字符",
        variant: "destructive",
      });
      return;
    }

    try {
      await adminAPI.createUser(createUserData);
      toast({
        title: "用户创建成功",
        description: `用户 ${createUserData.full_name} 已成功创建`,
      });
      setShowCreateDialog(false);
      setCreateUserData({
        username: '',
        email: '',
        password: '',
        full_name: '',
        phone: '',
        role: 'student'
      });
      fetchUsers();
    } catch (error: any) {
      console.error('创建用户失败:', error);
      toast({
        title: "创建用户失败",
        description: error.message || "请检查输入信息",
        variant: "destructive",
      });
    }
  };

  const handleDeleteUser = async () => {
    if (!selectedUser) return;

    try {
      await adminAPI.deleteUser(selectedUser.id);
      toast({
        title: "用户删除成功",
        description: `用户 ${selectedUser.full_name || selectedUser.username || '未知用户'} 已被删除`,
      });
      setShowDeleteDialog(false);
      setSelectedUser(null);
      fetchUsers();
    } catch (error: any) {
      console.error('删除用户失败:', error);
      toast({
        title: "删除用户失败",
        description: error.message || "请稍后重试",
        variant: "destructive",
      });
    }
  };

  const handleToggleUserStatus = async (user: User) => {
    try {
      await adminAPI.toggleUserStatus(user.id);
      toast({
        title: "用户状态更新成功",
        description: `用户 ${user.full_name || user.username || '未知用户'} 已${user.is_active ? '禁用' : '激活'}`,
      });
      fetchUsers();
    } catch (error: any) {
      console.error('更新用户状态失败:', error);
      toast({
        title: "更新用户状态失败",
        description: error.message || "请稍后重试",
        variant: "destructive",
      });
    }
  };

  const handleChangePassword = async () => {
    if (!selectedUser) return;

    // 验证密码
    if (!passwordChangeData.new_password) {
      toast({
        title: "密码不能为空",
        description: "请输入新密码",
        variant: "destructive",
      });
      return;
    }

    if (passwordChangeData.new_password.length < 6) {
      toast({
        title: "密码太短",
        description: "密码至少需要6个字符",
        variant: "destructive",
      });
      return;
    }

    if (passwordChangeData.new_password !== passwordChangeData.confirm_password) {
      toast({
        title: "密码不匹配",
        description: "两次输入的密码不一致",
        variant: "destructive",
      });
      return;
    }

    try {
      await adminAPI.changeUserPassword(selectedUser.id, passwordChangeData.new_password);
      toast({
        title: "密码修改成功",
        description: `用户 ${selectedUser.full_name || selectedUser.username} 的密码已更新`,
      });
      setShowPasswordDialog(false);
      setPasswordChangeData({ new_password: '', confirm_password: '' });
      setSelectedUser(null);
    } catch (error: any) {
      console.error('修改密码失败:', error);
      toast({
        title: "修改密码失败",
        description: error.message || "请稍后重试",
        variant: "destructive",
      });
    }
  };

  const handleViewUserDetail = (user: User) => {
    setSelectedUser(user);
    setShowUserDetailDialog(true);
  };

  const handleOpenPasswordDialog = (user: User) => {
    setSelectedUser(user);
    setShowPasswordDialog(true);
  };

  const filteredUsers = users.filter(user => {
    const searchLower = searchTerm.toLowerCase();
    const matchesSearch = !searchTerm ||
                         (user.full_name && user.full_name.toLowerCase().includes(searchLower)) ||
                         (user.username && user.username.toLowerCase().includes(searchLower)) ||
                         (user.email && user.email.toLowerCase().includes(searchLower));
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    const matchesStatus = statusFilter === 'all' ||
                         (statusFilter === 'active' && user.is_active) ||
                         (statusFilter === 'inactive' && !user.is_active);

    return matchesSearch && matchesRole && matchesStatus;
  });

  const getRoleBadge = (role: string) => {
    const roleConfig = {
      student: { label: '学生', className: 'bg-blue-100 text-blue-800' },
      teacher: { label: '教师', className: 'bg-green-100 text-green-800' },
      admin: { label: '管理员', className: 'bg-purple-100 text-purple-800' }
    };
    const config = roleConfig[role as keyof typeof roleConfig] || roleConfig.student;
    return <Badge className={config.className}>{config.label}</Badge>;
  };

  const getStatusBadge = (isActive: boolean) => {
    return isActive ? (
      <Badge className="bg-green-100 text-green-800">活跃</Badge>
    ) : (
      <Badge className="bg-red-100 text-red-800">禁用</Badge>
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-8">
        {/* 页面标题 */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">成员管理</h1>
            <p className="text-gray-600 mt-2">管理系统中的所有用户账户</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline" className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>导出</span>
            </Button>
            <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
              <DialogTrigger asChild>
                <Button className="flex items-center space-x-2">
                  <Plus className="w-4 h-4" />
                  <span>添加用户</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle>创建新用户</DialogTitle>
                  <DialogDescription>
                    填写用户信息创建新账户
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="username" className="text-right">
                      用户名
                    </Label>
                    <Input
                      id="username"
                      value={createUserData.username}
                      onChange={(e) => setCreateUserData({...createUserData, username: e.target.value})}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="email" className="text-right">
                      邮箱
                    </Label>
                    <Input
                      id="email"
                      type="email"
                      value={createUserData.email}
                      onChange={(e) => setCreateUserData({...createUserData, email: e.target.value})}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="password" className="text-right">
                      密码
                    </Label>
                    <Input
                      id="password"
                      type="password"
                      value={createUserData.password}
                      onChange={(e) => setCreateUserData({...createUserData, password: e.target.value})}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="full_name" className="text-right">
                      姓名
                    </Label>
                    <Input
                      id="full_name"
                      value={createUserData.full_name}
                      onChange={(e) => setCreateUserData({...createUserData, full_name: e.target.value})}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="phone" className="text-right">
                      手机号
                    </Label>
                    <Input
                      id="phone"
                      value={createUserData.phone}
                      onChange={(e) => setCreateUserData({...createUserData, phone: e.target.value})}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="role" className="text-right">
                      角色
                    </Label>
                    <Select value={createUserData.role} onValueChange={(value: 'student' | 'teacher') => setCreateUserData({...createUserData, role: value})}>
                      <SelectTrigger className="col-span-3">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="student">学生</SelectItem>
                        <SelectItem value="teacher">教师</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" onClick={handleCreateUser}>创建用户</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        {/* 搜索和筛选 */}
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input
                    placeholder="搜索用户名、姓名或邮箱..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <div className="flex gap-3">
                <Select value={roleFilter} onValueChange={setRoleFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="角色" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有角色</SelectItem>
                    <SelectItem value="student">学生</SelectItem>
                    <SelectItem value="teacher">教师</SelectItem>
                    <SelectItem value="admin">管理员</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="状态" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有状态</SelectItem>
                    <SelectItem value="active">活跃</SelectItem>
                    <SelectItem value="inactive">禁用</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 用户列表 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <UsersIcon className="w-5 h-5" />
              <span>用户列表</span>
              <Badge variant="secondary">{filteredUsers.length}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">用户</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">角色</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">状态</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">注册时间</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">最后登录</th>
                    <th className="text-right py-3 px-4 font-medium text-gray-600">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user, index) => (
                    <motion.tr
                      key={user.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b hover:bg-gray-50"
                    >
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                            {user.avatar ? (
                              <img src={user.avatar} alt="头像" className="w-full h-full rounded-full object-cover" />
                            ) : (
                              <span className="text-sm font-medium text-gray-600">
                                {user.full_name ? user.full_name.charAt(0) : user.username ? user.username.charAt(0) : '?'}
                              </span>
                            )}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{user.full_name || '未设置姓名'}</p>
                            <p className="text-sm text-gray-500">{user.username || '未设置用户名'}</p>
                            <p className="text-sm text-gray-500">{user.email || '未设置邮箱'}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        {getRoleBadge(user.role)}
                      </td>
                      <td className="py-4 px-4">
                        {getStatusBadge(user.is_active)}
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-1 text-sm text-gray-600">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(user.created_at)}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        {user.last_login ? (
                          <span className="text-sm text-gray-600">{formatDate(user.last_login)}</span>
                        ) : (
                          <span className="text-sm text-gray-400">从未登录</span>
                        )}
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center justify-end space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleViewUserDetail(user)}
                            title="查看详情"
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleOpenPasswordDialog(user)}
                            title="修改密码"
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleToggleUserStatus(user)}
                            title={user.is_active ? "禁用用户" : "启用用户"}
                          >
                            {user.is_active ? <UserX className="w-4 h-4" /> : <UserCheck className="w-4 h-4" />}
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setSelectedUser(user);
                              setShowDeleteDialog(true);
                            }}
                            title="删除用户"
                          >
                            <Trash2 className="w-4 h-4 text-red-500" />
                          </Button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* 用户详情对话框 */}
        <Dialog open={showUserDetailDialog} onOpenChange={setShowUserDetailDialog}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>用户详细信息</DialogTitle>
              <DialogDescription>
                查看用户的完整账户信息
              </DialogDescription>
            </DialogHeader>
            {selectedUser && (
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center">
                    <span className="text-xl font-medium text-gray-600">
                      {selectedUser.full_name ? selectedUser.full_name.charAt(0) : selectedUser.username ? selectedUser.username.charAt(0) : '?'}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold">{selectedUser.full_name || '未设置姓名'}</h3>
                    <p className="text-sm text-gray-500">{selectedUser.role === 'student' ? '学生' : selectedUser.role === 'teacher' ? '教师' : '管理员'}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-3">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">用户ID:</span>
                    <span className="text-sm text-gray-900">{selectedUser.id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">用户名:</span>
                    <span className="text-sm text-gray-900">{selectedUser.username}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">邮箱:</span>
                    <span className="text-sm text-gray-900">{selectedUser.email}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">手机号:</span>
                    <span className="text-sm text-gray-900">{selectedUser.phone || '未设置'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">账户状态:</span>
                    <Badge className={selectedUser.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                      {selectedUser.is_active ? '活跃' : '禁用'}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">邮箱验证:</span>
                    <Badge className={selectedUser.is_verified ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}>
                      {selectedUser.is_verified ? '已验证' : '未验证'}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">注册时间:</span>
                    <span className="text-sm text-gray-900">
                      {new Date(selectedUser.created_at).toLocaleDateString('zh-CN')}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-600">最后登录:</span>
                    <span className="text-sm text-gray-900">
                      {selectedUser.last_login ? new Date(selectedUser.last_login).toLocaleDateString('zh-CN') : '从未登录'}
                    </span>
                  </div>
                </div>

                <div className="flex justify-end space-x-2 pt-4 border-t">
                  <Button
                    variant="outline"
                    onClick={() => handleOpenPasswordDialog(selectedUser)}
                  >
                    修改密码
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setShowUserDetailDialog(false)}
                  >
                    关闭
                  </Button>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>

        {/* 修改密码对话框 */}
        <Dialog open={showPasswordDialog} onOpenChange={setShowPasswordDialog}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>修改用户密码</DialogTitle>
              <DialogDescription>
                为用户 "{selectedUser?.full_name || selectedUser?.username}" 设置新密码
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="new_password">新密码</Label>
                <div className="relative">
                  <Input
                    id="new_password"
                    type={showPassword ? "text" : "password"}
                    placeholder="请输入新密码（至少6位）"
                    value={passwordChangeData.new_password}
                    onChange={(e) => setPasswordChangeData(prev => ({
                      ...prev,
                      new_password: e.target.value
                    }))}
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </Button>
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirm_password">确认密码</Label>
                <Input
                  id="confirm_password"
                  type={showPassword ? "text" : "password"}
                  placeholder="请再次输入新密码"
                  value={passwordChangeData.confirm_password}
                  onChange={(e) => setPasswordChangeData(prev => ({
                    ...prev,
                    confirm_password: e.target.value
                  }))}
                />
              </div>
              {passwordChangeData.new_password && passwordChangeData.confirm_password &&
               passwordChangeData.new_password !== passwordChangeData.confirm_password && (
                <p className="text-sm text-red-600">两次输入的密码不一致</p>
              )}
            </div>
            <DialogFooter>
              <Button
                variant="outline"
                onClick={() => {
                  setShowPasswordDialog(false);
                  setPasswordChangeData({ new_password: '', confirm_password: '' });
                  setShowPassword(false);
                }}
              >
                取消
              </Button>
              <Button onClick={handleChangePassword}>
                确认修改
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* 删除确认对话框 */}
        <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>确认删除用户</DialogTitle>
              <DialogDescription>
                您确定要删除用户 "{selectedUser?.full_name || selectedUser?.username || '未知用户'}" 吗？此操作不可撤销。
              </DialogDescription>
            </DialogHeader>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowDeleteDialog(false)}>
                取消
              </Button>
              <Button variant="destructive" onClick={handleDeleteUser}>
                删除
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </AdminLayout>
  );
};

export default Users;

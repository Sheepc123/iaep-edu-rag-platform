# 教师端练习保存错误调试指南

## 🐛 问题描述
教师端在保存和发布练习时出现"fail to fetch"错误。

## 🔍 可能的原因分析

### 1. 网络连接问题
- 后端服务未启动或端口不正确
- 前端和后端端口冲突
- 防火墙阻止连接

### 2. CORS跨域问题
- 前端地址未在后端CORS配置中
- 请求头配置错误

### 3. 认证问题
- Token过期或无效
- 权限不足（非教师用户）

### 4. 数据格式问题
- 请求数据格式不正确
- 必填字段缺失

## 🛠️ 调试步骤

### 步骤1: 检查后端服务状态
```bash
# 在backend目录下运行
python run.py

# 或者检查健康状态
curl http://localhost:8000/health
```

**预期结果**: 返回健康状态JSON

### 步骤2: 检查前端网络请求
1. 打开浏览器开发者工具 (F12)
2. 切换到 Network 标签页
3. 尝试保存练习
4. 查看失败的请求详情

**检查要点**:
- 请求URL是否正确: `http://127.0.0.1:8000/api/v1/exercises/`
- 请求方法是否为POST
- 请求头是否包含Authorization
- 响应状态码和错误信息

### 步骤3: 验证用户认证
```javascript
// 在浏览器控制台执行
console.log('Access Token:', localStorage.getItem('access_token'));
console.log('Refresh Token:', localStorage.getItem('refresh_token'));
```

**如果Token为空**: 需要重新登录

### 步骤4: 使用API调试工具
打开 `frontend/debug_api.html` 文件进行逐步测试:

1. **测试后端连接**
2. **用户登录** (teacher123/123456)
3. **检查认证状态**
4. **测试练习创建**

## 🔧 常见解决方案

### 解决方案1: 重启服务
```bash
# 重启后端
cd backend
python run.py

# 重启前端
cd frontend
npm run dev
```

### 解决方案2: 清除浏览器缓存
1. 清除localStorage
2. 重新登录
3. 重试操作

### 解决方案3: 检查端口配置
确保配置正确:
- 后端: `http://127.0.0.1:8000`
- 前端: `http://localhost:5173`

### 解决方案4: 修复API请求
如果发现API请求问题，检查以下文件:
- `frontend/src/services/api.ts` - API配置
- `frontend/src/pages/teacher/ExerciseCreate.tsx` - 练习创建逻辑

## 📋 详细错误排查清单

### ✅ 后端检查
- [ ] 后端服务正在运行 (端口8000)
- [ ] 数据库连接正常
- [ ] 健康检查API响应正常
- [ ] CORS配置包含前端地址

### ✅ 前端检查
- [ ] 前端服务正在运行 (端口5173)
- [ ] API_BASE_URL配置正确
- [ ] 用户已成功登录
- [ ] Token存在且有效

### ✅ 网络检查
- [ ] 浏览器开发者工具显示请求详情
- [ ] 没有CORS错误
- [ ] 请求头包含正确的Authorization
- [ ] 请求体数据格式正确

## 🚨 紧急修复方案

如果问题持续存在，可以尝试以下紧急修复:

### 方案A: 使用模拟数据
临时禁用API调用，使用本地存储:
```javascript
// 在ExerciseCreate.tsx中临时添加
const saveExerciseLocal = (exerciseData, questions) => {
  const exercises = JSON.parse(localStorage.getItem('local_exercises') || '[]');
  const newExercise = {
    id: Date.now(),
    ...exerciseData,
    questions: questions,
    created_at: new Date().toISOString()
  };
  exercises.push(newExercise);
  localStorage.setItem('local_exercises', JSON.stringify(exercises));
  return newExercise;
};
```

### 方案B: 直接数据库操作
使用后端脚本直接创建练习:
```bash
cd backend
python database/create_test_data.py exercises
```

## 📊 错误日志分析

### 常见错误信息及解决方案

#### "Failed to fetch"
- **原因**: 网络连接问题或后端服务未启动
- **解决**: 检查后端服务状态，重启服务

#### "CORS policy"
- **原因**: 跨域请求被阻止
- **解决**: 检查后端CORS配置

#### "401 Unauthorized"
- **原因**: 认证失败或Token过期
- **解决**: 重新登录获取新Token

#### "403 Forbidden"
- **原因**: 权限不足
- **解决**: 确保使用教师账号登录

#### "422 Unprocessable Entity"
- **原因**: 请求数据格式错误
- **解决**: 检查请求数据格式和必填字段

## 🔄 完整测试流程

1. **环境准备**
   ```bash
   # 启动后端
   cd backend && python run.py
   
   # 启动前端
   cd frontend && npm run dev
   ```

2. **用户登录**
   - 访问: http://localhost:5173/login
   - 使用教师账号: teacher123/123456

3. **创建练习**
   - 访问: http://localhost:5173/teacher/exercises
   - 点击"创建练习"
   - 填写基本信息
   - 添加题目
   - 点击"保存草稿"或"发布练习"

4. **验证结果**
   - 检查是否成功跳转到练习列表
   - 确认新练习出现在列表中
   - 学生端验证是否可见

## 💡 预防措施

1. **定期检查服务状态**
2. **监控API响应时间**
3. **备份重要数据**
4. **保持依赖项更新**
5. **使用错误监控工具**

## 📞 获取帮助

如果问题仍然存在，请提供以下信息:
1. 浏览器控制台的完整错误信息
2. 网络请求的详细信息
3. 后端日志输出
4. 操作系统和浏览器版本
5. 具体的操作步骤

这将帮助更快地定位和解决问题。

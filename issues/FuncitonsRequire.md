# 教学实训智能体开发功能拆解

## 1. 项目初始化
- 主要内容：
  - 前端项目结构（如App、页面、组件目录）
  - 后端项目结构（如main.py、routers、models、services等）
  - 依赖管理（requirements.txt、package.json）

## 2. 用户与权限管理
- 主要类/函数/接口：
  - User类（属性：id, username, password_hash, role, ...）
  - AuthService（注册、登录、JWT生成与校验）
  - /api/register, /api/login, /api/userinfo等接口
  - 权限中间件（如Depends(get_current_user)）
- 逻辑概要：
  - 用户注册、登录、身份校验、权限分级

## 3. 知识库管理与解析
- 主要类/函数/接口：
  - KnowledgeDoc类（文档元数据、内容、向量表示等）
  - DocParser（PDF/Word/Markdown/TXT解析函数）
  - VectorStore（向量化与检索接口）
  - /api/knowledge/upload, /api/knowledge/search等接口
- 逻辑概要：
  - 支持多格式文档上传、解析、向量化、检索，知识库≤100M

## 4. 大模型本地推理服务
- 主要类/函数/接口：
  - LLMService（DeepSeek模型加载、推理、API封装）
  - /api/llm/ask, /api/llm/generate等接口
- 逻辑概要：
  - 本地推理服务，支持知识增强问答、内容生成

## 5. 教师端功能
- 主要类/函数/接口：
  - LessonDesigner（教学内容生成）
  - ExamGenerator（考核题与答案生成，题目需标注知识点）
  - AnalysisService（学情分析、自动批改、错误定位）
  - /api/teacher/lesson, /api/teacher/exam, /api/teacher/analysis等接口
- 逻辑概要：
  - 教师一键生成教学内容、考题、分析报告，题目与知识点强关联

## 6. 学生端功能
- 主要类/函数/接口：
  - QAService（智能问答）
  - PracticeService（个性化练习生成与评测）
  - /api/student/ask, /api/student/practice等接口
- 逻辑概要：
  - 学生提问、练习、自动评测与反馈

## 7. 管理端与大屏
- 主要类/函数/接口：
  - UserAdmin（用户管理）
  - ResourceAdmin（课件/资源管理）
  - DashboardService（统计与可视化）
  - /api/admin/users, /api/admin/resources, /api/admin/dashboard等接口
- 逻辑概要：
  - 管理员管理用户、资源，查看统计数据与导出

## 8. 本地化部署与文档
- 主要内容：
  - 部署脚本（如deploy.bat、README.md）
  - 环境配置说明
  - 用户/开发文档
- 逻辑概要：
  - 一键部署，文档完善，便于本地Windows运行 
# Intelligent Education Platform (Software Engineering Capstone Project)

> **Positioning**: A modern education management system integrating AI (LLM + local knowledge base) to provide a complete digital teaching solution for **students / teachers / administrators**.  
> **Goals**: Intelligent teaching assistance, digitized management, personalized learning, data visualization, and production-ready deployment & operations.

---

## 1. Overview

The *Intelligent Education Platform* is designed for practical teaching and training scenarios. It addresses common pain points such as high preparation cost for teachers (courseware and quizzes), lack of instant Q&A and feedback for students, and insufficient data-driven insights for administrators. The platform integrates the **DeepSeek AI API** with a **local knowledge base (FAISS)** to enable semantic search and grounded Q&A, and provides role-specific modules plus a large-screen analytics dashboard.

### 1.1 Key Capabilities
- **Student Portal**: learning dashboard, course learning, exercise system, AI learning assistant, personalized recommendations
- **Teacher Portal**: course/exercise creation & management, student progress tracking, knowledge base management, AI-assisted content generation, teaching analytics overview
- **Admin Portal**: user/resource management, teacher & student statistics, system health monitoring, large-screen overview dashboard

 Screenshots 

![Dashboard](docs/screenshots/1.png)
![AI-assistance](docs/screenshots/2.png)
![Student-Dashboard](docs/screenshots/3.png)
![Dashboard2](docs/screenshots/4.png)
![Dashboard3](docs/screenshots/5.png)
![Dashboard4](docs/screenshots/6.png)
![Dashboard5](docs/screenshots/7.png)
![Dashboard6](docs/screenshots/8.png)
![Dashboard7](docs/screenshots/9.png)
![Dashboard8](docs/screenshots/10.png)
![Dashboard9](docs/screenshots/11.png)
![Dashboard10](docs/screenshots/12.png)
![Dashboard11](docs/screenshots/13.png)
![Dashboard12](docs/screenshots/14.png)
![AI-assistance12](docs/screenshots/15.png)
![Student-Dashboard13](docs/screenshots/16.png)
![Dashboard21](docs/screenshots/17.png)
![Dashboard32](docs/screenshots/18.png)
![Dashboard43](docs/screenshots/19.png)


---

## 2. System Architecture

### 2.1 Frontend–Backend Separation
- **Frontend**: React + TypeScript (built with Vite)  
  - UI: Tailwind CSS + shadcn/ui component system  
  - Animation: Framer Motion  
  - Visualization: Recharts (line/bar/pie/radar/area charts)  
  - State: React Context  
  - Routing: React Router (multi-role routing)
- **Backend**: Python FastAPI  
  - ORM: SQLAlchemy  
  - Database: SQLite (dev), extensible to PostgreSQL/MySQL (production)  
  - Auth: JWT  
  - Password hashing: bcrypt  
  - Logging: Loguru  
  - File handling: document upload / parsing / storage
- **AI Integration**: DeepSeek AI API + FAISS vector store  
  - Document parsing: PDF / Word / Markdown  
  - Semantic search: vector retrieval + multi-turn context management

### 2.2 Modules (Logical View)
- **Business Modules**: course management, exercise system, student management, score/learning analytics, knowledge base management, AI assistant, dashboards
- **Infrastructure**: authentication & authorization, audit logging, file storage, vector indexing, caching (Redis, optional)

---

## 3. Project Structure (Example)

```text
softwareCup/
├── frontend/                 # Frontend
│   ├── src/
│   │   ├── components/       # Shared components
│   │   ├── pages/            # Pages
│   │   │   ├── public/       # Public pages
│   │   │   ├── student/      # Student portal
│   │   │   ├── teacher/      # Teacher portal
│   │   │   └── admin/        # Admin portal
│   │   ├── contexts/         # Global state
│   │   └── routes/           # Routing configs
└── backend/                  # Backend
    ├── app/
    │   ├── api/              # API routes
    │   ├── services/         # Business services (AI/RAG/retrieval)
    │   ├── models/           # SQLAlchemy models
    │   ├── schemas/          # Pydantic schemas
    │   └── utils/            # Utilities & middleware
    └── requirements.txt
```

---

## 4. Routing Design (Multi-Role)

### 4.1 Student
- `/student/dashboard` — learning overview
- `/student/courses` — course list
- `/student/exercises` — exercise list
- `/student/ai-assistant` — AI assistant
- `/student/profile` — profile

### 4.2 Teacher
- `/teacher/dashboard` — teaching overview
- `/teacher/courses` — course management
- `/teacher/exercises` — exercise management
- `/teacher/students` — student management
- `/teacher/knowledge-base` — knowledge base management
- `/teacher/ai-assistant` — teaching AI assistant

### 4.3 Admin
- `/admin/overview` — large-screen overview
- `/admin/users` — user management
- `/admin/resources` — resource management
- `/admin/teachers` — teacher statistics
- `/admin/students` — student statistics

---

## 5. Core Implementation

### 5.1 Authentication & Authorization
- **JWT**: access token (refresh token optional)
- **RBAC**: role-based access control (student/teacher/admin)
- **bcrypt**: secure password hashing
- Frontend: attach token via request interceptors; route guards to protect pages

### 5.2 AI Service (DeepSeek + RAG)
- Wrapped DeepSeek API into a unified service layer with multi-turn conversation context
- **Knowledge Base Workflow**:
  1) Document upload (PDF/Word/MD)  
  2) Parsing and chunking  
  3) Embedding generation  
  4) Indexing into FAISS (Top-K retrieval)  
  5) Inject retrieved passages into prompts for grounded generation  
  6) Return answer with cited passages (traceability)

> Note: SQLite FTS5 can also be used for full-text search and document indexing, complementary to vector retrieval.

### 5.3 Data Visualization & Dashboards
- Implemented dashboards using Recharts: line (trend), bar (comparison), pie (ratio), radar (multi-dimensional ability), area (accumulation)
- Supports KPI summaries, trend analysis, module usage distribution, and learning outcome metrics

---

## 6. Functional Modules (By Role)

### 6.1 Student Portal
- **Learning Dashboard**: study time, completion rate, accuracy, AI recommendations
- **Course Learning**: course list/details/chapters, progress tracking, multimedia support
- **Exercise System**: multi-type exercises, auto-grading (depending on implementation)
- **AI Assistant**: Q&A, study coaching, personalized suggestions

### 6.2 Teacher Portal
- **Teacher Dashboard**: teaching stats, student activity, publishing rates, quick actions, recent events
- **Course Management**: create/edit/publish, rich-text editing, chapter management (drag-and-drop ordering), AI-assisted content drafting
- **Exercise Management**: create/edit questions, answers/rubrics, publish & analyze results, AI-assisted quiz generation
- **Student Management**: student list/profile, learning progress, exercise records, learning reports (PDF export optional)
- **Knowledge Base Management**: upload/list/categorize documents, semantic search; generate courseware/exercises using KB + LLM

### 6.3 Admin Portal
- **User Management**: create/edit/disable, reset passwords, filtering/search, CSV import/export (optional)
- **Resource Management**: course/exercise/KB resources, auditing & categorization, backup & cleanup (optional)
- **Teacher/Student Analytics**: activity levels, content creation, coverage, teaching/learning metrics, AI usage statistics

---


---

## 7. Deployment & Operations

### 7.1 Development Environment
- OS: Windows / macOS / Linux
- Python: 3.9+
- Node.js: 18+
- DB: SQLite (dev); PostgreSQL/MySQL (optional for production)

### 7.2 Production (Huawei Cloud ECS)
- Recommended: 4 vCPU / 8 GB RAM+, SSD 100 GB+
- Two deployment options:
  - **Docker deployment**: build images + docker-compose; optional Nginx reverse proxy + SSL
  - **Traditional deployment**: Gunicorn/uWSGI for backend + static frontend hosting + Nginx/Apache

### 7.3 Monitoring Recommendations
- Performance: API latency, CPU/memory/disk, DB connections & slow queries
- Reliability: log aggregation, alerts, AI call failure rate
- Business metrics: user activity, feature usage frequency, AI usage statistics & quality feedback

---

## 8. Team Responsibilities (From Course Report)
- **Yueyang Liu**: overall architecture & backend development; AI integration and knowledge base (RAG) design  
- **Wanqi Wang**: frontend UI and user experience design  
- **Hao Sun**: algorithm design and data processing  

---

## 9. Summary

This project follows an end-to-end engineering workflow—from requirements analysis and system design to full-stack implementation and cloud deployment. It delivers a complete “AI + teaching workflow” loop with multi-role business modules, a RAG-based knowledge base, AI assistant features, analytics dashboards, and production-ready deployment capability, providing a strong foundation for further iteration.

# 前端部署与配置指南

## 🚀 快速开始

### 环境要求
- **Node.js**: >= 18.0.0
- **pnpm**: >= 8.0.0 (推荐) 或 npm >= 9.0.0
- **浏览器**: Chrome >= 90, Firefox >= 88, Safari >= 14

### 安装依赖
```bash
# 使用pnpm (推荐)
pnpm install

# 或使用npm
npm install
```

### 开发环境启动
```bash
# 启动开发服务器
pnpm dev

# 或
npm run dev

# 访问地址: http://localhost:5173
```

## 🔧 环境配置

### 环境变量配置
创建 `.env` 文件：
```bash
# API配置
VITE_API_BASE_URL=http://localhost:3000/api
VITE_API_TIMEOUT=10000

# 应用配置
VITE_APP_TITLE=智能教育平台
VITE_APP_VERSION=2.0.0

# 功能开关
VITE_ENABLE_AI_CHAT=true
VITE_ENABLE_ANALYTICS=false

# 第三方服务
VITE_SENTRY_DSN=your_sentry_dsn_here
VITE_GOOGLE_ANALYTICS_ID=your_ga_id_here
```

### 不同环境配置
```bash
# 开发环境 (.env.development)
VITE_API_BASE_URL=http://localhost:3000/api
VITE_LOG_LEVEL=debug

# 测试环境 (.env.staging)
VITE_API_BASE_URL=https://api-staging.example.com/api
VITE_LOG_LEVEL=info

# 生产环境 (.env.production)
VITE_API_BASE_URL=https://api.example.com/api
VITE_LOG_LEVEL=error
```

## 📦 构建部署

### 构建命令
```bash
# 构建生产版本
pnpm build

# 预览构建结果
pnpm preview

# 类型检查
pnpm type-check

# 代码检查
pnpm lint

# 代码格式化
pnpm format
```

### 构建优化配置
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // 输出目录
    outDir: 'dist',
    
    // 资源内联阈值
    assetsInlineLimit: 4096,
    
    // 代码分割
    rollupOptions: {
      output: {
        manualChunks: {
          // 第三方库分离
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-label'],
          animation: ['framer-motion'],
          icons: ['lucide-react'],
          charts: ['recharts']
        },
        // 文件命名
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
    
    // 压缩配置
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
});
```

## 🌐 部署方案

### 1. Nginx 部署
```nginx
# /etc/nginx/sites-available/education-platform
server {
    listen 80;
    server_name your-domain.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL配置
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # 静态文件目录
    root /var/www/education-platform/dist;
    index index.html;
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/javascript application/xml+rss 
               application/json image/svg+xml;
    
    # 缓存策略
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # HTML文件不缓存
    location ~* \.html$ {
        expires -1;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    
    # SPA路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API代理
    location /api/ {
        proxy_pass http://backend-server:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Docker 部署
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=http://backend:3000/api
    depends_on:
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 3. Vercel 部署
```json
// vercel.json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-api.com/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 4. GitHub Actions CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy Frontend

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'pnpm'
      
      - name: Install pnpm
        run: npm install -g pnpm
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Run tests
        run: pnpm test
      
      - name: Run linting
        run: pnpm lint
      
      - name: Type check
        run: pnpm type-check

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'pnpm'
      
      - name: Install pnpm
        run: npm install -g pnpm
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Build
        run: pnpm build
        env:
          VITE_API_BASE_URL: ${{ secrets.API_BASE_URL }}
      
      - name: Deploy to Server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/education-platform
            git pull origin main
            pnpm install
            pnpm build
            sudo systemctl reload nginx
```

## 🔍 监控与分析

### 性能监控
```typescript
// src/utils/performance.ts
export const reportWebVitals = (onPerfEntry?: (metric: any) => void) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

// 使用示例
reportWebVitals((metric) => {
  console.log(metric);
  // 发送到分析服务
  analytics.track('Web Vitals', metric);
});
```

### 错误监控
```typescript
// src/utils/errorTracking.ts
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,
  tracesSampleRate: 1.0,
});

export const captureError = (error: Error, context?: any) => {
  Sentry.captureException(error, { extra: context });
};
```

## 🔒 安全配置

### 内容安全策略 (CSP)
```html
<!-- index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline'; 
               img-src 'self' data: https:; 
               connect-src 'self' https://api.example.com;">
```

### 环境变量安全
```bash
# 敏感信息不要放在前端环境变量中
# ❌ 错误示例
VITE_API_SECRET=secret_key

# ✅ 正确示例
VITE_API_BASE_URL=https://api.example.com
```

## 📊 性能优化

### 构建分析
```bash
# 安装分析工具
pnpm add -D rollup-plugin-visualizer

# 生成构建分析报告
pnpm build --analyze
```

### 缓存策略
```typescript
// sw.js (Service Worker)
const CACHE_NAME = 'education-platform-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});
```

## 🐛 故障排除

### 常见问题
1. **构建失败**: 检查Node.js版本和依赖版本
2. **路由404**: 确保服务器配置了SPA回退
3. **API请求失败**: 检查CORS配置和环境变量
4. **样式不生效**: 检查Tailwind CSS配置

### 调试工具
```bash
# 开启详细日志
DEBUG=vite:* pnpm dev

# 分析构建产物
pnpm build --debug

# 检查依赖
pnpm list --depth=0
```

---

**部署负责人**: DevOps团队  
**文档版本**: v1.0  
**最后更新**: 2024年3月15日

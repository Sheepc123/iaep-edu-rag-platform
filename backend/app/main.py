"""
FastAPI 主应用入口
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import time
from loguru import logger

from .core.config import settings
from .core.database import init_database, check_database_health
from .api.v1.api import api_router


def create_application() -> FastAPI:
    """创建FastAPI应用实例"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="智能教育平台后端API",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )
    
    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 配置受信任主机中间件
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
        )
    
    # 添加请求处理时间中间件
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # 配置静态文件服务
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    # 配置头像静态文件服务
    if not os.path.exists("static"):
        os.makedirs("static")
    if not os.path.exists("static/avatars"):
        os.makedirs("static/avatars")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # 注册API路由
    app.include_router(api_router, prefix="/api/v1")
    
    return app


# 创建应用实例
app = create_application()


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 启动智能教育平台后端服务...")
    
    # 初始化数据库
    try:
        init_database()
        logger.info("✅ 数据库初始化完成")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        raise e
    
    # 检查数据库健康状态
    if check_database_health():
        logger.info("✅ 数据库连接正常")
    else:
        logger.error("❌ 数据库连接失败")
        raise Exception("数据库连接失败")
    
    logger.info(f"🎉 服务启动完成，运行在 http://{settings.HOST}:{settings.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("👋 智能教育平台后端服务正在关闭...")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能教育平台 API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "disabled"
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    db_status = check_database_health()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "timestamp": time.time(),
        "version": settings.APP_VERSION
    }


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """404错误处理"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "请求的资源不存在",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """500错误处理"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error", 
            "message": "服务器内部错误，请稍后重试"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # 配置日志
    logger.add(
        settings.LOG_FILE,
        rotation="1 day",
        retention="30 days",
        level=settings.LOG_LEVEL
    )
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

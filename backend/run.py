"""
项目启动脚本
"""
import uvicorn
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from loguru import logger


def main():
    """主启动函数"""
    
    # 配置日志
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    logger.add(
        settings.LOG_FILE,
        rotation="1 day",
        retention="30 days", 
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    
    logger.info("=" * 50)
    logger.info("🚀 启动智能教育平台后端服务")
    logger.info(f"📍 服务地址: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"🔧 调试模式: {'开启' if settings.DEBUG else '关闭'}")
    logger.info(f"📊 API文档: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info("=" * 50)
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )


if __name__ == "__main__":
    main()

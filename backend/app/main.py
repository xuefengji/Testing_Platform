from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api.router import router as api_router
from app.db.session import engine
from app.db.base import Base
from app.common.exception import (
    BizException,
    biz_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ===== 启动时 =====
    logger.info("🚀 App starting...")

    # 1️⃣ 尝试连接数据库并创建表
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database connected & tables created")
    except Exception as e:
        logger.warning(f"⚠️ Database connection failed: {e}")
        logger.warning("⚠️ Application will start without database connection.")
        logger.warning("⚠️ Please check your database configuration in .env file")

    yield

    # ===== 关闭时 =====
    logger.info("🛑 App shutting down...")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        docs_url="/docs",        # Swagger
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ===== CORS（前后端分离必备）=====
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],     # 生产环境建议收紧
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ===== 异常处理器 =====
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # ===== 路由 =====
    app.include_router(api_router)

    # ===== 健康检查 =====
    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok", "app": settings.APP_NAME}

    return app


app = create_app()

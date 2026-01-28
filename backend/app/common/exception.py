from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class BizException(Exception):
    """业务异常类"""
    def __init__(self, code: int = 400, message: str = "业务处理失败", data=None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)


def biz_exception_handler(request: Request, exc: BizException):
    """业务异常处理器"""
    return JSONResponse(
        status_code=200,  # 业务异常统一返回 200，通过 code 字段区分
        content={
            "code": exc.code,
            "success": False,
            "data": exc.data,
            "message": exc.message,
        },
    )


def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 异常处理器（FastAPI 的 HTTPException）"""
    return JSONResponse(
        status_code=200,  # 统一返回 200，通过 code 字段区分
        content={
            "code": exc.status_code,
            "success": False,
            "data": None,
            "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        },
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求参数验证异常处理器"""
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = ".".join(str(loc) for loc in error.get("loc", []))
        msg = error.get("msg", "验证失败")
        error_messages.append(f"{field}: {msg}")
    
    message = "; ".join(error_messages) if error_messages else "请求参数验证失败"
    
    return JSONResponse(
        status_code=200,
        content={
            "code": 422,
            "success": False,
            "data": None,
            "message": message,
        },
    )


def unhandled_exception_handler(request: Request, exc: Exception):
    """未处理的异常处理器（兜底）"""
    logger.exception(f"Unhandled exception: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=200,
        content={
            "code": 500,
            "success": False,
            "data": None,
            "message": "服务器内部错误，请稍后重试",
        },
    )
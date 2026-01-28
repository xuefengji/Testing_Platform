from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

# 全局接口返回字段
class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None


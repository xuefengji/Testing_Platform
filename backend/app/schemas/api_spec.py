from typing import Any, Literal
from pydantic import BaseModel, Field

HttpMethod = Literal["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"]
BodyType = Literal["none","json","form","raw"]

class Assertion(BaseModel):
    type: Literal["status_code","jsonpath_equals","contains","regex","response_time_lt"]
    config: dict[str, Any] = Field(default_factory=dict)
    order_no: int = 0

class Extractor(BaseModel):
    type: Literal["jsonpath","regex","header"]
    key: str
    expr: str
    order_no: int = 0

class RequestDef(BaseModel):
    method: HttpMethod
    path: str
    headers: dict[str, str] = Field(default_factory=dict)
    query: dict[str, Any] = Field(default_factory=dict)
    body_type: BodyType = "none"
    body: Any | None = None
    timeout_ms: int = 10000

class ApiSpec(BaseModel):
    request: RequestDef
    variables: dict[str, Any] = Field(default_factory=dict)  # 请求级默认变量
    assertions: list[Assertion] = Field(default_factory=list)
    extractors: list[Extractor] = Field(default_factory=list)
    pre: dict[str, Any] = Field(default_factory=dict)   # 预留
    post: dict[str, Any] = Field(default_factory=dict)  # 预留

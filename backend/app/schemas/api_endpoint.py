from pydantic import BaseModel, Field
from app.schemas.api_spec import ApiSpec

class ApiEndpointCreateIn(BaseModel):
    folder_id: int
    name: str
    method: str
    path: str
    owner_user_id: int
    spec: ApiSpec
    change_log: str | None = None

class ApiEndpointUpdateIn(BaseModel):
    folder_id: int | None = None
    name: str | None = None
    method: str | None = None
    path: str | None = None
    owner_user_id: int | None = None
    status: str | None = None

class ApiEndpointOut(BaseModel):
    id: int
    folder_id: int
    name: str
    method: str
    path: str
    owner_user_id: int
    status: str
    latest_version_id: int | None

class ApiEndpointDetailOut(ApiEndpointOut):
    latest_spec: dict  # 返回 spec_json（也可用 ApiSpec，但前端通常要原始 json）

class ApiVersionItem(BaseModel):
    id: int
    version: int
    is_latest: int
    change_log: str | None
    created_by: int
    created_at: str

class ApiVersionCreateIn(BaseModel):
    spec: ApiSpec
    change_log: str | None = None
    set_latest: bool = True

from pydantic import BaseModel

class LoginIn(BaseModel):
    name: str
    password: str
    project_id: int | None = None  # 可选：登录时直接选项目

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class User(BaseModel):
    pass
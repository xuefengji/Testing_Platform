from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.auth import LoginIn, TokenOut
from app.crud.user import get_user_by_name_or_email
from app.crud.project import get_user_roles_in_project
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.common.response import ApiResponse
from app.common.exception import BizException

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login", response_model=ApiResponse[TokenOut])
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = get_user_by_name_or_email(db, data.name)
    if not user:
        raise BizException(code=401, message="用户名或密码错误")
    if not verify_password(data.password, user.password_hash):
        raise BizException(code=401, message="用户名或密码错误")
    if user.is_disabled:
        raise BizException(code=403, message="账户已被禁用")
    pid = data.project_id
    roles = []
    if pid:
        roles = get_user_roles_in_project(db, user.id, pid)
        if not roles:
            raise BizException(code=403, message="您不是该项目的成员")

    access = create_access_token(user.id, pid, roles)
    refresh = create_refresh_token(user.id)
    return ApiResponse(
        code=200,
        success=True,
        data=TokenOut(access_token=access, refresh_token=refresh),
        message="登录成功"
    )

@auth_router.post("/register")
def create_user(db: Session = Depends(get_db)):
    pass

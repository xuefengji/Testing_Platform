from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import decode_token
from app.crud.user import get_user_by_id
from app.crud.project import get_user_roles_in_project

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if payload.get("typ") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    user_id = int(payload.get("sub"))
    user = get_user_by_id(db, user_id)
    if not user or user.is_disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User disabled")
    return user, payload

def require_project_member(db: Session = Depends(get_db), user_payload=Depends(get_current_user)):
    user, payload = user_payload
    pid = payload.get("pid")
    if not pid:
        raise HTTPException(status_code=400, detail="No project selected")
    roles = get_user_roles_in_project(db, user.id, int(pid))
    if not roles:
        raise HTTPException(status_code=403, detail="Not a project member")
    return user, int(pid), roles

def require_perm(perm: str):
    def _inner(user_ctx=Depends(require_project_member)):
        user, pid, roles = user_ctx
        # MVP：用“角色->权限”映射（先写死，后面再做表）
        role_perms = {
            "project_admin": {"api:read","api:write","api:version","folder:write"},
            "qa_lead": {"api:read","api:write","api:version","folder:write"},
            "qa": {"api:read"},
            "dev": {"api:read"},
        }
        perms = set()
        for r in roles:
            perms |= role_perms.get(r, set())
        if perm not in perms:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user, pid, roles
    return _inner

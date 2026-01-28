from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.deps import get_db, require_perm
from app.models.api_folder import ApiFolder

api_folders_router = APIRouter(prefix="/api-folders", tags=["api-folders"])

@api_folders_router.get("/tree")
def get_tree(user_ctx=Depends(require_perm("api:read")), db: Session = Depends(get_db)):
    user, pid, roles = user_ctx
    folders = db.scalars(select(ApiFolder).where(ApiFolder.project_id == pid).order_by(ApiFolder.order_no, ApiFolder.id)).all()

    # 组树（MVP）
    by_parent: dict[int | None, list[dict]] = {}
    for f in folders:
        by_parent.setdefault(f.parent_id, []).append({"id": f.id, "name": f.name, "children": []})

    def build(parent_id=None):
        nodes = by_parent.get(parent_id, [])
        for n in nodes:
            n["children"] = build(n["id"])
        return nodes

    return {"tree": build(None)}

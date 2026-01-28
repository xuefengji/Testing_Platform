from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.deps import get_db, require_perm, require_project_member
from app.models.api_endpoint import ApiEndpoint
from app.crud import api_endpoint as crud
from app.schemas.api_endpoint import (
    ApiEndpointCreateIn, ApiEndpointUpdateIn,
    ApiEndpointOut, ApiEndpointDetailOut,
    ApiVersionItem, ApiVersionCreateIn
)

api_endpoint_router = APIRouter(prefix="/api-endpoints", tags=["api-endpoints"])

@api_endpoint_router.get("")
def list_endpoints(
    folder_id: int | None = Query(None),
    keyword: str | None = Query(None),
    method: str | None = Query(None),
    owner_user_id: int | None = Query(None),
    status: str | None = Query(None),
    user_ctx=Depends(require_perm("api:read")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    stmt = select(ApiEndpoint).where(ApiEndpoint.project_id == pid)
    if folder_id is not None:
        stmt = stmt.where(ApiEndpoint.folder_id == folder_id)
    if keyword:
        stmt = stmt.where(ApiEndpoint.name.like(f"%{keyword}%"))
    if method:
        stmt = stmt.where(ApiEndpoint.method == method.upper())
    if owner_user_id:
        stmt = stmt.where(ApiEndpoint.owner_user_id == owner_user_id)
    if status:
        stmt = stmt.where(ApiEndpoint.status == status)

    rows = db.scalars(stmt.order_by(ApiEndpoint.id.desc()).limit(200)).all()
    return {"items": [
        {
            "id": r.id, "name": r.name, "method": r.method,
            "owner_user_id": r.owner_user_id, "path": r.path,
            "latest_version_id": r.latest_version_id,
            "folder_id": r.folder_id,
            "status": r.status
        } for r in rows
    ]}

@api_endpoint_router.post("", response_model=ApiEndpointOut)
def create_endpoint(
    data: ApiEndpointCreateIn,
    user_ctx=Depends(require_perm("api:write")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    # 用 Pydantic spec 转 dict 存 JSON
    spec_json = data.spec.model_dump()

    try:
        with db.begin():
            ep = crud.create_endpoint_with_v1(
                db,
                project_id=pid,
                folder_id=data.folder_id,
                name=data.name,
                method=data.method,
                path=data.path,
                owner_user_id=data.owner_user_id,
                created_by=user.id,
                spec_json=spec_json,
                change_log=data.change_log,
            )
        db.refresh(ep)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Create failed: {e}")

    return ApiEndpointOut(
        id=ep.id, folder_id=ep.folder_id, name=ep.name, method=ep.method,
        path=ep.path, owner_user_id=ep.owner_user_id, status=ep.status,
        latest_version_id=ep.latest_version_id
    )

@api_endpoint_router.get("/{endpoint_id}", response_model=ApiEndpointDetailOut)
def get_endpoint_detail(
    endpoint_id: int,
    user_ctx=Depends(require_perm("api:read")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    ep = crud.get_endpoint(db, pid, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Not found")

    latest_spec = None
    if ep.latest_version_id:
        ver = crud.get_version(db, ep.id, ep.latest_version_id)
        latest_spec = ver.spec_json if ver else None

    return ApiEndpointDetailOut(
        id=ep.id, folder_id=ep.folder_id, name=ep.name, method=ep.method,
        path=ep.path, owner_user_id=ep.owner_user_id, status=ep.status,
        latest_version_id=ep.latest_version_id,
        latest_spec=latest_spec or {}
    )

@api_endpoint_router.put("/{endpoint_id}", response_model=ApiEndpointOut)
def update_endpoint(
    endpoint_id: int,
    data: ApiEndpointUpdateIn,
    user_ctx=Depends(require_perm("api:write")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    ep = crud.get_endpoint(db, pid, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Not found")

    patch = {k: v for k, v in data.model_dump().items() if v is not None}
    if "method" in patch:
        patch["method"] = patch["method"].upper()

    with db.begin():
        ep = crud.update_endpoint_base(db, ep, patch)
    db.refresh(ep)

    return ApiEndpointOut(
        id=ep.id, folder_id=ep.folder_id, name=ep.name, method=ep.method,
        path=ep.path, owner_user_id=ep.owner_user_id, status=ep.status,
        latest_version_id=ep.latest_version_id
    )

@api_endpoint_router.get("/{endpoint_id}/versions", response_model=list[ApiVersionItem])
def get_versions(
    endpoint_id: int,
    user_ctx=Depends(require_perm("api:read")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    ep = crud.get_endpoint(db, pid, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Not found")

    vers = crud.list_versions(db, ep.id)
    return [
        ApiVersionItem(
            id=v.id, version=v.version, is_latest=v.is_latest,
            change_log=v.change_log, created_by=v.created_by,
            created_at=str(v.created_at)
        ) for v in vers
    ]

@api_endpoint_router.get("/{endpoint_id}/versions/{version_id}")
def get_version_detail(
    endpoint_id: int,
    version_id: int,
    user_ctx=Depends(require_perm("api:read")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    ep = crud.get_endpoint(db, pid, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Not found")

    ver = crud.get_version(db, ep.id, version_id)
    if not ver:
        raise HTTPException(status_code=404, detail="Version not found")
    return {"id": ver.id, "version": ver.version, "is_latest": ver.is_latest, "spec": ver.spec_json}

@api_endpoint_router.post("/{endpoint_id}/versions", response_model=ApiVersionItem)
def create_version(
    endpoint_id: int,
    data: ApiVersionCreateIn,
    user_ctx=Depends(require_perm("api:version")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    ep = crud.get_endpoint(db, pid, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Not found")

    spec_json = data.spec.model_dump()
    with db.begin():
        ver = crud.create_new_version(
            db,
            endpoint_id=ep.id,
            created_by=user.id,
            spec_json=spec_json,
            change_log=data.change_log,
            set_latest=data.set_latest
        )
    db.refresh(ver)
    return ApiVersionItem(
        id=ver.id, version=ver.version, is_latest=ver.is_latest,
        change_log=ver.change_log, created_by=ver.created_by,
        created_at=str(ver.created_at)
    )

@api_endpoint_router.post("/{endpoint_id}/versions/{version_id}/set-latest")
def set_latest(
    endpoint_id: int,
    version_id: int,
    user_ctx=Depends(require_perm("api:version")),
    db: Session = Depends(get_db),
):
    user, pid, roles = user_ctx
    ep = crud.get_endpoint(db, pid, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Not found")

    ver = crud.get_version(db, ep.id, version_id)
    if not ver:
        raise HTTPException(status_code=404, detail="Version not found")

    with db.begin():
        crud.set_latest_version(db, endpoint_id=ep.id, version_id=ver.id)
    return {"ok": True, "latest_version_id": ver.id}

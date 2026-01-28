from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from app.models.api_endpoint import ApiEndpoint
from app.models.api_endpoint_version import ApiEndpointVersion

def get_endpoint(db: Session, project_id: int, endpoint_id: int) -> ApiEndpoint | None:
    return db.scalar(select(ApiEndpoint).where(
        ApiEndpoint.project_id == project_id,
        ApiEndpoint.id == endpoint_id
    ))

def create_endpoint_with_v1(
    db: Session,
    *,
    project_id: int,
    folder_id: int,
    name: str,
    method: str,
    path: str,
    owner_user_id: int,
    created_by: int,
    spec_json: dict,
    change_log: str | None
) -> ApiEndpoint:
    ep = ApiEndpoint(
        project_id=project_id,
        folder_id=folder_id,
        name=name,
        method=method.upper(),
        path=path,
        owner_user_id=owner_user_id,
        status="active",
    )
    db.add(ep)
    db.flush()  # 生成 ep.id

    v1 = ApiEndpointVersion(
        endpoint_id=ep.id,
        version=1,
        is_latest=1,
        spec_json=spec_json,
        change_log=change_log,
        created_by=created_by,
    )
    db.add(v1)
    db.flush()

    ep.latest_version_id = v1.id
    db.add(ep)
    return ep

def update_endpoint_base(db: Session, ep: ApiEndpoint, patch: dict) -> ApiEndpoint:
    for k, v in patch.items():
        setattr(ep, k, v)
    db.add(ep)
    return ep

def list_versions(db: Session, endpoint_id: int) -> list[ApiEndpointVersion]:
    return db.scalars(
        select(ApiEndpointVersion)
        .where(ApiEndpointVersion.endpoint_id == endpoint_id)
        .order_by(ApiEndpointVersion.version.desc(), ApiEndpointVersion.id.desc())
    ).all()

def get_version(db: Session, endpoint_id: int, version_id: int) -> ApiEndpointVersion | None:
    return db.scalar(select(ApiEndpointVersion).where(
        ApiEndpointVersion.endpoint_id == endpoint_id,
        ApiEndpointVersion.id == version_id
    ))

def create_new_version(
    db: Session,
    *,
    endpoint_id: int,
    created_by: int,
    spec_json: dict,
    change_log: str | None,
    set_latest: bool = True
) -> ApiEndpointVersion:
    # 取当前最大 version
    max_ver = db.scalar(
        select(func.max(ApiEndpointVersion.version)).where(ApiEndpointVersion.endpoint_id == endpoint_id)
    ) or 0
    new_ver_no = int(max_ver) + 1

    ver = ApiEndpointVersion(
        endpoint_id=endpoint_id,
        version=new_ver_no,
        is_latest=1 if set_latest else 0,
        spec_json=spec_json,
        change_log=change_log,
        created_by=created_by,
    )
    db.add(ver)
    db.flush()

    if set_latest:
        # 清理旧 latest（同一 endpoint 只能有一个 latest）
        db.execute(
            update(ApiEndpointVersion)
            .where(ApiEndpointVersion.endpoint_id == endpoint_id, ApiEndpointVersion.id != ver.id)
            .values(is_latest=0)
        )
        # 更新 endpoint.latest_version_id
        db.execute(
            update(ApiEndpoint)
            .where(ApiEndpoint.id == endpoint_id)
            .values(latest_version_id=ver.id)
        )

    return ver

def set_latest_version(db: Session, *, endpoint_id: int, version_id: int):
    db.execute(
        update(ApiEndpointVersion)
        .where(ApiEndpointVersion.endpoint_id == endpoint_id)
        .values(is_latest=0)
    )
    db.execute(
        update(ApiEndpointVersion)
        .where(ApiEndpointVersion.endpoint_id == endpoint_id, ApiEndpointVersion.id == version_id)
        .values(is_latest=1)
    )
    db.execute(
        update(ApiEndpoint)
        .where(ApiEndpoint.id == endpoint_id)
        .values(latest_version_id=version_id)
    )

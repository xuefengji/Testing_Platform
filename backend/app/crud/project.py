from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.project import ProjectMember

def get_user_roles_in_project(db: Session, user_id: int, project_id: int) -> list[str]:
    rows = db.scalars(select(ProjectMember.role).where(
        ProjectMember.user_id == user_id,
        ProjectMember.project_id == project_id
    )).all()
    return list(rows)

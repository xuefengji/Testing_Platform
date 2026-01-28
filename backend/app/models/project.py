from sqlalchemy import String, DateTime, func, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Project(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

class ProjectMember(Base):
    __tablename__ = "project_member"
    __table_args__ = (UniqueConstraint("project_id","user_id", name="uq_project_user"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    role: Mapped[str] = mapped_column(String(50), index=True)  # project_admin/qa/...

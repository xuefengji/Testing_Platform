from sqlalchemy import String, Integer, DateTime, func, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ApiEndpoint(Base):
    __tablename__ = "api_endpoint"
    __table_args__ = (
        Index("idx_endpoint_project_folder", "project_id", "folder_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, index=True)
    folder_id: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str] = mapped_column(String(200))
    method: Mapped[str] = mapped_column(String(10))  # GET/POST...
    path: Mapped[str] = mapped_column(String(500))
    owner_user_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(20), default="active")  # draft/active/deprecated
    latest_version_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

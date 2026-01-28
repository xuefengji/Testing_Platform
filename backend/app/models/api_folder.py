from sqlalchemy import String, Integer, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ApiFolder(Base):
    __tablename__ = "api_folder"
    __table_args__ = (
        Index("idx_folder_project_parent", "project_id", "parent_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, index=True)
    parent_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(120))
    order_no: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

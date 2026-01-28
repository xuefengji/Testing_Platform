from sqlalchemy import Integer, DateTime, func, JSON, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ApiEndpointVersion(Base):
    __tablename__ = "api_endpoint_version"
    __table_args__ = (
        Index("idx_ver_endpoint", "endpoint_id"),
        Index("idx_ver_latest", "endpoint_id", "is_latest"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_id: Mapped[int] = mapped_column(Integer, index=True)
    version: Mapped[int] = mapped_column(Integer)  # 1,2,3...
    is_latest: Mapped[int] = mapped_column(Integer, default=1)  # MySQL bool 用 tinyint
    spec_json: Mapped[dict] = mapped_column(JSON)
    change_log: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_by: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

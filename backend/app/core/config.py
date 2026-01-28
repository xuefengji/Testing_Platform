from pydantic_settings import BaseSettings
from pydantic import Field
from urllib.parse import quote_plus
from pathlib import Path

# 获取 backend 目录的绝对路径
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    # ===== App =====
    APP_NAME: str = "AutoTest API"
    
    # ===== MySQL =====
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = Field(default="root", repr=False)  # 防止打印泄露
    MYSQL_DB: str = "autotest"

    # ===== Admin Init =====
    INIT_ADMIN_EMAIL: str | None = None
    INIT_ADMIN_PASSWORD: str | None = None
    INIT_ADMIN_NAME: str = "admin"

    # ===== JWT =====
    JWT_SECRET: str = Field(
        default="dev-secret-key-change-in-production-please-use-a-strong-random-key",
        repr=False
    )
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    def mysql_dsn(self) -> str:
        password = quote_plus(self.MYSQL_PASSWORD)
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{password}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            f"?charset=utf8mb4"
        )

    class Config:
        env_file = str(ENV_FILE) if ENV_FILE.exists() else ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.db.base import Base


import app.models  # noqa

config = context.config

# 日志配置
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 关键：告诉 Alembic 用哪个 metadata
target_metadata = Base.metadata


def run_migrations_online():
    # 🔥 覆盖 alembic.ini 里的 sqlalchemy.url
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.mysql_dsn()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()

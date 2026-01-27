from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@postgres:5432/postgres",
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    default_tenant_id: str = os.getenv("DEFAULT_TENANT_ID", "demo")


settings = Settings()

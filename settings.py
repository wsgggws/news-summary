import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = Field(default_factory=lambda: os.getenv("APP_ENV", "local"))

    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/newsdb"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_PRE_PING: bool = True

    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60

    model_config = SettingsConfigDict(
        env_file=[
            Path(".env"),
            Path(f".env.{os.getenv('APP_ENV', 'local')}"),
        ],
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略未知变量
    )


settings = Settings()

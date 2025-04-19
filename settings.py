import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = Field(default_factory=lambda: os.getenv("APP_ENV", "local"))

    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/newsdb"

    model_config = SettingsConfigDict(
        env_file=Path(f".env.{os.getenv('APP_ENV', 'local')}"),
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略未知变量
    )


settings = Settings()

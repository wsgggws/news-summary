import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    URL: str = "postgresql+asyncpg://user:password@localhost:5432/newsdb"
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    POOL_PRE_PING: bool = True

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.getenv('APP_ENV', 'local')}"),
        env_file_encoding="utf8",
        extra="ignore",
        env_prefix="DB_",
    )


class RedisSettings(BaseSettings):
    PASSWORD: str = "mypassword"
    HOST: str = "localhost"
    PORT: int = 6379
    BROKER_NUM: int = 1
    BACKEND_NUM: int = 2

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.getenv('APP_ENV', 'local')}"),
        env_file_encoding="utf8",
        extra="ignore",
        env_prefix="REDIS_",
    )


class Settings(BaseSettings):
    APP_ENV: str = "local"

    DEBUG: bool = False

    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60

    db: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()

    # TODO, 这里还需要查文档，如何避免重复配置变量
    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.getenv('APP_ENV', 'local')}"),
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略未知变量
    )


settings = Settings()

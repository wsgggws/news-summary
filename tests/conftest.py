import asyncio
from datetime import datetime, timedelta, timezone

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from jose import jwt

from app.main import app
from app.services.database import Base, engine
from settings import settings

assert settings.APP_ENV == "ci"
assert settings.db.URL.endswith("test_newsdb")


# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
# https://pypi.org/project/pytest-async-sqlalchemy/
# or poolclass = NullPool when create_async_engine
@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """全局数据库初始化（整个测试会话只执行一次）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"\n创建所有表: {settings.db.URL}")
    yield
    async with engine.begin() as conn:
        print(f"\n丢弃所有表: {settings.db.URL}")
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
def generate_token():
    def _generate_token(username="wsgggws", token_type="valid_token"):
        payload = {
            "sub": username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        if token_type == "expired_token":
            payload["exp"] = datetime.now(tz=timezone.utc) - timedelta(minutes=1)  # 生成过期 token
        elif token_type == "invalid_token":
            return "invalid.token.string"
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return _generate_token

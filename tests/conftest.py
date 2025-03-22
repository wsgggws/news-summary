import asyncio

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.services.database import Base, get_db
from config import TEST_DATABASE_URL

print(TEST_DATABASE_URL)
# ✅ 创建 SQLAlchemy 异步引擎
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    # poolclass=NullPool,
    # echo=True,
)

TestingSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


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
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"\n创建所有表: {TEST_DATABASE_URL}")
    yield
    async with test_engine.begin() as conn:
        print(f"\n丢弃所有表: {TEST_DATABASE_URL}")
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def client():

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

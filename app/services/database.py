from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import settings

# 创建异步的 SQLAlchemy 引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    # echo=True,
)
AsyncSession = async_sessionmaker(engine)


# 获取异步数据库会话
async def get_db():
    async with AsyncSession() as session:
        yield session  # 提供 session


async def init_db():
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)


# 所有被继承表 Base
class Base(DeclarativeBase):
    pass

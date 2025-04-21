from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import settings

# 创建异步的 SQLAlchemy 引擎, 默认是开启连接池的，这里更@GPT改了些参数
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
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

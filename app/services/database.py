from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import settings

# 创建异步的 SQLAlchemy 引擎, 默认是开启连接池的，这里更@GPT改了些参数
engine = create_async_engine(
    settings.db.URL,
    pool_size=settings.db.POOL_SIZE,
    max_overflow=settings.db.MAX_OVERFLOW,
    pool_timeout=settings.db.POOL_TIMEOUT,
    pool_recycle=settings.db.POOL_RECYCLE,
    pool_pre_ping=settings.db.POOL_PRE_PING,
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

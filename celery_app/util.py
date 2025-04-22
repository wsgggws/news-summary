from dateutil import parser as date_parser
from parsel import Selector
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings


def get_celery_async_session():
    engine = create_async_engine(
        settings.db.URL,
        pool_size=settings.db.POOL_SIZE,
        max_overflow=settings.db.MAX_OVERFLOW,
        pool_timeout=settings.db.POOL_TIMEOUT,
        pool_recycle=settings.db.POOL_RECYCLE,
        pool_pre_ping=settings.db.POOL_PRE_PING,
    )
    return async_sessionmaker(engine)


def parse_date(date_str: str = ""):
    """将 RSS 中的时间字符串解析为 datetime"""
    if not date_str:
        return None
    try:
        # feedparser 的 parsed_parsed 不一定有 → 使用 dateutil 兜底
        return date_parser.parse(date_str)
    except Exception as e:
        print(f"Failed to parse date: {date_str}, error: {e}")
        return None


def parse_description(description: str = ""):
    return Selector(description).xpath("//text()[normalize-space(.) != '']").extract_first()

import asyncio
import logging

from sqlalchemy.future import select

from app.models.rss import RSSFeed
from celery_app import celery_app
from celery_app.tasks.rss_crawler import do_one_feed
from celery_app.util import get_celery_async_session

logger = logging.getLogger(__name__)
logger.info("Starting RSS feed dispatch")


async def _dispatch_rss_fetch_logic():
    try:
        celery_session_marker = get_celery_async_session()
        async with celery_session_marker() as session:
            feeds = await session.execute(select(RSSFeed))
            feed_count = 0
            for feed in feeds.scalars():
                if feed.is_paused:
                    logger.warning(f"Feed {feed.title} {feed.url} is paused, ignoring dispatched")
                    continue
                do_one_feed.delay(str(feed.id), str(feed.url))  # type: ignore[attr-defined]
                feed_count += 1
            logger.info(f"Successfully dispatched {feed_count} RSS feeds")
    except Exception as e:
        logger.error(f"Error in RSS dispatch: {str(e)}")
        raise


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def dispatch_all_feeds(self):
    asyncio.run(_dispatch_rss_fetch_logic())

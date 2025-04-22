import asyncio

import pytest
from sqlalchemy.future import select

from app.models.rss import RSSArticle
from app.services.database import AsyncSession
from celery_app.tasks.rss_crawler import do_one_feed_logic
from tests.helper import test_feeds

articles_count = [3, 12]


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_do_one_feed_logic():
    for index, feed in enumerate(test_feeds):
        await do_one_feed_logic(feed["id"], feed["url"])
        async with AsyncSession() as async_session:
            articles = await async_session.execute(select(RSSArticle).where(RSSArticle.rss_id == feed["id"]))
            assert articles_count[index] == len(articles.scalars().all())

    await asyncio.sleep(0.1)

    # 第二次爬取将不更新
    for index, feed in enumerate(test_feeds):
        await do_one_feed_logic(feed["id"], feed["url"])
        async with AsyncSession() as async_session:
            articles = await async_session.execute(select(RSSArticle).where(RSSArticle.rss_id == feed["id"]))
            assert articles_count[index] == len(articles.scalars().all())

import asyncio
import logging
from typing import Dict, List

import aiohttp
import feedparser
import html2text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from app.models.rss import RSSArticle
from celery_app import celery_app
from celery_app.util import get_celery_async_session, parse_date, parse_description

logger = logging.getLogger(__name__)


@celery_app.task
def do_one_feed(rss_id: str, feed_url: str):
    asyncio.run(do_one_feed_logic(rss_id, feed_url))


async def do_one_feed_logic(rss_id: str, url: str):
    try:
        feed_html = await fetch_feed(url)
        if not feed_html:
            logger.error(f"Failed to fetch feed from {url}")
            return

        entries = parse_feed(html=feed_html)
        logger.info(f"Parsed {len(entries)} entries from feed")

        exist_urls = await get_exist_urls(rss_id)
        entries = discard_exists_entries(entries, exist_urls)
        logger.info(f"Found {len(entries)} new entries to process")

        articles = await fetch_articles(entries)
        articles = enhance_articles(articles)  # Use corrected function name
        await save_articles_to_db(rss_id, articles)
    except Exception as e:
        logger.error(f"Error in do_one_feed_logic for {rss_id} ({url}): {e}")
        raise
    else:
        logger.info(f"successful do_one_feed_logic for {rss_id} ({url})")


def enhance_articles(articles: List[Dict]) -> List[Dict]:
    for article in articles:
        html = article.get("article_html") or ""
        article["article_md"] = html2text.html2text(html)
        article["summary_md"] = "# TODO 接下来会实现"
    return articles


async def get_exist_urls(rss_id) -> set:
    exist_links = set()
    celery_async_session = get_celery_async_session()
    async with celery_async_session() as session:
        articles = await session.execute(select(RSSArticle).where(RSSArticle.rss_id == rss_id))
        for article in articles.scalars().all():
            exist_links.add(article.link)
    return exist_links


def discard_exists_entries(entries, exist_urls) -> List:
    return [entry for entry in entries if entry.get("link") not in exist_urls]


async def fetch_feed(url):
    logger.info(f"Fetching RSS feed: {url}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
        except Exception as e:
            logger.info(f"Error fetching RSS ({url}): {e}")
            return


def parse_feed(html):
    entries = []
    feed = feedparser.parse(html)
    for entry in feed.entries:
        description = parse_description(entry.get("summary") or entry.get("description") or "")
        entries.append(
            {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "description": description,
                "published_at": parse_date(entry.get("published") or ""),
            }
        )
    return entries


async def _async_download(entry, session, semaphore):
    async with semaphore:
        url = entry.get("link") or ""
        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    entry["article_html"] = await response.text()
                else:
                    logger.warning("%s status %s", url, response.status)
        except Exception as exc:
            logger.error("Download failed %s → %s", url, exc)
        return entry


async def fetch_articles(entries):
    semaphore = asyncio.Semaphore(10)  # 限制并发数
    async with aiohttp.ClientSession() as session:
        tasks = [_async_download(entry, session, semaphore) for entry in entries or []]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        articles = []
        for item in raw_results:
            if isinstance(item, Exception):
                logger.error("Article download exception: %s", item)
                continue
            articles.append(item)
        return articles


async def save_articles_to_db(rss_id, articles: List[Dict]):
    celery_async_session = get_celery_async_session()
    async with celery_async_session() as session:
        for article in articles or []:
            new_article = RSSArticle(rss_id=rss_id, **article)
            session.add(new_article)
        try:
            await session.commit()
            logger.info(f"Saved {len(articles)} new articles to database.")
        except IntegrityError as e:
            logger.error(f"IntegrityError during saving articles: {e}")
            await session.rollback()

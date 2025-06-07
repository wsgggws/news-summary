from asyncio import Semaphore

from openai import AsyncOpenAI

from celery_app.constants import PROMPT
from celery_app.util import logger
from settings import settings

async_client = AsyncOpenAI(base_url=settings.ai.BASE_URL, api_key=settings.ai.API_KEY)


async def sem_async_chat(article: dict, semaphore: Semaphore = Semaphore(10)):
    async with semaphore:
        return await async_chat(article)


async def async_chat(article: dict) -> dict:
    if not article:
        return article
    content = article.get("summary_md")
    if not content:
        return article
    if not settings.ai.API_KEY:
        return article
    params = {
        "model": settings.ai.MODEL,
        "messages": [
            {"role": "system", "content": PROMPT["SYSTEM"]},
            {"role": "user", "content": PROMPT["USER"].format(content=content)},
        ],
        "temperature": 0.1,
        "max_tokens": 4096,
        "timeout": 60,
    }
    try:
        response = await async_client.chat.completions.create(**params)
        content = response.choices[0].message.content
        article["summary_md"] = content
    except Exception as e:
        logger.error(f"{str(e)}", exc_info=True)
    finally:
        return article

import xml.etree.ElementTree as ET
from typing import Union

import aiohttp
import feedparser
from aiohttp.client import ClientTimeout
from pydantic import HttpUrl

from settings import settings


async def get_rss_title(url: Union[str, HttpUrl]) -> str:
    headers = {"User-Agent": settings.USER_AGENT}
    try:
        async with aiohttp.ClientSession(headers=headers, timeout=ClientTimeout(total=settings.RSS_TIMEOUT)) as session:
            async with session.get(str(url)) as response:
                if response.status != 200:
                    return ""

                content_type = response.headers.get("Content-Type", "")
                if "xml" not in content_type and "text" not in content_type:
                    return ""

                text = await response.text()
                root = ET.fromstring(text)
                tag = root.tag.lower()
                if tag == "rss" or tag.endswith("rss") or tag.endswith("feed") or tag.endswith("rdf"):
                    feed = feedparser.parse(text)
                    return feed.feed.get("title", "")
                else:
                    return ""
    except Exception:
        return ""


# 示例调用（测试用）
# if __name__ == "__main__":
#
#     async def main():
#         url = "https://xkcd.com/rss.xml"  # 你可以替换为任意 URL
#         url = "https://sspai.com/feed"  # 你可以替换为任意 URL
#         title = await get_rss_title(url)
#         print(f"Is valid RSS: {title}")
#
#     asyncio.run(main())

import asyncio

import pytest

from app.utils.validator import get_rss_title


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_validator():
    # 正常请求
    url = "https://sspai.com/feed"
    task1 = get_rss_title(url)

    # 超时异常
    url = "https://invalid_sspai.com/feed"
    task2 = get_rss_title(url)

    # https status code 404
    url = "https://sspai.com/feeds"
    task3 = get_rss_title(url)

    # 正常请求,但是 invalid RSS
    url = "https://wsgggws.github.io"
    task4 = get_rss_title(url)

    result = await asyncio.gather(*[task1, task2, task3, task4], return_exceptions=True)
    assert result == ["少数派", "", "", ""]

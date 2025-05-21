import asyncio

import pytest
from httpx import AsyncClient

from tests.helper import the_third_user


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_rss_subscribe_flow(generate_token, client: AsyncClient):
    """
    测试 RSS 订阅、获取、取消流程
    """
    token = generate_token(the_third_user["username"], "valid_token")
    headers = {"Authorization": f"Bearer {token}"}

    rss_data = {"url": "https://sspai.com/feed"}

    # ✅ 订阅 RSS
    response = await client.post("/api/v1/rss/subscribe", json=rss_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == rss_data["url"]
    assert data["title"] == "少数派"
    assert data["message"] == "success"
    rss_id = data["id"]

    # ❌ 再次订阅会抛出重复异常
    response = await client.post("/api/v1/rss/subscribe", json=rss_data, headers=headers)
    assert response.status_code == 400
    assert "URL has been subscribed for you." in response.text

    rss_data = {"url": "https://weekly.tw93.fun/rss.xml"}
    # Rate limit
    response = await client.post("/api/v1/rss/subscribe", json=rss_data, headers=headers)
    assert response.status_code == 429

    await asyncio.sleep(1 + 1)

    # ✅ 在一分钟后再次订阅该 RSS，订阅成功
    response = await client.post("/api/v1/rss/subscribe", json=rss_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == rss_data["url"]
    assert data["title"] == "潮流周刊"
    assert data["message"] == "success"
    rss_id = data["id"]

    # ✅ 获取当前用户所有订阅
    response = await client.get("/api/v1/rss/subscriptions", headers=headers)
    assert response.status_code == 200
    subs = response.json()
    assert any(feed["id"] == rss_id for feed in subs)

    # ✅ 取消订阅
    response = await client.delete(f"/api/v1/rss/unsubscribe/{rss_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "取消订阅成功"

    # ❌ 再次取消应返回未找到
    response = await client.delete(f"/api/v1/rss/unsubscribe/{rss_id}", headers=headers)
    assert response.status_code == 404
    assert "RSS id does not found." in response.text

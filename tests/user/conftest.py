from datetime import datetime, timedelta, timezone

import pytest_asyncio
from httpx import AsyncClient
from jose import jwt

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from tests.helper import the_first_user, the_second_user


@pytest_asyncio.fixture(scope="function")
def generate_token():
    def _generate_token(username="wsgggws", token_type="valid_token"):

        payload = {
            "sub": username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        if token_type == "expired_token":
            payload["exp"] = datetime.now(tz=timezone.utc) - timedelta(minutes=1)  # 生成过期 token
        elif token_type == "invalid_token":
            return "invalid.token.string"
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return _generate_token


# module 意味着在 user 这个模块下执行一次
@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_user_in_database(client: AsyncClient):
    # 插入两个个测试用户
    response = await client.post("/api/v1/user/register", json=the_first_user)
    assert response.status_code == 200
    response = await client.post("/api/v1/user/register", json=the_second_user)
    assert response.status_code == 200
    yield

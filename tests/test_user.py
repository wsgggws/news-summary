import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "test_user, expected_status, expected_details",
    [
        # 成功注册用例
        ({"username": "new_user", "email": "new_user@example.com", "password": "Passw0rd;"}, 200, ""),
        ({"username": "new_username", "email": "new_username@example.com", "password": "Passw0rd;"}, 200, ""),
        # 用户名重复
        ({"username": "new_user", "email": "new_email@example.com", "password": "Passw0rd;"}, 400, "(username)"),
        # 邮箱重复
        ({"username": "new_user2", "email": "new_user@example.com", "password": "Passw0rd;"}, 400, "(email)"),
        # 用户名长度不符合要求
        ({"username": "usr", "email": "invalid_username@example.com", "password": "Passw0rd;"}, 422, "username"),
        # 密码长度不符合要求
        ({"username": "new_user3", "email": "new_user3@example.com", "password": "short"}, 422, "password"),
        # 密码不符合复杂性要求
        ({"username": "new_user4", "email": "new_user4@example.com", "password": "NoSpecial123"}, 422, "password"),
        # 无效的邮箱格式
        ({"username": "new_user5", "email": "invalid_email", "password": "Passw0rd;"}, 422, "email"),
    ],
)
# @pytest.mark.asyncio
async def test_register_user(test_user, expected_status, expected_details, client):
    """测试用户注册的各种情况"""
    response = await client.post("/api/v1/user/register", json=test_user)
    assert response.status_code == expected_status
    assert expected_details in response.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, expected_status, expected_response",
    [
        # ✅ 正确的用户名和密码
        ("new_user", "Passw0rd;", 200, "access_token"),
        # ❌ 错误的用户名
        ("invalid_user", "correct_password", 401, "Incorrect username or password"),
        # ❌ 错误的密码
        ("new_user", "wrong_password", 401, "Incorrect username or password"),
        # ❌ 用户名为空
        ("", "correct_password", 422, "Username and password is required"),
        # ❌ 密码为空
        ("valid_user", "", 422, "Username and password is required"),
    ],
)
async def test_login_for_access_token(username, password, expected_status, expected_response, client: AsyncClient):
    """
    测试 `/token` 登录接口的不同情况
    """
    # 准备登录请求数据
    login_data = {"username": username, "password": password}
    response = await client.post("/api/v1/user/token", data=login_data)
    assert response.status_code == expected_status

    response_json = response.json()
    if expected_status == 200:
        assert "access_token" in response_json
        assert response_json["token_type"] == "bearer"
    else:
        assert expected_response in response_json["detail"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_user, token, expected_status, expected_response",
    [
        # ✅ 有效的 JWT 令牌
        ("new_user", "valid_token", 200, "username"),
        # ❌ 无效的 JWT 令牌
        ("new_user", "invalid_token", 401, "Could not validate credentials"),
        # ❌ 过期的 JWT 令牌
        ("new_user", "expired_token", 401, "Could not validate credentials"),
        # ❌ 没有提供 Token
        ("new_user", None, 401, "Not authenticated"),
    ],
)
async def test_user_me(current_user, token, expected_status, expected_response, generate_token, client: AsyncClient):
    """
    测试 `/me` 获取当前用户接口的不同情况
    """
    # 生成测试用的 JWT 令牌
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {generate_token(current_user, token)}"}

    response = await client.get("/api/v1/user/me", headers=headers)
    assert response.status_code == expected_status

    response_json = response.json()
    if expected_status == 200:
        assert "username" in response_json
    else:
        assert expected_response in response_json["detail"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_user, token, user_update, expected_status, expected_response",
    [
        # ✅ 修改用户名, new_username 也已经存在过了, 所以 400
        ("new_user", "valid_token", {"username": "new_username"}, 400, "(username)"),  # new_username 也已经存在过了
        # ✅ 修改用户名, # new_diff_username 也不存在, 所以 200，修改成功
        ("new_user", "valid_token", {"username": "new_diff_username"}, 200, "new_diff_username"),
        # ✅ 修改邮箱  email new_email@example.com 也已经存在过了, 所以 400
        ("new_username", "valid_token", {"email": "new_user@example.com"}, 400, "(email)"),
        # ✅ 修改邮箱  email new_diff_email@example.com 不存在, 所以 200 , 修改成功
        ("new_username", "valid_token", {"email": "new_diff_email@example.com"}, 200, "new_diff_email@example.com"),
        # ✅ 修改密码（不影响返回数据）
        ("new_username", "valid_token", {"password": "NewPassw0rd!"}, 200, "new_username"),
        # ❌ 无效 JWT 令牌
        ("", "invalid_token", {"username": "fail_username"}, 401, "Could not validate credentials"),
        # ❌ 过期 JWT 令牌
        ("", "expired_token", {"email": "fail_email@example.com"}, 401, "Could not validate credentials"),
        # ❌ 无 Token
        ("", None, {"username": "fail_username"}, 401, "Not authenticated"),
    ],
)
async def test_update_user_me(
    current_user, token, user_update, expected_status, expected_response, generate_token, client: AsyncClient
):
    """
    测试 `/me` 端点更新用户信息的不同情况
    """
    # 生成测试用的 JWT 令牌
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {generate_token(current_user, token)}"}

    response = await client.put("/api/v1/user/me", headers=headers, json=user_update)
    assert response.status_code == expected_status
    response_json = response.json()
    if expected_status == 200:
        if "password" not in user_update:
            assert user_update.get("username", user_update.get("email")) in response_json.values()
    else:
        assert expected_response in response_json["detail"]

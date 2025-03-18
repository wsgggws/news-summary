import pytest


@pytest.mark.run(order=1)
@pytest.mark.asyncio
async def test_register_first_user(client):
    # 成功注册用例
    first_user = {"username": "new_user", "email": "new_user@example.com", "password": "Passw0rd;"}
    response = await client.post("/api/v1/user/register", json=first_user)
    print(response.status_code, response.text)
    assert response.status_code == 200
    second_user = {"username": "new_user", "email": "new_email@example.com", "password": "Passw0rd;"}
    response = await client.post("/api/v1/user/register", json=second_user)
    assert response.status_code == 400
    thrid_user = {"username": "new_user2", "email": "new_user@example.com", "password": "Passw0rd;"}
    response = await client.post("/api/v1/user/register", json=thrid_user)
    assert response.status_code == 400


@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "test_user, expected_status",
    [
        # 用户名重复
        ({"username": "new_user", "email": "new_email@example.com", "password": "Passw0rd;"}, 400),
        # 邮箱重复
        ({"username": "new_user2", "email": "new_user@example.com", "password": "Passw0rd;"}, 400),
        # 用户名长度不符合要求
        ({"username": "usr", "email": "invalid_username@example.com", "password": "Passw0rd;"}, 422),
        # 密码长度不符合要求
        ({"username": "new_user3", "email": "new_user3@example.com", "password": "short"}, 422),
        # 密码不符合复杂性要求
        ({"username": "new_user4", "email": "new_user4@example.com", "password": "NoSpecial123"}, 422),
        # 无效的邮箱格式
        ({"username": "new_user5", "email": "invalid_email", "password": "Passw0rd;"}, 422),
    ],
)
@pytest.mark.asyncio
async def test_register_user(test_user, expected_status, client):
    """测试用户注册的各种情况"""
    response = await client.post("/api/v1/user/register", json=test_user)
    assert response.status_code == expected_status

import pytest

from db.application_dal import ApplicationDAL


async def create_user(async_client, params):
    response = await async_client.post("users", params=params)
    return response


@pytest.mark.asyncio
async def test_create_user_with_success(async_client, setup_db):
    params = {"name": "Ana Paula", "username": "anapaula"}

    response = await create_user(async_client, params)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_and_raise_exception(async_client, setup_db, mocker):
    params = {"name": "Ana Paula", "username": "anapaula"}

    create_user_mock = mocker.patch.object(ApplicationDAL, "create_user")
    create_user_mock.create_user.side_effect = Exception("Fake error", 400)

    response = await create_user(async_client, params)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_users_with_success(async_client, setup_db):
    params = {"name": "Ana Paula", "username": "anapaula"}
    await create_user(async_client, params)
    params = {"name": "Maria", "username": "maria"}
    await create_user(async_client, params)

    response = await async_client.get("users")

    result = response.json()
    assert response.status_code == 200
    assert result[0]["username"] == "anapaula"
    assert result[1]["username"] == "maria"
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_user_with_success(async_client, setup_db):
    params = {"name": "Ana Paula", "username": "anapaula"}
    response = await create_user(async_client, params)

    user_id = response.json()["id"]

    response = await async_client.get(f"users/{user_id}")

    result = response.json()
    assert response.status_code == 200
    assert result["username"] == "anapaula"

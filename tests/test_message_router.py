import uuid

import pytest


async def create_user(async_client, params):
    response = await async_client.post("users", params=params)
    return response


async def create_message(async_client):
    sender_params = {"name": "Ana Paula", "username": "anapaula"}
    sender = await create_user(async_client, sender_params)
    receiver_params = {"name": "Maria", "username": "maria"}
    receiver = await create_user(async_client, receiver_params)

    params = {
        "content": "Mensagem de Teste",
        "sender_id": sender.json()["id"],
        "receiver_id": receiver.json()["id"],
    }

    headers = {"x-real-ip": "168.227.17.187"}
    response = await async_client.post("messages", params=params, headers=headers)

    return response


@pytest.mark.asyncio
async def test_send_message_with_success(async_client, setup_db):
    response = await create_message(async_client)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_list_messages_with_success(async_client, setup_db):
    await create_message(async_client)

    headers = {"x-real-ip": "168.227.17.187"}

    response = await async_client.get("messages", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_message_with_success(async_client, setup_db):
    message = await create_message(async_client)

    message_id = message.json()["id"]

    headers = {"x-real-ip": "168.227.17.187"}

    response = await async_client.get(f"messages/{message_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["content"] == "Mensagem de Teste"


@pytest.mark.asyncio
async def test_reply_message_with_success(async_client, setup_db):
    message = await create_message(async_client)
    assert message.json()["reply_id"] is None

    message_id = message.json()["id"]

    headers = {"x-real-ip": "168.227.17.187"}

    params = {"content": "Resposta de Teste"}

    response = await async_client.put(
        f"messages/{message_id}/reply", headers=headers, params=params
    )

    assert response.status_code == 200
    assert response.json() == "Reply sent"

    message = await async_client.get(f"messages/{message_id}", headers=headers)

    assert message.json()["reply_id"] is not None


@pytest.mark.asyncio
async def test_forward_message_with_success(async_client, setup_db):
    message = await create_message(async_client)
    assert message.json()["forwarded_to_id"] is None
    message_id = message.json()["id"]

    user_params = {"name": "João", "username": "joao"}
    user = await create_user(async_client, user_params)
    user_id = user.json()["id"]

    headers = {"x-real-ip": "168.227.17.187"}

    params = {"forwarded_to_id": uuid.UUID(user_id)}

    response = await async_client.put(
        f"messages/{message_id}/forward", headers=headers, params=params
    )

    assert response.status_code == 200
    assert response.json() == "Message forwarded"

    message = await async_client.get(f"messages/{message_id}", headers=headers)

    assert message.json()["forwarded_to_id"] is not None


@pytest.mark.asyncio
async def test_delete_message_with_success(async_client, setup_db):
    message = await create_message(async_client)

    message_id = message.json()["id"]

    headers = {"x-real-ip": "168.227.17.187"}

    response = await async_client.delete(f"messages/{message_id}", headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_list_messages_with_block_by_rate_limit(async_client, setup_db):
    headers = {"x-real-ip": "168.227.17.187"}

    for i in range(20):
        response = await async_client.get("messages", headers=headers)

    assert response.status_code == 429

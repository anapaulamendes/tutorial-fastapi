import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

from db.config import engine, Base
from main import app

BASE_URL = "http://127.0.0.1:8000/"


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client


@pytest_asyncio.fixture
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

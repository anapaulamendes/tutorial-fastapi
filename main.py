from contextlib import asynccontextmanager

from fastapi import FastAPI
from ratelimit import RateLimitMiddleware, Rule
from rate_limit_client import client_ip
from ratelimit.backends.simple import MemoryBackend

from db.config import engine, Base
from routers import message_router, user_router

MEMORY_BACKEND = MemoryBackend()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    RateLimitMiddleware,
    authenticate=client_ip,
    backend=MEMORY_BACKEND,
    config={
        r"^/messages": [Rule(minute=10)],
    },
)

app.include_router(user_router.router)
app.include_router(message_router.router)


""""
It's deprecated
"""
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# @app.on_event('shutdown')
# async def shutdown_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

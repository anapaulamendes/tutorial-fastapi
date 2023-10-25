from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.config import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


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

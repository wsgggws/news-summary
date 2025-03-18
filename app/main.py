from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.routes import user
from app.services.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)


@app.get("/whoami")
async def root():
    return {"whoami": "news-summary"}

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.error_handlers import setup_exception_handlers
from app.routes import user
from app.services.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)

setup_exception_handlers(app)


@app.get("/whoami")
async def root():
    return {"whoami": "news-summary"}

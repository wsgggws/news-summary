import logging

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.error_handlers import setup_exception_handlers
from app.middleware_handlers import setup_middlewares
from app.routes import rss, user
from app.services.database import init_db

# 可以使用 zero code 的形式, 但不能使用 --reload 参数启动 fastapi 服务
# from app.tracer import initialize_tracer
# initialize_tracer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user.router)
app.include_router(rss.router)

setup_exception_handlers(app)
setup_middlewares(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/whoami")
async def root():
    logger.info("test otel logs to grafana")
    return {"whoami": "news-summary"}

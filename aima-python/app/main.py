"""AIMA Python AI 引擎入口:FastAPI 应用 + RocketMQ 消费者。"""
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.consumers.collect_consumer import start_collect_consumer
from app.consumers.generation_consumer import start_consumer
from app.core.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """应用启动时拉起 RocketMQ 消费者线程,关闭时随进程退出。"""
    threading.Thread(target=start_consumer, daemon=True).start()
    threading.Thread(target=start_collect_consumer, daemon=True).start()
    yield


app = FastAPI(
    title="AIMA Python AI Engine",
    version="0.1.0",
    description="感知/创作/编辑/质检 Agent 的 AI 引擎(M1 骨架)",
    lifespan=lifespan,
)
app.include_router(router)
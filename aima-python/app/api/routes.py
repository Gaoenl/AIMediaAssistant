"""内部接口路由(/internal/*),仅服务 Java 后端调用。"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.collect import collect

router = APIRouter(prefix="/internal")


class CollectRequest(BaseModel):
    """采集请求:M2 按 sources 决定采集哪些数据源。"""

    sources: list[str] = []


@router.get("/health")
async def health() -> dict[str, str]:
    """健康检查,供运维与 Java 探活。"""
    return {"status": "ok"}


@router.post("/collect")
async def collect_topics(req: CollectRequest) -> dict:
    """触发热点采集(由 Java Scheduler 定时调用)。"""
    return await collect(req.sources)
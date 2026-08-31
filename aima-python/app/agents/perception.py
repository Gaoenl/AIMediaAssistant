"""感知 Agent:并发采集 → 冷却/健康检查 → 回调 Java 入库。"""
import asyncio
import logging
import time

from app.agents.collectors import build_aggregator, build_collectors
from app.clients.topic_client import topic_client
from app.core.config import settings

logger = logging.getLogger(__name__)
# 进程内状态:source -> {fail_count, down, last_at}
_health: dict[str, dict] = {}
_aggregators: dict[str, object] = {}

def _due(name: str, collector) -> bool:
    """按冷却时间判断是否到采集时机。"""
    last = _health.get(name, {}).get("last_at", 0)
    return (time.time() - last) >= collector.cooldown_seconds

def _mark(name: str, ok: bool, now: float) -> None:
    state = _health.setdefault(name, {"fail_count": 0, "down": False, "last_at": 0})
    if ok:
        state["fail_count"] = 0
        state["down"] = False
        state["last_at"] = now
    else:
        state["fail_count"] += 1
        if state["fail_count"] >= settings.collect_fail_threshold:
            state["down"] = True
            logger.warning("采集源 %s 连续失败 %s 次,标记 DOWN", name, state["fail_count"])
async def perceive(sources: list[str] | None = None) -> int:
    """执行一轮采集,返回成功入库条数。"""
    collectors = build_collectors()
    targets = [n for n in collectors if not sources or n in sources]
    sem = asyncio.Semaphore(settings.collect_concurrency)

    async def run_one(name: str) -> list:
        now = time.time()
        if _health.get(name, {}).get("down"):
            # DOWN 源切聚合兜底;聚合也失败则跳过
            agg = _aggregators.setdefault(name, build_aggregator(name))
            if not _due(name, agg):
                return []
            try:
                items = await agg.fetch()
                _mark(name, True, now)
                logger.info("采集源 %s 由聚合兜底返回 %s 条", name, len(items))
                return items
            except Exception as e:
                logger.warning("采集源 %s 聚合兜底也失败: %s", name, e)
                return []
        collector = collectors[name]
        if not _due(name, collector):
            return []
        async with sem:
            try:
                items = await collector.fetch()
                _mark(name, True, now)
                logger.info("采集源 %s 返回 %s 条", name, len(items))
                return items
            except Exception as e:
                _mark(name, False, now)
                logger.warning("采集源 %s 失败: %s", name, e)
                return []

    results = await asyncio.gather(*(run_one(n) for n in targets))
    items = [item for batch in results for item in batch]
    if not items:
        logger.warning("本轮采集无数据")
        return 0
    return await topic_client.push_topics(items)
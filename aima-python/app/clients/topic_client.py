"""Java 内部接口客户端:热点批量入库(回调 /internal/v1/topics/collect)。"""
import logging
from datetime import timezone

import httpx

from app.agents.collectors.base import RawTopic
from app.core.config import settings

logger = logging.getLogger(__name__)


class TopicClient:
    def __init__(self, base_url: str = settings.java_base_url, timeout: float = 15.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def push_topics(self, items: list[RawTopic]) -> int:
        """批量回调 Java,返回 Java 确认入库条数。"""
        payload = [{
            "source": i.source,
            "sourceId": i.source_id,
            "title": i.title,
            "url": i.url,
            "description": i.description,
            "hotScore": i.hot_score,
            "collectedAt": i.collected_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        } for i in items]
        resp = self._client.post("/internal/v1/topics/collect", json=payload)
        resp.raise_for_status()
        data = resp.json().get("data") or {}
        count = data.get("count", len(payload))
        logger.info("热点回调成功,提交 %s 条,入库 %s 条", len(payload), count)
        return count
topic_client = TopicClient()
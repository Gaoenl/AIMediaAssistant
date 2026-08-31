"""RSS 采集器:36氪 / 虎嗅 共用。"""
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import httpx

from app.agents.collectors.base import Collector, RawTopic
RSS_SOURCES = {
    "rss_36kr": "https://36kr.com/feed",
    "rss_huxiu": "https://www.huxiu.com/rss/0.xml",
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"
def _age_hours(pub_date: str) -> float:
    try:
        dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 3600)
    except Exception:
        return 0.0
class RssCollector(Collector):
    def __init__(self, source: str):
        self.source = source

    async def fetch(self) -> list[RawTopic]:
        async with httpx.AsyncClient(timeout=10, headers={"User-Agent": UA}) as client:
            resp = await client.get(RSS_SOURCES[self.source])
            resp.raise_for_status()
        root = ET.fromstring(resp.text)
        items = []
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            if not title or not link:
                continue
            age = _age_hours(item.findtext("pubDate") or "")
            items.append(RawTopic(
                source=self.source,
                source_id=link,
                title=title,
                url=link,
                description=(item.findtext("description") or "")[:200],
                hot_score=max(20, 80 - int(age * 3)),
            ))
        return items
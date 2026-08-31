"""头条热榜采集器(实验源)。"""
import math

import httpx

from app.agents.collectors.base import Collector, RawTopic

URL = "https://www.toutiao.com/hot-event/hot-board/"


class ToutiaoCollector(Collector):
    source = "toutiao_hot"
    cooldown_seconds = 3600

    async def fetch(self) -> list[RawTopic]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36",
            "Referer": "https://www.toutiao.com/hot/",
        }
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            resp = await client.get(URL, params={"origin": "toutiao_pc"})
            resp.raise_for_status()
            data = resp.json().get("data", [])
        items = []
        for d in data:
            title = d.get("Title", "").strip()
            if not title:
                continue
            items.append(RawTopic(
                source=self.source,
                source_id=d.get("ClusterId") or title,
                title=title,
                url=d.get("Url", ""),
                hot_score=min(100, round(15 * math.log10(max(int(d.get("HotValue", 0) or 0), 1)))),
            ))
        return items
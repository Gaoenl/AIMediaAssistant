"""微博热搜采集器(实验源)。"""
import math
from urllib.parse import quote

import httpx

from app.agents.collectors.base import Collector, RawTopic

URL = "https://weibo.com/ajax/side/hotSearch"


class WeiboCollector(Collector):
    source = "weibo_hot"
    cooldown_seconds = 3600

    async def fetch(self) -> list[RawTopic]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36",
            "Referer": "https://weibo.com/",
        }
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            resp = await client.get(URL)
            resp.raise_for_status()
            realtime = (resp.json().get("data") or {}).get("realtime", [])
        items = []
        for rank, r in enumerate(realtime, start=1):
            word = r.get("word", "").strip()
            if not word:
                continue
            num = int(r.get("num", 0) or 0)
            score = min(100, round(15 * math.log10(max(num, 1)))) if num else max(0, 100 - rank * 2)
            items.append(RawTopic(
                source=self.source,
                source_id=word,
                title=word,
                url=f"https://s.weibo.com/weibo?q={quote(word)}",
                description=r.get("note", "")[:200],
                hot_score=score,
            ))
        return items
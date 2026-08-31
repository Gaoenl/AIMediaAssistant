"""抖音热榜采集器(实验源,需 UA/Referer,可能被风控)。"""
import math
from urllib.parse import quote

import httpx

from app.agents.collectors.base import Collector, RawTopic

URL = "https://www.douyin.com/aweme/v1/web/hot/search/list/"


class DouyinCollector(Collector):
    source = "douyin_hot"
    cooldown_seconds = 3600

    async def fetch(self) -> list[RawTopic]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
            "Referer": "https://www.douyin.com/hot",
        }
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            resp = await client.get(URL)
            resp.raise_for_status()
            word_list = (resp.json().get("data") or {}).get("word_list", [])
        items = []
        for w in word_list[:50]:
            word = w.get("word", "").strip()
            if not word:
                continue
            items.append(RawTopic(
                source=self.source,
                source_id=w.get("sentence_id") or word,
                title=word,
                url=f"https://www.douyin.com/search/{quote(word)}",
                hot_score=min(100, round(15 * math.log10(max(int(w.get("hot_value", 0) or 0), 1)))),
            ))
        return items
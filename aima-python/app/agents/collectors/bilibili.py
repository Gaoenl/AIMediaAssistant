"""B站热门采集器。"""
import math

import httpx

from app.agents.collectors.base import Collector, RawTopic

URL = "https://api.bilibili.com/x/web-interface/ranking/v2"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"
class BilibiliCollector(Collector):
    source = "bilibili_hot"

    async def fetch(self) -> list[RawTopic]:
        async with httpx.AsyncClient(timeout=10, headers={"User-Agent": UA}) as client:
            resp = await client.get(URL, params={"rid": 0, "type": "all"})
            resp.raise_for_status()
            data = resp.json().get("data") or {}
            video_list = data.get("list", [])
        items = []
        for v in video_list:
            bvid = v.get("bvid", "")
            if not bvid:
                continue
            view = int(v.get("stat", {}).get("view", 0) or 0)
            items.append(RawTopic(
                source=self.source,
                source_id=bvid,
                title=v.get("title", "").strip(),
                url=f"https://www.bilibili.com/video/{bvid}",
                description=v.get("desc", "")[:200],
                hot_score=min(100, round(20 * math.log10(max(view, 1)))),
            ))
        return items
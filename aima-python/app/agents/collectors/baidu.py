"""百度热搜采集器(实验源)。"""
import math
import re

import httpx

from app.agents.collectors.base import Collector, RawTopic

URL = "https://top.baidu.com/api/board"


def _parse_hot(value) -> int:
    """支持 "1234万" / "1.2亿" 等字符串。"""
    try:
        m = re.match(r"([\d.]+)(万|亿)?", str(value).strip())
        num = float(m.group(1))
        return int(num * (10000 if m.group(2) == "万" else 100000000 if m.group(2) == "亿" else 1))
    except Exception:
        return 0


class BaiduCollector(Collector):
    source = "baidu_hot"
    cooldown_seconds = 3600

    async def fetch(self) -> list[RawTopic]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36",
            "Referer": "https://top.baidu.com/board?tab=realtime",
        }
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            resp = await client.get(URL, params={"platform": "wise", "tab": "realtime"})
            resp.raise_for_status()
            cards = (resp.json().get("data") or {}).get("cards", [])
        items = []
        for card in cards:
            top = card.get("topcontent") or {}
            word = top.get("word", "").strip()
            if not word:
                continue
            items.append(RawTopic(
                source=self.source,
                source_id=word,
                title=word,
                url=top.get("url", ""),
                description=top.get("desc", "")[:200],
                hot_score=min(100, round(15 * math.log10(max(_parse_hot(top.get("hotScore", 0)), 1)))),
            ))
        return items
import httpx

from app.agents.collectors.base import Collector, RawTopic

URL = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"

class ZhihuCollector(Collector):
    source = "zhihu_hot"
    async def fetch(self) -> list[RawTopic]:
        async with httpx.AsyncClient(timeout=10, headers={"User-Agent": UA}) as client:
            resp = await client.get(URL, params={"limit": 50})
            resp.raise_for_status()
            data = resp.json().get("data", [])
        items = []
        for rank, item in enumerate(data, start=1):
            target = item.get("target", {})
            source_id = str(target.get("id", ""))
            if not source_id:
                continue
            items.append(RawTopic(
                source=self.source,
                source_id=source_id,
                title=target.get("title", "").strip(),
                url=f"https://www.zhihu.com/question/{source_id}",
                description=target.get("excerpt", "")[:200],
                hot_score=max(0, 100 - rank * 2),
            ))
        return items

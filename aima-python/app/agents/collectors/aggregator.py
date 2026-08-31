"""聚合兜底采集器:实验源 DOWN 时接管(vvhan 免费聚合,字段以服务方文档为准)。"""
import httpx

from app.agents.collectors.base import Collector, RawTopic

VVHAN_MAP = {
    "douyin_hot": "douyinHot",
    "weibo_hot": "wbHot",
    "baidu_hot": "baiduRD",
    "zhihu_hot": "zhihuHot",
    "toutiao_hot": "toutiao",
}


class AggregatorCollector(Collector):
    def __init__(self, source: str):
        self.source = source
        self._slug = VVHAN_MAP[source]

    async def fetch(self) -> list[RawTopic]:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"https://api.vvhan.com/api/hotlist/{self._slug}")
            resp.raise_for_status()
            data = resp.json().get("data", [])
        items = []
        for d in data:
            title = (d.get("title") or "").strip()
            if not title:
                continue
            hot = 0
            try:
                hot = int(str(d.get("hot", "0")).replace(",", ""))
            except Exception:
                hot = 50
            items.append(RawTopic(
                source=self.source,
                source_id=title,
                title=title,
                url=d.get("url", ""),
                hot_score=hot or 50,
            ))
        return items
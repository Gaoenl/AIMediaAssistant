"""节日/节气日历采集器(静态 JSON,近 7 天窗口)。"""
import json
from datetime import date, timedelta
from pathlib import Path

from app.agents.collectors.base import Collector, RawTopic

_FESTIVALS_FILE = Path(__file__).parent / "data" / "festivals.json"


class FestivalCollector(Collector):
    source = "festival"
    cooldown_seconds = 86400  # 每日一次

    async def fetch(self) -> list[RawTopic]:
        festivals = json.loads(_FESTIVALS_FILE.read_text(encoding="utf-8"))
        today = date.today()
        window = {today + timedelta(days=offset) for offset in range(-7, 8)}
        items = []
        for f in festivals:
            d = date.fromisoformat(f["date"])
            if d not in window:
                continue
            name = f["name"]
            items.append(RawTopic(
                source=self.source,
                source_id=f"{d.isoformat()}-{name}",
                title=f"{name}将至,相关热点值得提前布局",
                description="关键词:" + ",".join(f.get("keywords", [])),
                hot_score=int(f.get("weight", 70)),
            ))
        return items
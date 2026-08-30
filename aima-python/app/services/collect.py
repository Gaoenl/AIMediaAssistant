"""热点采集服务:M2 接入知乎热榜 / B站热门 / 36氪 RSS / 节日日历。"""
from typing import Any


async def collect(sources: list[str]) -> dict[str, Any]:
    """采集并归一化热点,返回候选选题列表。

    M1:占位实现。
    M2:每个数据源一个采集器(collectors/ 包),统一归一化 + 热度评分,
       由 Java Scheduler 定时调用本接口。
    """
    return {"items": []}
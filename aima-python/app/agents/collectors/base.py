"""热点采集器基类与统一数据结构。"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RawTopic:
    """归一化热点条目,字段与 Java topic 表对齐。"""
    source: str
    source_id: str
    title: str
    url: str = ""
    description: str = ""
    hot_score: int = 0
    collected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class Collector(ABC):
    """热点采集器基类:每个来源一个实现,独立失败隔离。"""

    source: str = ""            # 来源标识,与 Java topic.source 一致
    cooldown_seconds: int = 1800  # 采集冷却时间(官方源 30 分钟)

    @abstractmethod
    async def fetch(self) -> list[RawTopic]:
        """拉取并归一化热点;网络/解析失败抛异常,由编排层隔离。"""
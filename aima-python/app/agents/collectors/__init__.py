"""采集器注册表:9 个来源 + 聚合兜底工厂。"""
from app.agents.collectors.baidu import BaiduCollector
from app.agents.collectors.bilibili import BilibiliCollector
from app.agents.collectors.douyin import DouyinCollector
from app.agents.collectors.festival import FestivalCollector
from app.agents.collectors.rss import RssCollector
from app.agents.collectors.toutiao import ToutiaoCollector
from app.agents.collectors.weibo import WeiboCollector
from app.agents.collectors.zhihu import ZhihuCollector


def build_collectors() -> dict[str, object]:
    """返回 来源名 -> Collector 实例。"""
    return {
        "zhihu_hot": ZhihuCollector(),
        "bilibili_hot": BilibiliCollector(),
        "rss_36kr": RssCollector("rss_36kr"),
        "rss_huxiu": RssCollector("rss_huxiu"),
        "festival": FestivalCollector(),
        "douyin_hot": DouyinCollector(),
        "weibo_hot": WeiboCollector(),
        "baidu_hot": BaiduCollector(),
        "toutiao_hot": ToutiaoCollector(),
    }


def build_aggregator(source: str) -> object:
    """构造聚合兜底采集器。"""
    from app.agents.collectors.aggregator import AggregatorCollector
    return AggregatorCollector(source)
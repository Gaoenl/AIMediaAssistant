"""RocketMQ 消费者:接收采集任务并驱动一轮感知采集。"""
import asyncio
import json
import logging
import threading

from rocketmq.client import ConsumeStatus, PushConsumer

from app.agents.perception import perceive
from app.core.config import settings

logger = logging.getLogger(__name__)


def _handle_collect(msg) -> ConsumeStatus:
    try:
        body = json.loads(msg.body.decode("utf-8"))
        logger.info("收到采集任务 collectId=%s", body.get("collectId"))
        asyncio.run(perceive())
        return ConsumeStatus.CONSUME_SUCCESS
    except Exception:
        logger.exception("采集任务失败,交给 MQ 重试")
        return ConsumeStatus.RECONSUME_LATER


def start_collect_consumer() -> None:
    """启动热点采集消费者(独立线程常驻)。"""
    consumer = PushConsumer(settings.collect_consumer_group)
    consumer.set_name_server_address(settings.rocketmq_nameserver)
    consumer.subscribe(settings.collect_topic, _handle_collect)
    consumer.start()
    logger.info("RocketMQ 采集消费者已启动 topic=%s group=%s",
                settings.collect_topic, settings.collect_consumer_group)
    threading.Event().wait()
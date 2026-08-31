"""RocketMQ 消费者:接收生成任务并驱动"拉参数 → 生成 → 回调"链路。

重试语义(与方案一致):
- 瞬时异常(网络/依赖不可用)  → 返回 RECONSUME_LATER,交给 RocketMQ 消费重试;
- 业务失败(生成结果 FAILED)  → 仍回调 Java 并返回 CONSUME_SUCCESS,
  业务级重试由 Java 任务状态机控制(上限 2 次),避免 MQ 无限重投。
"""
import asyncio
import json
import logging
import threading

from rocketmq.client import ConsumeStatus, PushConsumer
from app.clients.java_client import java_client
from app.core.config import settings
from app.services.generation import generate_article

logger = logging.getLogger(__name__)


def _handle_message(msg) -> ConsumeStatus:
    """单条生成任务回调:按 taskId 拉参数、执行生成、回传结果。"""
    try:
        body = json.loads(msg.body.decode("utf-8"))
        task_id = body["taskId"]
        logger.info("收到生成任务 taskId=%s", task_id)

        # 1) 消息体只带 taskId,任务参数从 Java 拉取
        task = java_client.get_task(task_id)
        # 2) 执行生成(M2 为 LangGraph Agent 编排)
        result = asyncio.run(generate_article(task.topic, task.stylePrompt))
        # 3) 无论成功失败都回调 Java,由任务状态机决定后续
        java_client.send_callback(task_id, result)
        return ConsumeStatus.CONSUME_SUCCESS
    except Exception:
        logger.exception("消费任务失败,交给 MQ 重试")
        return ConsumeStatus.RECONSUME_LATER


def start_consumer() -> None:
    """启动 RocketMQ 消费者(在独立线程中运行,进程内常驻)。"""
    consumer = PushConsumer(settings.consumer_group)
    consumer.set_name_server_address(settings.rocketmq_nameserver)
    consumer.subscribe(settings.topic, _handle_message)
    consumer.start()
    logger.info("RocketMQ 消费者已启动 topic=%s group=%s",
                settings.topic, settings.consumer_group)
    threading.Event().wait()  # 阻塞当前线程,保持消费者存活

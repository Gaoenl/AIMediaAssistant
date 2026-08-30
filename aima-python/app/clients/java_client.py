"""Java 后端内部 API 客户端:集中封装"拉取任务 / 回传结果"。

M2 需补充内部签名鉴权(请求头携带 appKey + 签名),防止 /internal 被外部调用。
"""
import httpx

from app.core.config import settings
from app.schemas.task import GenerationResult, TaskInfo


class JavaClient:
    """Java 侧 /internal/v1/tasks/* 的轻量客户端。"""

    def __init__(self, base_url: str = settings.java_base_url, timeout: float = 10.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def get_task(self, task_id: str) -> TaskInfo:
        """按 taskId 拉取任务参数(消息体只带 taskId,参数从 Java 获取)。"""
        resp = self._client.get(f"/internal/v1/tasks/{task_id}")
        resp.raise_for_status()
        return TaskInfo.model_validate(resp.json()["data"])

    def send_callback(self, task_id: str, result: GenerationResult) -> None:
        """生成完成后回调 Java,由 Java 落库并更新任务状态。"""
        resp = self._client.post(
            f"/internal/v1/tasks/{task_id}/callback",
            json=result.model_dump(exclude_none=True),
        )
        resp.raise_for_status()


# 全局单例,消费者与服务共用
java_client = JavaClient()
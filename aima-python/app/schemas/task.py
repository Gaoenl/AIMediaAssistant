"""任务相关契约:字段与 Java 侧 dto 对齐(camelCase)。"""
from typing import Optional

from pydantic import BaseModel


class TaskInfo(BaseModel):
    """Java 返回的任务信息(对应 /internal/v1/tasks/{id} 的 data)。"""

    id: str
    status: str              # PENDING / RUNNING / SUCCESS / FAILED
    topic: str
    stylePrompt: str
    title: Optional[str] = None
    content: Optional[str] = None
    qualityScore: Optional[int] = None
    error: Optional[str] = None


class GenerationResult(BaseModel):
    """生成结果:回传给 Java 回调接口的请求体。"""

    status: str                       # SUCCESS / FAILED
    title: Optional[str] = None
    content: Optional[str] = None
    qualityScore: Optional[int] = None
    error: Optional[str] = None  # 失败原因
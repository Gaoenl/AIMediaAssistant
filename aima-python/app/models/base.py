"""模型供应商抽象:所有供应商统一异步 chat 接口。"""
from abc import ABC, abstractmethod
class BaseProvider(ABC):
    """大模型供应商基类。"""

    @abstractmethod
    async def chat(self, system: str, user: str, temperature: float = 0.7) -> str:
        """调用模型,返回纯文本回答。"""
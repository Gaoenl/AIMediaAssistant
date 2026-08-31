from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.models.base import BaseProvider


class OpenAICompatibleProvider(BaseProvider):
    """用 ChatOpenAI 统一封装三家供应商。"""

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 60.0):
        self._llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=0.7,
            timeout=timeout,
            max_retries=2,  # SDK 层自动重试,抗瞬时抖动
        )

    async def chat(self, system: str, user: str, temperature: float = 0.7) -> str:
        """组装 system/user 消息并异步调用模型。"""
        llm = self._llm.bind(temperature=temperature)
        response = await llm.ainvoke([
            SystemMessage(content=system),
            HumanMessage(content=user),
        ])
        return response.content
"""Mock 供应商:不产生真实调用,用于离线联调。"""
import asyncio

from app.models.base import BaseProvider

"""M2 联调用:返回固定占位文本。"""


class MockProvider(BaseProvider):
    """M2 联调用:返回固定占位文本。"""

    async def chat(self, system: str, user: str, temperature: float = 0.7) -> str:
        await asyncio.sleep(0.3)
        return "这是一段 mock 模型生成的内容,用于在未配置真实密钥时打通链路。"
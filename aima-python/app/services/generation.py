"""生成服务:M1 返回 mock 结果;M2 替换为 LangGraph 创作/编辑/质检流程。"""
import asyncio

from app.schemas.task import GenerationResult
"""生成服务:M2 起由 LangGraph 编排 创作->编辑->质检 流程。"""
from app.agents.orchestrator import run_generation

async def generate_article(topic: str, style_prompt: str) -> GenerationResult:
      """根据主题与风格执行完整生成链路(mock 或真实模型)。"""
      return await run_generation(topic, style_prompt)
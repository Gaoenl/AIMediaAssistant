"""生成服务:M1 返回 mock 结果;M2 替换为 LangGraph 创作/编辑/质检流程。"""
import asyncio

from app.schemas.task import GenerationResult


async def generate_article(topic: str, style_prompt: str) -> GenerationResult:
    """根据主题与风格生成一篇文章。

    M1:模拟 2 秒耗时后返回占位内容,用于打通 MQ → 生成 → 回调链路。
    M2:创作 Agent(大纲→正文)→ 编辑 Agent(分段/AI 词过滤)→ 质检(打分),
       见开发方案 M2 里程碑。
    """
    await asyncio.sleep(2)
    return GenerationResult(
        status="SUCCESS",
        title=f"关于「{topic}」的深度解读",
        content=(
            f"# 关于「{topic}」的深度解读\n\n"
            f"这是一篇由 AIMA 生成的示例文章,风格:{style_prompt}\n\n"
            "本段为 M1 占位内容,后续由创作 Agent 生成。"
        ),
        qualityScore=85,
    )
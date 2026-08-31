"""编辑 Agent:润色并过滤 AI 味表达。"""
import re
import logging
from app.agents.prompts import AI_WORDS, EDIT_SYSTEM
from app.models import provider

logger = logging.getLogger(__name__)
async def edit_node(state: dict) -> dict:
    """输入初稿,输出润色后正文。"""
    content = state.get("content", "")
    user = f"请润色以下文章,去掉AI味词汇(如{'/'.join(AI_WORDS)}),保持原意:\n\n{content}"
    polished = await provider.chat(EDIT_SYSTEM, user, temperature=0.4)
    for word in AI_WORDS:
        polished = polished.replace(word, "")
    polished = re.sub(r"\n{3,}", "\n\n", polished).strip()
    logger.info(f"润色前: {content}\n润色后: {polished}")
    return {"content": polished or content}
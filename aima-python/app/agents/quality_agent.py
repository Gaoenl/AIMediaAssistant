"""质检 Agent:规则 + LLM 打分,产出分数与反馈。"""
import json
import re
import logging
from app.agents.prompts import AI_WORDS, QUALITY_SYSTEM
from app.models import provider
logger = logging.getLogger(__name__)

def _rule_score(content: str) -> int:
    """硬规则打分:字数不足扣分,AI味词每个扣 5 分。"""
    score = 100
    if len(content) < 300:
        score -= 20
    hits = [w for w in AI_WORDS if w in content]
    score -= len(hits) * 5
    return max(0, score)


async def quality_node(state: dict) -> dict:
    """输入润色后正文,输出 score 与 feedback。"""
    content = state.get("content", "")
    user = f"请评估以下文章并打分:\n\n{content}"
    raw = await provider.chat(QUALITY_SYSTEM, user, temperature=0.2)
    try:
        cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
        data = json.loads(cleaned)
        llm_score = int(data.get("score", 60))
        feedback = str(data.get("feedback", ""))
    except Exception:
        llm_score = 60
        feedback = "质检模型输出无法解析,按 60 分处理"
    rule = _rule_score(content)
    score = max(0, min(100, int(llm_score * 0.7 + rule * 0.3)))
    logger.info(f"质检: {score=}, {feedback=}")
    return {"score": score, "feedback": feedback}
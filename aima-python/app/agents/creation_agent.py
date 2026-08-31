"""创作 Agent:根据主题/风格/反馈生成标题与初稿。"""
from app.agents.prompts import CREATION_SYSTEM
from app.models import provider
import logging
logger = logging.getLogger(__name__)
async def creation_node(state: dict) -> dict:
    """输入 topic/style/feedback,输出 title/content。"""
    """输入 topic/style/feedback,输出 title/content。"""
    topic = state["topic"]
    style = state["style"]
    feedback = state.get("feedback")
    feedback_text = f"\n上一轮质检反馈(请针对性改进):{feedback}" if feedback else ""
    user = (f"主题:{topic}\n风格要求:{style}\n"
            f"要求:先给出文章标题,再输出正文,总字数不少于400字。{feedback_text}")
    text = await provider.chat(CREATION_SYSTEM, user, temperature=0.8)
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    title = lines[0].lstrip("# ").strip() if lines else topic
    content = "\n".join(lines[1:]).strip() or text.strip()
    logger.info(f"创作Agent: {title}\n{content}")
    return {"title": title, "content": content, "attempts": state.get("attempts", 0) + 1}
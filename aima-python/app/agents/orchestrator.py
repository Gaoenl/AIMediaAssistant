"""LangGraph 编排:创作 -> 编辑 -> 质检,不达标带反馈重写。"""
from typing import TypedDict, Optional

from langgraph.graph import END, START, StateGraph

from app.agents.creation_agent import creation_node
from app.agents.editing_agent import edit_node
from app.agents.quality_agent import quality_node
from app.core.config import settings
from app.schemas.task import GenerationResult

class GenerationState(TypedDict):
    """图状态:每个键独立通道,未被节点返回的键自动保留。"""
    topic: str
    style: str
    title: Optional[str]
    content: Optional[str]
    feedback: Optional[str]
    attempts: int
    score: Optional[int]
def _route_after_quality(state: dict) -> str:
    """质检路由:达标结束;未达标且未超轮数则带反馈重写,否则失败。"""
    if state.get("score") is not None and state["score"] >= settings.quality_threshold:
        return "success"
    if state.get("attempts", 0) >= settings.quality_max_attempts:
        return "failed"
    return "retry"
def _build_graph():
    graph = StateGraph(GenerationState)
    graph.add_node("create",creation_node)
    graph.add_node("edit",edit_node)
    graph.add_node("quality",quality_node)
    graph.add_edge(START, "create")
    graph.add_edge("create", "edit")
    graph.add_edge("edit", "quality")
    graph.add_conditional_edges("quality", _route_after_quality,
                                {"retry": "create", "success": END, "failed": END})
    return graph.compile()
# 进程内单例,避免重复编译
_graph = _build_graph()
async def run_generation(topic: str, style: str) -> GenerationResult:
    """执行 创作->编辑->质检 全流程,返回回调 Java 的结果。"""
    initial = {"topic": topic, "style": style, "title": None, "content": None,
               "feedback": None, "attempts": 0, "score": None}
    result = await _graph.ainvoke(initial)
    score = result.get("score")
    if score is not None and score >= settings.quality_threshold:
        return GenerationResult(status="SUCCESS", title=result.get("title"),
                                content=result.get("content"), qualityScore=score)
    return GenerationResult(status="FAILED", title=result.get("title"),
                            content=result.get("content"), qualityScore=score,
                            error=f"质检未达标(得分 {score},阈值 {settings.quality_threshold})")

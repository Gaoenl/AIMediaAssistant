"""生成服务单测:M1 验证 mock 返回符合 Java 回调契约。"""
import pytest

from app.services.generation import generate_article


@pytest.mark.asyncio
async def test_generate_article_success():
    result = await generate_article("AI 智能媒体", "小红书口语化")
    assert result.status == "SUCCESS"
    assert "AI 智能媒体" in result.title
    assert result.qualityScore is not None
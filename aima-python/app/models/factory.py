from app.core.config import settings
from app.models.base import BaseProvider
from app.models.mock_provider import MockProvider
from app.models.openai_compatible import OpenAICompatibleProvider


def create_provider() -> BaseProvider:
    """根据 settings.model_provider 返回对应供应商实例。"""
    provider =settings.model_provider.lower()
    if provider=="mock":
        return MockProvider()
    if provider == "deepseek":
        return OpenAICompatibleProvider(settings.deepseek_base_url,
                                        settings.deepseek_api_key,
                                        settings.model_name)
    if provider == "qwen":
        return OpenAICompatibleProvider(settings.qwen_base_url,
                                        settings.qwen_api_key,
                                        settings.model_name)
    if provider == "hunyuan":
        return OpenAICompatibleProvider(settings.hunyuan_base_url,
                                        settings.hunyuan_api_key,
                                        settings.model_name)
    raise ValueError(f"未知模型供应商:{provider}")
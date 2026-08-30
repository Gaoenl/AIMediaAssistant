"""全局配置:所有外部依赖通过环境变量注入(前缀 AIMA_),支持 .env 文件。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """AIMA Python AI 引擎配置。

    环境变量示例:
      AIMA_JAVA_BASE_URL=http://localhost:8080
      AIMA_ROCKETMQ_NAMESERVER=127.0.0.1:9876
    """

    # Java 后端地址:用于拉取任务参数与回传生成结果
    java_base_url: str = "http://localhost:8080"

    # RocketMQ 消费配置
    rocketmq_nameserver: str = "127.0.0.1:9876"
    consumer_group: str = "aima-generation-group"
    topic: str = "aima-generation-task"

    # 模型配置(M2 启用):当前默认 mock,不产生真实调用费用
    model_provider: str = "mock"  # mock / deepseek / qwen / hunyuan
    model_name: str = "deepseek-v3"

    model_config = SettingsConfigDict(env_prefix="AIMA_", env_file=".env")


# 全局单例,业务代码直接 import settings
settings = Settings()
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
    rocketmq_nameserver: str = "121.40.128.24:9876"
    consumer_group: str = "aima-generation-group"
    topic: str = "aima-generation-task"

    # ---- 模型配置(M2)----
    model_provider: str = "deepseek"  # mock / deepseek / qwen / hunyuan
    model_name: str = "deepseek-v4-flash"
    quality_threshold: int = 75  # 质检通过线
    quality_max_attempts: int = 3  # 质检不达标时的重写轮数上限
    # 各供应商 OpenAI 兼容 endpoint 与密钥
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_api_key: str = ""
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    qwen_api_key: str = ""
    hunyuan_base_url: str = "https://api.hunyuan.cloud.tencent.com/v1"
    hunyuan_api_key: str = ""
    model_config = SettingsConfigDict(env_prefix="AIMA_", env_file=".env")


# 全局单例,业务代码直接 import settings
settings = Settings()
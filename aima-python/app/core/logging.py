"""统一日志配置。M4 可升级为 JSON 格式 + taskId 结构化字段,便于采集分析。"""
import logging


def setup_logging() -> None:
    """初始化根日志:INFO 级别,带时间戳与模块名。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
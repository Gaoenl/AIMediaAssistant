package com.aima.task.mq;

/**
 * RocketMQ 消息体:只携带 taskId,任务参数由 Python 通过 internal API 获取,
 * 避免大消息与参数不一致。
 */
public record GenerationTaskMessage(String taskId) {
}
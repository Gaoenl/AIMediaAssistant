package com.aima.task.mq;

import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.springframework.stereotype.Component;

/**
 * 生成任务消息生产者:统一封装 topic 与发送逻辑。
 */
@Component
public class GenerationTaskProducer {

    public static final String TOPIC = "aima-generation-task";

    private final RocketMQTemplate rocketMQTemplate;

    public GenerationTaskProducer(RocketMQTemplate rocketMQTemplate) {
        this.rocketMQTemplate = rocketMQTemplate;
    }

    /** 发送生成任务消息(同步发送,M2 可改异步 + 失败重试) */
    public void send(String taskId) {
        rocketMQTemplate.syncSend(TOPIC, new GenerationTaskMessage(taskId));
    }
}
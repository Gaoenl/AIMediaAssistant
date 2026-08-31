package com.aima.topic.mq;

import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.springframework.stereotype.Component;

import java.util.UUID;

/** 热点采集消息生产者 */
@Component
public class TopicCollectProducer {

    public static final String TOPIC = "aima-collect-task";

    private final RocketMQTemplate rocketMQTemplate;

    public TopicCollectProducer(RocketMQTemplate rocketMQTemplate) {
        this.rocketMQTemplate = rocketMQTemplate;
    }

    /** 发送一轮全量采集任务 */
    public void send() {
        rocketMQTemplate.syncSend(TOPIC, new TopicCollectMessage(UUID.randomUUID().toString()));
    }
}
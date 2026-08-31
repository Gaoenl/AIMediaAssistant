package com.aima.scheduler;

import com.aima.topic.mq.TopicCollectProducer;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** 热点采集调度:每 30 分钟触发一轮(实验源由 Python 冷却节流) */
@Component
public class TopicCollectScheduler {

    private final TopicCollectProducer producer;

    public TopicCollectScheduler(TopicCollectProducer producer) {
        this.producer = producer;
    }

    @Scheduled(cron = "0 */30 * * * ?")
    public void collectHotTopics() {
        producer.send();
    }
}
package com.aima.topic.dto;

import java.time.Instant;

/** Python 采集回调的单条热点 */
public record TopicCollectItem(
        String source,
        String sourceId,
        String title,
        String url,
        String description,
        Integer hotScore,
        Instant collectedAt) {
}
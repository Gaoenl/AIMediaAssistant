package com.aima.topic.dto;

import java.time.Instant;

/** 热点选题视图(返回前端) */
public record TopicView(
        String id,
        String source,
        String sourceId,
        String title,
        String url,
        String description,
        Integer hotScore,
        String trend,
        Instant collectedAt,
        Instant createdAt) {
}
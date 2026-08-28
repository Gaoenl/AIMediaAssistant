package com.aima.task.dto;

import java.time.Instant;

/** 生成任务视图(返回给前端) */
public record TaskView(
        String id,
        String status,          // PENDING / RUNNING / SUCCESS / FAILED
        String topic,
        String stylePrompt,
        String title,           // 生成结果
        String content,         // 生成结果
        Integer qualityScore,   // 质检分
        Instant createdAt,
        Instant updatedAt) {
}
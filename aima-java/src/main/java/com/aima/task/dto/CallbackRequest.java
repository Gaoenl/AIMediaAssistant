package com.aima.task.dto;

/** Python 生成完成后的回调请求 */
public record CallbackRequest(
        String status,          // SUCCESS / FAILED
        String title,           // 文章标题(成功时)
        String content,         // 文章正文(成功时)
        Integer qualityScore,
        String error) { // 质检分(0-100,成功时)
}
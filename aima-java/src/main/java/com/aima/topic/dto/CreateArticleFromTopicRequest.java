package com.aima.topic.dto;

import jakarta.validation.constraints.NotBlank;

/** 从选题发起生成请求(主题取热点标题,无需前端传) */
public record CreateArticleFromTopicRequest(
        @NotBlank(message = "风格提示词不能为空") String stylePrompt) {
}
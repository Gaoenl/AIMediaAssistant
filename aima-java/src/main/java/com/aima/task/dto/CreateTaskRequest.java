package com.aima.task.dto;


import javax.validation.constraints.NotBlank;

/** 提交生成任务请求 */
public record CreateTaskRequest(
        @NotBlank(message = "主题不能为空") String topic,
        @NotBlank(message = "风格提示词不能为空") String stylePrompt) {
}
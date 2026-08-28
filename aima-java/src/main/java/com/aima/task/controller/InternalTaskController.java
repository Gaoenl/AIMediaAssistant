package com.aima.task.controller;

import com.aima.common.ApiResponse;
import com.aima.task.dto.CallbackRequest;
import com.aima.task.dto.TaskView;
import com.aima.task.service.TaskService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Java↔Python 内部接口(不走前端鉴权,/internal/** 已在 SecurityConfig 放行)。
 * M2 需补充内部签名鉴权,防止外部直接调用。
 */
@RestController
@RequestMapping("/internal/v1/tasks")
public class InternalTaskController {

    private final TaskService taskService;

    public InternalTaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    /** Python 拉取任务参数(消息体只带 taskId) */
    @GetMapping("/{id}")
    public ApiResponse<TaskView> get(@PathVariable String id) {
        return ApiResponse.ok(taskService.get(id));
    }

    /** Python 生成完成后回调,更新任务状态与文章结果 */
    @PostMapping("/{id}/callback")
    public ApiResponse<Void> callback(@PathVariable String id,
                                      @RequestBody CallbackRequest request) {
        taskService.handleCallback(id, request);
        return ApiResponse.ok();
    }
}
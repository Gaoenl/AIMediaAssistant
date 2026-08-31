package com.aima.task.controller;

import com.aima.common.ApiResponse;
import com.aima.task.dto.CreateTaskRequest;
import com.aima.task.dto.TaskView;
import com.aima.task.service.TaskService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


/** 前端生成任务接口 */
@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class GenerationTaskController {

    private final TaskService taskService;

    /** 提交生成任务(异步,MQ 触发 Python) */
    @PostMapping("/articles/generate")
    public ApiResponse<TaskView> generate(@RequestBody @Valid CreateTaskRequest request) {
        return ApiResponse.ok(taskService.submit(request));
    }

    /** 查询任务状态(前端轮询) */
    @GetMapping("/tasks/{id}")
    public ApiResponse<TaskView> get(@PathVariable("id") String id) {
        return ApiResponse.ok(taskService.get(id));
    }
}

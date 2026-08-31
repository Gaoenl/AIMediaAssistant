package com.aima.topic.controller;

import com.aima.common.ApiResponse;
import com.aima.task.dto.CreateTaskRequest;
import com.aima.task.dto.TaskView;
import com.aima.task.service.TaskService;
import com.aima.topic.dto.CreateArticleFromTopicRequest;
import com.aima.topic.dto.TopicView;
import com.aima.topic.service.TopicService;
import com.baomidou.mybatisplus.core.metadata.IPage;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

/** 前端选题池接口 */
@RestController
@RequestMapping("/api/v1/topics")
public class TopicController {

    private final TopicService topicService;
    private final TaskService taskService;

    public TopicController(TopicService topicService, TaskService taskService) {
        this.topicService = topicService;
        this.taskService = taskService;
    }

    /** 选题池分页(热度倒序) */
    @GetMapping
    public ApiResponse<IPage<TopicView>> page(
            @RequestParam(value = "source", required = false) String source,
            @RequestParam(value = "minScore", required = false) Integer minScore,
            @RequestParam(defaultValue = "1") long page,
            @RequestParam(defaultValue = "20") long size) {
        return ApiResponse.ok(topicService.page(source, minScore, page, size));
    }

    /** 从选题发起生成(主题=热点标题,风格自选) */
    @PostMapping("/{id}/create-article")
    public ApiResponse<TaskView> createArticle(@PathVariable("id") String id,
                                               @RequestBody @Valid CreateArticleFromTopicRequest request) {
        TopicView topic = topicService.get(id);
        return ApiResponse.ok(taskService.submit(new CreateTaskRequest(topic.title(), request.stylePrompt())));
    }
}
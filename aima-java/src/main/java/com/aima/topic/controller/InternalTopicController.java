package com.aima.topic.controller;

import com.aima.common.ApiResponse;
import com.aima.topic.dto.TopicCollectRequest;
import com.aima.topic.service.TopicService;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/** Java↔Python 内部接口:热点批量入库(/internal 已在 SecurityConfig 放行) */
@RestController
@RequestMapping("/internal/v1/topics")
public class InternalTopicController {

    private final TopicService topicService;

    public InternalTopicController(TopicService topicService) {
        this.topicService = topicService;
    }

    /** Python 采集回调:批量 upsert */
    @PostMapping("/collect")
    public ApiResponse<Map<String, Integer>> collect(@RequestBody TopicCollectRequest request) {
        int count = topicService.collect(request.items());
        return ApiResponse.ok(Map.of("count", count));
    }
}
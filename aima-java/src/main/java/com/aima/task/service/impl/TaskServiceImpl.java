package com.aima.task.service.impl;

import com.aima.common.BusinessException;
import com.aima.task.dto.CallbackRequest;
import com.aima.task.dto.CreateTaskRequest;
import com.aima.task.dto.TaskView;
import com.aima.task.entity.GenerationTask;
import com.aima.task.mapper.GenerationTaskMapper;
import com.aima.task.mq.GenerationTaskProducer;
import com.aima.task.service.TaskService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 生成任务服务实现。
 * M1:任务状态存内存 Map(重启丢失);M2 替换为 MySQL generation_task 表,
 *     并引入 RUNNING 状态与业务级重试(上限 2 次)。
 */
@Service
@RequiredArgsConstructor
public class TaskServiceImpl implements TaskService {

    /** 业务级最大重试次数 */
    public static final int MAX_RETRY = 2;
    private final GenerationTaskMapper taskMapper;
    private final GenerationTaskProducer producer;



    /** 提交任务:写入 PENDING 状态,投递 MQ 消息 */
    @Override
    @Transactional
    public TaskView submit(CreateTaskRequest request) {
        Instant now = Instant.now();
        GenerationTask task = GenerationTask.builder()
                .id(UUID.randomUUID().toString())
                .status("PENDING")
                .topic(request.topic())
                .stylePrompt(request.stylePrompt())
                .retryCount(0)
                .createdAt(now)
                .updatedAt(now)
                .build();
        taskMapper.insert(task);
        producer.send(task.getId());
        return toView(task);

    }

    /** 查询任务,不存在则抛 404 */
    @Override
    public TaskView get(String id) {
        return toView(require(id));
    }

    @Override
    public TaskView start(String id) {
        GenerationTask task = require(id);
        // 幂等:MQ 重投消息可能重复触发 start,PENDING 才推进,其余状态直接返回
        if ("PENDING".equals(task.getStatus())) {
            task.setStatus("RUNNING");
            task.setUpdatedAt(Instant.now());
            taskMapper.updateById(task);
        }
        return toView(task);

    }

    /**
     * 处理回调:仅 PENDING/RUNNING 状态可接收;
     * 已结束任务收到重复回调直接拒绝,保证状态机幂等。
     */
    @Override
    public void handleCallback(String id, CallbackRequest callback) {
        GenerationTask task = require(id);
        // 幂等:已结束任务忽略重复回调
        if ("SUCCESS".equals(task.getStatus()) || "FAILED".equals(task.getStatus())) {
            throw new BusinessException(409, "任务已结束,忽略重复回调");
        }
        Instant now = Instant.now();
        if ("SUCCESS".equals(callback.status())) {
            task.setStatus("SUCCESS");
            task.setTitle(callback.title());
            task.setContent(callback.content());
            task.setQualityScore(callback.qualityScore());
            task.setError(null);
            task.setUpdatedAt(now);
            taskMapper.updateById(task);
            return;
        }
        // FAILED:业务级重试,最多 MAX_RETRY 次
        if (task.getRetryCount() < MAX_RETRY) {
            task.setRetryCount(task.getRetryCount() + 1);
            task.setStatus("RUNNING");
            task.setError(callback.error());
            task.setUpdatedAt(now);
            taskMapper.updateById(task);
            producer.send(task.getId());
            return;
        }
        task.setStatus("FAILED");
        task.setError(callback.error());
        task.setUpdatedAt(now);
        taskMapper.updateById(task);
    }

    private GenerationTask require(String id) {
        GenerationTask task = taskMapper.selectById(id);
        if (task == null) {
            throw new BusinessException(404, "任务不存在");
        }
        return task;
    }
    private TaskView toView(GenerationTask t) {
        return new TaskView(t.getId(), t.getStatus(), t.getTopic(), t.getStylePrompt(),
                t.getTitle(), t.getContent(), t.getQualityScore(),
                t.getRetryCount(), t.getError(), t.getCreatedAt(), t.getUpdatedAt());
    }
}
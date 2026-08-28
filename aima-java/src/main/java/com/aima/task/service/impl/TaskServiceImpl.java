package com.aima.task.service.impl;

import com.aima.common.BusinessException;
import com.aima.task.dto.CallbackRequest;
import com.aima.task.dto.CreateTaskRequest;
import com.aima.task.dto.TaskView;
import com.aima.task.mq.GenerationTaskProducer;
import com.aima.task.service.TaskService;
import org.springframework.stereotype.Service;

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
public class TaskServiceImpl implements TaskService {

    private final Map<String, TaskView> tasks = new ConcurrentHashMap<>();
    private final GenerationTaskProducer producer;

    public TaskServiceImpl(GenerationTaskProducer producer) {
        this.producer = producer;
    }

    /** 提交任务:写入 PENDING 状态,投递 MQ 消息 */
    @Override
    public TaskView submit(CreateTaskRequest request) {
        String id = UUID.randomUUID().toString();
        TaskView task = new TaskView(id, "PENDING", request.topic(), request.stylePrompt(),
                null, null, null, Instant.now(), null);
        tasks.put(id, task);
        producer.send(id);
        return task;
    }

    /** 查询任务,不存在则抛 404 */
    @Override
    public TaskView get(String id) {
        TaskView task = tasks.get(id);
        if (task == null) {
            throw new BusinessException(404, "任务不存在");
        }
        return task;
    }

    /**
     * 处理回调:仅 PENDING/RUNNING 状态可接收;
     * 已结束任务收到重复回调直接拒绝,保证状态机幂等。
     */
    @Override
    public void handleCallback(String id, CallbackRequest callback) {
        TaskView current = get(id);
        if (!"PENDING".equals(current.status()) && !"RUNNING".equals(current.status())) {
            throw new BusinessException(409, "任务已结束,忽略重复回调");
        }
        TaskView updated = new TaskView(id, callback.status(), current.topic(), current.stylePrompt(),
                callback.title(), callback.content(), callback.qualityScore(),
                current.createdAt(), Instant.now());
        tasks.put(id, updated);
    }
}
package com.aima.task.service;

import com.aima.task.dto.CallbackRequest;
import com.aima.task.dto.CreateTaskRequest;
import com.aima.task.dto.TaskView;

/** 生成任务服务接口 */
public interface TaskService {

    /** 提交生成任务:创建任务并发送 MQ 消息 */
    TaskView submit(CreateTaskRequest request);

    /** 查询任务(前端轮询) */
    TaskView get(String id);

    /** 处理 Python 回调,更新任务状态与文章结果 */
    void handleCallback(String id, CallbackRequest callback);
}
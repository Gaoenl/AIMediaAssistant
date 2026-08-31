package com.aima.task.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

/** 生成任务实体,对应 generation_task 表(M2 起持久化)。 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@TableName("generation_task")
public class GenerationTask {

    @TableId(type = IdType.INPUT)   // UUID 由业务生成
    private String id;

    private String status;

    private String topic;

    @TableField("style_prompt")
    private String stylePrompt;

    private String title;

    private String content;

    @TableField("quality_score")
    private Integer qualityScore;

    @TableField("retry_count")
    private Integer retryCount = 0;

    @TableField("error_msg")
    private String error;

    @TableField("created_at")
    private Instant createdAt;

    @TableField("updated_at")
    private Instant updatedAt;

}
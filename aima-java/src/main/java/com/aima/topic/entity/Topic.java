package com.aima.topic.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.Instant;

/** 热点选题实体,对应 topic 表(M3)。 */
@Data
@TableName("topic")
public class Topic {

    @TableId(type = IdType.INPUT)
    private String id;

    private String source;
    @TableField("source_id")
    private String sourceId;
    private String title;
    private String url;
    private String description;
    @TableField("hot_score")
    private Integer hotScore;
    private String trend;
    @TableField("collected_at")
    private Instant collectedAt;
    @TableField("created_at")
    private Instant createdAt;

}
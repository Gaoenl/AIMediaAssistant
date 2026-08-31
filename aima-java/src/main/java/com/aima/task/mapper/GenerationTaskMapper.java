package com.aima.task.mapper;

import com.aima.task.entity.GenerationTask;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/** 生成任务 Mapper(MyBatis Plus)。 */
@Mapper
public interface GenerationTaskMapper extends BaseMapper<GenerationTask> {
}
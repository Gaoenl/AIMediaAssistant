package com.aima.topic.mapper;

import com.aima.topic.entity.Topic;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/** 热点 Mapper(MyBatis Plus)。 */
@Mapper
public interface TopicMapper extends BaseMapper<Topic> {
}
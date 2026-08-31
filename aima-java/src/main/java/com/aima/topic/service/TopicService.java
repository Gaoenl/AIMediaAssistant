package com.aima.topic.service;

import com.aima.topic.dto.TopicCollectItem;
import com.aima.topic.dto.TopicView;
import com.baomidou.mybatisplus.core.metadata.IPage;
import java.util.List;

public interface TopicService {

    /** Python 采集回调:批量 upsert,返回处理条数 */
    int collect(List<TopicCollectItem> items);

    /** 按 id 查询,不存在抛 404 */
    TopicView get(String id);

    /** 选题池分页(热度倒序) */
    IPage<TopicView> page(String source, Integer minScore, long page, long size);
}
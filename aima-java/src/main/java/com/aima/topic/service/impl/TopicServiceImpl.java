package com.aima.topic.service.impl;

import com.aima.common.BusinessException;
import com.aima.topic.dto.TopicCollectItem;
import com.aima.topic.dto.TopicView;
import com.aima.topic.entity.Topic;
import com.aima.topic.mapper.TopicMapper;
import com.aima.topic.service.TopicService;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * 热点服务实现(M3.1)。
 * - collect:按 (source, source_id) upsert,并计算 trend;
 * - page:选题池热度倒序分页。
 */
@Service
@RequiredArgsConstructor
public class TopicServiceImpl implements TopicService {

    private final TopicMapper topicMapper;

    @Override
    @Transactional
    public int collect(List<TopicCollectItem> items) {
        int count = 0;
        for (TopicCollectItem item : items) {
            if (item.source() == null || item.sourceId() == null || item.title() == null) {
                continue;
            }
            Topic exists = topicMapper.selectOne(new LambdaQueryWrapper<Topic>()
                    .eq(Topic::getSource, item.source())
                    .eq(Topic::getSourceId, item.sourceId()));
            if (exists == null) {
                Topic t = new Topic();
                t.setId(UUID.randomUUID().toString());
                t.setSource(item.source());
                t.setSourceId(item.sourceId());
                t.setTitle(item.title());
                t.setUrl(item.url());
                t.setDescription(item.description());
                t.setHotScore(item.hotScore() == null ? 0 : item.hotScore());
                t.setTrend("NEW");
                t.setCollectedAt(item.collectedAt() == null ? Instant.now() : item.collectedAt());
                t.setCreatedAt(Instant.now());
                topicMapper.insert(t);
            } else {
                int old = exists.getHotScore() == null ? 0 : exists.getHotScore();
                int nowScore = item.hotScore() == null ? 0 : item.hotScore();
                exists.setTitle(item.title());
                exists.setUrl(item.url());
                exists.setDescription(item.description());
                exists.setHotScore(nowScore);
                exists.setTrend(trend(old, nowScore));
                exists.setCollectedAt(item.collectedAt() == null ? Instant.now() : item.collectedAt());
                topicMapper.updateById(exists);
            }
            count++;
        }
        return count;
    }

    private String trend(int old, int now) {
        if (now - old > 5) return "RISING";
        if (old - now > 5) return "FALLING";
        return "FLAT";
    }

    @Override
    public TopicView get(String id) {
        Topic topic = topicMapper.selectById(id);
        if (topic == null) {
            throw new BusinessException(404, "热点不存在");
        }
        return toView(topic);
    }

    @Override
    public IPage<TopicView> page(String source, Integer minScore, long page, long size) {
        LambdaQueryWrapper<Topic> qw = new LambdaQueryWrapper<Topic>()
                .eq(StringUtils.hasText(source), Topic::getSource, source)
                .ge(minScore != null, Topic::getHotScore, minScore)
                .orderByDesc(Topic::getHotScore);
        return topicMapper.selectPage(new Page<>(page, size), qw).convert(this::toView);
    }

    private TopicView toView(Topic t) {
        return new TopicView(t.getId(), t.getSource(), t.getSourceId(), t.getTitle(),
                t.getUrl(), t.getDescription(), t.getHotScore(), t.getTrend(),
                t.getCollectedAt(), t.getCreatedAt());
    }
}
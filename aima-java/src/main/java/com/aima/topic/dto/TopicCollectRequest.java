package com.aima.topic.dto;

import java.util.List;

/** Python 采集回调请求体 */
public record TopicCollectRequest(List<TopicCollectItem> items) {
}
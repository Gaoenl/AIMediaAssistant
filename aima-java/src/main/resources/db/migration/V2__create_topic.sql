CREATE TABLE topic (
                       id            VARCHAR(64)   PRIMARY KEY,
                       source        VARCHAR(32)   NOT NULL,   -- zhihu_hot/bilibili_hot/rss_36kr/rss_huxiu/festival
                       source_id     VARCHAR(128)  NOT NULL,   -- 上游唯一ID
                       title         VARCHAR(512)  NOT NULL,
                       url           VARCHAR(1024),
                       description   TEXT,
                       hot_score     INT           NOT NULL DEFAULT 0,
                       trend         VARCHAR(16),              -- NEW/RISING/FLAT/FALLING
                       collected_at  TIMESTAMPTZ   NOT NULL,
                       created_at    TIMESTAMPTZ   NOT NULL,
                       UNIQUE (source, source_id)
);
CREATE TABLE article (
                         id            VARCHAR(64)   PRIMARY KEY,
                         task_id       VARCHAR(64)   NOT NULL,
                         topic         VARCHAR(512)  NOT NULL,
                         title         VARCHAR(512),
                         content       TEXT,
                         style_prompt  VARCHAR(1024),
                         quality_score INT,
                         status        VARCHAR(16)   NOT NULL DEFAULT 'DRAFT', -- DRAFT/REVIEWING/APPROVED/REJECTED/PUBLISHED
                         reject_reason VARCHAR(1024),
                         created_at    TIMESTAMPTZ   NOT NULL,
                         updated_at    TIMESTAMPTZ   NOT NULL
);

CREATE TABLE audit_log (
                           id          BIGSERIAL   PRIMARY KEY,
                           article_id  VARCHAR(64) NOT NULL,
                           action      VARCHAR(32) NOT NULL,   -- SUBMIT/APPROVE/REJECT/PUBLISH
                           operator    VARCHAR(64) NOT NULL,
                           comment     VARCHAR(1024),
                           created_at  TIMESTAMPTZ NOT NULL
);
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS embedding (
                                         id          BIGSERIAL PRIMARY KEY,
                                         entity_type VARCHAR(32) NOT NULL,   -- article/style_profile
                                         entity_id   VARCHAR(64) NOT NULL,
                                         chunk_text  TEXT NOT NULL,
                                         embedding   vector(1024),
                                         created_at  TIMESTAMPTZ NOT NULL
);
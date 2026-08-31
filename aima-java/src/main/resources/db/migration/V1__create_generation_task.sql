-- M2 V1:生成任务表(MyBatis Plus + PostgreSQL)
CREATE TABLE generation_task (
                                 id            VARCHAR(64)   PRIMARY KEY,
                                 status        VARCHAR(16)   NOT NULL,
                                 topic         VARCHAR(512)  NOT NULL,
                                 style_prompt  VARCHAR(1024) NOT NULL,
                                 title         VARCHAR(512),
                                 content       TEXT,
                                 quality_score INT,
                                 retry_count   INT           NOT NULL DEFAULT 0,
                                 error_msg     VARCHAR(1024),
                                 created_at    TIMESTAMPTZ   NOT NULL,
                                 updated_at    TIMESTAMPTZ   NOT NULL
);

CREATE INDEX idx_generation_task_status ON generation_task (status);
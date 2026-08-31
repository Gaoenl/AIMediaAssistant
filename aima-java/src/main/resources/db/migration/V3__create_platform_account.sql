CREATE TABLE platform_account (
                                  id                      VARCHAR(64) PRIMARY KEY,
                                  platform                VARCHAR(32) NOT NULL,   -- wechat
                                  name                    VARCHAR(128) NOT NULL,
                                  app_id                  VARCHAR(128),
                                  secret_encrypted        TEXT,        -- AES-256-GCM
                                  token                   VARCHAR(128),
                                  encoding_aes_key_encrypted TEXT,
                                  status                  VARCHAR(16) NOT NULL DEFAULT 'ENABLED',
                                  daily_limit             INT NOT NULL DEFAULT 1,
                                  min_interval_minutes    INT NOT NULL DEFAULT 60,
                                  created_at              TIMESTAMPTZ NOT NULL,
                                  updated_at              TIMESTAMPTZ NOT NULL
);

CREATE TABLE publish_task (
                              id                    VARCHAR(64) PRIMARY KEY,
                              article_id            VARCHAR(64) NOT NULL,
                              platform              VARCHAR(32) NOT NULL,
                              account_id            VARCHAR(64) NOT NULL,
                              status                VARCHAR(24) NOT NULL DEFAULT 'PENDING', -- PENDING/PUBLISHING/WAIT_CALLBACK/SUCCESS/FAILED
                              media_id              VARCHAR(128),
                              publish_id            VARCHAR(128),
                              scheduled_at          TIMESTAMPTZ,
                              published_at          TIMESTAMPTZ,
                              callback_at           TIMESTAMPTZ,
                              callback_payload_json TEXT,
                              error                 VARCHAR(1024),
                              retry_count           INT NOT NULL DEFAULT 0,
                              created_at            TIMESTAMPTZ NOT NULL,
                              updated_at            TIMESTAMPTZ NOT NULL
);
CREATE INDEX idx_publish_task_status ON publish_task (status);
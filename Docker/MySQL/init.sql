DROP DATABASE IF EXISTS snsapp;

DROP USER IF EXISTS 'testuser'@'%';


CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';

CREATE DATABASE IF NOT EXISTS snsapp
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;


GRANT ALL PRIVILEGES ON snsapp.* TO 'testuser'@'%';

FLUSH PRIVILEGES;

USE snsapp;

-- ============================================================
-- つどい (tsudoi) データベース 初期化スクリプト
-- MySQL 8.0 / utf8mb4
--
-- テーブル作成順は外部キーの参照先(親)を先に作る:
--   users → households → family_members → events → fee_rules
--   → applications → application_participants → admins
-- ============================================================

SET NAMES utf8mb4;

-- ------------------------------------------------------------
-- 1. users : ユーザー(主催者・参加者の区別なし)
-- ------------------------------------------------------------
CREATE TABLE users (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    email                VARCHAR(255) NOT NULL UNIQUE,
    password_hash        VARCHAR(255) NOT NULL,
    email_changed_at     DATETIME NULL,
    password_changed_at  DATETIME NULL,
    is_banned            BOOLEAN NOT NULL DEFAULT FALSE,
    created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at           DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 2. households : 世帯(新規登録時にsolo世帯を自動作成)
-- ------------------------------------------------------------
CREATE TABLE households (
    id          VARCHAR(36) PRIMARY KEY,
    leader_id   INT NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at  DATETIME NULL,
    CONSTRAINT fk_households_leader
        FOREIGN KEY (leader_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 3. family_members : 家族メンバー
-- ------------------------------------------------------------
CREATE TABLE family_members (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    household_id  VARCHAR(36) NOT NULL,
    relation      ENUM('本人','夫','妻','息子','娘','父','母','祖母','祖父','その他') NOT NULL,
    name          VARCHAR(100) NULL,
    gender        ENUM('男','女','その他') NULL,
    birth_date    DATE NOT NULL,
    email         VARCHAR(255) NULL,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at    DATETIME NULL,
    CONSTRAINT fk_family_members_household
        FOREIGN KEY (household_id) REFERENCES households(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 4. events : イベント
-- ------------------------------------------------------------
CREATE TABLE events (
    id                   VARCHAR(36) PRIMARY KEY,
    owner_id             INT NOT NULL,
    title                VARCHAR(255) NOT NULL,
    start_at             DATETIME NOT NULL,
    place                VARCHAR(255) NOT NULL,
    address              VARCHAR(255) NOT NULL,
    capacity             INT NULL,
    deadline             DATETIME NULL,
    description          TEXT NOT NULL,
    items_to_bring       TEXT NOT NULL,
    schedule             TEXT NOT NULL,
    hold_condition       ENUM('雨天決行','雨天中止') NOT NULL,
    cancellation_policy  TEXT NOT NULL,
    emergency_contact    VARCHAR(20) NOT NULL,
    payment_method       ENUM('現地払い','事前払い') NOT NULL,
    payment_deadline     DATE NULL,
    status               ENUM('下書き','公開','締切') NOT NULL DEFAULT '公開',
    created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at           DATETIME NULL,
    CONSTRAINT fk_events_owner
        FOREIGN KEY (owner_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 5. fee_rules : 料金区分(イベントに付随)
-- ------------------------------------------------------------
CREATE TABLE fee_rules (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    event_id    VARCHAR(36) NOT NULL,
    tier_name   VARCHAR(50) NOT NULL,
    min_age     INT NOT NULL,
    max_age     INT NOT NULL,
    gender      ENUM('男','女','その他') NULL,
    fee         INT NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  DATETIME NULL,
    CONSTRAINT fk_fee_rules_event
        FOREIGN KEY (event_id) REFERENCES events(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_fee_rules_min_age CHECK (min_age >= 0),
    CONSTRAINT chk_fee_rules_max_age CHECK (max_age >= min_age),
    CONSTRAINT chk_fee_rules_fee     CHECK (fee >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 6. applications : 申込(ヘッダー)
-- ------------------------------------------------------------
CREATE TABLE applications (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    event_id      VARCHAR(36) NOT NULL,
    household_id  VARCHAR(36) NOT NULL,
    total_amount  INT NOT NULL,
    applied_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at    DATETIME NULL,
    CONSTRAINT fk_applications_event
        FOREIGN KEY (event_id) REFERENCES events(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_applications_household
        FOREIGN KEY (household_id) REFERENCES households(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 7. application_participants : 申込参加者(明細・スナップショット)
--    複合主キー (application_id, member_id) で同一申込内の重複を防止
-- ------------------------------------------------------------
CREATE TABLE application_participants (
    application_id  INT NOT NULL,
    member_id       INT NOT NULL,
    fee_rule_id     INT NOT NULL,
    amount          INT NOT NULL,
    deleted_at      DATETIME NULL,
    PRIMARY KEY (application_id, member_id),
    CONSTRAINT fk_ap_application
        FOREIGN KEY (application_id) REFERENCES applications(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_ap_member
        FOREIGN KEY (member_id) REFERENCES family_members(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_ap_fee_rule
        FOREIGN KEY (fee_rule_id) REFERENCES fee_rules(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 8. admins : サービス管理者(一般ユーザーと別系統の認証)
-- ------------------------------------------------------------
CREATE TABLE admins (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    email          VARCHAR(255) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at     DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

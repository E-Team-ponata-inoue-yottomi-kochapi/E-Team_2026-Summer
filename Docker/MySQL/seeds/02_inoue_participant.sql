-- ============================================================
-- 井上担当：参加者側テストデータ
-- 前提：主催者側SQLが先に実行されていること
-- ログイン用パスワード：inoue1111 ⇒ passwordpassword
-- ============================================================

-- ユーザー作成
-- inoue_user_id = 3001
INSERT INTO
    users (id, email, password_hash)
VALUES
    (
        3001,
        'inoue@example.com',
        'pbkdf2:sha256:260000$ltKpVAn9ZjKAsfOT$2e03ac183990ff20d783bbb2d4b3530c19badf56613c09d7b5db8e3573fbcbed'
    );


-- 世帯作成
-- inoue_household_id = '00000000-0000-0000-0000-000000003001'
INSERT INTO
    households (id, leader_id)
VALUES
    (
        '00000000-0000-0000-0000-000000003001',
        3001
    );


-- 家族メンバー作成
-- 太郎：3001
-- 花子：3002
-- 幸子：3003
INSERT INTO
    family_members (
        id,
        household_id,
        relation,
        name,
        gender,
        birth_date,
        email
    )
VALUES
    (
        3001,
        '00000000-0000-0000-0000-000000003001',
        '本人',
        '井上 太郎',
        '男',
        '1990-01-01',
        'inoue@example.com'
    ),
    (
        3002,
        '00000000-0000-0000-0000-000000003001',
        '妻',
        '井上 花子',
        '女',
        '1991-09-07',
        NULL
    ),
    (
        3003,
        '00000000-0000-0000-0000-000000003001',
        '娘',
        '井上 幸子',
        '女',
        '2020-07-07',
        NULL
    );


-- イベント申込作成
-- application_id = 3001
-- 申込日はイベントの締切日（2026-07-24）より前に設定
INSERT INTO
    applications (
        id,
        event_id,
        household_id,
        total_amount,
        applied_at
    )
VALUES
    (
        3001,
        'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64',
        '00000000-0000-0000-0000-000000003001',
        4000,
        '2026-07-20 10:00:00'
    );


-- イベント参加者作成
INSERT INTO
    application_participants (
        application_id,
        member_id,
        fee_rule_id,
        member_name_snapshot,
        relation_snapshot,
        age_at_application,
        fee_rule_name_snapshot,
        amount
    )
VALUES
    (
        3001,
        3001,
        5555,
        '井上 太郎',
        '本人',
        36,
        '大人',
        1500
    ),
    (
        3001,
        3002,
        5555,
        '井上 花子',
        '妻',
        34,
        '大人',
        1500
    ),
    (
        3001,
        3003,
        7777,
        '井上 幸子',
        '娘',
        6,
        '子ども',
        1000
    );

-- 井上主催イベント作成
-- inoue_event_id = '30010000-0000-4000-8000-000000000001'
INSERT INTO
    events (
        id,
        owner_id,
        title,
        start_at,
        place,
        address,
        capacity,
        deadline,
        description,
        items_to_bring,
        schedule,
        hold_condition,
        cancellation_policy,
        emergency_contact,
        payment_method,
        payment_deadline,
        status
    )
VALUES
    (
        '30010000-0000-4000-8000-000000000001',
        3001,
        '井上主催テストイベント',
        '2026-09-20 10:00:00',
        '奈良公園',
        '奈良県奈良市雑司町',
        30,
        '2026-09-15 23:59:59',
        'F-028マイページ表示確認用のテストイベントです',
        '飲み物・タオル',
        '09:30集合 10:00開始 12:00終了',
        '雨天決行',
        '開催日前日までキャンセル可能',
        '090-1234-5678',
        '現地払い',
        NULL,
        '公開'
    );
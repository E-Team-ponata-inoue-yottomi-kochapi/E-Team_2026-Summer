-- ユーザー作成
-- kochapi_user_id = 1111
-- パスワードはpasswordpassword
-- 主催者＆イベント未申込
INSERT INTO
    users (id, email, password_hash)
VALUES
    (
        1111,
        'test777@example.com',
        'pbkdf2:sha256:260000$ltKpVAn9ZjKAsfOT$2e03ac183990ff20d783bbb2d4b3530c19badf56613c09d7b5db8e3573fbcbed'
    );

-- householdsの作成
-- kochapi_household_id = '7f3a9c12-6d54-4b8e-9f21-3c8d7e5a1b20'
INSERT INTO
    households (id, leader_id)
VALUES
    ('7f3a9c12-6d54-4b8e-9f21-3c8d7e5a1b20', 1111);

-- family_membersの作成
-- kochapi_family_members_id_001 = 2222
-- kochapi_family_members_id_002 = 3333
-- kochapi_family_members_id_003 = 4444
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
        2222,
        '7f3a9c12-6d54-4b8e-9f21-3c8d7e5a1b20',
        '本人',
        '日本　太郎',
        '男',
        '1996-07-07',
        'test777@example.com'
    );

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
        3333,
        '7f3a9c12-6d54-4b8e-9f21-3c8d7e5a1b20',
        '娘',
        '日本　花子',
        '女',
        '2010-05-05',
        'test555@example.com'
    );

INSERT INTO
    family_members (
        id,
        household_id,
        relation,
        name,
        gender,
        birth_date
    )
VALUES
    (
        4444,
        '7f3a9c12-6d54-4b8e-9f21-3c8d7e5a1b20',
        '娘',
        '日本　桃子',
        '女',
        '2022-09-09'
    );

-- eventsの作成
-- kochapi_event_id = 'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64'
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
        status
    )
VALUES
    (
        'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64',
        1111,
        'テストイベント：夏越の大祓',
        '2026-06-30 16:00:00',
        '伊勢神宮（内宮）',
        '三重県伊勢市宇治館町１',
        24,
        '2026-06-23 23:59:59',
        '古くから12月の大祓と共に全国の神社でも行われている行事です',
        '雨具・暑さ対策グッズ・フォーマルな服装',
        '15時集合　16時大祓催行　17時解散',
        '雨天決行',
        '荒天中止（当日10時までにご連絡いたします）',
        '080-1234-5678',
        '現地払い',
        '公開'
    );

-- fee_rulesの作成
-- kochapi_fee_rules_id_001 = 5555
-- kochapi_fee_rules_id_002 = 7777
-- kochapi_fee_rules_id_003 = 8888
INSERT INTO
    fee_rules (id, event_id, tier_name, min_age, max_age, fee)
VALUES
    (
        5555,
        'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64',
        '大人',
        18,
        120,
        1500
    );

INSERT INTO
    fee_rules (id, event_id, tier_name, min_age, max_age, fee)
VALUES
    (
        7777,
        'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64',
        '子ども',
        6,
        17,
        1000
    );

INSERT INTO
    fee_rules (id, event_id, tier_name, min_age, max_age, fee)
VALUES
    (
        8888,
        'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64',
        '未就学児',
        0,
        5,
        0
    );

-- 参加者
INSERT INTO
    users (id, email, password_hash)
VALUES
    (
        1999,
        'test000@example.com',
        'pbkdf2:sha256:260000$ltKpVAn9ZjKAsfOT$2e03ac183990ff20d783bbb2d4b3530c19badf56613c09d7b5db8e3573fbcbed'
    );

-- householdsの作成
-- kochapi_household_id = '9a6b2c41-8e73-4d95-b126-5f9c3a7e2048'
INSERT INTO
    households (id, leader_id)
VALUES
    ('9a6b2c41-8e73-4d95-b126-5f9c3a7e2048', 1999);

-- family_membersの作成
-- kochapi_family_members_id_001 = 1999
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
        1999,
        '9a6b2c41-8e73-4d95-b126-5f9c3a7e2048',
        '本人',
        '日本　次郎',
        '男',
        '1999-12-31',
        'test000@example.com'
    );

-- イベント申込作成
-- application_id = 1999
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
        1999,
        'b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64',
        '9a6b2c41-8e73-4d95-b126-5f9c3a7e2048',
        1500,
        '2026-07-19 11:00:00'
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
        1999,
        1999,
        5555,
        '日本　次郎',
        '本人',
        27,
        '大人',
        1500
    );

-- deleteユーザー
INSERT INTO
    users (id, email, password_hash, deleted_at)
VALUES
    (
        3939,
        'deleteuser@example.com',
        'pbkdf2:sha256:260000$ltKpVAn9ZjKAsfOT$2e03ac183990ff20d783bbb2d4b3530c19badf56613c09d7b5db8e3573fbcbed',
        '2026-08-25 00:00:00'
    );

-- householdsの作成
-- kochapi_household_id = 'delxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxdel'
INSERT INTO
    households (id, leader_id)
VALUES
    ('delxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxdel', 3939);

-- family_membersの作成
-- kochapi_family_members_id_001 = 3939
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
        3939,
        'delxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxdel',
        '本人',
        'DELETEユーザー',
        '男',
        '2000-10-06',
        'deleteuser@example.com'
    );

-- banユーザー
INSERT INTO
    users (id, email, password_hash, is_banned)
VALUES
    (
        8282,
        'banuser@example.com',
        'pbkdf2:sha256:260000$ltKpVAn9ZjKAsfOT$2e03ac183990ff20d783bbb2d4b3530c19badf56613c09d7b5db8e3573fbcbed',
        TRUE
    );

-- householdsの作成
-- kochapi_household_id = 'banxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxban'
INSERT INTO
    households (id, leader_id)
VALUES
    ('banxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxban', 8282);

-- family_membersの作成
-- kochapi_family_members_id_001 = 8282
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
        8282,
        'banxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxban',
        '本人',
        'BANユーザー',
        '男',
        '2000-08-02',
        'banuser@example.com'
    );
-- ------------------------------------------------------------
-- 【主催者側】
-- ------------------------------------------------------------
SET @event_id        = 'event-ponta-001';
SET @fee_rule_adult_id = 6661;  -- 大人の料金区分id
SET @fee_rule_child_id = 6662;  -- 子供の料金区分id
SET @fee_rule_infant_id = 6663;  -- 未就学児の料金区分id

-- ------------------------------------------------------------
-- 参加者側】
-- ------------------------------------------------------------
-- users(参加者)
INSERT INTO users (id, email, password_hash)
VALUES (5001, 'yottomi@gmail.com', 'scrypt:32768:8:1$6ZxurNf1m4X9HaRi$f1890d83c7cf0b7b231973f979747510ef9b66f7a63063398b0b6f40a23b014addb0c60c2f841e23c6a5044f9c8bf524062c5fcc30a471fbf225bc4747c457b9');
SET @participant_id = 5001;

-- households(よっとみの世帯)
SET @household_id = 'household-yottomi-001';

INSERT INTO households (id, leader_id, created_at)
VALUES (@household_id, @participant_id, NOW());

-- family_members(よっとみ世帯メンバー)
INSERT INTO family_members (id, household_id, relation, name, gender, birth_date, email, created_at)
VALUES
    (5001, @household_id, '本人', 'yottomi太郎', '男', '1990-05-03', 'yottomi@gmail.com', NOW()),
    (5002, @household_id, '妻', 'yottomi花子', '女', '1990-08-10', NULL, NOW()),
    (5003, @household_id, '息子', 'yottomi次郎', '男', '2016-08-10', NULL, NOW()),
    (5004, @household_id, '娘', 'yottomi郁子', '女', '2018-07-24' ,null, NOW());

SET @member_self_id = 5001;
SET @member_wife_id = 5002;
SET @member_child1_id = 5003;
SET @member_child2_id = 5004;

-- applications(よっとみの世帯からイベントへの申込)
INSERT INTO applications (id, event_id, household_id, total_amount, applied_at)
VALUES (5001, @event_id, @household_id, 0 , NOW());

SET @application_id = 5001;

-- application_participants(よっとみ家からの参加者)
INSERT INTO application_participants (
    application_id, member_id, fee_rule_id, member_name_snapshot,
    relation_snapshot, age_at_application, fee_rule_name_snapshot, amount
)
VALUES
    (@application_id, @member_self_id, @fee_rule_adult_id, 'テスト太郎', '本人', 36, '大人', 0),
    (@application_id, @member_child1_id, @fee_rule_child_id, 'テスト次郎', '息子', 9, '子供', 0);

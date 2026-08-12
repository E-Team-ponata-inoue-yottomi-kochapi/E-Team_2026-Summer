/*
user.id = 9999
email = 'ponta@example.com'
events.id = 'event-ponta-001'　＊　無料イベント
fee_rules.id = 6661(大人)0円/6662(小人)0円/6663(未就学児)0円
*/

-- users
-- パスワードはpasswordpassword
-- ↓↓ password_hash ↓↓
SET @pw ='pbkdf2:sha256:260000$ltKpVAn9ZjKAsfOT$2e03ac183990ff20d783bbb2d4b3530c19badf56613c09d7b5db8e3573fbcbed';

INSERT INTO users (id, email, password_hash) 
VALUES(9999,'ponta@example.com', @pw);

-- households
INSERT INTO households (id, leader_id)
VALUES('ponta-family', 9999);

-- family_members
INSERT INTO family_members (id, household_id, relation, name, gender, birth_date)
VALUES
(9991, 'ponta-family', '本人', '伊邪那岐命', '男', '1996-08-27'),
(9992, 'ponta-family', '妻', '伊邪那美命', '女', '1996-10-05'),
(9993, 'ponta-family', '息子', '建速須佐之男命', '男', '2014-06-10'),
(9994, 'ponta-family', '娘', '天照大御神', '女', '2024-01-01');

-- events
INSERT INTO events (id, title, start_at, place, address, capacity, deadline, description, items_to_bring, schedule, hold_condition, cancellation_policy, emergency_contact, payment_method, owner_id, status)
VALUES('event-ponta-001', '天岩戸まつり〜光を〜取り戻す宴', '2026-09-15 18:00:00', '天安河原（あまのやすかわら）', '宮崎県西臼杵郡高千穂町大字岩戸1073-1', 50, '2026-09-08 23:59:59', '須佐之男命の乱暴により天照大御神が天岩戸にお隠れになりました。神々が集まり、賑やかな宴を開いて岩戸を開けていただく、無料の地域交流イベントです。', '鏡・榊・楽器など、宴を盛り上げてくれるもの', '18:00集合　18:30宴開始　20:00天岩戸が開く　20:30解散', '雨天決行', '無料のため連絡だけください。', '999-9999-9999', '現地払い', 9999, '公開' );

-- fee_rules
INSERT INTO fee_rules (id, event_id, tier_name, min_age, max_age, fee)
VALUES
(6661, 'event-ponta-001', '大人', 18, 120, 0),
(6662, 'event-ponta-001', '子ども', 6, 17, 0),
(6663, 'event-ponta-001', '未就学児', 0, 5, 0);

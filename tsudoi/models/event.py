import uuid
# import pymysql
# event_id = str(uuid.uuid4())

from util.db import get_connection


#######################################################################
# イベントの本体に関するmodel関数
#######################################################################

# 公開中のイベント一覧を取得する(status='公開'で絞り込み)
def get_open_events():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM events WHERE deleted_at IS NULL AND status='公開' ORDER BY created_at DESC;"
            cursor.execute(sql)
            events = cursor.fetchall()
            return events
    except pymysql.Error:
        raise
    finally:
        conn.close()

# イベントを1件取得する(statusによる絞り込みはしない、公開判定は呼び出し側で行う)
def find_event_by_id(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM events WHERE id=%s AND deleted_at IS NULL;"
            cursor.execute(sql, (event_id,))
            event = cursor.fetchone()
            return event if event else None
    # except pymysql.Error:
    #     raise
    finally:
        conn.close()

#　イベント主催者の氏名とowner_idを取得する
#(users.nameが無いためfamily_membersとJOINで氏名を取得)
def get_owner_by_event_id(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT f.name, e.owner_id FROM events as e INNER JOIN households as h ON e.owner_id=h.leader_id INNER JOIN family_members as f ON h.id=f.household_id WHERE e.id=%s AND f.relation='本人' ;"
            cursor.execute(sql, (event_id,))
            owner = cursor.fetchone()
            return owner
    except pymysql.Error:
        raise
    finally:
        conn.close()

# イベントを新規作成する(events.idはUUIDで生成)
def create_event(owner_id, title, start_at, place, address, capacity, deadline,
                 description, items_to_bring, schedule, hold_condition,
                 cancellation_policy, emergency_contact, payment_method,
                 payment_deadline, status):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            new_id  = str(uuid.uuid4())
            sql = """INSERT INTO events
                    (id, owner_id, title, start_at, place, address, capacity, deadline,
                    description, items_to_bring, schedule, hold_condition,
                    cancellation_policy, emergency_contact, payment_method,
                    payment_deadline, status)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s,
                     %s, %s, %s,
                     %s, %s );"""
            cursor.execute(sql, (new_id, owner_id, title, start_at, place, address, capacity, deadline,
                    description, items_to_bring, schedule, hold_condition,
                    cancellation_policy, emergency_contact, payment_method,
                    payment_deadline, status))
            conn.commit()
            return new_id
    # except pymysql.MySQLError:
    #     raise
    finally:
        conn.close()

# イベントの編集処理をする
def update_event(event_id, title, start_at, place, address, capacity, deadline,
                 description, items_to_bring, schedule, hold_condition,
                 cancellation_policy, emergency_contact, payment_method,
                 payment_deadline ):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """UPDATE events SET
                    title=%s, start_at=%s, place=%s, address=%s, capacity=%s, deadline=%s,
                    description=%s, items_to_bring=%s, schedule=%s, hold_condition=%s,
                    cancellation_policy=%s, emergency_contact=%s, payment_method=%s,
                    payment_deadline=%s, updated_at=NOW()
                    WHERE id=%s;"""
            cursor.execute(sql, (title, start_at, place, address, capacity, deadline,
                    description, items_to_bring, schedule, hold_condition,
                    cancellation_policy, emergency_contact, payment_method,
                    payment_deadline, event_id))
            conn.commit()
            return cursor.rowcount
    # except pymysql.MySQLError:
    #     raise
    finally:
        conn.close()

# イベントを論理削除する
def soft_delete_event(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE events SET deleted_at=NOW() WHERE id=%s;"
            cursor.execute(sql, (event_id,))
            conn.commit()
            return cursor.rowcount
    # except pymysql.MySQLError:
    #     raise
    finally:
        conn.close()

#######################################################################
# 料金区分に関するmodel関数
#######################################################################

# イベントの料金区分一覧を取得する(min_ageを降順表示/区分0件（異常時）でも空リストを返す)
def get_fee_rules_by_event_id(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM fee_rules WHERE event_id=%s AND deleted_at IS NULL ORDER BY min_age DESC;"
            cursor.execute(sql, (event_id,))
            fee_rules = cursor.fetchall()
        return fee_rules
    # except pymysql.Error as e:
    #     raise
    finally:
        conn.close()

# イベント作成時の料金区分作成（複数件）する
def create_fee_rule(event_id, tier_name, min_age, max_age, gender, fee):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO fee_rules
                    (event_id, tier_name, min_age, max_age, gender, fee)
                    VALUES (%s, %s, %s, %s, %s, %s );"""
            cursor.execute(sql, (event_id, tier_name, min_age, max_age, gender, fee))
            conn.commit()
            return cursor.lastrowid
    # except pymysql.MySQLError:
    #     raise
    finally:
        conn.close()

# イベント編集時に登録済みの料金区分を論理削除する
def delete_fee_rules_by_event(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE fee_rules SET deleted_at = NOW() WHERE event_id=%s AND deleted_at IS NULL;"
            cursor.execute(sql, (event_id,))
            conn.commit()
            return cursor.rowcount
    # except pymysql.MySQLError:
    #     raise
    finally:
        conn.close()
def list_events_by_owner(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT id, title, start_at, status "
                "FROM events "
                "WHERE owner_id = %s "
                "AND deleted_at IS NULL"
                )
            cursor.execute(sql, (user_id,))
            events = cursor.fetchall()
            return events
    finally:
        conn.close()
        

# イベントのidはUUIDになっているのでモデルでレコード作成時に生成する
# import uuid

# event_id = str(uuid.uuid4())

import pymysql
from util.db import get_connection

def get_open_events():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM events WHERE deleted_at IS NULL AND status='公開' ORDER BY created_at DESC;"
            cursor.execute(sql)
            events = cursor.fetchall()
            return events
    # except pymysql.Error as e:
    #     raise
    finally:
        conn.close()

def find_event_by_id(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM events WHERE id=%s AND status='公開' AND deleted_at IS NULL;"
            cursor.execute(sql, (event_id,))
            event = cursor.fetchone()
            return event if event else None
    # except pymysql.Error as e:
    #     raise
    finally:
        conn.close()

def get_owner_by_event_id(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT f.name, e.owner_id FROM events as e INNER JOIN households as h ON e.owner_id=h.leader_id INNER JOIN family_members as f ON h.id=f.household_id WHERE e.id=%s AND f.relation='本人' ;"
            cursor.execute(sql, (event_id,))
            owner = cursor.fetchone()
        return owner if owner else None
    # except pymysql.Error as e:
    #     raise
    finally:
        conn.close()

def get_fee_rules_by_event_id(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM fee_rules WHERE event_id=%s ORDER BY min_age DESC;"
            cursor.execute(sql, (event_id,))
            fee_rules = cursor.fetchall()
        return fee_rules if fee_rules else None
    # except pymysql.Error as e:
    #     raise
    finally:
        conn.close()

def list_events_by_owner(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, title, start_at, status FROM events WHERE owner_id = %s"
            cursor.execute(sql, (user_id,))
            events = cursor.fetchall()
            return events
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()
        
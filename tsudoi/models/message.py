from util.db import get_connection
import uuid

# メッセージ作成
def create_event_message(user_id, event_id, body):
    event_message_id = str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO event_messages (id, user_id, event_id, body) VALUES (%s, %s, %s, %s);"
            cursor.execute(sql, (event_message_id, user_id, event_id, body))
            conn.commit()
            return event_message_id
    finally:
        conn.close()

# 未削除メッセージ全件取得
def get_open_event_messages(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # メッセージ一覧は古い順
            sql = "SELECT em.id,  em.user_id, f.name, em.body, em.created_at FROM event_messages as em INNER JOIN households as h ON em.user_id=h.leader_id INNER JOIN family_members as f ON h.id=f.household_id WHERE em.event_id=%s AND f.relation='本人' AND em.deleted_at is NULL ORDER BY em.created_at ASC, em.id ASC;"
            cursor.execute(sql, (event_id,))
            open_event_messages = cursor.fetchall()
            return open_event_messages
    finally:
        conn.close()

# メッセージの論理削除
def soft_delete_event_message(event_id, event_message_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql ="UPDATE event_messages SET deleted_at=NOW() WHERE event_id=%s AND id=%s;"
            cursor.execute(sql, (event_id, event_message_id))
            conn.commit()
    finally:
        conn.close()

# メッセージ１件取得
def find_event_message_by_event_message_id(event_message_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM event_messages WHERE id=%s;"
            cursor.execute(sql, (event_message_id,))
            message = cursor.fetchone()
            return message
    finally:
        conn.close()
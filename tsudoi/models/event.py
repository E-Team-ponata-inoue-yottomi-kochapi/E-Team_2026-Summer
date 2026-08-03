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
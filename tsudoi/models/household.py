import pymysql
from util.db import get_connection

def get_household_by_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, leader_id FROM households WHERE leader_id = %s"
            cursor.execute(sql, (user_id,))
            household = cursor.fetchone()
            return household
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()

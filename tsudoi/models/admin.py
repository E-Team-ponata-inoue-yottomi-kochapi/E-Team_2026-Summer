import pymysql
from util.db import get_connection

# 追加関数：admin_requiredで使用する
def find_admin_by_id(admin_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT admin_id FROM admins WHERE admin_id=%s;"
            cursor.execute(sql,(admin_id,))
            admin = cursor.fetchone()
            return admin
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()


# F-030 ログイン時に使用
def find_admin_by_email(email):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT admin_id, email, password_hash FROM admins WHERE email=%s;"
            cursor.execute(sql,(email,))
            admin = cursor.fetchone()
            return admin
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()
from util.db import get_connection
import pymysql


# 申込情報を1件取得する(applicant_required判定に使用)
def find_application_by_id(application_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, event_id, household_id, total_amount, applied_at, updated_at FROM applications WHERE id=%s;"
            cursor.execute(sql, (application_id,))
            application = cursor.fetchone()
            return application
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()

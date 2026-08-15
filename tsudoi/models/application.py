import pymysql
from util.db import get_connection

def list_applications_by_household(household_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT applications.id, applications.event_id, "
                "applications.total_amount, applications.applied_at, "
                "events.title AS event_title, "
                "events.start_at AS event_start_at, "
                "events.status AS event_status "
                "FROM applications "
                "INNER JOIN events ON applications.event_id = events.id "
                "WHERE applications.household_id = %s"
            )

            cursor.execute(sql, (household_id,))
            applications = cursor.fetchall()
            return applications
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()

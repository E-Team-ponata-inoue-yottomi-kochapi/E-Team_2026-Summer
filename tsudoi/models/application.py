from util.db import get_connection



# 申込情報を1件取得する(applicant_required判定に使用)
def find_application_by_id(application_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, event_id, household_id, total_amount, applied_at, updated_at FROM applications WHERE id=%s;"
            cursor.execute(sql, (application_id,))
            application = cursor.fetchone()
            return application
    finally:
        conn.close()


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
    finally:
        conn.close()

import pymysql
from util.db import get_connection

def summarize_applications_by_event(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT applications.id AS application_id, "
                "applications.household_id, "
                "application_participants.member_id, "
                "application_participants.member_name_snapshot, "
                "application_participants.relation_snapshot, "
                "application_participants.age_at_application, "
                "application_participants.fee_rule_name_snapshot, "
                "application_participants.amount, "
                "family_members.gender "
                "FROM applications "
                "INNER JOIN application_participants ON applications.id = application_participants.application_id "
                "INNER JOIN family_members ON application_participants.member_id = family_members.id "
                "WHERE applications.event_id = %s"
            )
            cursor.execute(sql, (event_id,))
            summary_rows = cursor.fetchall()
            return summary_rows
    except pymysql.MySQLError:
        raise
    finally:
        conn.close()

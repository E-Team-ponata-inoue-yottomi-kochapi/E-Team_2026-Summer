from util.db import get_connection


# 指定したイベントの料金区分一覧を取得する
def get_fee_rules(event_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM fee_rules WHERE event_id = %s AND deleted_at IS NULL;"
            cursor.execute(sql, (event_id,))
            return cursor.fetchall()
    finally:
        conn.close()


# 申し込みを新規作成し、発行されたIDを返す
def insert_application(event_id, household_id, total_amount):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO applications (event_id, household_id, applied_at, total_amount)
                VALUES (%s, %s, NOW(), %s)
            """
            cursor.execute(sql, (event_id, household_id, total_amount))
            application_id = cursor.lastrowid
        conn.commit()
        return application_id
    finally:
        conn.close()


# 申し込みの参加者明細を1件追加する
def insert_application_participant(application_id, member_id, fee_rule_id, member_name_snapshot, relation_snapshot, age_at_application, fee_rule_name_snapshot, amount):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO application_participants (
                    application_id, member_id, fee_rule_id,
                    member_name_snapshot, relation_snapshot, age_at_application,
                    fee_rule_name_snapshot, amount
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                application_id, member_id, fee_rule_id,
                member_name_snapshot, relation_snapshot, age_at_application,
                fee_rule_name_snapshot, amount
            ))
        conn.commit()
    finally:
        conn.close()


# 指定した申し込みの参加者一覧を取得する
def get_application_participants(application_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM application_participants WHERE application_id = %s AND deleted_at IS NULL;"
            cursor.execute(sql, (application_id,))
            return cursor.fetchall()
    finally:
        conn.close()


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


# 申し込みIDから、申し込み内容をf取得する
def get_application(application_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM applications WHERE id = %s AND canceled_at IS NULL;"
            cursor.execute(sql, (application_id,))
            return cursor.fetchone()
    finally:
        conn.close()
        
# 申し込み内容を更新する
#関数名の一致を回避
def update_application_total(application_id, total_amount):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE applications
                SET total_amount = %s, updated_at = NOW()
                WHERE id = %s
            """
            cursor.execute(sql, (total_amount, application_id))
        conn.commit()
    finally:
        conn.close()


# 申し込みに紐づく参加者明細を削除する
def delete_application_participants(application_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            #論理削除では重複が発生するため、削除する
            sql = "DELETE FROM application_participants WHERE application_id = %s"
            cursor.execute(sql, (application_id,))
        conn.commit()
    finally:
        conn.close()
        
# 申し込みをキャンセルする
def cancel_application(application_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE applications SET canceled_at = NOW() WHERE id = %s"
            cursor.execute(sql, (application_id,))
        conn.commit()
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
                "WHERE applications.household_id = %s "
                "AND applications.canceled_at IS NULL "
                "AND events.deleted_at IS NULL"
            )
            cursor.execute(sql, (household_id,))
            applications = cursor.fetchall()
            return applications
    finally:
        conn.close()
        
        
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
                "WHERE applications.event_id = %s "
                "AND applications.canceled_at IS NULL"
            )
            cursor.execute(sql, (event_id,))
            summary_rows = cursor.fetchall()
            return summary_rows
    finally:
        conn.close()

# チャット機能権限用
def find_application_by_event_id_and_household_id(event_id, household_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM applications WHERE event_id=%s AND household_id=%s AND canceled_at IS NULL;"
            cursor.execute(sql, (event_id, household_id))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()
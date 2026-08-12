from util.db import get_connection

#ログイン中のユーザーが紐づく世帯を取得する
def get_household_by_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM households WHERE leader_id = %s AND deleted_at IS NULL;"
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
    finally:
        conn.close()
#指定した世帯に属する家族メンバー一覧を取得する
def get_family_members(household_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM family_members WHERE household_id = %s AND deleted_at IS NULL ORDER By created_at ASC;"
            cursor.execute(sql, (household_id,))
            return cursor.fetchall()
    finally:
        conn.close()

#家族メンバーを新規で追加する
def insert_family_member(household_id,relation,name,gender,birth_date,email):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO family_members(
                household_id,
                relation,
                name,
                gender,
                birth_date,
                email)
                VALUES(%s,%s,%s,%s,%s,%s)
                """
            cursor.execute(sql, (household_id, relation, name,gender,birth_date,email))
            conn.commit()
    finally:
        conn.close()
        
#家族メンバー情報を更新する
def update_family_member(member_id, relation, name, gender, birth_date, email):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql ="""
            UPDATE family_members
            SET relation = %s,
                name = %s,
                gender = %s,
                birth_date = %s,
                email = %s
            WHERE id = %s            
            """
            cursor.execute(sql, (relation,name,gender,birth_date,email,member_id))
        conn.commit()
    finally:
        conn.close()
        
#家族メンバーの論理削除
def delete_family_member(member_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE family_members SET deleted_at = NOW() WHERE id = %s"
            cursor.execute(sql, (member_id,))
        conn.commit()
    finally:
        conn.close()
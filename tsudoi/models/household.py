import uuid
from util.db import get_connection


#　user_idから世帯を特定する
def get_household_by_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM households WHERE leader_id=%s AND deleted_at IS NULL;"
            cursor.execute(sql,(user_id,))
            return cursor.fetchone()
    finally:
        conn.close()

#指定した世帯に属する家族メンバー一覧を取得する
def get_family_members(household_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM family_members WHERE household_id = %s AND deleted_at IS NULL ORDER BY created_at ASC;"
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
def soft_delete_family_member(member_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE family_members SET deleted_at = NOW() WHERE id = %s"
            cursor.execute(sql, (member_id,))
        conn.commit()
    finally:
        conn.close()

# idから家族メンバーを1件取得する
def get_family_member_by_id(member_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM family_members WHERE id=%s AND deleted_at IS NULL;"
            cursor.execute(sql, (member_id,))
            return cursor.fetchone()
    finally:
        conn.close()

# 新規登録と同時にhouseholdIDを生成する
def create_household(leader_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            new_id = str(uuid.uuid4())
            sql = "INSERT INTO households (id, leader_id) VALUES (%s, %s);"
            cursor.execute(sql, (new_id, leader_id))
            conn.commit()
            return new_id
    finally:
        conn.close()
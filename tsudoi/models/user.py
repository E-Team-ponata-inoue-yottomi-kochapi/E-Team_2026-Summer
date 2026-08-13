import pymysql
from util.db import get_connection

# ユーザーに関するクラス
class User:
    @classmethod
    # ユーザーを新規作成
    def create_user(cls, email, password_hash):
        conn = get_connection()
        try:
            # カーソルを取得
            with conn.cursor() as cursor:
                # プレースホルダー（%s）を使用してSQLインジェクションを防ぐ
                # プレースホルダーはDBによって異なる
                sql = "INSERT INTO users (email, password_hash) VALUES (%s, %s);"
                cursor.execute(sql, (email, password_hash))
                conn.commit()
                # 作成したレコードのIDを返す
                return cursor.lastrowid
        # MySQL関連のエラーを一括で捕まえている
        # モデルでは処理せず、例外発生を上げるだけ
        except pymysql.MySQLError:
            raise
        # 例外発生時でも必ずしてほしい処理を書く（接続を閉じるなど）
        finally:
            conn.close()

    @classmethod
    # メールアドレスからユーザー情報を取得
    def find_user_by_email(cls, email):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email=%s;"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                return user
        except pymysql.MySQLError:
            raise
        finally:
            conn.close()

    # IDから情報を取得
    @classmethod
    def find_user_by_id(cls, user_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id, email, created_at FROM users WHERE id = %s;"
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()
                return user
        except pymysql.MySQLError:
            raise
        finally:
            conn.close()

    # ユーザー情報を更新
    @classmethod
    def update_user(cls, user_id, email, password_hash):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                # 指定したユーザーのメールアドレスとパスワードを更新
                sql = "UPDATE users SET email = %s, password_hash = %s WHERE id = %s;"
                cursor.execute(sql, (email, password_hash, user_id))
                conn.commit()              
                # 更新された行数を返す
                return cursor.rowcount
        except pymysql.MySQLError:
            raise
        finally:
            conn.close()

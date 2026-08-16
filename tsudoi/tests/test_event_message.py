# docker exec -it tsudoi-Flask bash
# python -m unittest discover -s tests

import unittest
from models.message import create_event_message, get_open_event_messages
from util.db import get_connection
from app import app

# 練習用データ
# event_message_id = "event_message_id_0001"
# user_id = 1234567890
# event_id = "event_id_0001"
# body = "testdata_0001"

# def test_create_event_message(event_message_id, user_id, event_id, body):
#     return event_message_id, user_id, event_id, body

# test_case = test_create_event_message(event_message_id, user_id, event_id, body)

# 第２段階：ハッピーパス用（認証・認可確認なし）
class TestMessageModel(unittest.TestCase):
    # 各テストメソッドの実行後に呼ばれ、テストで登録したデータを削除する
    def tearDown(self):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM event_messages WHERE id=%s;"
                cursor.execute(sql, (self.event_message_id,))
                conn.commit()
        finally:
            conn.close()
        result = get_open_event_messages(self.event_id)
        if result:
            print(f"削除後：{ result[-1] }\n")

    # １．イベントメッセージ新規作成とその取得についてのテスト
    def test_create_event_messages(self):
        # self.assertEqual("event_message_id_0001", test_case[0])
        # self.assertEqual(1234567890, test_case[1])
        # self.assertEqual("event_id_0001", test_case[2])
        # self.assertEqual("testdata_0001", test_case[3])

        # 第２段階ではModelを直接テストするため、認証・認可は確認しない
        # そのため、イベント主催者だが参加申込をしていないユーザー1111でも、
        # event_messagesへの登録・取得ができる
        user_id = 1111
        self.event_id = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body = "これは第２段階テスト用です"
        self.event_message_id = create_event_message(user_id, self.event_id, self.body)
        result = get_open_event_messages(self.event_id)
        print(f"TestMessageModel\ntest_create_event_messages")
        print("１．イベントメッセージ新規作成とその取得についてのテスト")
        print(f"登録後：{ result[-1] }")
        # get_open_event_messagesが昇順のため、最後のメッセージを取得
        self.assertEqual(self.body, result[-1]["body"])

# 第３段階：認証用
class TestMessageControllerAuthenticated(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED'] = False
        self.app                       = app.test_client()
        self.event_message_id          = None
        # 第４段階に合わせて参加申請しているidへ変更
        # 第３段階は認証テストだが、現在は認可デコレータも適用されているため、
        # 認証後に認可を通過できる参加申込済みユーザー3001を使用する
        self.user_id                   = 3001
        self.event_id                  = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body                      = None

    # 各テストメソッドの実行後に呼ばれ、テストで登録したデータを削除する
    def tearDown(self):
        if self.event_message_id is None:
            return
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM event_messages WHERE id=%s;"
                cursor.execute(sql, (self.event_message_id,))
                conn.commit()
        finally:
            conn.close()
        result = get_open_event_messages(self.event_id)
        if result:
            print(f"削除後：{ result[-1] }\n")

    # ２．ログイン済ユーザー：画面表示テスト
    def test_messages_view_as_authenticated_user(self):
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.get(f"/events/{self.event_id}/messages/",
                                follow_redirects=False,
                                )

        # 正常に処理
        self.assertEqual(200, response.status_code)
        print("TestMessageControllerAuthenticated\ntest_messages_view_as_authenticated_user")
        print("２．ログイン済ユーザー：画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ３．ログイン済ユーザー：投稿テスト
    def test_create_process_as_authenticated_user(self):
        self.body = "これは第３段階テスト用です"

        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        # 正常に処理
        self.assertEqual(302, response.status_code)
        self.assertIn("messages", response.location)

        # 作成されたメッセージの取得
        result = get_open_event_messages(self.event_id)
        self.event_message_id = result[-1]["id"]
        self.assertEqual(self.body, result[-1]["body"])
        print("TestMessageControllerAuthenticated\ntest_create_process_as_authenticated_user")
        print("３．ログイン済ユーザー：投稿テスト")
        print(f"ステータスコード：{response.status_code}")
        print(f"登録後：{ result[-1] }")

    # ４．未ログインユーザー：画面表示テスト
    def test_messages_view_as_unauthenticated_user(self):
        # 未ログインのままHTTPリクエスト
        response = self.app.get(f"/events/{self.event_id}/messages/",
                                follow_redirects=False,
                                )

        # ログイン画面へ遷移
        self.assertEqual(302, response.status_code)
        self.assertIn("login", response.location)
        print("TestMessageControllerAuthenticated\ntest_messages_view_as_unauthenticated_user")
        print("４．未ログインユーザー：画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ５．未ログインユーザー：投稿テスト
    def test_create_process_as_unauthenticated_user(self):
        self.body = "これは第３段階テスト用です"

        # 未ログインのままHTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        # ログイン画面へ遷移
        self.assertEqual(302, response.status_code)
        self.assertIn("login", response.location)
        print("TestMessageControllerAuthenticated\ntest_create_process_as_unauthenticated_user")
        print("５．未ログインユーザー：投稿テスト")
        print(f"ステータスコード：{response.status_code}\n")

# 第４段階：認可用
class TestMessageAuthorization(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED'] = False
        self.app                       = app.test_client()
        self.event_message_id          = None
        # イベント主催者＆イベント参加未申込
        # 第４段階ではController経由で認可チェックを行うため、
        # ログイン済みでも、このイベントには参加申込していないため、閲覧・投稿ともに権限エラー（403）になるユーザー
        self.unauthorized_user         = 1111
        self.event_id                  = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body                      = None

    # ６．ログイン済＆イベント未申込ユーザー：画面表示テスト
    def test_messages_view_as_unauthorized_user(self):
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.unauthorized_user
        self.assertEqual(self.unauthorized_user, session["user_id"])

        # HTTPリクエスト
        response = self.app.get(f"/events/{self.event_id}/messages/",
                                follow_redirects=False,
                                )

        # 権限エラー
        self.assertEqual(403, response.status_code)
        print("TestMessageAuthorization\ntest_messages_view_as_unauthorized_user")
        print("６．ログイン済＆イベント未申込ユーザー：画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ７．ログイン済＆イベント未申込ユーザー：投稿テスト
    def test_create_process_as_unauthorized_user(self):
        self.body = "これは第４段階テスト用です"

        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.unauthorized_user
        self.assertEqual(self.unauthorized_user, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        # 権限エラー
        self.assertEqual(403, response.status_code)
        print("TestMessageAuthorization\ntest_create_process_as_unauthorized_user")
        print("７．ログイン済＆イベント未申込ユーザー：投稿テスト")
        print(f"ステータスコード：{response.status_code}\n")

if __name__ == '__main__':
    unittest.main()
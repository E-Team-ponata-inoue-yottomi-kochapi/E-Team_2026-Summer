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

# 第２段階：ハッピーパス用
class TestCreateFunction(unittest.TestCase):
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

    # イベントメッセージ新規作成とその取得についてのテスト
    def test_create_event_messages(self):
        # self.assertEqual("event_message_id_0001", test_case[0])
        # self.assertEqual(1234567890, test_case[1])
        # self.assertEqual("event_id_0001", test_case[2])
        # self.assertEqual("testdata_0001", test_case[3])
        user_id = 1111
        self.event_id = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        body = "これはテスト用です"
        self.event_message_id = create_event_message(user_id, self.event_id, body)
        result = get_open_event_messages(self.event_id)
        print(f"TestCreateFunction\ntest_create_event_messagesテスト結果")
        print(f"登録後：{ result[-1] }")
        # get_open_event_messagesが昇順のため、最後のメッセージを取得
        self.assertEqual("これはテスト用です", result[-1]["body"])

# 第３段階：認証用
class TestMessageController(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED'] = False
        self.app                       = app.test_client()
        self.event_message_id          = None
        self.user_id                   = 1111
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

    def test_messages_view_as_logged_in_user(self):
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        response = self.app.get(f"/events/{self.event_id}/messages/",
                                follow_redirects=False,
                                )
        self.assertEqual(200, response.status_code)
        print("TestMessageController\ntest_messages_view_as_logged_in_userテスト結果")
        print(f"ステータスコード：{response.status_code}")

    def test_create_process_as_logged_in_user(self):
        self.body = "これは第３段階テスト用です"
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        response = self.app.post(f"/events/{self.event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )
        self.assertEqual(302, response.status_code)
        self.assertIn("messages", response.location)

        result = get_open_event_messages(self.event_id)
        self.event_message_id = result[-1]["id"]
        self.assertEqual(self.body, result[-1]["body"])
        print("TestMessageController\ntest_create_process_as_logged_in_userテスト結果")
        print(f"ステータスコード：{response.status_code}")
        print(f"登録後：{ result[-1] }")

if __name__ == '__main__':
    unittest.main()
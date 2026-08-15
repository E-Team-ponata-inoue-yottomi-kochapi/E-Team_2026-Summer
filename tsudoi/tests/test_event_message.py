# docker exec -it tsudoi-Flask bash
# python -m unittest discover -s tests

import unittest
from models.message import create_event_message, get_open_event_messages
from util.db import get_connection

# 練習用データ
# event_message_id = "event_message_id_0001"
# user_id = 1234567890
# event_id = "event_id_0001"
# body = "testdata_0001"

# def test_create_event_message(event_message_id, user_id, event_id, body):
#     return event_message_id, user_id, event_id, body

# test_case = test_create_event_message(event_message_id, user_id, event_id, body)

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
        print(f"削除後：{ result }")

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
        print(f"登録後：{ result }")
        # get_open_event_messagesが昇順のため、最後のメッセージを取得
        self.assertEqual("これはテスト用です", result[-1]["body"])
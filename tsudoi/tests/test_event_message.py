# docker exec -it tsudoi-Flask bash
# python -m unittest discover -s tests

import unittest
from models.message import create_event_message, get_open_event_messages, soft_delete_event_message
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
        if self.event_message_id is None:
            return None
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM event_messages WHERE id=%s;"
                cursor.execute(sql, (self.event_message_id,))
                conn.commit()
        finally:
            conn.close()
        result = get_open_event_messages(self.event_id)
        self.aft_msgs_count = len(result)
        print(f"テストデータ物理削除後の件数：{ self.aft_msgs_count }件\n")
        if result:
            print(f"テストデータ物理削除後のDB：{ result[-1] }\n")

    # ２nd-１．イベントメッセージ新規作成とその取得についてのテスト
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
        messages = get_open_event_messages(self.event_id)
        self.bef_msgs_count = len(messages)
        self.event_message_id = create_event_message(user_id, self.event_id, self.body)
        result = get_open_event_messages(self.event_id)
        print(f"TestMessageModel\ntest_create_event_messages")
        print("２nd-１．イベントメッセージ新規作成とその取得についてのテスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"投稿後のDB：{ result[-1] }")
        # get_open_event_messagesが昇順のため、最後のメッセージを取得
        self.assertEqual(self.body, result[-1]["body"])

# 第３段階：認証用
class TestMessageControllerAuthenticated(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        self.title                     = "TestMessageControllerAuthenticated"
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
        messages = get_open_event_messages(self.event_id)
        self.bef_msgs_count = len(messages)

    # 各テストメソッドの実行後に呼ばれ、テストで登録したデータを削除する
    def tearDown(self):
        if self.event_message_id is None:
            return None
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM event_messages WHERE id=%s;"
                cursor.execute(sql, (self.event_message_id,))
                conn.commit()
        finally:
            conn.close()
        result = get_open_event_messages(self.event_id)
        self.aft_msgs_count = len(result)
        print(f"テストデータ物理削除後の件数：{ self.aft_msgs_count }件")
        if result:
            print(f"テストデータ物理削除後のDB：{ result[-1] }\n")

    # ３rd-１．ログイン済ユーザー：画面表示テスト
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
        print(f"{self.title}\ntest_messages_view_as_authenticated_user")
        print("３rd-１．ログイン済ユーザー：画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ３rd-２．ログイン済ユーザー：投稿テスト
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
        print(f"{self.title}\ntest_create_process_as_authenticated_user")
        print("３rd-２．ログイン済ユーザー：投稿テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}")
        print(f"投稿後のDB：{ result[-1] }")

    # ３rd-３．未ログインユーザー：画面表示テスト
    def test_messages_view_as_unauthenticated_user(self):
        # 未ログインのままHTTPリクエスト
        response = self.app.get(f"/events/{self.event_id}/messages/",
                                follow_redirects=False,
                                )

        # ログイン画面へ遷移
        self.assertEqual(302, response.status_code)
        self.assertIn("login", response.location)
        print(f"{self.title}\ntest_messages_view_as_unauthenticated_user")
        print("３rd-３．未ログインユーザー：画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ３rd-４．未ログインユーザー：投稿テスト
    def test_create_process_as_unauthenticated_user(self):
        self.body = "これは第３段階テスト用です"

        # 未ログインのままHTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        messages = get_open_event_messages(self.event_id)
        self.aft_msgs_count = len(messages)

        # ログイン画面へ遷移
        self.assertEqual(302, response.status_code)
        self.assertIn("login", response.location)
        print(f"{self.title}\ntest_create_process_as_unauthenticated_user")
        print("３rd-４．未ログインユーザー：投稿テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}")
        print(f"投稿後の件数：{self.aft_msgs_count}件\n")

# 第４段階：認可用
class TestMessageAuthorization(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        self.title                     = "TestMessageAuthorization"
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED'] = False
        self.app                       = app.test_client()
        # イベント主催者＆イベント参加未申込
        # 第４段階ではController経由で認可チェックを行うため、
        # ログイン済みでも、このイベントには参加申込していないため、閲覧・投稿ともに権限エラー（403）になるユーザー
        self.unauthorized_user         = 1111
        self.event_id                  = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body                      = None
        messages = get_open_event_messages(self.event_id)
        self.bef_msgs_count = len(messages)

    # ４th-１．ログイン済＆イベント未申込ユーザー：画面表示テスト
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
        print(f"{self.title}\ntest_messages_view_as_unauthorized_user")
        print("４th-１．ログイン済＆イベント未申込ユーザー：画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ４th-２．ログイン済＆イベント未申込ユーザー：投稿テスト
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

        messages = get_open_event_messages(self.event_id)
        self.aft_msgs_count = len(messages)

        # 権限エラー
        self.assertEqual(403, response.status_code)
        print(f"{self.title}\ntest_create_process_as_unauthorized_user")
        print("４th-２．ログイン済＆イベント未申込ユーザー：投稿テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}")
        print(f"投稿後の件数：{self.aft_msgs_count}件\n")

# 第５段階：検証用
class TestMessageAbnormalCase(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        self.title                     = "TestMessageAbnormalCase"
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED'] = False
        self.app                       = app.test_client()
        self.user_id                   = 3001
        self.existent_event_id         = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body                      = None
        messages = get_open_event_messages(self.existent_event_id)
        self.bef_msgs_count = len(messages)
        self.nonexistent_event_id      = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

    # ５th-１：未入力テスト
    def test_create_process_as_empty_body(self):
        self.error_msg = "メッセージを入力してください".encode('utf-8')

        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.existent_event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        messages = get_open_event_messages(self.existent_event_id)
        self.aft_msgs_count = len(messages)

        # 未入力時は画面再表示
        self.assertEqual(200, response.status_code)
        self.assertIn(self.error_msg, response.data)
        # DB増減チェック
        self.assertEqual(self.bef_msgs_count, self.aft_msgs_count)

        print(f"{self.title}\ntest_create_process_as_empty_body")
        print("５th-１：未入力テスト")
        print(f"ステータスコード：{response.status_code}")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"投稿後の件数：{self.aft_msgs_count}件\n")

    # ５th-２：文字数制限テスト
    def test_create_process_as_too_long_body(self):
        self.body = "あ" * 301
        self.error_msg = "300文字以内で入力してください".encode('utf-8')

        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.existent_event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        messages = get_open_event_messages(self.existent_event_id)
        self.aft_msgs_count = len(messages)

        # 入力文字オーバー時は画面再表示
        self.assertEqual(200, response.status_code)
        self.assertIn(self.error_msg, response.data)
        # DB増減チェック
        self.assertEqual(self.bef_msgs_count, self.aft_msgs_count)

        print(f"{self.title}\ntest_create_process_as_too_long_body")
        print("５th-２：文字数制限テスト")
        print(f"ステータスコード：{response.status_code}")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"投稿後の件数：{self.aft_msgs_count}件\n")

    # ５th-３：存在しないイベントIDのチャット画面表示テスト
    def test_messages_view_as_nonexistent_event(self):
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.get(f"/events/{self.nonexistent_event_id}/messages/",
                                follow_redirects=False,
                                )

        # チャット対象のイベントが存在しない場合は404
        self.assertEqual(404, response.status_code)

        print(f"{self.title}\ntest_messages_view_as_nonexistent_event")
        print("５th-３：存在しないイベントIDの画面表示テスト")
        print(f"ステータスコード：{response.status_code}\n")

    # ５th-４：存在しないイベントIDへの投稿テスト
    def test_create_process_as_nonexistent_event(self):
        self.body = "これは第５段階テスト用です"
    
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.nonexistent_event_id}/messages/",
                                data={"body": self.body},
                                follow_redirects=False,
                                )

        messages = get_open_event_messages(self.existent_event_id)
        self.aft_msgs_count = len(messages)

        # チャット対象のイベントが存在しない場合は404
        self.assertEqual(404, response.status_code)

        # DB増減チェック
        self.assertEqual(self.bef_msgs_count, self.aft_msgs_count)

        print(f"{self.title}\ntest_create_process_as_nonexistent_event")
        print("５th-４：存在しないイベントIDへの投稿テスト")
        print(f"ステータスコード：{response.status_code}")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"投稿後の件数：{self.aft_msgs_count}件\n")

# <追加機能：削除>
# # 第1段階：ウォーキングスケルトン用
# class TestMessageController(unittest.TestCase):
#     # 各テストメソッドの実行前に呼ばる
#     def setUp(self):
#         self.title                     = "TestMessageController"
#         # テストのため無効化
#         app.config['WTF_CSRF_ENABLED'] = False
#         self.app                       = app.test_client()
    
#     # １st-１：メッセージ削除のController疎通テスト
#     def test_delete_process(self):
#         # HTTPリクエスト
#         response = self.app.delete(f"/events/test-event/messages/delete-message",
#                                 follow_redirects=False,
#                                 )

#         self.assertEqual(200, response.status_code)
#         self.assertEqual("メッセージ削除".encode('utf-8'), response.data)

#         print(f"{self.title}\ntest_delete_process")
#         print("１st-１：メッセージ削除のController疎通テスト")
#         print(f"ステータスコード：{response.status_code}")

# 第２段階：ハッピーパス用（認証・認可確認なし）
class TestMessageModelForDelete(unittest.TestCase):
        # 各テストメソッドの実行後に呼ばれ、テストで登録したデータを物理削除する
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
        self.aft_msgs_count = len(result)
        print(f"テストデータ物理削除後の件数：{ self.aft_msgs_count }件\n")
        if result:
            print(f"テストデータ物理削除後のDB：{ result[-1] }\n")

    # ２nd-２：認証・認可なしのメッセージ論理削除テスト
    def test_delete_message(self):
        user_id = 3001
        self.event_id = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body = "これは第２段階テスト：削除用です"
        messages = get_open_event_messages(self.event_id)
        self.bef_msgs_count = len(messages)
        self.event_message_id = create_event_message(user_id, self.event_id, self.body)
        result = get_open_event_messages(self.event_id)
        bef_delete_msg = result[-1]
        self.assertIn(self.body, bef_delete_msg["body"])

        print(f"TestMessageModelForDelete\ntest_delete_message")
        print("２nd-２：認証・認可なしのメッセージ論理削除テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"論理削除前のDB：{ bef_delete_msg }")

        soft_delete_event_message(self.event_id, self.event_message_id)
        results = get_open_event_messages(self.event_id)
        id_list = []
        for result in results:
            id_list.append(result["id"])
        self.assertNotIn(self.event_message_id, id_list)

        conn =get_connection()
        try:
            with conn.cursor()as cursor:
                sql = "SELECT * FROM event_messages WHERE event_id=%s AND id=%s;"
                cursor.execute(sql, (self.event_id, self.event_message_id))
                result = cursor.fetchone()
        finally:
            conn.close()

        self.assertIsNotNone(result["deleted_at"])
        print(f"論理削除後のDB：{ result }")

# 第３段階：認証用
class TestMessageControllerAuthenticatedForDelete(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        self.title                     = "TestMessageControllerAuthenticatedForDelete"
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED'] = False
        self.app                       = app.test_client()
        self.user_id                   = 3001
        self.event_id                  = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body                      = "これは第３段階テスト：削除用です"
        messages = get_open_event_messages(self.event_id)
        self.bef_msgs_count = len(messages)
        self.event_message_id          = create_event_message(self.user_id, self.event_id, self.body)

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
        self.aft_msgs_count = len(result)
        print(f"テストデータ物理削除後の件数：{ self.aft_msgs_count }件\n")
        if result:
            print(f"テストデータ物理削除後のDB：{ result[-1] }\n")

    # ３rd-５：ログイン済みユーザー：論理削除テスト
    def test_delete_message_as_authenticated_user(self):
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.user_id
        self.assertEqual(self.user_id, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/{self.event_message_id}",
                                follow_redirects=False,
                                )
        self.assertEqual(302, response.status_code)
        self.assertIn(self.event_id, response.location)

        conn =get_connection()
        try:
            with conn.cursor()as cursor:
                sql = "SELECT * FROM event_messages WHERE event_id=%s AND id=%s;"
                cursor.execute(sql, (self.event_id, self.event_message_id))
                result = cursor.fetchone()
        finally:
            conn.close()

        self.assertIsNotNone(result["deleted_at"])

        print(f"{self.title}\ntest_delete_message")
        print("３rd-５：ログイン済みユーザー：論理削除テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}")
        print(f"論理削除後のDB：{ result }")

    # ３rd-６：未ログインユーザー：論理削除テスト
    def test_delete_message_as_unauthenticated_user(self):
        # 未ログインのままHTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/{self.event_message_id}",
                                follow_redirects=False,
                                )

        # ログイン画面へ遷移
        self.assertEqual(302, response.status_code)
        self.assertIn("login", response.location)

        conn =get_connection()
        try:
            with conn.cursor()as cursor:
                sql = "SELECT * FROM event_messages WHERE event_id=%s AND id=%s;"
                cursor.execute(sql, (self.event_id, self.event_message_id))
                result = cursor.fetchone()
        finally:
            conn.close()

        print(f"{self.title}\ntest_delete_message_as_unauthenticated_user")
        print("３rd-６：未ログインユーザー：論理削除テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}")
        print(f"論理削除失敗後：{ result }")

# 第４段階：認可用
class TestMessageAuthorizationForDelete(unittest.TestCase):
    # 各テストメソッドの実行前に呼ばる
    def setUp(self):
        self.title                               = "TestMessageAuthorizationForDelete"
        # テストのため無効化
        app.config['WTF_CSRF_ENABLED']           = False
        self.app                                 = app.test_client()
        # 参加者＆メッセージ投稿者
        self.authorized_user                     = 3001
        # 主催者＆イベント未申込
        self.unauthorized_user_not_applied       = 1111
        # 参加者＆メッセージ非投稿者
        self.unauthorized_user_not_owner         = 1999
        self.event_id                            = "b8e4d521-9f6a-4c37-a812-5d7e3f9b2c64"
        self.body                                = "これは第４段階テスト：削除用です"
        messages = get_open_event_messages(self.event_id)
        self.bef_msgs_count = len(messages)
        self.event_message_id                    = create_event_message(self.authorized_user, self.event_id, self.body)

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
        self.aft_msgs_count = len(result)
        print(f"テストデータ物理削除後の件数：{ self.aft_msgs_count }件\n")
        if result:
            print(f"テストデータ物理削除後のDB：{ result[-1] }\n")

    # ４th-３．ログイン済＆イベント未申込ユーザー：削除テスト
    def test_delete_message_as_unauthorized_user_not_applied(self):
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.unauthorized_user_not_applied
        self.assertEqual(self.unauthorized_user_not_applied, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/{self.event_message_id}",
                                follow_redirects=False,
                                )

        # 権限エラー
        self.assertEqual(403, response.status_code)

        conn =get_connection()
        try:
            with conn.cursor()as cursor:
                sql = "SELECT * FROM event_messages WHERE event_id=%s AND id=%s;"
                cursor.execute(sql, (self.event_id, self.event_message_id))
                result = cursor.fetchone()
        finally:
            conn.close()

        print(f"{self.title}\ntest_delete_message_as_unauthorized_user_not_applied")
        print("４th-３．ログイン済＆イベント未申込ユーザー：削除テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}")
        print(f"論理削除失敗後：{ result }")

    # ４th-４．ログイン済＆イベント申込＆メッセージ非投稿ユーザー：削除テスト
    def test_delete_message_as_unauthorized_user_not_owner(self):
        # ログイン処理
        with self.app.session_transaction() as session:
            session["user_id"] = self.unauthorized_user_not_owner
        self.assertEqual(self.unauthorized_user_not_owner, session["user_id"])

        # HTTPリクエスト
        response = self.app.post(f"/events/{self.event_id}/messages/{self.event_message_id}",
                                follow_redirects=False,
                                )

        # 権限エラー
        self.assertEqual(403, response.status_code)

        conn =get_connection()
        try:
            with conn.cursor()as cursor:
                sql = "SELECT * FROM event_messages WHERE event_id=%s AND id=%s;"
                cursor.execute(sql, (self.event_id, self.event_message_id))
                result = cursor.fetchone()
        finally:
            conn.close()

        print(f"{self.title}\ntest_delete_message_as_unauthorized_user_not_owner")
        print("４th-４．ログイン済＆イベント申込＆メッセージ非投稿ユーザー：削除テスト")
        print(f"投稿前の件数：{self.bef_msgs_count}件")
        print(f"ステータスコード：{response.status_code}\n")
        print(f"論理削除失敗後：{ result }")

if __name__ == '__main__':
    unittest.main()
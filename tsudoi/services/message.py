from flask import session
from models.household import get_household_by_user
from models.application import find_application_by_event_id_and_household_id
from models.message import create_event_message
from models.event import find_event_by_id

# チェット機能権限用
def get_household_id_by_user_id():
    user_id = session.get("user_id")
    result = get_household_by_user(user_id)
    if result is None:
        return None
    household_id = result["id"]
    return household_id

# チャット機能権限チェック
def can_access_event_chat(event_id):
    # イベントの存在有無
    event = find_event_by_id(event_id)
    if event is None:
        return None
    household_id = get_household_id_by_user_id()
    result = find_application_by_event_id_and_household_id(event_id, household_id)
    return bool(result)

# 検証と作成
def create_message(user_id, event_id, body):
    error_msgs = []

    # 投稿対象イベントの存在有無
    event = find_event_by_id(event_id)
    if event is None:
        return None

    if not body:
        error_msgs.append("メッセージを入力してください")

    if body and len(body) > 300:
        error_msgs.append("300文字以内で入力してください")

    if error_msgs:
        return {"valid": False, "error_msgs": error_msgs}
    
    event_message_id = create_event_message(user_id, event_id, body)
    return {"valid": True, "data": event_message_id}

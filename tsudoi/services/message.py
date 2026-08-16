from flask import session
from models.household import get_household_by_user
from models.application import find_application_by_event_id_and_household_id

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
    household_id = get_household_id_by_user_id()
    result = find_application_by_event_id_and_household_id(event_id, household_id)
    return bool(result)

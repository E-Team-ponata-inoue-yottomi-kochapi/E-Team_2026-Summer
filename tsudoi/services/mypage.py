from models.user import User
from models.household import get_household_by_user
from models.application import list_applications_by_household
from models.event import list_events_by_owner
from werkzeug.security import generate_password_hash

def get_current_user(user_id):
    # user_idを使って、現在のユーザー情報をDBから取得する
    user = User.find_user_by_id(user_id)
    return user

def update_user(user_id, email, password):
    # 平文のパスワードをハッシュ化してからModelへ渡す
    password_hash = generate_password_hash(password)
    # DBを更新し、更新された行数を受け取る
    updated_count = User.update_user(user_id, email, password_hash)
    return updated_count

def get_mypage(user_id):
    household = get_household_by_user(user_id)
    household_id = household["id"]
    applications = list_applications_by_household(household_id)
    events = list_events_by_owner(user_id)

    return {
        "applications": applications,
        "events": events
    }

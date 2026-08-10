from models.user import User

def get_current_user(user_id):
    # user_idを使って、現在のユーザー情報をDBから取得する
    user = User.find_user_by_id(user_id)
    return user

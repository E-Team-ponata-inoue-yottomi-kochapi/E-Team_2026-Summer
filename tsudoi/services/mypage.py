from models.user import User
from models.household import get_household_by_user
from models.application import list_applications_by_household
from models.event import list_events_by_owner
from werkzeug.security import generate_password_hash, check_password_hash
import re

def get_current_user(user_id):
    # user_idを使って、現在のユーザー情報をDBから取得する
    user = User.find_user_by_id(user_id)
    return user

def validate_user_update(user_id, email, password):
    errors = []

    # 新規登録と同じメールアドレス形式チェック
    # 先頭ドット、ドット連続、@直前のドットを禁止
    ng_pattern = r'\A(?!\.|.*(\.{2,}|\.{1,}@)).*\Z'

    # 一般的なメールアドレス形式
    basic_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

    # メールアドレス未入力
    if not email:
        errors.append("メールアドレスを入力してください")

    # メールアドレスが入力された場合のみチェック
    if email:

        # 長さチェック
        if len(email) > 254:
            errors.append("メールアドレスが長すぎます")

        # 形式チェック
        if re.fullmatch(ng_pattern, email) is None:
            errors.append("メールアドレスの形式が違います")
        elif re.fullmatch(basic_pattern, email) is None:
            errors.append("メールアドレスの形式が違います")

    # パスワードが入力された場合のみチェック
    if password:

        # 15文字未満
        if len(password) < 15:
            errors.append("パスワードは15文字以上で設定してください")

        # 空白文字を含んでいる
        if re.search(r"\s", password):
            errors.append("パスワードにスペースは使用できません")

    # ここまでで入力エラーがあればDBを使ったメール重複確認は行わない
    if errors:
        return errors

    # メールアドレス重複チェック
    existing_user = User.find_user_by_email(email)

    # 見つかったユーザーが自分以外ならエラー
    if existing_user and existing_user["id"] != user_id:
        errors.append("登録済みのアドレスです")

    return errors

def update_user(user_id, email, password):
    # 現在のユーザー情報を取得
    current_user = User.find_user_with_password_by_id(user_id)

    # ユーザーが存在しない場合
    if current_user is None:
        return "update_failed"

    # メールアドレスが変更されたか
    email_changed = email != current_user["email"]

    # パスワードが変更されたか
    password_changed = False

    if password:
        password_changed = not check_password_hash(current_user["password_hash"], password)

    # メールもパスワードも変更されていない
    if not email_changed and not password_changed:
        return "no_change"

    # パスワードが変更されている場合
    if password_changed:
        password_hash = generate_password_hash(password)

        row_count = User.update_user(user_id, email, password_hash)

    # パスワードが変更されていない場合
    else:
        row_count = User.update_email(user_id, email)

    # DBを更新できなかった場合
    if row_count != 1:
        return "update_failed"

    # メール・パスワード両方変更
    if email_changed and password_changed:
        return "email_password_updated"

    # メールのみ変更
    if email_changed:
        return "email_updated"

    # パスワードのみ変更
    return "password_updated"

def get_mypage(user_id):
    household = get_household_by_user(user_id)

    # 世帯が存在しない場合
    if household is None:
        return None
    
    household_id = household["id"]
    
    applications = list_applications_by_household(household_id)
    events = list_events_by_owner(user_id)

    return {
        "applications": applications,
        "events": events
    }

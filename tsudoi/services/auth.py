from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

def signup(email, password, password_confirmation):
    messages = []
    # ローカル部の最低限の形式チェック
    # 先頭ドットはNG
    # ドットの連続はNG
    # @マーク直前のドットはNG
    ng_pattern = r'\A(?!\.|.*(\.{2,}|\.{1,}@)).*\Z'

    # 形式が正しくても実在するメールアドレスとは限らないため、実在確認にはメール認証などが必要
    # 一般的なメールアドレス形式
    basic_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

    if not email or not password or not password_confirmation:
        messages.append("未入力の項目があります")

    if email and len(email) > 254:
        messages.append("メールアドレスが長すぎます")

    if email:
        if re.fullmatch(ng_pattern, email) is None:
            messages.append("メールアドレスの形式が違います")
        elif re.fullmatch(basic_pattern, email) is None:
            messages.append("メールアドレスの形式が違います")

    if password and re.search(r"\s", password):
        messages.append("パスワードにスペースは使用できません")

    if password and password_confirmation and password != password_confirmation:
        messages.append("パスワードが一致しません")

    # 入力チェックでエラーがあればDB操作を行わず結果を返す（辞書型）
    if messages:
        return {"valid": False, "messages": messages}

    # 入力チェックを通過したらメールアドレスの重複を確認
    existing_user = User.find_user_by_email(email)
    if existing_user:
        messages.append("登録済みのアドレスです")
        return {"valid": False, "messages": messages}

    # 全チェック通過したらパスワードのハッシュ化・ユーザー新規作成
    password_hash = generate_password_hash(password)
    user_id = User.create_user(email, password_hash)
    return {"valid": True, "data": {"user_id": user_id}}

def login(email, password):

    # if not email or not password:
    #     return {"valid": False, "messages": ["未入力の項目があります"]}

    user = User.find_user_by_email(email)

    if not user:
        # 第三者にメールアドレスの登録有・無やどちらが間違っているかを知らせない
        return {"valid": False, "messages": ["メールアドレスorパスワードが違います"]}

    if not check_password_hash(user["password_hash"], password):
        return{"valid": False, "messages": ["メールアドレスorパスワードが違います"]}

    # if user["is_banned"] is True:
    #     return {"valid": False, "messages": ["ログインエラー：管理者へお問い合わせください"]}

    return {"valid": True, "data": {"user_id": user["id"]}}
from flask import Blueprint, render_template, redirect, url_for
from services.mypage import get_current_user
# auth_guard.py実装後に追加
# from util.auth_guard import login_required

mypage_bp = Blueprint("mypage", __name__)

# マイページ
@mypage_bp.route("/mypage", methods=["GET"])
# auth_guard.py実装後に追加
# @login_required
def mypage_view():
    return render_template("mypage/index.html")

# ユーザー編集画面表示
@mypage_bp.route("/user/edit", methods=["GET"])
# auth_guard.py実装後に追加
# @login_required
def user_edit_view():
    # ステージ2ではテスト用ユーザーIDを固定で使用
    user_id = 3001

    # serviceからユーザー情報を取得
    user = get_current_user(user_id)

    return render_template("mypage/settings.html", user = user)

# ユーザー編集処理
@mypage_bp.route("/user", methods=["POST"])
# auth_guard.py実装後に追加
# @login_required
def user_edit_process():
    errors =[]
    
    # TODO: 入力チェックを実装する
    # 例：
    # if ユーザー名が空欄:
    # errors.append("エラー時遷移確認用のエラーです")

    # エラーがある場合
    if errors:
        return render_template("mypage/settings.html", error_messages=errors) # errorsリストの内容をerror_massegesとしてHTMLで利用できるようにする

    # TODO: Modelを使ってユーザー情報を更新する

    # 更新成功後はマイページへ移動
    return redirect(url_for("mypage.mypage_view"))
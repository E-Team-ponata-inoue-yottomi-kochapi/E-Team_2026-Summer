from flask import Blueprint, render_template, redirect, url_for, request, session
from services.mypage import get_current_user, update_user, get_mypage
from util.auth_guard import login_required

mypage_bp = Blueprint("mypage", __name__)

# マイページ
@mypage_bp.route("/mypage", methods=["GET"])
@login_required
def mypage_view():
    # セッションからログイン中のユーザーIDを取得r
    user_id = session.get("user_id")
    # serviceからマイページ表示に必要な情報を取得
    mypage_data = get_mypage(user_id)
    # mypage_dataにはapplicationsテーブルとeventsテーブルの情報が入っているので、それぞれで分けて変数に格納
    applications = mypage_data["applications"]
    events = mypage_data["events"]

    return render_template("mypage/index.html", applications = applications, events = events)

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

    # 第2段階ではテスト用ユーザーIDを固定
    user_id = 3001

    # フォームから入力値を取得
    email = request.form.get("email")
    password = request.form.get("password")
    
    # TODO: 入力チェックは後続段階で実装
    # 例：
    # if ユーザー名が空欄:
    # errors.append("エラー時遷移確認用のエラーです")

    # エラーがある場合
    if errors:
        return render_template("mypage/settings.html", error_messages=errors) # errorsリストの内容をerror_massegesとしてHTMLで利用できるようにする

    # Serviceを使ってユーザー情報を更新(受け取ったupdate_countは現状使っていないが、後々異常系判定に利用する)
    updated_count = update_user(user_id, email, password)

    # 更新成功後はマイページへ移動
    return redirect(url_for("mypage.mypage_view"))

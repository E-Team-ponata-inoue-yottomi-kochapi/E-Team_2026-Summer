from flask import Blueprint, render_template, redirect, url_for, request, session, flash, abort
import pymysql
import logging
from services.mypage import get_current_user, update_user, get_mypage, validate_user_update
from util.auth_guard import login_required
from config.constants import MYPAGE_ENDPOINT

mypage_bp = Blueprint("mypage", __name__)
logger = logging.getLogger(__name__)

# マイページ
@mypage_bp.route("/mypage", methods=["GET"])
@login_required
def mypage_view():
    # セッションからログイン中のユーザーIDを取得
    user_id = session.get("user_id")
    try:
        # serviceからマイページ表示に必要な情報を取得
        mypage_data = get_mypage(user_id)
    except pymysql.MySQLError as e:
        logger.exception("MySQLエラーが発生しました: %s", e)
        abort(500)

    # 世帯が存在しない場合
    if mypage_data is None:
        logger.error("ログインユーザーに紐づく世帯が存在しません: user_id=%s", user_id)
        abort(500)

    # mypage_dataにはapplicationsテーブルとeventsテーブルの情報が入っているので、それぞれで分けて変数に格納
    applications = mypage_data["applications"]
    events = mypage_data["events"]

    return render_template("mypage/index.html", applications = applications, events = events, title="マイページ")

# ユーザー編集画面表示
@mypage_bp.route("/user/edit", methods=["GET"])
@login_required
def user_edit_view():
    # セッションからログイン中のユーザーIDを取得
    user_id = session.get("user_id")
    try:
        # serviceからユーザー情報を取得
        user = get_current_user(user_id)

    except pymysql.MySQLError as e:
        logger.exception("MySQLエラーが発生しました: %s", e)
        abort(500)

    # ユーザーが存在しない場合
    if user is None:
        logger.error("ログイン中のユーザー情報が存在しません: %s", user_id)
        abort(500)

    return render_template("mypage/settings.html", user = user, title="ユーザー編集", back_page_url=url_for(MYPAGE_ENDPOINT), back_page_title="マイページ")

# ユーザー編集処理
@mypage_bp.route("/user", methods=["POST"])
@login_required
def user_edit_process():
    # セッションからログイン中のユーザーIDを取得
    user_id = session.get("user_id")

    # フォームから入力値を取得
    # メールアドレスは前後の空白を除去
    email = request.form.get("email", "").strip()
    # パスワードは空白を除去しない、空白が含まれていた場合はバリデーションでエラーにする
    password = request.form.get("password", "")
    
    try:
        # Serviceで入力チェック
        errors = validate_user_update(user_id, email, password)

        # 入力エラーがある場合
        if errors:
            user = get_current_user(user_id)
            #入力したパスワードを画面に残す
            user["email"] = email
            return render_template("mypage/settings.html", user=user, error_messages=errors, title="ユーザー編集", back_page_url=url_for(MYPAGE_ENDPOINT), back_page_title="マイページ")

        # Serviceに更新処理を依頼
        result = update_user(user_id, email, password)

    except pymysql.MySQLError as e:
        logger.exception("MySQLエラーが発生しました: %s", e)
        abort(500)

    # Serviceの結果によってメッセージを変更
    if result == "email_password_updated":
        flash("メールアドレスとパスワードを更新しました")

    elif result == "email_updated":
        flash("メールアドレスを更新しました")

    elif result == "password_updated":
        flash("パスワードを更新しました")

    elif result == "no_change":
        flash("変更はありません")

    elif result == "update_failed":
        flash("ユーザー情報を更新できませんでした")

    # 更新処理後はマイページへ移動
    return redirect(url_for("mypage.mypage_view"))

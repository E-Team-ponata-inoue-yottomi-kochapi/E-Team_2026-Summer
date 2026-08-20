from flask import Blueprint, session, render_template, redirect, url_for, request, abort
import pymysql
from util.auth_guard import login_required
from services.auth import signup, login
from models.household import get_household_by_user, get_family_members
import logging

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)

@auth_bp.route("/signup", methods=["GET"])
def signup_view():
    if session.get("user_id") is None:
        return render_template("auth/signup.html", title="新規登録", messages=[], email="")
    # ログイン済みの場合にマイページへ遷移
    return redirect(url_for("mypage.mypage_view"))

@auth_bp.route("/signup", methods=["POST"])
def signup_process():
    # controllerがフォームデータを取得
    # 入力がなかったら空文字を渡す
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    password_confirmation = request.form.get("password_confirmation", "")
    try:
        # サービスで行った入力チェックの結果を取得
        result = signup(email, password, password_confirmation)
    except pymysql.MySQLError as e:
        # DBエラーは入力エラーではないため500エラーを返す
        logger.exception('MySQLエラーが発生しました: %s', e)
        abort(500)

    # 入力チェックでエラーになった場合
    if result["valid"] is False:
        # titleはbase.htmlの{{title}}に表示される（渡さない場合、タブには「つどい」のみが表示される）
        # 入力エラーがあれば登録画面を再表示
        return render_template("auth/signup.html", title="新規登録", messages=result["messages"], email=email)

    # 入力チェックを通った場合
    # 新規登録したユーザーIDをセッションに保存
    session['user_id'] = result["data"]["user_id"]
    # 新規登録が完了したらプロフィール・家族情報登録へ遷移
    return redirect(url_for("household.household_list_view"))

@auth_bp.route("/login", methods=["GET"])
def login_view():
    if session.get("user_id") is None:
        return render_template("auth/login.html", title="ログイン", messages=[], email="")
    # ログイン済みの場合はマイページへ遷移する
    return redirect(url_for("mypage.mypage_view"))

@auth_bp.route("/login", methods=["POST"])
def login_process():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    try:
        result = login(email, password)
    except pymysql.MySQLError as e:
        # DBエラーは入力エラーではないため500エラーを返す
        logger.exception('MySQLエラーが発生しました: %s', e)
        abort(500)

    if result["valid"] is False:
        return render_template("auth/login.html", title="ログイン", messages=result["messages"], email=email)

    session['user_id'] = result["data"]["user_id"]
    return redirect(url_for("mypage.mypage_view"))

@auth_bp.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for("auth.login_view"))

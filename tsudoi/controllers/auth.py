from flask import Blueprint, session, render_template, redirect, url_for, request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET"])
def signup_view():
    if session.get("user_id") is None:
        return render_template("auth/signup.html")
    # ログイン済みの場合はマイページへ遷移する
    return "マイページへ遷移"

@auth_bp.route("/signup", methods=["POST"])
def signup_process():
    return "家族情報登録へ進む"

@auth_bp.route("/login", methods=["GET"])
def login_view():
    if session.get("user_id") is None:
        return render_template("auth/login.html")
	# ログイン済みの場合はマイページへ遷移する
    return "マイページへ遷移"

@auth_bp.route("/login", methods=["POST"])
def login_process():
    return "マイページへ遷移"

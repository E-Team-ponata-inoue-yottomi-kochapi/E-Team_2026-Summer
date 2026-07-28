from flask import Blueprint, render_template, redirect, url_for


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ログイン画面表示
@admin_bp.route("/login", methods=["GET"])
def login_view():
    return render_template("admin/admin_login.html")

# ログイン処理
@admin_bp.route("/login", methods=["POST"])
def login_process():
    return redirect(url_for("admin.dashboard_view"))

# ダッシュボード画面表示
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard_view():
    return render_template("admin/dashboard.html")

# 登録アカウント一覧画面表示
@admin_bp.route("/users", methods=["GET"])
def users_list_view():
    return render_template("admin/accounts.html")

# 作成済みイベント一覧画面表示
@admin_bp.route("/events", methods=["GET"])
def event_list_view():
    return render_template("admin/events.html")

# ログアウト処理
@admin_bp.route("/logout", methods=["POST"])
def logout_process():
    return redirect(url_for("admin.login_view"))
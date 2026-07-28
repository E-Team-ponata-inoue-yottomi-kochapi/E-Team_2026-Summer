# ============================================================
# 【チュートリアル用・削除予定】
# ぽんたが、チュートリアルとして仮実装。チュートリアル完了後、
# 削除してから本実装に置き換える。
# このコードの内容と処理を理解し、言語化できるようにすること！
# ============================================================
from flask import Blueprint, render_template,session,redirect,url_for

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET"])
def signup_view():
    return render_template("auth/signup.html")



# 開発中の骨組み確認用。本実装では削除してください。
@auth_bp.route("/login/dev", methods=["GET"])
def dev_login():
    session["user_id"] = 1  # 仮のユーザーIDをセッションにセット
    return redirect(url_for("household.household_list_view"))
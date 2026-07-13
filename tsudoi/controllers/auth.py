# ============================================================
# 【チュートリアル用・削除予定】
# ぽんたが、チュートリアルとして仮実装。チュートリアル完了後、
# 削除してから本実装に置き換える。
# このコードの内容と処理を理解し、言語化できるようにすること！
# ============================================================
from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET"])
def signup_view():
    return render_template("auth/signup.html")

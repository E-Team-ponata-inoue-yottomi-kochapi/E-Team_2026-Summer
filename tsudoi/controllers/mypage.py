from flask import Blueprint, render_template

mypage_bp = Blueprint("mypage", __name__)

@mypage_bp.route("/mypage", methods=["GET"])
def mypage_view():
    return render_template("mypage/mypage.html")
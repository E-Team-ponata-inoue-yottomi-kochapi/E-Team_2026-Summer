from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET"])
def signup_view():
    return render_template("auth/signup.html")
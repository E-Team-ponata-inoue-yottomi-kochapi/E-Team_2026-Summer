from flask import Blueprint, session, render_template, redirect, url_for, request

event_bp = Blueprint("event", __name__, url_prefix="/events")

@event_bp.route("/", methods=["GET"])
def list_view():
    # if session.get("user_id") is None:
    #     return redirect(url_for('auth.login_view'))
    return render_template("event/event_list.html")

@event_bp.route("/<string:id>", methods=["GET"])
def detail_view(id):
    # if session.get("user_id") is None:
    #     return redirect(url_for('auth.login_view'))
    return render_template("event/event_detail.html")
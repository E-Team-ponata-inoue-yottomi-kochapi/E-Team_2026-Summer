from flask import Blueprint, session, render_template, redirect, url_for, request
from models.event import get_open_events

event_bp = Blueprint("event", __name__, url_prefix="/events")


# イベント一覧表示画面
@event_bp.route("/", methods=["GET"])
def list_view():
    # if session.get("user_id") is None:
    #     return redirect(url_for('auth.login_view'))
    events = get_open_events()
    return render_template("event/event_list.html", title="イベント一覧", events=events)


# イベント詳細表示画面
@event_bp.route("/<string:id>", methods=["GET"])
def detail_view(id):
    # if session.get("user_id") is None:
    #     return redirect(url_for('auth.login_view'))
    return render_template("event/event_detail.html")


# イベント作成画面表示
@event_bp.route("/new", methods=["GET"])
# @login_required
def new_view():
 
    return render_template("event/event_form.html")


# イベント作成処理
@event_bp.route("/", methods=["POST"])
# @login_required
def create_process():
    #仮ID
    event_id = 1
    return redirect(url_for("event.detail_view", id=event_id))

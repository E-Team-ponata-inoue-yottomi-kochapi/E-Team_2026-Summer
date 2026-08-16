from flask import Blueprint, session, render_template, redirect, url_for, request, abort
from models.event import get_open_events
from services.event import get_event_detail
import pymysql
from util.auth_guard import login_required
import logging
from services.message import can_access_event_chat

event_bp = Blueprint("event", __name__, url_prefix="/events")
logger = logging.getLogger(__name__)

# イベント一覧表示画面
@event_bp.route("/", methods=["GET"])
@login_required
def list_view():
    try:
        events = get_open_events()
    except pymysql.MySQLError as e:
        logger.exception('MySQLエラーが発生しました: %s', e)
        abort(500)

    return render_template("event/event_list.html", title="イベント一覧", events=events)


# イベント詳細表示画面
@event_bp.route("/<string:event_id>", methods=["GET"])
@login_required
def detail_view(event_id):
    try:
        result = get_event_detail(event_id)
        if result is None:
            abort(404)
        event = result["event"]
        owner = result["owner"]
        fee_rules = result["fee_rules"]
        # 画面の表示切り分け用
        can_chat = can_access_event_chat(event_id)
    except pymysql.MySQLError as e:
        logger.exception('MySQLエラーが発生しました: %s', e)
        abort(500)
    return render_template("event/event_detail.html", title="イベント詳細", event=event, owner=owner, fee_rules=fee_rules, can_chat=can_chat)


# イベント作成画面表示
@event_bp.route("/new", methods=["GET"])
# @login_required
def new_view():
 
    return render_template("event/event_form.html")


# イベント作成処理
@event_bp.route("/", methods=["POST"])
# @login_required
def create_process():

    return redirect(url_for("event.detail_view", event_id=event_id))

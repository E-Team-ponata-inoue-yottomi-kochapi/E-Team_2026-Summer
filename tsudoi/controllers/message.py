from flask import Blueprint, session, render_template, redirect, url_for, request, abort
from models.message import get_open_event_messages, soft_delete_event_message
from util.auth_guard import login_required, chat_required, delete_message_required
from services.message import create_message
import pymysql
import logging
from config.constants import EVENT_DETAIL_ENDPOINT

message_bp = Blueprint("message", __name__, url_prefix="/events/<string:event_id>/messages")
logger = logging.getLogger(__name__)

# メッセージ表示画面
@message_bp.route("/", methods=["GET"])
@login_required
@chat_required
def messages_view(event_id):
    user_id = session.get("user_id")
    event_messages = get_open_event_messages(event_id)
    return render_template("message/message_list.html", title="チャットルーム", event_id=event_id, event_messages=event_messages, error_msgs=[], body="", user_id=user_id, back_page_url=url_for(EVENT_DETAIL_ENDPOINT, event_id=event_id), back_page_title="イベント詳細")

# メッセージ作成
@message_bp.route("/", methods=["POST"])
@login_required
@chat_required
def create_process(event_id):
    user_id = session.get("user_id")
    body = request.form.get("body", "")
    try:
        result = create_message(user_id, event_id, body)
    except pymysql.Error as e:
        # DBエラーは入力エラーではないため500エラーを返す
        logger.exception('MySQLエラーが発生しました: %s', e)
        abort(500)

    # 既存メッセージの取得
    event_messages = get_open_event_messages(event_id)

    # 入力チェックでエラーの場合
    if result["valid"] is False:
        return render_template("message/message_list.html", title="チャットルーム", event_id=event_id, event_messages=event_messages, error_msgs=result["error_msgs"], body=body, user_id=user_id, back_page_url=url_for(EVENT_DETAIL_ENDPOINT, event_id=event_id), back_page_title="イベント詳細")

    return redirect(url_for("message.messages_view", event_id=event_id))

# メッセージ削除
@message_bp.route("/<string:event_message_id>", methods=["POST"])
@login_required
@chat_required
@delete_message_required
def delete_process(event_id, event_message_id):
    soft_delete_event_message(event_id, event_message_id)
    return redirect(url_for("message.messages_view", event_id=event_id))
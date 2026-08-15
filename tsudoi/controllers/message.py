from flask import Blueprint, session, render_template, redirect, url_for, request, abort
from models.message import get_open_event_messages, create_event_message

message_bp = Blueprint("message", __name__, url_prefix="/events/<string:event_id>/messages")

@message_bp.route("/", methods=["GET"])
def messages_view(event_id):
    event_messages = get_open_event_messages(event_id)
    return render_template("message/message_list.html", title="チャットルーム", event_id=event_id, event_messages=event_messages)

@message_bp.route("/", methods=["POST"])
def create_process(event_id):
    # 認証・Session実装前のため、固定ユーザーIDを使用
    user_id = 1111
    body = request.form.get("body", "")
    create_event_message(user_id, event_id, body)
    return redirect(url_for("message.messages_view", event_id=event_id))
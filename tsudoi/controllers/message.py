from flask import Blueprint, session, render_template, redirect, url_for, request, abort
from models.message import get_open_event_messages, create_event_message
from util.auth_guard import login_required, chat_required

message_bp = Blueprint("message", __name__, url_prefix="/events/<string:event_id>/messages")

# メッセージ表示画面
@message_bp.route("/", methods=["GET"])
@login_required
@chat_required
def messages_view(event_id):
    event_messages = get_open_event_messages(event_id)
    return render_template("message/message_list.html", title="チャットルーム", event_id=event_id, event_messages=event_messages)

# メッセージ作成
@message_bp.route("/", methods=["POST"])
@login_required
@chat_required
def create_process(event_id):
    user_id = session.get("user_id")
    body = request.form.get("body", "")
    create_event_message(user_id, event_id, body)
    return redirect(url_for("message.messages_view", event_id=event_id))
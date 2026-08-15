from flask import Blueprint, session, render_template, redirect, url_for, request, abort

message_bp = Blueprint("message", __name__, url_prefix="/events/<string:event_id>/messages")

@message_bp.route("/", methods=["GET"])
def messages_view(event_id):
    event = {"id": event_id}
    return render_template("message/message_list.html", title="チャットルーム", event=event)

@message_bp.route("/", methods=["POST"])
def create_process(event_id):
    event = {"id": event_id}
    message = "hello, chatroom!!"
    return render_template("message/message_list.html", title="チャットルーム", message=message, event=event)
from functools import wraps
from flask import Blueprint, session, render_template, redirect, url_for

application_bp = Blueprint("application", __name__, url_prefix="/apply")


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login_view'))
        return func(*args, **kwargs)
    return wrapper


@application_bp.route('/events/<string:event_id>/', methods=["GET"])
@login_required
def apply_view(event_id):
    members = [
        {"id": 1, "name": "田中太郎"},
        {"id": 2, "name": "田中花子"},
    ]  # 仮データ
    return render_template('application/apply_form.html', event_id=event_id, members=members, application=None)


@application_bp.route('/events/<int:event_id>/confirm', methods=["POST"])
@login_required
def apply_confirmation_view(event_id):
    # フォームで選択されたmember_idsを受け取り、まだ保存せず画面表示のみ
    event = {"id": event_id, "name": "サンプルイベント"}
    participants = [
        {"member_name_snapshot": "田中太郎", "fee_rule_name_snapshot": "大人", "amount": 3000},
        {"member_name_snapshot": "田中花子", "fee_rule_name_snapshot": "子供", "amount": 1500},
    ]
    total_amount = sum(p["amount"] for p in participants)
    return render_template(
        'application/apply_confirmation.html', event=event, event_id=event_id, participants=participants, total_amount=total_amount
    )


@application_bp.route('/events/<int:event_id>/create', methods=["POST"])
@login_required
def apply_create_process(event_id):
    # INSERT処理
    application_id = 1  # 仮:保存後に発行されたID
    return redirect(url_for('application.apply_summary_view', id=application_id))


@application_bp.route('/applications/<int:id>/summary', methods=["GET"])
@login_required
def apply_summary_view(id):
    event = {"id": "dummy-event-id", "name": "サンプルイベント"}
    participants = [
        {"member_name_snapshot": "田中太郎", "fee_rule_name_snapshot": "大人", "amount": 3000},
        {"member_name_snapshot": "田中花子", "fee_rule_name_snapshot": "子供", "amount": 1500},
    ]
    total_amount = sum(p["amount"] for p in participants)
    return render_template(
        'application/apply_summary.html', event=event, application_id=id, participants=participants, total_amount=total_amount
    )


@application_bp.route('/applications/<int:id>/edit', methods=["GET"])
@login_required
def apply_edit_view(id):
    application = {"id": id}
    members = [
        {"id": 1, "name": "田中太郎", "age": 40},
        {"id": 2, "name": "田中花子", "age": 8},
    ]
    return render_template('application/apply_form.html', event_id=None, members=members, application=application)


@application_bp.route('/applications/<int:id>/edit', methods=["POST"])
@login_required
def apply_edit_process(id):
    return redirect(url_for('application.apply_summary_view', id=id))
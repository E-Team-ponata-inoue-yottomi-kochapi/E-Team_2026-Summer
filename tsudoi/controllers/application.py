from functools import wraps
from flask import Blueprint, session, render_template, redirect, url_for
from flask import flash
# auth_guard.py実装後に追加
# from util.auth_guard import login_required


application_bp = Blueprint("application", __name__, url_prefix="/apply")

# ログイン権限デコレータ
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login_view'))
        return func(*args, **kwargs)
    return wrapper


# 集計画面
@application_bp.route("/events/<string:event_id>/applications", methods=["GET"])
# auth_guard.py実装後に追加
# @login_required
def summary_view(event_id):
    return render_template("event/summary.html", event_id = event_id)
    

#申込フォーム表示/参加メンバー選択画面
@application_bp.route('/events/<string:event_id>/', methods=["GET"])
# @login_required
def apply_view(event_id):
    members = [
        {"id": 1, "name": "田中太郎"},
        {"id": 2, "name": "田中花子"},
    ]  # 仮データ
    return render_template('application/apply_form.html', event_id=event_id, members=members, application=None)

  
#申し込み内容確認画面
@application_bp.route('/events/<string:event_id>/confirm', methods=["GET","POST"])
# @login_required
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
  
#申し込み確定処理
@application_bp.route('/events/<string:event_id>/create', methods=["POST"])
# @login_required
def apply_create_process(event_id):
    application_id = 1  # 仮:保存後に発行されたID
    flash("申し込みが完了しました")
    return redirect(url_for('event.detail_view', id=event_id))

  
#申し込み内容編集画面
@application_bp.route('/applications/<int:id>/edit', methods=["GET"])
# @login_required
def apply_edit_view(id):
    application = {"id": id}
    members = [
        {"id": 1, "name": "田中太郎", "age": 40},
        {"id": 2, "name": "田中花子", "age": 8},
    ]
    return render_template('application/apply_form.html', event_id=None, members=members, application=application)

  
#申し込み編集処理
@application_bp.route('/applications/<int:id>/edit', methods=["POST"])
# @login_required
def apply_edit_process(id):
    return redirect(url_for('mypage.mypage_view'))

  
#キャンセル処理→マイページに遷移
@application_bp.route('/applications/<int:id>/cancel',methods=["POST"])
# @login_required
def apply_cancel_process(id):
    return redirect(url_for('mypage.mypage_view'))




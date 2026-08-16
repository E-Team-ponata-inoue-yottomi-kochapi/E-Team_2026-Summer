from flask import Blueprint, session, request, render_template, redirect, url_for
from flask import flash
from services.application import summarize_applications
# auth_guard.py実装後に追加
from util.auth_guard import login_required, host_required, applicant_required

#必要なデータの呼び出し
from models.household import get_household_by_user, get_family_members
from models.application import get_application, cancel_application
from services.application import build_participants_preview, create_application, update_application
from models.event import find_event_by_id

application_bp = Blueprint("application", __name__, url_prefix="/apply")


# 集計画面
@application_bp.route("/events/<string:event_id>/applications", methods=["GET"])
@login_required
@host_required
def summary_view(event_id):
    summary = summarize_applications(event_id)

    return render_template(
        "event/summary.html",
        event_id = event_id,
        total_participants = summary["total_participants"],
        total_amount = summary["total_amount"],
        fee_summary = summary["fee_summary"],
        gender_summary = summary["gender_summary"],
        household_summary = summary["household_summary"],
        household_count = summary["household_count"],
        event = summary["event"]
        )


#申込フォーム表示/参加メンバー選択画面
@application_bp.route('/events/<string:event_id>/', methods=["GET", "POST"])
@login_required
def apply_view(event_id):
    household = get_household_by_user(session['user_id'])
    members = get_family_members(household['id'])
    #メンバー全員の料金を計算して表示する
    all_member_ids = [str(m['id']) for m in members]
    participants_preview = build_participants_preview(event_id, household['id'], all_member_ids)
    preview_by_id = {p['member_id']: p for p in participants_preview}
    return render_template('application/apply_form.html', event_id=event_id, members=members, application=None,preview_by_id=preview_by_id,)

  
#申し込み内容確認画面
@application_bp.route('/events/<string:event_id>/confirm', methods=["POST"])
@login_required
def apply_confirmation_view(event_id):
    # フォームで選択されたmember_idsを受け取り、まだ保存せず画面表示のみ
    household = get_household_by_user(session['user_id'])
    member_ids = request.form.getlist('member_ids')
    #申込画面に表示するデータの取得
    participants = build_participants_preview(event_id, household['id'], member_ids)
    total_amount = sum(p["amount"] for p in participants)
    event = find_event_by_id(event_id)
    return render_template(
        'application/apply_confirmation.html', event=event, event_id=event_id, participants=participants, total_amount=total_amount
    )
  
#申し込み確定処理
@application_bp.route('/events/<string:event_id>/create', methods=["POST"])
@login_required
def apply_create_process(event_id):
    household = get_household_by_user(session['user_id'])
    member_ids = request.form.getlist('member_ids')
    #申込完了ページがないため変数の代入をしていません
    create_application(event_id, household['id'], member_ids)
    flash("申し込みが完了しました")
    return redirect(url_for('event.detail_view', event_id=event_id))

  
#申し込み内容編集画面
@application_bp.route('/applications/<int:id>/edit', methods=["GET"])
@login_required
@applicant_required
def apply_edit_view(id):
    application = get_application(id)
    household = get_household_by_user(session['user_id'])
    members = get_family_members(household['id'])
    #メンバー全員の料金を計算して表示する
    all_member_ids = [str(m['id']) for m in members]
    participants_preview = build_participants_preview(application['event_id'], household['id'], all_member_ids)
    preview_by_id = {p['member_id']: p for p in participants_preview}
    return render_template('application/apply_form.html', event_id=None, members=members, application=application,preview_by_id=preview_by_id,)

  
#申し込み編集処理
@application_bp.route('/applications/<int:id>/edit', methods=["POST"])
@login_required
@applicant_required
def apply_edit_process(id):
    application = get_application(id)
    household = get_household_by_user(session['user_id'])
    member_ids = request.form.getlist('member_ids')

    update_application(id, application['event_id'], household['id'], member_ids)

    flash("申し込み内容を更新しました")
    return redirect(url_for('mypage.mypage_view'))

  
#キャンセル処理→マイページに遷移
@application_bp.route('/applications/<int:id>/cancel',methods=["POST"])
@login_required
@applicant_required
def apply_cancel_process(id):
    cancel_application(id)
    flash("申し込みをキャンセルしました")
    return redirect(url_for('mypage.mypage_view'))

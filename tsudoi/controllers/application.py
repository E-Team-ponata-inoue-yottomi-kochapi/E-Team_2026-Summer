from flask import Blueprint, session, request, render_template, redirect, url_for, abort, flash
import pymysql
import logging
from services.application import summarize_applications
from util.auth_guard import login_required, host_required, applicant_required

#必要なデータの呼び出し
from models.household import get_household_by_user, get_family_members
from models.application import get_application, cancel_application,get_application_participants,find_application_by_event_id_and_household_id
from services.application import build_participants_preview, create_application, update_application, is_deadline_passed, validate_member_ids, is_capacity_exceeded, is_capacity_exceeded_on_edit,is_empty_selection
from models.event import find_event_by_id

from config.constants import EVENT_DETAIL_ENDPOINT, EVENT_APPLY_ENDPOINT

application_bp = Blueprint("application", __name__, url_prefix="/apply")
logger = logging.getLogger(__name__)


# 集計画面
@application_bp.route("/events/<string:event_id>/applications", methods=["GET"])
@login_required
@host_required
def summary_view(event_id):
    try:
        summary = summarize_applications(event_id)

    except pymysql.MySQLError as e:
        logger.exception("MySQLエラーが発生しました: %s", e)
        abort(500)

    return render_template(
        "event/summary.html",
        event_id = event_id,
        total_participants = summary["total_participants"],
        total_amount = summary["total_amount"],
        fee_summary = summary["fee_summary"],
        gender_summary = summary["gender_summary"],
        household_summary = summary["household_summary"],
        household_count = summary["household_count"],
        event = summary["event"],
        title="参加者一覧・集計",
        back_page_url=url_for(EVENT_DETAIL_ENDPOINT, event_id=event_id),
        back_page_title="イベント詳細"
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
    #saved_member_ids=set()を追加
    return render_template('application/apply_form.html', 
                           event_id=event_id, 
                           event=find_event_by_id(event_id), 
                           members=members, 
                           application=None,preview_by_id=preview_by_id,
                           saved_member_ids=set(),
                           title="イベント申込フォーム",
                           back_page_url=url_for(EVENT_DETAIL_ENDPOINT, event_id=event_id),
                           back_page_title="イベント詳細"
                           )

  
#申し込み内容確認画面
@application_bp.route('/events/<string:event_id>/confirm', methods=["POST"])
@login_required
def apply_confirmation_view(event_id):
    # フォームで選択されたmember_idsを受け取り、まだ保存せず画面表示のみ
    household = get_household_by_user(session['user_id'])
    member_ids = request.form.getlist('member_ids')
    #自分の世帯メンバーか確認、それ以外ならエラー
    if not validate_member_ids(household['id'], member_ids):
        abort(403)
    
    #店員超過のため申し込みできない
    event = find_event_by_id(event_id) 
    if is_capacity_exceeded(event, len(member_ids)):
        flash("定員を超えるため、申し込めません。", "error")
        return redirect(url_for('event.detail_view', event_id=event_id))
        
    #申込画面に表示するデータの取得
    participants = build_participants_preview(event_id, household['id'], member_ids)
    total_amount = sum(p["amount"] for p in participants)
    return render_template(
        'application/apply_confirmation.html', event=event, event_id=event_id, participants=participants, total_amount=total_amount, title="申込内容確認", back_page_url=url_for(EVENT_APPLY_ENDPOINT, event_id=event_id), back_page_title="イベント申込フォーム"
    )
  
#申し込み確定処理
@application_bp.route('/events/<string:event_id>/create', methods=["POST"])
@login_required
def apply_create_process(event_id):
    household = get_household_by_user(session['user_id'])
    event = find_event_by_id(event_id)
    
    if is_deadline_passed(event):
        flash("このイベントの申込期限は終了しています", "error")
        return redirect(url_for('event.detail_view', event_id=event_id))
        
    #すでに同じイベントに同じ世帯の申し込みがないか確認する
    existing_application = find_application_by_event_id_and_household_id(event_id,household['id'])
    if existing_application:
        flash("すでにこのイベントに申し込み済みです", "error")
        return redirect(url_for('event.detail_view', event_id=event_id))
    
    member_ids = request.form.getlist('member_ids')
    
    if is_empty_selection(member_ids):
            flash("参加者を1人以上選択してください", "error")
            return redirect(url_for('event.detail_view', event_id=event_id))
    
    #自分の世帯メンバーか確認、それ以外ならエラー
    if not validate_member_ids(household['id'], member_ids):
        abort(403)
        
    #店員超過のため申し込みできない
    event = find_event_by_id(event_id) 
    if is_capacity_exceeded(event, len(member_ids)):
        flash("定員を超えるため、申し込めません。", "error")
        return redirect(url_for('event.detail_view', event_id=event_id))
        
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
    
    saved_participants = get_application_participants(id)
    preview_by_id = {p['member_id']: p for p in saved_participants}
    saved_member_ids = set(preview_by_id.keys())

    # イベント申込みに追加されていないメンバーは、その場で新規に計算する
    missing_member_ids = [str(m['id']) for m in members if m['id'] not in preview_by_id]
    if missing_member_ids:
        new_preview = build_participants_preview(application['event_id'], household['id'], missing_member_ids)
        for p in new_preview:
            preview_by_id[p['member_id']] = p
    
    return render_template('application/apply_form.html', 
                           event_id=None, 
                           event=find_event_by_id(application['event_id']), 
                           members=members, 
                           application=application,preview_by_id=preview_by_id,
                           saved_member_ids=saved_member_ids,
                           title="イベント申込内容編集",
                           back_page_url=url_for(EVENT_DETAIL_ENDPOINT, event_id=application['event_id']),
                           back_page_title="イベント詳細"
                           )
    

  
#申し込み編集処理
@application_bp.route('/applications/<int:id>/edit', methods=["POST"])
@login_required
@applicant_required
def apply_edit_process(id):
    application = get_application(id)
    household = get_household_by_user(session['user_id'])
    event = find_event_by_id(application['event_id'])
    
    if is_deadline_passed(event):
        flash("このイベントの申込期限は終了しています", "error")
        return redirect(url_for('mypage.mypage_view'))
    
    member_ids = request.form.getlist('member_ids')
    
    #参加者が1人以上いないとエラーを表示
    if is_empty_selection(member_ids):
            flash("参加者を1人以上選択してください", "error")
            return redirect(url_for('mypage.mypage_view'))
    
    if not validate_member_ids(household['id'], member_ids):
        abort(403) 
    
    #更新時に家族をカウントせずにカウントして再度申し込みの定員数を確認
    if is_capacity_exceeded_on_edit(event, id, len(member_ids)):
        flash("定員を超えるため、更新できません。", "error")
        return redirect(url_for('mypage.mypage_view'))
    
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

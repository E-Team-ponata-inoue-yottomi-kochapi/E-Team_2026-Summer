from flask import Blueprint, session, render_template, redirect, url_for, request, abort, flash
from models.event import get_open_events, create_event, create_fee_rule, update_event, delete_fee_rules_by_event
from services.event import get_event_detail, has_overlapping_fee_rules
import pymysql
from util.auth_guard import login_required, host_required
import logging
from services.message import can_access_event_chat
from datetime import datetime, timedelta
from models.household import get_household_by_user
from models.application import list_applications_by_household
from models.application import find_application_by_event_id_and_household_id
from models.application import summarize_applications_by_event

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

    # 申込済みイベントのIDを取得する
    household = get_household_by_user(session['user_id'])
    applied_event_ids = set()
    if household:
        applications = list_applications_by_household(household['id'])
        applied_event_ids = {a['event_id'] for a in applications}

    # バッジをつける処理
    for event in events:
        if event['id'] in applied_event_ids:
            event['badge_status'] = 'sakura'
        elif event['deadline'] and event['deadline'] - datetime.now() <= timedelta(days=3):
            event['badge_status'] = 'dry'
        else:
            event['badge_status'] = 'open'

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

        # ログイン中の世帯が表示中のイベントに参加済みかどうか
        household = get_household_by_user(session['user_id'])
        application = find_application_by_event_id_and_household_id(event_id,household['id'])

        # 定員に対して今何人申し込んでるか？
        participant_count = len(summarize_applications_by_event(event_id))

    except pymysql.MySQLError as e:
        logger.exception('MySQLエラーが発生しました: %s', e)
        abort(500)
    return render_template("event/event_detail.html", title="イベント詳細", event=event, owner=owner, fee_rules=fee_rules, can_chat=can_chat, application=application, participant_count=participant_count)


# イベント作成画面表示
@event_bp.route("/new", methods=["GET"])
@login_required
def new_view():
 
    return render_template("event/event_form.html", event=None, fee_rules=None)


# イベント作成処理
@event_bp.route("/", methods=["POST"])
@login_required
def create_process():
    tier_names=request.form.getlist('tier_name')
    min_ages=request.form.getlist('min_age')
    max_ages=request.form.getlist('max_age')
    genders=request.form.getlist('gender')
    fees=request.form.getlist('fee')

        # 料金区分と年齢の入力チェック
    if any(
        tier_name and (not min_age or not max_age)
        for tier_name, min_age, max_age in zip(tier_names, min_ages, max_ages)
    ):
        flash("料金区分の最小年齢と最大年齢を入力してください", "error")
        return redirect(url_for("event.new_view")) 

    # 料金区分の重複チェック
    if has_overlapping_fee_rules(tier_names, min_ages, max_ages, genders):
        flash("料金区分の年齢範囲が重複しています", "error")
        return redirect(url_for("event.new_view"))

    event_id = create_event(
        owner_id=session['user_id'],
        title=request.form.get('title'),
        start_at=request.form.get('start_at'),
        place=request.form.get('place'),
        address=request.form.get('address'),
        capacity=request.form.get('capacity') or None,
        deadline=request.form.get('deadline') or None,
        description=request.form.get('description'),
        items_to_bring=request.form.get('items_to_bring'),
        schedule=request.form.get('schedule'),
        hold_condition=request.form.get('hold_condition'),
        cancellation_policy=request.form.get('cancellation_policy'),
        emergency_contact=request.form.get('emergency_contact'),
        payment_method=request.form.get('payment_method'),
        payment_deadline=request.form.get('payment_deadline') or None,
        # TODO：ステータスの定数化をする
        status='公開',
    )

    for tier_name, min_age, max_age, gender, fee in zip(tier_names, min_ages, max_ages, genders, fees):
        if not tier_name:
            continue
        create_fee_rule(
            event_id=event_id,
            tier_name=tier_name,
            min_age=min_age,
            max_age=max_age,
            gender=gender or None,
            fee=fee,
        )

    return redirect(url_for("event.detail_view", event_id=event_id))

# イベント編集画面表示
@event_bp.route("/<string:event_id>/edit", methods=["GET"])
@login_required
@host_required
def event_edit_view(event_id):
    result = get_event_detail(event_id)
    if result is None:
        abort(404)
    return render_template("event/event_form.html", event=result["event"],fee_rules=result["fee_rules"])

# イベント編集処理
@event_bp.route("/<string:event_id>/edit", methods=["POST"])
@login_required
@host_required
def event_edit_process(event_id):
    # フォームから料金区分を取得
    tier_names = request.form.getlist('tier_name')
    min_ages = request.form.getlist('min_age')
    max_ages = request.form.getlist('max_age')
    genders = request.form.getlist('gender')
    fees = request.form.getlist('fee')

    # 料金区分と年齢の入力チェック
    if any(
        tier_name and (not min_age or not max_age)
        for tier_name, min_age, max_age in zip(tier_names, min_ages, max_ages)
    ):
        flash("料金区分の最小年齢と最大年齢を入力してください", "error")
        return redirect(url_for("event.event_edit_view", event_id=event_id)) 

    # 料金区分の重複チェック
    if has_overlapping_fee_rules(tier_names, min_ages, max_ages, genders):
        flash("料金区分の年齢範囲が重複しています", "error")
        return redirect(url_for("event.event_edit_view", event_id=event_id))

    # イベント情報を更新
    update_event(
        event_id=event_id,
        title=request.form.get('title'),
        start_at=request.form.get('start_at'),
        place=request.form.get('place'),
        address=request.form.get('address'),
        capacity=request.form.get('capacity') or None,
        deadline=request.form.get('deadline') or None,
        description=request.form.get('description'),
        items_to_bring=request.form.get('items_to_bring'),
        schedule=request.form.get('schedule'),
        hold_condition=request.form.get('hold_condition'),
        cancellation_policy=request.form.get('cancellation_policy'),
        emergency_contact=request.form.get('emergency_contact'),
        payment_method=request.form.get('payment_method'),
        payment_deadline=request.form.get('payment_deadline') or None,
    )

    # 既存の料金区分を削除
    delete_fee_rules_by_event(event_id)

    # 新しい料金区分を登録
    for tier_name, min_age, max_age, gender, fee in zip(tier_names, min_ages, max_ages, genders, fees):
        if not tier_name:
            continue
        create_fee_rule(
            event_id=event_id,
            tier_name=tier_name,
            min_age=min_age,
            max_age=max_age,
            gender=gender or None,
            fee=fee,
        )
    return redirect(url_for("event.detail_view", event_id=event_id))

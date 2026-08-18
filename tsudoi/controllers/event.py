from flask import Blueprint, session, render_template, redirect, url_for, request, abort
from models.event import get_open_events, create_event, create_fee_rule
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
@login_required
def new_view():
 
    return render_template("event/event_form.html")


# イベント作成処理
@event_bp.route("/", methods=["POST"])
@login_required
def create_process():
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
    tier_names=request.form.getlist('tier_name')
    min_ages=request.form.getlist('min_age')
    max_ages=request.form.getlist('max_age')
    genders=request.form.getlist('gender')
    fees=request.form.getlist('fee')

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
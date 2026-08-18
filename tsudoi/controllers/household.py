from flask import Blueprint, session, render_template, redirect, url_for, request
from util.auth_guard import login_required
from models.user import User

from models.household import (
    get_household_by_user,
    get_family_members,
    insert_family_member,
    update_family_member,
    delete_family_member,
)

household_bp = Blueprint("household", __name__, url_prefix="/household")

#家族一覧ページ表示
@household_bp.route('/', methods=["GET"])
@login_required
def household_list_view():
    household = get_household_by_user(session['user_id'])
    members = get_family_members(household['id'])
    has_self = any(m['relation'] == '本人' for m in members)

    user_email = None
    if not has_self:
        user = User.find_user_by_id(session['user_id'])
        user_email = user['email']

    return render_template('household/household_list.html', members=members,has_self=has_self,user_email=user_email)

#家族追加処理→家族一覧表示
@household_bp.route('/member/create', methods=["POST"])
@login_required
def member_create_process():
    household = get_household_by_user(session['user_id'])
    insert_family_member(
        household_id=household['id'],
        relation=request.form.get('relation'),
        name=request.form.get('name'),
        gender=request.form.get('gender'),
        birth_date=request.form.get('birth_date'),
        email=request.form.get('email'),
    )
    return redirect(url_for('household.household_list_view'))

#家族情報編集処理
@household_bp.route('/member/<int:id>/edit', methods=["POST"])
@login_required
def member_edit_process(id):
    update_family_member(
        member_id=id,
        relation=request.form.get('relation'),
        name=request.form.get('name'),
        gender=request.form.get('gender'),
        birth_date=request.form.get('birth_date'),
        email=request.form.get('email'),
    )
    return redirect(url_for('household.household_list_view'))

#メンバー削除処理
@household_bp.route('/member/<int:id>/delete', methods=["POST"])
@login_required
def member_delete_process(id):
    delete_family_member(id)
    return redirect(url_for('household.household_list_view'))

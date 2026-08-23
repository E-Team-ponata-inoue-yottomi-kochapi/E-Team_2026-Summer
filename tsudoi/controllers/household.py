from flask import Blueprint, session, render_template, redirect, url_for, request,flash
from util.auth_guard import login_required, owner_required

from models.user import User

from services.household import is_relation_duplicated,is_self_member,validate_member_input,is_changing_self_relation

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
    relation = request.form.get('relation')
    
    # 必須項目・日付のバリデーション
    errors = validate_member_input(relation, birth_date)
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for('household.household_list_view'))
    
    #本人、妻、夫は1人しか追加できない
    if is_relation_duplicated(household['id'], relation):
        flash(f"「{relation}」はすでに登録されています", "error")
        return redirect(url_for('household.household_list_view'))

    insert_family_member(
        household_id=household['id'],
        relation=request.form.get('relation'),
        name=request.form.get('name'),
        gender=request.form.get('gender') or None,
        birth_date=request.form.get('birth_date'),
        email=request.form.get('email'),
    )
    return redirect(url_for('household.household_list_view'))

#家族情報編集処理
@household_bp.route('/member/<int:id>/edit', methods=["POST"])
@login_required
@owner_required
def member_edit_process(id):
    relation = request.form.get('relation')
    birth_date = request.form.get('birth_date')
    
    errors = validate_member_input(relation,birth_date)
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for('household.household_list_view'))
    
    # 本人の続柄は、他の続柄に変更できないようにする
    if is_changing_self_relation(id, relation):
        flash("本人の続柄は変更できません", "error")
        return redirect(url_for('household.household_list_view'))
    
    update_family_member(
        member_id=id,
        relation=request.form.get('relation'),
        name=request.form.get('name'),
        gender=request.form.get('gender') or None,
        birth_date=request.form.get('birth_date'),
        email=request.form.get('email'),
    )
    return redirect(url_for('household.household_list_view'))

#メンバー削除処理
@household_bp.route('/member/<int:id>/delete', methods=["POST"])
@login_required
@owner_required
def member_delete_process(id):
    if is_self_member(id):
        flash("本人は削除できません", "error")
        return redirect(url_for('household.household_list_view'))
    delete_family_member(id)
    return redirect(url_for('household.household_list_view'))

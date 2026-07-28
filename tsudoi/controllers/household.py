from functools import wraps
from flask import Blueprint, session, render_template, redirect, url_for

household_bp = Blueprint("household", __name__, url_prefix="/household")

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('login_view'))
        return func(*args, **kwargs)
    return wrapper


@household_bp.route('', methods=["GET"])
@login_required
def household_list_view():
    members = [
        {"id": 1, "name": "田中太郎"},
        {"id": 2, "name": "田中花子"},
    ]
    return render_template('household/list.html', members=members)

@household_bp.route('/member/new', methods=["GET"])
@login_required
def member_new_view():
    return render_template('household/form.html', member=None)


@household_bp.route('/member/create', methods=["POST"])
@login_required
def member_create_process():
    return redirect(url_for('household.household_list_view'))


@household_bp.route('/member/<int:id>/edit', methods=["GET"])
@login_required
def member_edit_view(id):
    member = {"id": id, "name": ""}
    return render_template('household/form.html', member=member)


@household_bp.route('/member/<int:id>/edit', methods=["POST"])
@login_required
def member_edit_process(id):
    return redirect(url_for('household.household_list_view'))


@household_bp.route('/member/<int:id>/delete', methods=["POST"])
@login_required
def member_delete_process(id):
    return redirect(url_for('household.household_list_view'))
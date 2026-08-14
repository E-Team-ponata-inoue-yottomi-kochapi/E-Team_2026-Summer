# python標準ライブラリ / Flaskの機能
from functools import wraps
from flask import session, abort, redirect, url_for

# 独自のmodel関数
from models.admin import find_admin_by_id
from models.household import get_household_by_user, get_family_member_by_id
from models.event import find_event_by_id
from models.application import find_application_by_id


# ログイン権限デコレータ(L)
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login_view'))
        return func(*args, **kwargs)
    return wrapper

# adminログイン認証(L/ad)
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('admin_id') is None:
            abort(401)
        admin = find_admin_by_id(session['admin_id'])
        if admin is None:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

# 共通処理
def verify_household_owner(resource):
    if resource is None:
        abort(404)
    my_household = get_household_by_user(session['user_id'])
    if my_household is None or resource['household_id'] != my_household['id']:
        abort(403)

# 世帯主（アカウントオーナー本人）(L/O)
def owner_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        member = get_family_member_by_id(kwargs.get('id'))
        verify_household_owner(member)
        return func(*args, **kwargs)
    return wrapper

# イベント主催者(L/H)
def host_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        event_id = kwargs.get('id') or kwargs.get('event_id')
        event = find_event_by_id(event_id)
        if event is None:
            abort(404)
        if event['owner_id'] != session.get('user_id'):
            abort(403)
        return func(*args, **kwargs)
    return wrapper

# 申し込み者(L/AP)
def applicant_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        application = find_application_by_id(kwargs.get('application_id'))
        verify_household_owner(application)
        return func(*args, **kwargs)
    return wrapper
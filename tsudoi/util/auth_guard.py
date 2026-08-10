# python標準ライブラリ / Flaskの機能
from functools import wraps
from flask import g, session, abort, redirect, url_for

# 独自のmodel関数

# ログイン権限デコレータ
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login_view'))
        return func(*args, **kwargs)
    return wrapper

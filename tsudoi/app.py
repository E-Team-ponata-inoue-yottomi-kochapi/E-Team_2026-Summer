# Flaskクラスのインポート + csrfクラスのインポート
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

# settings.SECRET_KEY＠１８行目に使用
from config import settings

# BluePrintインスタンスのインポート
from controllers.auth import auth_bp
from controllers.household import household_bp
from controllers.event import event_bp
from controllers.application import application_bp
from controllers.mypage import mypage_bp
from controllers.admin import admin_bp

from util.logger import logger_config

# appインスタンス生成　＋　cookie署名用key設定
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

# ログ機能の初期化設定（app.py起動時に1度だけ実行）
logger_config()

# Blueprintの登録
app.register_blueprint(auth_bp)
app.register_blueprint(household_bp)
app.register_blueprint(event_bp)
app.register_blueprint(application_bp)
app.register_blueprint(mypage_bp)
app.register_blueprint(admin_bp) 


# CSRF対策
csrf = CSRFProtect(app)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html", title="500エラー"),500

# このファイルが直接実行される時のみ「ファイルの中身」を実行する。
# このファイルがインポートされたときは「ファイルの中身」は実行されない。
# app.run　Flaskの開発用サーバーを起動
# host="0.0.0.0",#コンテナ外からのアクセス許可
# port=5000,#待機ポート指定
# debug=True)　エラー表示とコード更新時の自動リロード有効化
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

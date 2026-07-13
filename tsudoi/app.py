# ============================================================
# 【チュートリアル用・削除予定】
# ぽんたが、チュートリアルとして仮実装。チュートリアル完了後、
# 削除してから本実装に置き換える。
# このコードの内容と処理を理解し、言語化できるようにすること！
# ============================================================
from flask import Flask

from config import settings
from controllers.auth import auth_bp

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

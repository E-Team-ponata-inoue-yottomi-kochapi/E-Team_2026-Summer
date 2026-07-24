from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import settings
from controllers.auth import auth_bp
from controllers.mypage import mypage_bp

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(mypage_bp)

# CSRF対策
csrf = CSRFProtect(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


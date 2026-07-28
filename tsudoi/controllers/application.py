from flask import Blueprint, render_template
# auth_guard.py実装後に追加
# from util.auth_guard import login_required

application_bp = Blueprint("application", __name__)

# 集計画面
@application_bp.route("/events/<string:event_id>/applications", methods=["GET"])
# auth.guard.py実装後に追加
# @login_required
def summary_view(event_id):
    return render_template("event/summary.html", event_id = event_id)

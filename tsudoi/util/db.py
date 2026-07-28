# ============================================================
# 【チュートリアル用・削除予定】
# ぽんたが、チュートリアルとして仮実装。チュートリアル完了後、
# 削除してから本実装に置き換える。
# このコードの内容と処理を理解し、言語化できるようにすること！
# ============================================================
import pymysql
from config import settings


def get_connection():
    return pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_DATABASE,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

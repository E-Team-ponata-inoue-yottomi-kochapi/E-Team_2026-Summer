import logging
import os
from datetime import datetime

def logger_config():
    # ログの出力名を設定
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # utilまでの絶対パスを取得
    dir_util = os.path.dirname(__file__)
    # tsudoiまでの絶対パスを取得
    dir_tsudoi = os.path.dirname(dir_util)

    # ログの保存先とファイル名のフォーマットを設定
    log_filename = 'logs/app_' + datetime.now().strftime("%Y-%m-%d") + '.log'

    # 第一引数の下流に第二引数が連結される
    dir_path = os.path.join(dir_tsudoi, 'logs')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    FORMAT = '%(asctime)s | [%(filename)s:%(lineno)d] | %(levelname)s | %(message)s'

    log_path = os.path.join(dir_tsudoi, log_filename)

    fl_handler = logging.FileHandler(log_path, encoding="utf-8")
    fl_handler.setLevel(logging.WARNING)
    # FileHandlerによる出力フォーマットを先で定義した'format'に設定
    fl_handler.setFormatter(logging.Formatter(FORMAT))
    root_logger.addHandler(fl_handler)

    st_handler = logging.StreamHandler()
    st_handler.setLevel(logging.DEBUG)
    # StreamHandlerによる出力フォーマットを先で定義した'format'に設定
    st_handler.setFormatter(logging.Formatter(FORMAT))
    root_logger.addHandler(st_handler)
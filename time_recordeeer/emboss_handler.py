from time_recordeeer.freee import freee
import os
import json

def handle(args):
    # 設定ファイルを読み込む
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    with open(os.path.join(config_path, 'config.json')) as f:
        # company_idとemp_idを取得する。
        api = freee(json.load(f))
    # タイムレコーダー登録APIを叩く
    if not api.get_message():
        res = api.register_time_clocks(args.state)
        return res
    return api.get_message()
from time_recordeeer.freee import freee
import os

def handle(args):
    # company_idとemp_idを取得する。
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    api = freee(config_path)
    # タイムレコーダー登録APIを叩く
    res = api.register_time_clocks(args.state)
    return res

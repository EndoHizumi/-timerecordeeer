import requests
import json
import webbrowser
from datetime import date
from typing import Dict


class freee:
    headers = {'Authorization': '', 'accept': 'application/json'}
    company_id = ''
    emp_id = ''

    def __init__(self, path):
        script_path = path
        with open(f'{script_path}/config.json') as f:
            config = json.load(ｆ)
            if config.get('access_token'):
                self.headers['Authorization'] = f'Bearer {config.get("access_token")}'
                emp_info = requests.get("https://api.freee.co.jp/hr/api/v1/users/me", headers=self.headers).json()
                self.company_id = emp_info['companies'][0]['id']
                self.emp_id = emp_info['companies'][0]['employee_id']
            else:
                print('config.jsonにアクセストークンが登録されていません。認証ページにログインしてアクセストークンを取得してください')
                token_url = f"{config['token_url']}?client_id={config['client_id']}&redirect_uri={config['redirect_uri']}&response_type={config['response_type']}"
                webbrowser.open(token_url)
                return

    def register_time_clocks(self, state: str):
        payload: Dict[str, str] = {'company_id': self.company_id, 'type': state, 'emp_id': self.emp_id, 'base_date': date.today().strftime('%Y-%m-%d')}
        responce = requests.post(f"https://api.freee.co.jp/hr/api/v1/employees/{self.emp_id}/time_clocks", headers=self.headers, data=payload)
        if not responce.status_code == 201:
            raise ValueError(responce.json())
        return responce.json()

    def get_available_type(self) -> str:
        attendance_state_map = {'break_begin': 'clockIn', 'break_out': 'breakIn', 'clock_in': 'clockOut'}
        url = f"https://api.freee.co.jp/hr/api/v1/employees/{self.emp_id}/time_clocks/available_types?company_id={self.company_id}"
        responce = requests.get(url, headers=self.headers).json()
        return attendance_state_map[responce['available_types'][0]]

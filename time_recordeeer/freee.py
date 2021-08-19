import requests
import json
import webbrowser
from datetime import date
from typing import Dict

from requests.models import Response


class freee:
    headers = {'Authorization': '', 'accept': 'application/json'}
    company_id = ''
    emp_id = ''
    message = ''
    config = {}

    def __init__(self, config_data: dict):
        config = config_data
        if not config.get('access_token'):
            print('config.jsonにアクセストークンが登録されていません。認証ページにログインして認可コードを取得してください')
            token_url = f'https://accounts.secure.freee.co.jp/public_api/authorize?client_id={config["client_id"]}&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code'
            webbrowser.open(token_url)
            auth_code: str = input('認可コード：')
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            body = {
                'grant_type': 'authorization_code',
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'code': auth_code,
                'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
            }
            res = requests.post(
                'https://accounts.secure.freee.co.jp/public_api/token', headers=self.headers, data=body).json()
            config['access_token'] = res['access_token']
            config['refresh_token'] = res['refresh_token']
        self.headers['Authorization'] = f'Bearer {config.get("access_token")}'
        res = requests.get(
            'https://api.freee.co.jp/hr/api/v1/users/me', headers=self.headers)
        emp_info = res.json()
        if res.status_code == 200:
            self.company_id = emp_info['companies'][0]['id']
            self.emp_id = emp_info['companies'][0]['employee_id']
        else:
             self.message = emp_info.get('message')
        self.config = config

    def register_time_clocks(self, state: str):
        payload: Dict[str, str] = {'company_id': self.company_id, 'type': state,
                                   'emp_id': self.emp_id, 'base_date': date.today().strftime('%Y-%m-%d')}
        responce = requests.post(
            f'https://api.freee.co.jp/hr/api/v1/employees/{self.emp_id}/time_clocks', headers=self.headers, data=payload)
        if not responce.status_code == 201:
            raise ValueError(responce.json())
        return responce.json()

    def get_available_type(self) -> str:
        attendance_state_map = {'break_begin': 'clockIn', 'break_out': 'breakIn', 'clock_in': 'clockOut'}
        url = f'https://api.freee.co.jp/hr/api/v1/employees/{self.emp_id}/time_clocks/available_types?company_id={self.company_id}'
        responce = requests.get(url, headers=self.headers).json()
        return attendance_state_map[responce['available_types'][0]]

    def get_message(self) -> str:
        return self.message

    def get_config(self) -> dict:
        return self.config

"""API Token class for token management"""

from datetime import datetime
import requests


class ApiToken:
    token = None

    def __init__(self, auth_url, *args, **kwargs):
        self.auth_url = auth_url
        self.credentials = kwargs
        self._get_token()

    def _get_token(self):
        url = self.auth_url + 'token/'
        response = requests.post(url=url, data=self.credentials)
        self.token = response.json()

    def needs_refresh(self):
        expires_at = datetime.strptime(
            self.token.get('expires_at'),
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        return expires_at < datetime.now()

    def refresh(self):
        url = self.auth_url + 'token/'
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.credentials.get('client_id'),
            'refresh_token': self.token.get('refresh_token'),
        }
        response = requests.post(url=url, data=data)
        self.token = response.json()
        return response

    def revoke(self):
        url = self.auth_url + 'revoke/'
        data = {
            'client_id': self.credentials.get('client_id'),
            'refresh_token': self.token.get('refresh_token'),
        }
        headers = {'Authorization': f'Bearer {self.token.get("access_token")}'}
        response = requests.post(url=url, data=data, headers=headers)
        return response

    def info(self):
        url = self.auth_url + 'info/'
        data = {
            'client_id': self.credentials.get('client_id'),
            'token': self.token.get('access_token'),
        }
        headers = {'Authorization': f'Bearer {self.token.get("access_token")}'}
        response = requests.post(url=url, data=data, headers=headers)
        return response

    def __str__(self):
        return self.token.get('access_token', None)

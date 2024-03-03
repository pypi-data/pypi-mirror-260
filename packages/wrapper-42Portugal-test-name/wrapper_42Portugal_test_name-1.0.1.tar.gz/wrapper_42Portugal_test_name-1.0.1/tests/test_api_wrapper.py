# tests/test_api_token.py

from unittest import TestCase, mock

from api_wrapper.api_wrapper import ApiWrapper


class TestApiWrapper(TestCase):
    @mock.patch('requests.post')
    def test_api_creation(self, mock_post):
        mock_post.return_value.json.return_value = {
            'access_token': 'test-access-token',
            'refresh_token': 'test-refresh-token',
            'token_type': 'bearer',
            'expires_at': '2000-03-02T17:59:00.340552Z',
            'scope': 'openid',
            'user': 1,
            'application': 'test-app'
        }
        params = {
            'base_url': 'http://localhost:8000/api/',
            'auth_url': 'http://localhost:8000/auth/',
            'client_secret': 'test-client-secret',
            'client_id': 'test-client-id',
            'grant_type': 'client_credentials',
            'scope': 'test-scope'
        }
        api = ApiWrapper(**params)
        base_url = params.pop('base_url')
        auth_url = params.pop('auth_url')
        self.assertEqual(api.base_url, base_url)
        mock_post.assert_called_once_with(
            url=auth_url + 'token/',
            data=params
        )

        self.assertEqual(str(api.token), 'test-access-token')
        self.assertEqual(
            api.token.token.get('refresh_token'),
            'test-refresh-token'
        )
        self.assertTrue(api.token.needs_refresh())

# tests/test_api_token.py

from unittest import TestCase, mock

from api_wrapper.api_token import ApiToken


class TestApiToken(TestCase):
    @mock.patch('requests.post')
    def test_token_creation(self, mock_post):
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
            'auth_url': 'http://localhost:8000/',
            'client_secret': 'test_secret',
            'client_id': 'test_id',
            'grant_type': 'client_credentials',
            'scope': 'test_scope'
        }
        token = ApiToken(**params)
        auth_url = params.pop('auth_url')
        self.assertEqual(token.credentials, params)
        self.assertEqual(token.auth_url, auth_url)
        mock_post.assert_called_once_with(
            url=auth_url + 'token/',
            data=params
        )

        self.assertEqual(str(token), 'test-access-token')
        self.assertEqual(
            token.token.get('refresh_token'),
            'test-refresh-token'
        )
        self.assertTrue(token.needs_refresh())

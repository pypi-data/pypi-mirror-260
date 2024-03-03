import requests

from .api_token import ApiToken


class ApiWrapper:
    token_class = ApiToken

    def __init__(self, base_url, *args, **kwargs):

        self.base_url = base_url
        self.token = ApiToken(**kwargs)
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.token),
        }

    def get_token_class(self):
        assert self.token_class is not None, (
            "'%s' should either be a subclass of ApiToken"
            "or override the 'get_token_class' method"
            % self.__class__.__name__
        )
        return self.token_class

    def req_handler(func):
        def wrapper(self, *args, **kwargs):
            if self.token_needs_refresh():
                self.refresh_token()
            response = func(self, *args, **kwargs)
            return response

        return wrapper

    @req_handler
    def request(self, method, url, data=None):
        endpoint = self.base_url + url
        response = requests.request(
            method=method,
            url=endpoint,
            json=data,
            headers=self.headers,
        )
        return response

    def get(self, url, params={}):
        return self.request('GET', url, data=params)

    def post(self, url, data={}):
        return self.request('POST', url, data=data)

    def patch(self, url, data={}):
        return self.request('PATCH', url, data=data)

    def put(self, url, data={}):
        return self.request('PUT', url, data=data)

    def delete(self, url, data={}):
        return self.request('DELETE', url, data=data)

    def head(self, url):
        return self.request('HEAD', url)

    def options(self, url):
        return self.request('OPTIONS', url)

    @req_handler
    def get_token_info(self):
        return self.token.info()

    @req_handler
    def revoke_token(self):
        return self.token.revoke()

    def refresh_token(self):
        self.token.refresh()
        self.headers['Authorization'] = 'Bearer ' + str(self.token)

    def token_needs_refresh(self):
        return self.token.needs_refresh()

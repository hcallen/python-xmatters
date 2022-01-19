import requests
from requests_oauthlib import OAuth2Session

from session import xMattersSession


class BasicAuth(object):
    def __init__(self, base_url, credentials):
        self.base_resource = base_url
        self._session = requests.Session()
        self._session.auth = credentials

    def session(self):
        return xMattersSession(self)

    def get(self, url):
        return self._session.get(url)


class OAuth(object):
    def __init__(self, base_url=None, client_id=None, credentials=None, refresh_url=None, token=None):
        pass

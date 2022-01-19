import requests
from requests_oauthlib import OAuth2Session

from xmatters.session import xMattersSession


class AuthBase(object):
    def __init__(self, base_url, session):
        if base_url.endswith('/'):
            self.base_url = base_url[:-1]
        else:
            self.base_url = base_url

        self.s = session

    def session(self):
        return xMattersSession(self)

    def get(self, url):
        return self.s.get(url)


class BasicAuth(AuthBase):
    def __init__(self, base_url, credentials):
        self._session = requests.Session()
        self._session.auth = credentials
        super(BasicAuth, self).__init__(base_url, self._session)


class OAuth(object):
    def __init__(self, base_url=None, client_id=None, credentials=None, refresh_url=None, token=None):
        pass

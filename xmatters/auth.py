import requests
from requests_oauthlib import OAuth2Session


class Connection(object):
    def __init__(self, session):
        self._session = session

    def get(self, url):
        return self._session.get(url)


class BasicAuth(Connection):
    def __init__(self, credentials):
        self._session = requests.Session()
        self._session.auth = credentials
        super(BasicAuth, self).__init__(self._session)


class OAuth(Connection):
    def __init__(self, base_url=None, credentials=None, client_id=None, token=None):
        super(OAuth, self).__init__(client_id, )

import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

from .utils import Connection


class BasicAuth(Connection):
    def __init__(self, base_url, credentials):
        self.base_url = base_url
        self.session = requests.Session()
        if credentials and not isinstance(credentials, tuple):
            raise TypeError('credentials must be a tuple of (username, password)')
        self.session.auth = credentials
        super(BasicAuth, self).__init__(self)


class OAuth2(Connection):
    _endpoints = {'token': '/oauth2/token'}

    def __init__(self, base_url, client_id, credentials=None, token=None, token_storage=None):
        if credentials and token:
            raise ValueError('Provide a token or credentials, not both')
        if not credentials and not token and token_storage and token_storage.token is None:
            raise ValueError('Must provide credentials to fetch token')
        if credentials is None and token is None and token_storage is None:
            raise ValueError('You must provide at least one token retrieval method')
        if credentials and not isinstance(credentials, tuple):
            raise TypeError('credentials must be a tuple of (username, password)')
        if token and not isinstance(token, dict):
            raise TypeError('token must be a dict')
        self.base_url = base_url
        self.client_id = client_id
        self.token_storage = token_storage
        self.credentials = credentials
        self.token_updater = self.token_storage.write_token if self.token_storage else None
        self.token_url = '{}{}'.format(self.base_url, self._endpoints.get('token'))
        self.session = self._get_session()
        self.token = token if token else self._get_token()
        self.session.token = self.token

        # update storage token if differs from self.token
        if self.token_storage and token_storage.token != self.token:
            self.token_storage.token = self.token
        super(OAuth2, self).__init__(self)

    def fetch_token(self):
        if self.credentials is None:
            raise ValueError('Must provide credentials in-order to fetch token')
        return self.session.fetch_token(token_url=self.token_url, username=self.credentials[0],
                                        password=self.credentials[1], include_client_id=True, timeout=3)

    def _get_token(self):
        if self.credentials:
            return self.fetch_token()
        elif self.token_storage:
            return self.token_storage.token
        else:
            return None

    def _get_session(self):
        client = LegacyApplicationClient(client_id=self.client_id)
        auto_refresh_kwargs = {'client_id': self.client_id}
        return OAuth2Session(client=client, auto_refresh_url=self.token_url,
                             auto_refresh_kwargs=auto_refresh_kwargs,
                             token_updater=self.token_updater)

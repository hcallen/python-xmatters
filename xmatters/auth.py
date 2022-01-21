import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

from .utils import Connection, TokenStorageBase


class BasicAuth(Connection):
    def __init__(self, base_url, credentials):
        self._session = requests.Session()
        if credentials and not isinstance(credentials, tuple):
            raise TypeError('credentials must be a tuple of (username, password)')
        self._session.auth = credentials
        self.base_url = base_url[:-1] if base_url.endswith('/') else base_url
        super(BasicAuth, self).__init__(self._session)


class OAuth(Connection):
    def __init__(self, base_url, client_id, credentials=None, token=None, token_storage=None):
        self.base_url = base_url[:-1] if base_url.endswith('/') else base_url
        self.token_url = '{base_url}/oauth2/token'.format(base_url=self.base_url)
        self.client_id = client_id
        if token_storage and not isinstance(token_storage, TokenStorageBase):
            raise TypeError('token_storage must be subclassed from TokenStorageBase')
        self.token_storage = token_storage
        if credentials and not isinstance(credentials, tuple):
            raise TypeError('credentials must be a tuple of (username, password)')
        self.credentials = credentials
        if token and not isinstance(token, dict):
            raise TypeError('token must be a dict')

        self.token_updater = self.token_storage.write_token if self.token_storage else None

        client = LegacyApplicationClient(client_id=self.client_id)
        auto_refresh_kwargs = {'client_id': self.client_id}
        self._session = OAuth2Session(client=client, auto_refresh_url=self.token_url,
                                      auto_refresh_kwargs=auto_refresh_kwargs,
                                      token_updater=self.token_updater)

        # determine token
        if credentials:
            self.token = self._session.fetch_token(token_url=self.token_url, username=self.credentials[0],
                                                   password=self.credentials[1], include_client_id=True)
            if self.token_storage:
                self.token_storage.write_token(self.token)
        elif token:
            self.token = token
        elif self.token_storage:
            self.token = self.token_storage.read_token()
        else:
            raise TypeError('Invalid combination of credentials, token and token_storage arguments')

        # assign token to session
        self._session.token = self.token

        super(OAuth, self).__init__(self._session)

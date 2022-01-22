import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from urllib3.util.retry import Retry
from xmatters.common import Error


class Connection(object):
    def __init__(self, parent):
        self._max_retries = None
        self.timeout = None
        self.session = parent.session
        self.base_url = parent.base_url

    def get(self, url, params=None):
        return self.request('GET', url, params)

    def request(self, method, url, params):
        r = self.session.request(method=method, url=url, params=params, timeout=self.timeout)
        if not r.ok:
            raise Exception(
                '{status_code} - {reason} - {url}'.format(status_code=r.status_code, reason=r.reason, url=url))
        data = r.json()
        # if xMatters API error
        if 'code' in data.keys():
            raise Exception(Error(data))
        else:
            return data

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, retries):
        self._max_retries = retries
        retry = Retry(total=retries,
                      backoff_factor=0.1,
                      status_forcelist=[500, 502, 503, 504])
        retry_adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', retry_adapter)


class BasicAuth(Connection):
    def __init__(self, base_url, credentials):
        self.base_url = base_url if not base_url.endswith('/') else base_url[:-1]
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
        self.base_url = base_url if not base_url.endswith('/') else base_url[:-1]
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

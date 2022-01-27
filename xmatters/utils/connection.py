import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from urllib3.util.retry import Retry
from urllib import parse
from typing import Optional
from xmatters.utils.errors import ApiError


class Connection(object):
    def __init__(self):
        self.instance_url = None
        self.api_path = None
        self._max_retries = None
        self.timeout = None
        self.session = None
        self.base_url = None

    def init_session(self, base_url, timeout, max_retries):
        self.base_url = base_url
        p_url = parse.urlparse(self.base_url)
        self.api_path = p_url.path
        self.instance_url = 'https://{}'.format(p_url.netloc)
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, url, params=None):
        return self.request('GET', url, params)

    def request(self, method, url, params):
        r = self.session.request(method=method, url=url, params=params, timeout=self.timeout)
        if not r.ok:
            err_msg = '{status_code} - {reason} - {url}'.format(status_code=r.status_code, reason=r.reason, url=url)
            raise Exception(err_msg)
        data = r.json()
        # if xMatters API error
        if len(data) == 3 and all(k in data.keys() for k in ('code', 'reason', 'message')):
            raise ApiError(data)
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

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class BasicAuthxMSession(Connection):
    def __init__(self, username: str, password: str, *args, **kwargs) -> None:
        super(BasicAuthxMSession, self).__init__()
        self.username = username
        self.password = password

    def init_session(self, base_url, timeout, max_retries):
        self.session.auth = (self.username, self.password)
        self.session = requests.Session()
        super(BasicAuthxMSession, self).init_session(base_url, timeout, max_retries)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OAuth2xMSession(Connection):
    _endpoints = {'token': '/oauth2/token'}

    def __init__(self, client_id: str, username: Optional[str] = None, password: Optional[str] = None,
                 token: Optional[dict] = None, token_storage=None, *args, **kwargs) -> None:
        super(OAuth2xMSession, self).__init__()
        self.token_url = None
        self.client_id = client_id
        self.token_storage = token_storage
        self.username = username
        self.password = password
        self.token = token
        self.token_updater = self.token_storage.write_token if self.token_storage else None

    def init_session(self, base_url, timeout, max_retries):
        self.token_url = '{}{}'.format(base_url, self._endpoints.get('token'))
        self.token = self.token if self.token else self._get_token()
        self.session = self._get_session()
        self.session.token = self.token

        # update storage token if differs from self.token
        if self.token_storage and self.token_storage.read_token() != self.token:
            self.token_storage.write_token(self.token)

        super(OAuth2xMSession, self).init_session(base_url, timeout, max_retries)

    def _fetch_token(self):
        return self.session.fetch_token(token_url=self.token_url, username=self.username,
                                        password=self.password, include_client_id=True, timeout=3)

    def _get_token(self):
        # TODO: account for passing only a refresh token
        if None not in (self.username, self.password):
            return self._fetch_token()
        elif self.token_storage:
            return self.token_storage.read_token()
        else:
            return None

    def _get_session(self):
        client = LegacyApplicationClient(client_id=self.client_id)
        auto_refresh_kwargs = {'client_id': self.client_id}
        return OAuth2Session(client=client, auto_refresh_url=self.token_url,
                             auto_refresh_kwargs=auto_refresh_kwargs,
                             token_updater=self.token_updater)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ApiBridge(object):
    """ Base for api objects who need to make api calls """

    def __init__(self, parent, data=None):
        self.con = parent.con
        self.self_url = None
        self_link = data.get('links', {}).get('self') if data else None
        if self_link:
            self.self_url = '{}{}'.format(self.con.instance_url, self_link)
        else:
            self.self_url = None

    def build_url(self, endpoint: str) -> str:
        if self.con.base_url in endpoint:
            return endpoint
        # if already has api path, use xmatters instance url as prefix
        if endpoint.startswith(self.con.api_path):
            url_prefix = self.con.instance_url
        elif self.self_url:
            url_prefix = self.self_url
        else:
            url_prefix = self.con.base_url
        return '{}{}'.format(url_prefix, endpoint)

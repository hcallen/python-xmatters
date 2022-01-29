from urllib import parse

import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from urllib3.util.retry import Retry

from xmatters.errors import xMattersError, ApiAuthorizationError


class Connection(object):
    def __init__(self):
        self.instance_url = None
        self.api_path = None
        self._max_retries = None
        self.timeout = None
        self.session = None
        self.base_url = None

    def init_session(self, base_url, **kwargs):
        self.base_url = base_url
        p_url = parse.urlparse(self.base_url)
        self.api_path = p_url.path
        self.instance_url = 'https://{}'.format(p_url.netloc)
        self.timeout = kwargs.get('timeout')
        if kwargs.get('max_retries'):
            self.max_retries = kwargs.get('max_retries')

    def get(self, url, params=None):
        return self.request('GET', url, params)

    def request(self, method, url, params):
        r = self.session.request(method=method, url=url, params=params, timeout=self.timeout)
        data = r.json()
        if r.status_code == 401:
            raise ApiAuthorizationError(data)
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


class BasicAuth(Connection):
    def __init__(self, username, password):
        """
        Class used to authentication requests using basic authentication

        :param username: xMatters username
        :type username: str
        :param password: xMatters password
        :type password: str
        """
        super(BasicAuth, self).__init__()
        self.username = username
        self.password = password

    def init_session(self, base_url, **kwargs):
        self.session.auth = (self.username, self.password)
        self.session = requests.Session()
        super(BasicAuth, self).init_session(base_url, **kwargs)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OAuth2Auth(Connection):
    _endpoints = {'token': '/oauth2/token'}

    def __init__(self, client_id, token=None, username=None, password=None, token_storage=None):
        """
        Class used to authentication requests using OAuth2 authentication.

        The method used to obtain a token are used in the following order:  token, username & password, token_storage.

        :param client_id: xMatters instance client id
        :type client_id: str
        :param token: Authentication token. Can be just a refresh token (as a str) or a token object (as a dict)
        :type token: str or dict, optional
         :param username: xMatters username
        :type username: str, optional
        :param password: xMatters password
        :type password: str, optional
        :param token_storage: Class instance used to store token returned during a refresh.
            Any class instance will be accepted as long as it has "read_token" and "write_token" methods.
        :type token_storage: :class:`xmatters.utils.TokenFileStorage`, optional
        """

        super(OAuth2Auth, self).__init__()
        self.client_id = client_id
        self.token_storage = token_storage
        self.username = username
        self.password = password
        self._token = token
        self.session = None

    def init_session(self, base_url, **kwargs):
        token_url = '{}{}'.format(base_url, self._endpoints.get('token'))
        client = LegacyApplicationClient(client_id=self.client_id)
        auto_refresh_kwargs = {'client_id': self.client_id}
        token_updater = self.token_storage.write_token if self.token_storage else None
        self.session = OAuth2Session(client=client, auto_refresh_url=token_url,
                                     auto_refresh_kwargs=auto_refresh_kwargs,
                                     token_updater=token_updater)
        self.session.token = self._get_token()

        # update storage token if differs from self.token
        if self.token_storage and self.token_storage.read_token() != self.token:
            self.token_storage.write_token(self.token)

        super(OAuth2Auth, self).init_session(base_url, **kwargs)

    def _get_token(self):
        if self._token and isinstance(self._token, dict):
            return self._token
        elif self._token and isinstance(self._token, str):
            return self.session.refresh_token(token_url=self.session.auto_refresh_url, refresh_token=self._token,
                                              timeout=3,
                                              kwargs=self.session.auto_refresh_kwargs)
        elif None not in (self.username, self.password):
            return self.session.fetch_token(token_url=self.session.auto_refresh_url, username=self.username,
                                            password=self.password, include_client_id=True, timeout=3)
        elif self.token_storage:
            return self.token_storage.read_token()
        else:
            raise xMattersError('Unable to obtain token with provided arguments')

    @property
    def token(self):
        return self.session.token if self.session else self._token

    @token.setter
    def token(self, token):
        if self.session:
            self.session.token = token
        else:
            self._token = token

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

    def build_url(self, endpoint):
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

import warnings
from urllib import parse

import requests.exceptions
from dateutil import tz, parser
from requests.adapters import HTTPAdapter
from requests_oauthlib.oauth2_session import TokenUpdated
from urllib3.util.retry import Retry

import xmatters.auth
import xmatters.errors as err

# ignore TokenUpdated warning
# only occurs when token_updater isn't defined in OAuth2Session
from xmatters.utils import snake_to_camelcase

warnings.simplefilter('always', TokenUpdated)

TIME_PARAMETERS = ('at', 'from', 'to', 'after', 'before', 'createdFrom', 'createdTo', 'createdBefore', 'createdAfter')


class Connection(object):
    def __init__(self, auth, **kwargs):
        self.auth = auth
        self.api_base_url = self.auth.api_base_url
        p_url = parse.urlparse(self.api_base_url)
        self.api_path = p_url.path
        self.instance_url = 'https://{}'.format(p_url.netloc)
        self.timeout = kwargs.get('timeout', 5)
        self.max_retries = kwargs.get('max_retries', 3)

    def get(self, url, params=None, **kwargs):
        params = self._process_params(params, kwargs)
        return self.request('GET', url=url, params=params)

    def post(self, url, data):
        return self.request('POST', url=url, data=data)

    def delete(self, url):
        return self.request('DELETE', url=url)

    def request(self, method, url, data=None, params=None):
        r = self.auth.session.request(method=method, url=url, params=params, json=data, timeout=self.timeout)

        # token expired in OAuth2 session and not caught by automatic refresh
        if r.status_code == 401 and isinstance(self.auth, xmatters.auth.OAuth2Auth):
            self.auth.refresh_token()
            r = self.auth.session.request(method=method, url=url, params=params, json=data, timeout=self.timeout)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            err.ErrorFactory(r)

        # a resource was not found in response to a DELETE request.
        if r.status_code == 204 and r.request.method == 'DELETE':
            raise err.NoContentError(r)

        return r.json()

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, retries):
        """
        Specifies the maximum number of retries to attempt.

        Retries are attempted for the following status codes:

            * *429* -- Rate limit exceeded
            * *500* -- Internal server error
            * *502* -- Bad gateway
            * *503* -- Service unavailable
            * *504* -- Gateway timeout

        :param retries: maximum number of retries to attempt
        :type retries: int
        :return: None
        :rtype: None
        """
        self._max_retries = retries
        retry = Retry(total=retries,
                      backoff_factor=1,
                      status_forcelist=[429, 500, 502, 503, 504])
        retry_adapter = HTTPAdapter(max_retries=retry)
        self.auth.session.mount('https://', retry_adapter)

    @staticmethod
    def _process_params(params, kwargs):

        params = params if params else {}
        params.update(kwargs)

        # update keys for 'dot' params
        for k in list(params.keys()):
            if '_dot_' in k:
                v = params.pop(k)
                k = k.replace('_dot_', '.')
                params[k] = v
        # convert snakecase keys to camelcase
        for k in list(params.keys()):
            if '_' in k:
                v = params.pop(k)
                k = snake_to_camelcase(k)
                params[k] = v

        # apply utc offset to timestamp parameters
        for k, v in params.items():
            if k in TIME_PARAMETERS:
                params[k] = parser.isoparse(v).astimezone(tz.tzutc()).isoformat()
        return params

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()



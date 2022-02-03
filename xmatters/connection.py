from datetime import datetime
from urllib import parse

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import xmatters.errors as err
import xmatters.utils as util

class Connection(object):
    def __init__(self, base_url, session, **kwargs):
        self.base_url = base_url
        self.session = session
        p_url = parse.urlparse(self.base_url)
        self.api_path = p_url.path
        self.instance_url = 'https://{}'.format(p_url.netloc)
        self.timeout = kwargs.get('timeout')
        if kwargs.get('max_retries'):
            self.max_retries = kwargs.get('max_retries')

    def get(self, url, params=None):
        return self.request('GET', url=url, params=params)

    def post(self, url, data, params=None):
        return self.request('POST', url=url, data=data, params=params)

    def delete(self, url):
        return self.request('DELETE', url=url)

    def request(self, method, url, data=None, params=None):
        if data and params:
            r = self.session.request(method=method, url=url, json=data, params=params, timeout=self.timeout)
        elif params:
            r = self.session.request(method=method, url=url, params=params, timeout=self.timeout)
        elif data:
            r = self.session.request(method=method, url=url, json=data, timeout=self.timeout)
        else:
            r = self.session.request(method=method, url=url, timeout=self.timeout)
        data = r.json()
        if not r.ok or r.status_code == 204:
            raise err.errors_factory(data)
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


class ApiBridge(object):
    """ Base for api objects that need to make requests """

    def __init__(self, parent, data=None):
        if not parent.con:
            raise err.AuthorizationError('authentication not provided')

        self.con = parent.con
        self.self_url = None
        self_link = data.get('links', {}).get('self') if data else None
        self.self_url = '{}{}'.format(self.con.instance_url, self_link) if self_link else None

    def build_url(self, endpoint):
        # don't do anything if endpoint is full path
        if self.con.instance_url in endpoint:
            return endpoint

        if endpoint.startswith(self.con.api_path):
            url_prefix = self.con.instance_url
        elif self.self_url:
            url_prefix = self.self_url
        else:
            url_prefix = self.con.base_url
        return '{}{}'.format(url_prefix, endpoint)

    @staticmethod
    def build_params(arg_params, params=None):
        params = params if params else {}
        for k, v in arg_params.items():
            if v and k not in params.keys():
                if isinstance(v, datetime):
                    params[k] = v.isoformat()
                elif isinstance(v, util.TimeAttribute) and v.datetime().tzname() is None:
                    params[k] = v.local_datetime().isoformat()
                else:
                    params[k] = v
        return params

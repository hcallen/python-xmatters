import json

from requests.adapters import HTTPAdapter

API_MAX_LIMIT = 1000


class Error(object):
    """ xMatters Error common object"""

    def __init__(self, data):
        self.code = data.get('code')
        self.reason = data.get('reason')
        self.message = data.get('message')

    def __repr__(self):
        return '<Error {code} - {reason} - {message}>'.format(code=self.code, reason=self.reason, message=self.message)

    def __str__(self):
        return self.__repr__()


class ApiComponent(object):
    def __init__(self, parent, data=None):
        self.base_url = parent.base_url if not parent.base_url.endswith('/') else parent.base_url[:-1]
        if data and 'links' in data.keys():
            self_link = data.get('links').get('self').replace('/api/xm/1', '')
            self.base_resource = '{}{}'.format(parent.base_url, self_link)
        else:
            self.base_resource = self.base_url

        self.con = parent.con if hasattr(parent, 'con') else None
        self.timeout = parent.timeout if hasattr(parent, 'timeout') else None
        self.retries = parent.retries if hasattr(parent, 'retries') else None
        if self.con and hasattr(parent, 'retries'):
            # apply max retries and set timeout
            retry_adapter = HTTPAdapter(max_retries=self.retries)
            self.con.session.mount('https://', retry_adapter)

    def build_url(self, endpoint):
        return '{base_resource}{endpoint}'.format(base_resource=self.base_resource, endpoint=endpoint)


class Connection(ApiComponent):
    def __init__(self, parent):
        super(Connection, self).__init__(parent)
        self.session = None

    def get(self, url, params):
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


class TokenFileStorage(object):
    def __init__(self, token_file_path):
        self.file_path = token_file_path

    def read_token(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def write_token(self, token):
        with open(self.file_path, 'w') as f:
            json.dump(token, f, indent=4)

    @property
    def token(self):
        return self.read_token()

    @token.setter
    def token(self, token):
        self.write_token(token)

    def __repr__(self):
        return '<TokenFileStorage - {}>'.format(self.file_path)

    def __str__(self):
        return self.__repr__()


class Pagination(ApiComponent):
    def __init__(self, parent, data, constructor, limit):
        super(Pagination, self).__init__(parent)

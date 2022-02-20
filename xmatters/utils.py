import json
import pathlib

from xmatters import errors as err


def snake_to_camelcase(s):
    parts = s.split('_')
    return parts[0].lower() + ''.join(part.title() for part in parts[1:])


def camel_to_snakecase(s):
    return s[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in s[1:]]).lstrip('_')


class TokenFileStorage(object):
    """
    Used to store session token in a file.

    :param token_filepath: filepath to store token in
    :type token_filepath: str or :class:`pathlib.Path`
    """

    def __init__(self, token_filepath):
        if not isinstance(token_filepath, pathlib.Path):
            self.token_filepath = pathlib.Path(token_filepath)

    def read_token(self):
        """ Read token from file """
        if not self.token_filepath.is_file():
            return None
        else:
            with open(self.token_filepath, 'r') as f:
                return json.load(f)

    def write_token(self, token):
        """
        Write token to file

        :param token: token object
        :type token: dict
        """
        with open(self.token_filepath, 'w') as f:
            json.dump(token, f, indent=4)

    @property
    def token(self):
        return self.read_token()

    @token.setter
    def token(self, token):
        self.write_token(token)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ApiBase(object):
    """ Base for api objects """

    def __init__(self, parent, data=None, endpoint=None):
        # parent passed without a connection
        if not hasattr(parent, '_con') or not getattr(parent, '_con'):
            raise err.AuthorizationError('authentication not provided')

        self._con = getattr(parent, '_con')
        self._api_data = data

        if data:
            self_link = data.get('links', {}).get('self')
            self._base_resource = '{}{}'.format(self._con.instance_url, self_link) if self_link else None
        elif endpoint:
            self._base_resource = '{}{}'.format(self._con.api_base_url, endpoint)
        else:
            self._base_resource = self._con.api_base_url

    def _get_url(self, endpoint=None):
        if not endpoint:
            return self._base_resource

        # don't do anything if endpoint is full path
        if endpoint and endpoint.startswith(self._con.instance_url):
            return endpoint

        # if not a query parameter (starts with '?') and missing prepended '/', prepend '/'
        endpoint = '/' + endpoint if (not endpoint.startswith('/') and not endpoint.startswith('?')) else endpoint

        if endpoint.startswith(self._con.api_path):
            url_prefix = self._con.instance_url
        elif self._base_resource:
            url_prefix = self._base_resource
        else:
            url_prefix = self._con.api_base_url
        return '{}{}'.format(url_prefix, endpoint)
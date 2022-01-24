import json
import os.path
import pathlib
from typing import Optional


class ApiBridge(object):
    """ Base for api objects who need to make api calls """

    def __init__(self, parent, data=None):
        self.con = parent.con  # pass connection from parent
        self.resource_url = None
        self.resources = None
        self_link = self._get_self_link(data)
        self._set_resource_url(self_link)
        self._set_resources(self_link)

    def build_url(self, endpoint: str) -> str:
        # if endpoint already contains base url, don't do anything
        if self.con.base_url in endpoint:
            return endpoint
        # if self link, use xmatters instance url as prefix
        if endpoint.startswith(self.con.api_prefix):
            prefix = self.con.xm_url
        # use resource url as prefix
        else:
            prefix = self.resource_url
        return '{}{}'.format(prefix, endpoint)

    def _set_resource_url(self, self_link: Optional[str]) -> None:
        if self_link:
            self.resource_url = '{}{}'.format(self.con.xm_url, self_link)
        else:
            self.resource_url = self.con.base_url

    def _set_resources(self, self_link: Optional[str]) -> None:
        resource_endpoint = self.resource_url.replace(self.con.base_url, '')
        if resource_endpoint:
            self.resources = resource_endpoint.split('/')[1::2]
        else:
            self.resources = None

    @staticmethod
    def _get_self_link(data):
        if data and 'links' in data.keys():
            self_link = data.get('links').get('self')
            self_link = self_link[:-1] if self_link.endswith('/') else self_link
            return self_link
        else:
            return None

    def _remove_api_prefix(self, url: str) -> str:
        """
        Remove api prefix ('/api/xm/1') from url.
        :param url: resource endpoint
        :return: url w/o api prefix prepended
        """
        return url if self.con.api_prefix not in url else url.replace(self.con.api_prefix, '')


class TokenFileStorage(object):
    def __init__(self, token_path, token_filename):
        if not isinstance(token_path, pathlib.Path):
            token_path = pathlib.Path(token_path) if token_path else pathlib.Path()

        if token_path.is_file():
            self.token_path = token_path
        else:
            token_filename = token_filename
            self.token_path = token_path / token_filename

    def read_token(self):

        if not self.token_path.is_file():
            return None
        else:
            with open(self.token_path, 'r') as f:
                return json.load(f)

    def write_token(self, token):
        with open(self.token_path, 'w') as f:
            json.dump(token, f, indent=4)

    @property
    def token(self):
        return self.read_token()

    @token.setter
    def token(self, token):
        self.write_token(token)

    def __repr__(self):
        return '<TokenFileStorage - {}>'.format(self.token_path)

    def __str__(self):
        return self.__repr__()

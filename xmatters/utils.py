import json
from abc import ABC, abstractmethod


class ApiComponent(object):
    def __init__(self, parent, data=None):
        self.base_url = parent.base_url

        if data and 'links' in data.keys():
            self_link = data.get('links').get('self').replace('/api/xm/1', '')
            self.base_resource = '{}{}'.format(parent.base_url, self_link)
        else:
            self.base_resource = parent.base_url

        self.con = parent.con if hasattr(parent, 'con') else parent

    def build_url(self, endpoint):
        return '{}{}'.format(self.base_resource, endpoint)


class Connection(object):
    def __init__(self, session):
        self._session = session

    def get(self, url):
        r = self._session.get(url)
        return r.json()


class TokenStorageBase(ABC):

    @abstractmethod
    def read_token(self):
        pass

    @abstractmethod
    def write_token(self, token):
        pass


class TokenFileStorage(TokenStorageBase):
    def __init__(self, token_file_path):
        self.file_path = token_file_path

    def read_token(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write_token(self, token):
        with open(self.file_path, 'w') as f:
            json.dump(token, f, indent=4)

    def __repr__(self):
        return '<TokenFileStorage - {}>'.format(self.file_path)

    def __str__(self):
        return self.__repr__()

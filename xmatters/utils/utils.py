import json


class ApiComponent(object):
    def __init__(self, parent, data=None):
        self.con = parent.con
        if data and 'links' in data.keys():
            self_link = self._remove_api_prefix(data.get('links').get('self'))
            self.base_resource = '{}{}'.format(self.con.base_url, self_link)
        else:
            self.base_resource = self.con.base_url

    def build_url(self, endpoint):
        endpoint = self._remove_api_prefix(endpoint)
        return '{base_resource}{endpoint}'.format(base_resource=self.base_resource, endpoint=endpoint)

    def _remove_api_prefix(self, endpoint):
        return endpoint if not endpoint.startswith(self.con.api_prefix) else endpoint.replace(self.con.api_prefix, '')


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

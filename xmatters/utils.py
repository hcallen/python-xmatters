import json
import pathlib


def snake_to_camelcase(s):
    return s[0].lower() + ''.join(part.title() for part in s.split('_')[1:])


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



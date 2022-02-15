import json
import pathlib

from dateutil import tz, parser

import xmatters.connection
import xmatters.factories
from xmatters.objects.common import PaginationLinks


class TimeAttribute(str):
    def local(self):
        return parser.isoparse(self).astimezone(tz.tzlocal()).isoformat()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self)


class TokenFileStorage(object):
    def __init__(self, token_filepath):
        if not isinstance(token_filepath, pathlib.Path):
            self.token_filepath = pathlib.Path(token_filepath)

    def read_token(self):
        if not self.token_filepath.is_file():
            return None
        else:
            with open(self.token_filepath, 'r') as f:
                return json.load(f)

    def write_token(self, token):
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


class Pagination(xmatters.connection.ApiBridge):
    """
    Iterator to handle returned pagination objects from the xMatters API.

    :param parent: class that initialized Pagination
    :type parent: subclass of :class:`xmatters.connection.ApiBridge`
    :param data: request return data
    :type data: request return data
    :param constructor: class used to process request data into representation of an API object.
    :type constructor: class
    """
    def __init__(self, parent, data, constructor):

        super(Pagination, self).__init__(parent, data)
        self.parent = parent
        self.constructor = constructor
        self.state = 0  # count of items iterated
        self.total = None
        self._init_data = data

        # properties change every page
        self.count = None
        self.data = None
        self.links = None
        self.index = None
        self._set_pagination_properties(data)

    def goto_next_page(self):
        url = self.get_url(self.links.next)
        data = self.con.get(url, params=None)
        self._set_pagination_properties(data)

    def _set_pagination_properties(self, data):
        self.count = data.get('count')
        self.data = data.get('data')
        links = data.get('links')
        self.links = PaginationLinks(links) if links else None
        self.total = data.get('total')
        self.index = 0

    def _get_object(self, item_data):
        if issubclass(self.constructor, xmatters.factories.Factory):
            data_object = self.constructor.compose(self, item_data)
        elif issubclass(self.constructor, xmatters.connection.ApiBridge):
            data_object = self.constructor(self, item_data)
        else:
            data_object = self.constructor(item_data)
        return data_object

    def __iter__(self):
        return self

    def __next__(self):

        if self.state == self.total:
            raise StopIteration()

        if self.index == self.count and self.links and self.links.next:
            self.goto_next_page()

        if self.index < self.count:
            item_data = self.data[self.index]
            self.index += 1
            self.state += 1
            return self._get_object(item_data)

    def __len__(self):
        return self.total

    def __repr__(self):
        return '<{} {} {} objects>'.format(self.__class__.__name__, self.total, self.constructor.__name__)

    def __str__(self):
        return self.__repr__()
from dateutil import parser, tz

import xmatters.utils


class TimeAttribute(str):
    def local(self):
        """
        Get timestamp adjusted to your local timezone.

        :return: ISO-8601 formatted timestamp
        :rtype: str
        """
        return parser.isoparse(self).astimezone(tz.tzlocal()).isoformat()

    def local_dt(self):
        """
        Get datetime object adjusted to your local timezone.

        :return: datetime object adjusted to your local timezone
        :rtype: :class:`datetime.datetime`
        """
        return parser.isoparse(self).astimezone(tz.tzlocal())

    def datetime(self):
        """
        Get datetime object.

        :return: datetime object
        :rtype: :class:`datetime.datetime`
        """
        return parser.isoparse(self)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self)


class Pagination(xmatters.utils.ApiBase):
    """
    Iterator to handle returned pagination objects from the xMatters API.

    :param parent: class that initialized Pagination
    :type parent: subclass of :class:`xmatters.connection.ApiBridge`
    :param data: request data
    :type data: dict
    :param constructor: class used to process request data into representation of an API object.
    :type constructor: class
    """

    def __init__(self, parent, data, constructor):
        super(Pagination, self).__init__(parent, data)

        self.constructor = constructor

        self.state = 0  #: :vartype: int
        """ Count of total objects iterated """

        self.total = None  #: :vartype: int
        """ Count of total objects within pagination """

        self.count = None  #: :vartype: int
        """ Count of total objects in page """

        self.links = None

        self.index = None  #: :vartype: int
        """ Count of objects iterated from current page """

        self._set_pagination_properties(data)

    def _goto_next_page(self):
        url = self._get_url(self.links.next)
        data = self._con.get(url, params=None)
        self._set_pagination_properties(data)

    def _set_pagination_properties(self, data):
        self.count = data.get('count')
        self.data = data.get('data')
        links = data.get('links')
        self.links = PaginationLinks(self, links) if links else None
        self.total = data.get('total')
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.state == self.total:
            raise StopIteration()

        if self.index == self.count and self.links and self.links.next:
            self._goto_next_page()

        if self.index < self.count:
            item_data = self.data[self.index]
            self.index += 1
            self.state += 1
            return self.constructor(self, item_data)

    def __len__(self):
        return self.total

    def __repr__(self):
        return '<{} {} {} objects>'.format(self.__class__.__name__, self.total, self.constructor.__name__)

    def __str__(self):
        return self.__repr__()


class PaginationLinks(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(PaginationLinks, self).__init__(parent, data)
        self.next = data.get('next')    #: :vartype: str
        self.previous = data.get('previous')   #: :vartype: str
        self.self = data.get('self')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
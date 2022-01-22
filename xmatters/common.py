from xmatters.utils import ApiComponent


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


class PaginationLinks(object):
    def __init__(self, data):
        self.next = data.get('next')
        self.previous = data.get('previous')
        self.self = data.get('self')


class Pagination(object):
    def __init__(self, parent, data, constructor):
        self.parent = parent
        self.constructor = constructor

        # properties reset every page
        self.count = None
        self.data = None
        self.links = None
        self.total = None
        self.index = None
        self._set_pagination_properties(data)

    def _set_pagination_properties(self, data):
        self.count = data.get('count')
        self.data = data.get('data')
        self.links = PaginationLinks(data.get('links'))
        self.total = data.get('total')
        self.index = 0

    def goto_next_page(self):
        data = self.parent.con.get(self.parent.build_url(self.links.next.replace('/api/xm/1', '')))
        self._set_pagination_properties(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.count and self.links.next:
            self.goto_next_page()
        if self.index < self.count:
            data_object = self.constructor(self.parent, self.data[self.index])
            self.index += 1
            return data_object
        else:
            raise StopIteration()

    def __len__(self):
        return self.total

    def __repr__(self):
        return '<Pagination {} {} objects>'.format(self.total, self.constructor.__name__)

    def __str__(self):
        return self.__repr__()


class Recipient(ApiComponent):
    def __init__(self, parent, data):
        super(Recipient, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.external_key = data.get('externalKey')
        self.externally_owned = data.get('externallyOwned')
        self.locked = data.get('locked')
        self.status = data.get('status')
        self.links = SelfLink(data.get('links'))

    def __repr__(self):
        return '<Recipient {}>'.format(self.recipient_type)

    def __str__(self):
        return self.__repr__()


class ReferenceById(object):
    def __init__(self, data):
        self.id = data.get('id')


class ReferenceByIdAndSelfLink(ApiComponent):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')
        self.links = SelfLink(data.get('links', {}))


class SelfLink(object):
    def __init__(self, data):
        self.self = data.get('self')

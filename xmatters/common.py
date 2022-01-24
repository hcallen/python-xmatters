import inspect
from xmatters.utils.utils import ApiBridge


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

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Pagination(ApiBridge):
    def __init__(self, parent, data, cons, cons_identifier=None):
        super(Pagination, self).__init__(parent, data)
        self.parent = parent
        self.cons = cons
        self.cons_identifier = cons_identifier
        self.num_parameters = len(inspect.signature(self.cons).parameters)
        self.state = 0  # count of items iterated

        # properties reset every page
        self.count = None
        self.data = None
        self.links = None
        self.total = None
        self.index = None
        self._set_pagination_properties(data)

    def goto_next_page(self):
        url = self.build_url(self.links.next)
        data = self.con.get(url)
        self._set_pagination_properties(data)

    def _set_pagination_properties(self, data):
        self.count = data.get('count')
        self.data = data.get('data')
        links = data.get('links')
        self.links = PaginationLinks(links) if links else None
        self.total = data.get('total')
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.state == self.total:
            raise StopIteration()

        if self.index == self.count and self.links and self.links.next:
            self.goto_next_page()

        if self.index < self.count:
            item_data = self.data[self.index]

            if self.num_parameters == 3:
                object_type = item_data.get(self.cons_identifier)
                data_object = self.cons(self.parent, item_data, object_type)
            elif self.num_parameters == 2:
                data_object = self.cons(self.parent, item_data)
            else:
                data_object = self.cons(item_data)

            self.index += 1
            self.state += 1
            return data_object

    def __len__(self):
        return self.total

    def __repr__(self):
        return '<{} {} {} objects>'.format(self.__class__.__name__, self.total, self.cons.__name__)

    def __str__(self):
        return self.__repr__()


class Recipient(ApiBridge):
    def __init__(self, parent, data):
        super(Recipient, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.external_key = data.get('externalKey')
        self.externally_owned = data.get('externallyOwned')
        self.locked = data.get('locked')
        self.status = data.get('status')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class RecipientReference(ApiBridge):
    def __init__(self, parent, data):
        super(RecipientReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class SelfLink(ApiBridge):
    def __init__(self, parent, data):
        super(SelfLink, self).__init__(parent, data)
        self.self = data.get('self')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientPointer(ApiBridge):
    def __init__(self, parent, data):
        super(RecipientPointer, self).__init__(parent, data)
        self.id = data.get('id')
        self.recipient_type = data.get('recipient')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceById(object):
    def __init__(self, data):
        self.id = data.get('id')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndSelfLink(ApiBridge):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()



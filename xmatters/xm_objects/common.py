import inspect
import xmatters.connection


class PaginationLinks(object):
    def __init__(self, data):
        self.next = data.get('next')
        self.previous = data.get('previous')
        self.self = data.get('self')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Pagination(xmatters.connection.ApiBridge):
    def __init__(self, parent, data, cons, cons_identifier=None):
        super(Pagination, self).__init__(parent, data)
        self.parent = parent
        self.cons = cons
        self.cons_identifier = cons_identifier
        self._params_count = len(inspect.signature(self.cons).parameters)
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

    def _get_object(self, data):
        if self._params_count == 3:
            object_type = data.get(self.cons_identifier)
            data_object = self.cons(self, data, object_type)
        elif self._params_count == 2:
            data_object = self.cons(self, data)
        else:
            data_object = self.cons(data)
        return data_object

    def _reset(self):
        self.state = 0
        self._set_pagination_properties(self._init_data)

    def __iter__(self):
        return self

    def __next__(self):

        if self.state == self.total:
            self._reset()
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
        return '<{} {} {} objects>'.format(self.__class__.__name__, self.total, self.cons.__name__)

    def __str__(self):
        return self.__repr__()


class Recipient(xmatters.connection.ApiBridge):
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


class RecipientReference(xmatters.connection.ApiBridge):
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


class SelfLink(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(SelfLink, self).__init__(parent, data)
        self.self = data.get('self')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientPointer(xmatters.connection.ApiBridge):
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


class ReferenceByIdAndSelfLink(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PropertyDefinition(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.help_text = data.get('helpText')
        self.default = data.get('default')
        self.max_length = data.get('maxLength')
        self.min_length = data.get('minLength')
        self.pattern = data.get('pattern')
        self.validate = data.get('validate')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class RequestReference(object):
    def __init__(self, data):
        self.request_id = data.get('requestId')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
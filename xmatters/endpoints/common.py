import inspect
import re
from xmatters.connection import ApiBridge


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
        self.params_count = len(inspect.signature(self.cons).parameters)
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
        if self.params_count == 3:
            object_type = data.get(self.cons_identifier)
            data_object = self.cons(self, data, object_type)
        elif self.params_count == 2:
            data_object = self.cons(self, data)
        else:
            data_object = self.cons(data)
        return data_object

    def _reset(self):
        self.state = 0
        self._set_pagination_properties(self._init_data)

    def _check_index(self, index):
        adj_index = index if index >= 0 else index + self.total
        if adj_index < 0 or adj_index >= self.total:
            raise IndexError('index out of range, index={} pagination length={}'.format(index, self.total))

    def _get_item_by_index(self, index):
        url = self.build_url(self.links.self)
        url = re.sub('^(.*offset=)[0-9]+(.*limit=)[0-9]+(.*)$', '\g<1>{}\g<2>{}\g<3>'.format(index, 1), url)

        data = self.con.get(url).get('data')[0]
        return self._get_object(data)

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

    def __getitem__(self, key):
        if isinstance(key, int):
            self._check_index(key)
            key = key if key >= 0 else key + self.total
            return self._get_item_by_index(key)
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step

            # set default values if None
            start = start if start else 0
            stop = stop if stop else self.total
            step = step if step else 1

            # ensure indexes are within range
            [self._check_index(k) for k in (start, (stop - 1))]

            # offset with total if either start or stop are negative
            index = start if start >= 0 else start + self.total
            stop = stop if stop >= 0 else stop + self.total

            # check step
            if step == 0:
                raise ValueError('slice step cannot be zero')
            # if step negative
            index = (index + self.total - 1) if step < 0 else index
            stop = (stop + self.total + 1) if step < 0 else stop

            items = []
            while index > stop and index >= 0:
                items.append(self._get_item_by_index(index))
                index += step
            return items

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

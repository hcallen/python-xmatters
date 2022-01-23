import xmatters.constructors
from xmatters.utils.utils import ApiComponent


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

    def goto_next_page(self):
        url = self.parent.build_url(self.links.next)
        data = self.parent.con.get(url)
        self._set_pagination_properties(data)

    def _set_pagination_properties(self, data):
        self.count = data.get('count')
        self.data = data.get('data')
        links = data.get('links')
        self.links = PaginationLinks(links) if links else None
        self.total = data.get('total')
        self.index = 0
        self.state = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.state == self.total:
            raise StopIteration()

        if self.index == self.count and self.links and self.links.next:
            self.goto_next_page()

        if self.index < self.count:
            if issubclass(self.constructor, ApiComponent):
                data_object = self.constructor(self.parent, self.data[self.index])
            else:
                data_object = self.constructor(self.data[self.index])
            self.index += 1
            self.state += 1
            return data_object

    def __len__(self):
        return self.total

    def __repr__(self):
        return '<{} {} {} objects>'.format(self.__class__.__name__, self.total, self.constructor.__name__)

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
        links = data.get('links')
        self.links = SelfLink(links) if links else None

    def get_self(self):
        data = self.con.get(self.base_resource)
        return xmatters.constructors.recipient_factory(self, self.recipient_type, data) if data else None

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class RecipientReference(ApiComponent):
    def __init__(self, parent, data):
        super(RecipientReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(links) if links else None

    def get_self(self):
        data = self.con.get(self.base_resource)
        return xmatters.constructors.recipient_factory(self, self.recipient_type, data) if data else None

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class SelfLink(object):
    def __init__(self, data):
        self.self = data.get('self')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientPointer(ApiComponent):
    def __init__(self, parent, data):
        super(RecipientPointer, self).__init__(parent, data)
        self.id = data.get('id')
        self.recipient_type = data.get('recipient')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceById(ApiComponent):
    def __init__(self, parent, data):
        super(ReferenceById, self).__init__(parent, data)
        self.id = data.get('id')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndRecipientType(ReferenceById):
    def __init__(self, parent, data):
        super(ReferenceByIdAndRecipientType, self).__init__(parent, data)
        self.recipientType = data.get('recipientType')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndSelfLink(ReferenceById):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')
        links = data.get('links')
        self.links = SelfLink(links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndName(ReferenceById):
    def __init__(self, parent, data):
        super(ReferenceByIdAndName, self).__init__(parent, data)
        self.name = data.get('name')

    def __repr__(self):
        return '<{} >'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndTargetName(ReferenceById):
    def __init__(self, parent, data):
        super(ReferenceByIdAndTargetName, self).__init__(parent, data)
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')

    def __repr__(self):
        return '<{} >'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()

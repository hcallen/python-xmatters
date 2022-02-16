import xmatters.connection
import xmatters.utils


class PaginationLinks(object):
    def __init__(self, data):
        self.next = data.get('next')    #: :vartype: str
        self.previous = data.get('previous')   #: :vartype: str
        self.self = data.get('self')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Recipient(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(Recipient, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.target_name = data.get('targetName')   #: :vartype: str
        self.recipient_type = data.get('recipientType')   #: :vartype: str
        self.external_key = data.get('externalKey')   #: :vartype: str
        self.externally_owned = data.get('externallyOwned')   #: :vartype: bool
        self.locked = data.get('locked')    #: :vartype: bool
        self.status = data.get('status')    #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class RecipientReference(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(RecipientReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.target_name = data.get('targetName')   #: :vartype: str
        self.recipient_type = data.get('recipientType')   #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class SelfLink(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(SelfLink, self).__init__(parent, data)
        self.self = data.get('self')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientPointer(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(RecipientPointer, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.recipient_type = data.get('recipient')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceById(object):
    def __init__(self, data):
        self.id = data.get('id')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndSelfLink(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        links = data.get('links')  #:
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PropertyDefinition(object):
    def __init__(self, data):
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')    #: :vartype: str
        self.description = data.get('description')   #: :vartype: str
        self.help_text = data.get('helpText')   #: :vartype: str
        self.default = data.get('default')    #: :vartype: str
        self.max_length = data.get('maxLength')   #: :vartype: int
        self.min_length = data.get('minLength')   #: :vartype: int
        self.pattern = data.get('pattern')    #: :vartype: str
        self.validate = data.get('validate')   #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class RequestReference(object):
    def __init__(self, data):
        self.request_id = data.get('requestId')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class QuotaItem(object):
    def __init__(self, data):
        self.total = data.get('total')    #: :vartype: int
        self.active = data.get('active')    #: :vartype: int
        self.unused = data.get('unused')   #: :vartype: int

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

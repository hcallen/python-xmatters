import xmatters.connection
import xmatters.utils


class PaginationLinks(object):
    def __init__(self, data):
        self.next = data.get('next')    #:
        self.previous = data.get('previous')    #:
        self.self = data.get('self')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Recipient(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(Recipient, self).__init__(parent, data)
        self.id = data.get('id')    #:
        self.target_name = data.get('targetName')    #:
        self.recipient_type = data.get('recipientType')    #:
        self.external_key = data.get('externalKey')    #:
        self.externally_owned = data.get('externallyOwned')    #:
        self.locked = data.get('locked')    #:
        self.status = data.get('status')    #:
        links = data.get('links')  #:
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class RecipientReference(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(RecipientReference, self).__init__(parent, data)
        self.id = data.get('id')    #:
        self.target_name = data.get('targetName')    #:
        self.recipient_type = data.get('recipientType')    #:
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class SelfLink(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(SelfLink, self).__init__(parent, data)
        self.self = data.get('self')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientPointer(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(RecipientPointer, self).__init__(parent, data)
        self.id = data.get('id')    #:
        self.recipient_type = data.get('recipient')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceById(object):
    def __init__(self, data):
        self.id = data.get('id')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndSelfLink(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')    #:
        links = data.get('links')  #:
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PropertyDefinition(object):
    def __init__(self, data):
        self.id = data.get('id')    #:
        self.name = data.get('name')    #:
        self.description = data.get('description')    #:
        self.help_text = data.get('helpText')    #:
        self.default = data.get('default')    #:
        self.max_length = data.get('maxLength')    #:
        self.min_length = data.get('minLength')    #:
        self.pattern = data.get('pattern')    #:
        self.validate = data.get('validate')    #:

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
        self.total = data.get('total')    #:
        self.active = data.get('active')    #:
        self.unused = data.get('unused')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

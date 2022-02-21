import xmatters.connection
import xmatters.objects
import xmatters.utils
import xmatters.objects.events


class Recipient(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(Recipient, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.target_name = data.get('targetName')  #: :vartype: str
        self.recipient_type = data.get('recipientType')  #: :vartype: str
        self.external_key = data.get('externalKey')  #: :vartype: str
        self.externally_owned = data.get('externallyOwned')  #: :vartype: bool
        self.locked = data.get('locked')  #: :vartype: bool
        self.status = data.get('status')  #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.targeted = data.get('targeted')  #: :vartype: bool
        self.delivery_status = data.get('deliveryStatus')  #: :vartype: str
        response = data.get('response')
        self.response = xmatters.objects.events.UserDeliveryResponse(self, response) if response else None  #: :vartype: :class:`~xmatters.objects.events.UserDeliveryResponse`

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class RecipientReference(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(RecipientReference, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.target_name = data.get('targetName')  #: :vartype: str
        self.recipient_type = data.get('recipientType')  #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.recipient_type, self.target_name)

    def __str__(self):
        return self.__repr__()


class SelfLink(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(SelfLink, self).__init__(parent, data)
        self.self = data.get('self')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientPointer(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(RecipientPointer, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.recipient_type = data.get('recipient')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceById(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(ReferenceById, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByIdAndSelfLink(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PropertyDefinition(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(PropertyDefinition, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str
        self.description = data.get('description')  #: :vartype: str
        self.help_text = data.get('helpText')  #: :vartype: str
        self.default = data.get('default')  #: :vartype: str
        self.max_length = data.get('maxLength')  #: :vartype: int
        self.min_length = data.get('minLength')  #: :vartype: int
        self.pattern = data.get('pattern')  #: :vartype: str
        self.validate = data.get('validate')  #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class RequestReference(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(RequestReference, self).__init__(parent, data)
        self.request_id = data.get('requestId')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ReferenceByType(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(ReferenceByType, self).__init__(parent, data)
        self.type = data.get('type')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class QuotaItem(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(QuotaItem, self).__init__(parent, data)
        self.total = data.get('total')  #: :vartype: int
        self.active = data.get('active')  #: :vartype: int
        self.unused = data.get('unused')  #: :vartype: int

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PersonReference(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(PersonReference, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.target_name = data.get('targetName')  #: :vartype: str
        self.first_name = data.get('firstName')  #: :vartype: str
        self.last_name = data.get('lastName')  #: :vartype: str
        self.recipient_type = data.get('recipientType')  #: :vartype: str
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def full_name(self):
        """

        :rtype: str
        """
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()
import xmatters.events
from xmatters.common import Recipient

from xmatters.people import PersonReference
from xmatters.utils.connection import ApiBridge

class Notification(ApiBridge):
    def __init__(self, parent, data):
        super(Notification, self).__init__(parent, data)
        self.id = data.get('id')
        self.category = data.get('category')
        recipient = data.get('recipient')
        self.recipient = Recipient(parent, recipient) if recipient else None
        self.delivery_status = data.get('deliveryStatus')
        self.created = data.get('created')
        self.delivery_attempted = data.get('deliveryAttempted')
        event = data.get('event')
        self.event = xmatters.events.EventReference(parent, data) if event else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Response(ApiBridge):
    def __init__(self, parent, data):
        super(Response, self).__init__(parent, data)
        self.comment = data.get('comment')
        notification = data.get('notification')
        self.notification = Notification(self, notification) if notification else None
        options = data.get('options', {}).get('data')
        self.options = [xmatters.events.ResponseOption(r) for r in options] if options else None
        self.source = data.get('source')
        self.received = data.get('received')
        self.response = data.get('response')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditAnnotation(ApiBridge):
    def __init__(self, parent, data):
        super(AuditAnnotation, self).__init__(parent, data)
        event = data.get('event')
        self.event = xmatters.events.EventReference(parent, data) if event else None
        author = data.get('author')
        self.author = PersonReference(parent, author) if author else None
        self.comment = data.get('comment')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Audit(ApiBridge):
    def __init__(self, parent, data):
        super(Audit, self).__init__(parent, data)
        self.type = data.get('type')
        event = data.get('event')
        self.event = xmatters.events.EventReference(parent, data) if event else None
        self.order_id = data.get('orderId')
        self.at = data.get('at')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()

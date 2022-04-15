import xmatters.utils
import xmatters.objects.common
import xmatters.objects.events


class ScheduledMessage(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(ScheduledMessage, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        owner = data.get('owner')
        self.owner = xmatters.objects.common.PersonReference(self, owner) if owner else None
        event = data.get('event')
        self.event = xmatters.objects.events.Event(self, event) if event else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class MessageRecurrence(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(MessageRecurrence, self).__init__(parent, data)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

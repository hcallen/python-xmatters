from xmatters.common import SelfLink
import xmatters.events
from xmatters.utils.connection import ApiBridge


class EventFloodFilter(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SuppressionMatch(ApiBridge):
    def __init__(self, parent, data):
        super(SuppressionMatch, self).__init__(parent, data)
        self.id = data.get('id')
        self.event_id = data.get('eventId')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventSuppression(ApiBridge):
    def __init__(self, parent, data):
        super(EventSuppression, self).__init__(parent, data)
        event = data.get('event')
        self.event = xmatters.events.EventReference(self, event) if event else None
        match = data.get('match')
        self.match = SuppressionMatch(self, data) if match else None
        self.at = data.get('at')
        filters = data.get('filters', [])
        self.filter = [EventFloodFilter(f) for f in filters]
        self.links = SelfLink(self, data.get('links'))

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

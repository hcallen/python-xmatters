import xmatters.utils as util
import xmatters.factories as factory
from xmatters.connection import ApiBridge
from xmatters.endpoints.common import Pagination, SelfLink
from xmatters.endpoints.forms import FormReference
from xmatters.endpoints.people import PersonReference, Person


class SubscriptionCriteriaReference(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.operator = data.get('operator')
        self.value = data.get('value')
        self.values = data.get('values', [])

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Subscription(ApiBridge):
    _endpoints = {'get_subscribers': '/subscribers'}

    def __init__(self, parent, data):
        super(Subscription, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        form = data.get('form')
        self.form = FormReference(form) if form else None
        owner = data.get('owner')

        self.owner = PersonReference(self, owner)
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None
        self.notification_delay = data.get('notificationDelay')
        criteria = data.get('criteria', {})
        self.criteria = Pagination(self, criteria, SubscriptionCriteriaReference) if criteria.get('data') else []
        recipients = data.get('recipients', {})
        self.recipients = Pagination(self, recipients, factory.recipient) if recipients.get('data') else []
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, factory.device_name) if tdns.get('data') else []
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def get_subscribers(self):
        url = self.build_url(self._endpoints.get('get_subscribers'))
        subscribers = self.con.get(url)
        return Pagination(self, subscribers, Person) if subscribers.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()



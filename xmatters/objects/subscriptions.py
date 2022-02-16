import xmatters.connection
import xmatters.utils
import xmatters.factories as factory
import xmatters.objects.forms
from xmatters.objects.common import SelfLink
from xmatters.utils import Pagination
from xmatters.objects.people import Person


class SubscriptionCriteriaReference(object):
    def __init__(self, data):
        self.name = data.get('name')    #:
        self.operator = data.get('operator')    #:
        self.value = data.get('value')    #:
        self.values = data.get('values', [])    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Subscription(xmatters.connection.ApiBridge):
    _endpoints = {'get_subscribers': '/subscribers'}

    def __init__(self, parent, data):
        super(Subscription, self).__init__(parent, data)
        self.id = data.get('id')    #:
        self.name = data.get('name')    #:
        self.description = data.get('description')    #:
        form = data.get('form')
        self.form = xmatters.objects.forms.FormReference(form) if form else None    #: :vartype: :class:`xmatters.objects.forms.FormReference`
        owner = data.get('owner')

        self.owner = xmatters.objects.people.PersonReference(self, owner)    #: :vartype: :class:`xmatters.objects.people.PersonReference`
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None    #: :vartype: :class:`xmatters.utils.TimeAttribute`
        self.notification_delay = data.get('notificationDelay')    #:
        criteria = data.get('criteria', {})
        self.criteria = Pagination(self, criteria, SubscriptionCriteriaReference) if criteria.get('data') else []    #: :vartype: :class:`xmatters.utils.Pagination` of :class:`xmatters.objects.subscriptions.SubscriptionCriteriaReference`
        r = data.get('recipients', {})
        self.recipients = Pagination(self, r, factory.RecipientFactory) if r.get('data') else []    #: :vartype: :class:`xmatters.utils.Pagination` of :class:`xmatters.utils.RecipientFactory`
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, factory.DeviceNameFactory) if tdns.get('data') else []    #: :vartype: :class:`xmatters.utils.Pagination` of :class:`xmatters.utils.DeviceNameFactory`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`xmatters.objects.common.SelfLink`

    def get_subscribers(self, params=None, **kwargs):
        url = self.get_url(self._endpoints.get('get_subscribers'))
        subscribers = self.con.get(url, params=params, **kwargs)
        return Pagination(self, subscribers, Person) if subscribers.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

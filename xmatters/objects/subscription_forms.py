import xmatters.factories
import xmatters.objects.forms
import xmatters.objects.utils
import xmatters.utils
import xmatters.connection
import xmatters.objects.plans
import xmatters.objects.roles
import xmatters.objects.common
from xmatters.objects.utils import Pagination


class SubscriptionForm(xmatters.utils.ApiBase):
    _endpoints = {'target_device_names': '?embed=deviceNames',
                  'visible_target_device_names': '?embed=deviceNames',
                  'property_definitions': '?embed=propertyDefinitions',
                  'roles': '?embed=roles'}

    def __init__(self, parent, data):
        super(SubscriptionForm, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        self.description = data.get('description')   #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, data) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
        self.scope = data.get('scope')    #: :vartype: str
        form = data.get('form')
        self.form = xmatters.objects.forms.FormReference(self, form) if form else None    #: :vartype: :class:`~xmatters.objects.forms.FormReference`
        created = data.get('created')
        self.created = xmatters.objects.utils.TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        self.one_way = data.get('oneWay')    #: :vartype: bool
        self.subscribe_others = data.get('subscribeOthers')    #: :vartype: bool
        self.notification_delay = data.get('notificationDelay')   #: :vartype: int
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def target_device_names(self):
        url = self._get_url(self._endpoints.get('target_device_names'))
        data = self._con.get(url)
        tdns = data.get('targetDeviceNames', {})
        return Pagination(self, tdns, xmatters.factories.DeviceNameFactory) if tdns.get('data') else []

    @property
    def visible_target_device_names(self):
        url = self._get_url(self._endpoints.get('visible_target_device_names'))
        data = self._con.get(url)
        vtdns = data.get('visibleTargetDeviceNames', {})
        return Pagination(self, vtdns, xmatters.factories.DeviceNameFactory) if vtdns.get('data') else []

    @property
    def property_definitions(self):
        url = self._get_url(self._endpoints.get('property_definitions'))
        data = self._con.get(url)
        ps = data.get('propertyDefinitions', {})
        return Pagination(self, ps, xmatters.factories.PropertiesFactoryBase) if ps.get('data') else []

    @property
    def roles(self):
        url = self._get_url(self._endpoints.get('roles'))
        data = self._con.get(url).get('roles')
        roles = data.get('roles')
        return Pagination(self, roles, xmatters.objects.roles.Role) if roles else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormReference(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(SubscriptionFormReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

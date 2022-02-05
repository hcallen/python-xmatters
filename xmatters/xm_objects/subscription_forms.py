import xmatters.xm_objects.forms as forms
import xmatters.factories as factory
import xmatters.utils as utils
from xmatters.connection import ApiBridge
from xmatters.xm_objects import plans as plans
from xmatters.xm_objects.common import Pagination, SelfLink
from xmatters.xm_objects.roles import Role


class SubscriptionForm(ApiBridge):
    _endpoints = {'target_device_names': '?embed=deviceNames',
                  'visible_target_device_names': '?embed=deviceNames',
                  'property_definitions': '?embed=propertyDefinitions',
                  'roles': '?embed=roles'}

    def __init__(self, parent, data):
        super(SubscriptionForm, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        plan = data.get('plan')
        self.plan = plans.PlanReference(data) if plan else None
        self.scope = data.get('scope')
        form = data.get('form')
        self.form = forms.FormReference(form) if form else None
        created = data.get('created')
        self.created = utils.TimeAttribute(created) if created else None
        self.one_way = data.get('oneWay')
        self.subscribe_others = data.get('subscribeOthers')
        self.notification_delay = data.get('notificationDelay')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def target_device_names(self):
        url = self.build_url(self._endpoints.get('target_device_names'))
        data = self.con.get(url)
        tdns = data.get('targetDeviceNames', {})
        return list(Pagination(self, tdns, factory.device_name)) if tdns.get('data') else []

    @property
    def visible_target_device_names(self):
        url = self.build_url(self._endpoints.get('visible_target_device_names'))
        data = self.con.get(url)
        vtdns = data.get('visibleTargetDeviceNames', {})
        return list(Pagination(self, vtdns, factory.device_name)) if vtdns.get('data') else []

    @property
    def property_definitions(self):
        url = self.build_url(self._endpoints.get('property_definitions'))
        data = self.con.get(url)
        ps = data.get('propertyDefinitions', {})
        return list(Pagination(self, ps, factory.plan_property)) if ps.get('data') else []

    @property
    def roles(self):
        url = self.build_url(self._endpoints.get('roles'))
        data = self.con.get(url).get('roles')
        roles = data.get('roles')
        return list(Pagination(self, roles, Role)) if roles else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormReference(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        plan = data.get('plan')
        self.plan = plans.PlanReference(plan) if plan else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

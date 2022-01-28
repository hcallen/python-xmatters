import xmatters.utils.factories
from xmatters.common import Pagination, SelfLink
from xmatters.forms import Form
from xmatters.integrations import Integration
from xmatters.people import Person
from xmatters.plan_constants import PlanConstant
from xmatters.plan_endpoints import Endpoint
from xmatters.shared_libraries import SharedLibrary
from xmatters.utils.connection import ApiBridge


class PlanPointer(object):
    def __init__(self, data):
        self.id = data.get('id')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PlanReference(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Plan(ApiBridge):
    _endpoints = {'creator': '?embed=creator',
                  'constants': '/constants',
                  'get_forms': '/forms',
                  'get_integrations': '/integrations',
                  'get_constants': '/constants',
                  'get_properties': '/property-definitions',
                  'get_libraries': '/shared-libraries',
                  'get_endpoints': '/endpoints'}

    def __init__(self, parent, data):
        super(Plan, self).__init__(parent, data)
        self.id = data.get('id')
        self.plan_type = data.get('planType')
        self.name = data.get('name')
        self.description = data.get('description')
        self.enabled = data.get('enabled')
        self.editable = data.get('editable')
        self.logging_level = data.get('loggingLevel')
        self.accessible = data.get('accessibleByAll')
        self.flood_control = data.get('floodControl')
        self.created = data.get('created')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None
        self.position = data.get('position')

    def get_forms(self, params=None):
        url = self.build_url(self._endpoints.get('get_forms'))
        forms = self.con.get(url, params)
        return Pagination(self, forms, Form) if forms.get('data') else []

    def get_constants(self, params=None):
        url = self.build_url(self._endpoints.get('get_constants'))
        constants = self.con.get(url, params)
        return Pagination(self, constants, PlanConstant) if constants.get('data') else []

    def get_integrations(self, params=None):
        url = self.build_url(self._endpoints.get('get_integrations'))
        ints = self.con.get(url, params)
        return Pagination(self, ints, Integration) if ints.get('data') else []

    def get_properties(self, params=None):
        url = self.build_url(self._endpoints.get('get_properties'))
        props = self.con.get(url, params)
        return Pagination(self, props, xmatters.utils.factories.prop_factory) if props.get(
            'data') else []

    def get_libraries(self, params=None):
        url = self.build_url(self._endpoints.get('get_libraries'))
        libs = self.con.get(url, params)
        return Pagination(self, libs, SharedLibrary) if libs.get('data') else []

    def get_endpoints(self, params=None):
        url = self.build_url(self._endpoints.get('get_endpoints'))
        endpoints = self.con.get(url, params)
        return Pagination(self, endpoints, Endpoint) if endpoints.get('data') else []

    # TODO
    def get_subscription_forms(self, params=None):
        pass

    @property
    def creator(self):
        url = self.build_url(self._endpoints.get('creator'))
        creator = self.con.get(url).get('creator')
        return Person(self, creator) if creator else None

    @property
    def constants(self):
        return self.get_constants()

    @property
    def endpoints(self):
        return self.get_endpoints()

    @property
    def forms(self):
        return self.get_forms()

    @property
    def integrations(self):
        return self.get_integrations()

    @property
    def property_definitions(self):
        return self.get_properties()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()

import xmatters.factories as factory
import xmatters.xm_objects.forms
import xmatters.xm_objects.plan_endpoints
from xmatters.connection import ApiBridge
from xmatters.xm_objects.common import Pagination, SelfLink
from xmatters.xm_objects.integrations import Integration
from xmatters.xm_objects.people import Person
from xmatters.xm_objects.plan_constants import PlanConstant
from xmatters.xm_objects.shared_libraries import SharedLibrary
from xmatters.xm_objects.subscription_forms import SubscriptionForm


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
                  'get_forms': '/forms',
                  'get_form_by_id': '/forms/{form_id}',
                  'get_integrations': '/integrations',
                  'get_integration_by_id': '/integrations/{int_id}',
                  'get_constants': '/constants',
                  'get_properties': '/property-definitions',
                  'get_libraries': '/shared-libraries',
                  'get_library_by_id': '/shared-libraries/{lib_id}',
                  'get_endpoints': '/endpoints',
                  'get_subscription_forms': '/subscription-forms',
                  'delete_constant': '/constants/{const_id}',
                  'delete_endpoints': '/endpoints/{end_id}',
                  'delete_property': '/property-definitions/{prop_id}'}

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
        fs = self.con.get(url, params)
        return Pagination(self, fs, xmatters.xm_objects.forms.Form) if fs.get('data') else []

    # TODO: Test
    def get_form_by_id(self, form_id):
        url = self.build_url(self._endpoints.get('get_form_by_id').format(form_id=form_id))
        data = self.con.get(url)
        return xmatters.xm_objects.forms.Form(self, data) if data else None

    # TODO: Test
    def create_form(self, data):
        url = self.build_url(self._endpoints.get('get_forms'))
        data = self.con.post(url, data=data)
        return xmatters.xm_objects.forms.Form(self, data) if data else None

    # TODO: Test
    def update_form(self, data):
        url = self.build_url(self._endpoints.get('get_forms'))
        data = self.con.post(url, data=data)
        return xmatters.xm_objects.forms.Form(self, data) if data else None

    def get_constants(self, params=None):
        url = self.build_url(self._endpoints.get('get_constants'))
        constants = self.con.get(url, params)
        return Pagination(self, constants, PlanConstant) if constants.get('data') else []

    # TODO: Test
    def create_constant(self, data):
        url = self.build_url(self._endpoints.get('get_constants'))
        data = self.con.post(url, data=data)
        return PlanConstant(self, data) if data else None

    # TODO: Test
    def update_constant(self, data):
        url = self.build_url(self._endpoints.get('get_constants'))
        data = self.con.post(url, data=data)
        return PlanConstant(self, data) if data else None

    # TODO: Test
    def delete_constant(self, constant_id):
        url = self.build_url(self._endpoints.get('delete_constant').format(const_id=constant_id))
        data = self.con.delete(url)
        return PlanConstant(self, data) if data else None

    def get_integrations(self, params=None):
        url = self.build_url(self._endpoints.get('get_integrations'))
        ints = self.con.get(url, params)
        return Pagination(self, ints, Integration) if ints.get('data') else []

    # TODO: Test
    def get_integration_by_id(self, integration_id):
        url = self.build_url(self._endpoints.get('get_integration_by_id').format(int_id=integration_id))
        data = self.con.get(url)
        return Integration(self, data) if data else None

    # TODO: Test
    def create_integration(self, data):
        url = self.build_url(self._endpoints.get('get_integrations'))
        data = self.con.post(url, data=data)
        return Integration(self, data) if data else None

    # TODO: Test
    def update_integration(self, data):
        url = self.build_url(self._endpoints.get('get_integrations'))
        data = self.con.post(url, data=data)
        return Integration(self, data) if data else None

    # TODO: Test
    def delete_integration(self, integration_id):
        url = self.build_url(self._endpoints.get('get_integration_by_id').format(int_id=integration_id))
        data = self.con.delete(url)
        return Integration(self, data) if data else None

    def get_properties(self, params=None):
        url = self.build_url(self._endpoints.get('get_properties'))
        props = self.con.get(url, params)
        return Pagination(self, props, factory.plan_property) if props.get('data') else []

    # TODO: Test
    def create_property(self, data):
        url = self.build_url(self._endpoints.get('get_properties'))
        data = self.con.post(url, data=data)
        return factory.plan_property(data) if data else None

    # TODO: Test
    def update_property(self, data):
        url = self.build_url(self._endpoints.get('get_properties'))
        data = self.con.post(url, data=data)
        return factory.plan_property(data) if data else None

    # TODO: Test
    def delete_property(self, property_id):
        url = self.build_url(self._endpoints.get('delete_property').format(prop_id=property_id))
        data = self.con.delete(url)
        return factory.plan_property(data) if data else None

    def get_shared_libraries(self, params=None):
        url = self.build_url(self._endpoints.get('get_libraries'))
        libs = self.con.get(url, params)
        return Pagination(self, libs, SharedLibrary) if libs.get('data') else []

    # TODO: Test
    def get_shared_library_by_id(self, library_id):
        url = self.build_url(self._endpoints.get('get_library_by_id').format(lib_id=library_id))
        data = self.con.get(url)
        return SharedLibrary(data) if data else None

    # TODO: Test
    def create_shared_library(self, data):
        url = self.build_url(self._endpoints.get('get_libraries'))
        data = self.con.post(url, data=data)
        return SharedLibrary(data) if data else None

    # TODO: Test
    def update_shared_library(self, data):
        url = self.build_url(self._endpoints.get('get_libraries'))
        data = self.con.post(url, data=data)
        return SharedLibrary(data) if data else None

    # TODO: Test
    def delete_shared_library(self, library_id):
        url = self.build_url(self._endpoints.get('get_library_by_id').format(lib_id=library_id))
        data = self.con.delete(url)
        return SharedLibrary(data) if data else None

    def get_endpoints(self, params=None):
        url = self.build_url(self._endpoints.get('get_endpoints'))
        endpoints = self.con.get(url, params)
        return Pagination(self, endpoints, xmatters.xm_objects.plan_endpoints.Endpoint) if endpoints.get('data') else []

    # TODO: Test
    def create_endpoint(self, data):
        url = self.build_url(self._endpoints.get('get_endpoints'))
        data = self.con.post(url, data=data)
        return xmatters.xm_objects.plan_endpoints.Endpoint(self, data) if data else None

    # TODO: Test
    def update_endpoint(self, data):
        url = self.build_url(self._endpoints.get('get_endpoints'))
        data = self.con.post(url, data=data)
        return xmatters.xm_objects.plan_endpoints.Endpoint(self, data) if data else None

    # TODO: Test
    def delete_endpoint(self, endpoint_id):
        url = self.build_url(self._endpoints.get('delete_endpoint').format(end_id=endpoint_id))
        data = self.con.delete(url)
        return xmatters.xm_objects.plan_endpoints.Endpoint(self, data) if data else None

    def get_subscription_forms(self, params=None):
        url = self.build_url(self._endpoints.get('get_subscription_forms'))
        sub_forms = self.con.get(url, params)
        return Pagination(self, sub_forms, SubscriptionForm) if sub_forms.get('data') else []

    # TODO: Test
    def create_subscription_form(self, data):
        url = self.build_url(self._endpoints.get('get_subscription_forms'))
        data = self.con.post(url, data=data)
        return SubscriptionForm(self, data) if data else None

    # TODO: Test
    def update_subscription_form(self, data):
        url = self.build_url(self._endpoints.get('get_subscription_forms'))
        data = self.con.post(url, data=data)
        return SubscriptionForm(self, data) if data else None

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

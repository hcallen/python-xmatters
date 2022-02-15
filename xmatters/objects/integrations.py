from xmatters.objects.common import ReferenceById, SelfLink
from xmatters.utils import Pagination
from xmatters.objects.people import PersonReference
import xmatters.objects.plan_endpoints
import xmatters.objects.plans
from xmatters.connection import ApiBridge


class IntegrationReference(object):
    def __init__(self, data):
        self.id = data.get('id')
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(plan) if plan else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IntegrationLog(ApiBridge):
    def __init__(self, parent, data):
        super(IntegrationLog, self).__init__(parent, data)
        self.id = data.get('id')
        integration = data.get('integration')
        self.integration = IntegrationReference(integration) if integration else None
        self.completed = data.get('completed')
        self.request_method = data.get('requestMethod')
        self.request_headers = data.get('requestHeaders')
        self.request_parameters = data.get('requestParameters')
        self.request_body = data.get('requestBody')
        self.remote_address = data.get('remoteAddress')
        self.request_id = data.get('requestId')
        self.status = data.get('status')
        by = data.get('by')
        self.by = PersonReference(self, by) if by else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Integration(ApiBridge):
    _endpoints = {'get_logs': '/logs'}

    def __init__(self, parent, data):
        super(Integration, self).__init__(parent, data)
        self.id = data.get('id')
        plan = data.get('plan')
        self.plan = ReferenceById(plan) if plan else None
        form = data.get('form')
        self.form = ReferenceById(form) if form else None
        self.name = data.get('name')
        self.integration_type = data.get('integrationType')
        self.operation = data.get('operation')
        self.triggered_by = data.get('triggeredBy')
        self.created_by = data.get('createdBy')
        self.authentication_type = data.get('authenticationType')
        endpoint = data.get('endpoint')
        self.endpoint = xmatters.objects.plan_endpoints.Endpoint(self, endpoint) if endpoint else None
        self.deployed = data.get('deployed')
        self.script = data.get('script')
        self.migrated_outbound_trigger = data.get('migratedOutboundTrigger')
        self.origin_type = data.get('originType')
        self.is_run_by_service_owner = data.get('isRunByServiceOwner')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    
    def get_logs(self):
        endpoint = self.get_url(self._endpoints.get('get_logs'))
        url = self.get_url(endpoint)
        logs = self.con.get(url)
        return Pagination(self, logs, IntegrationLog) if logs.get('data') else []

    @property
    def logs(self):
        return self.get_logs()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()

import xmatters.utils.factories
from xmatters.audit import Audit
from xmatters.common import Pagination
from xmatters.device_types import DeviceTypes
from xmatters.dynamic_teams import DynamicTeam
from xmatters.events import Event, DeviceName
from xmatters.external_conference_bridges import ConferenceBridge
from xmatters.forms import Form
from xmatters.groups import Group
from xmatters.incidents import Incident
from xmatters.oncall import OnCall, OnCallSummary
from xmatters.people import Person
from xmatters.plans import Plan
from xmatters.temporary_absences import TemporaryAbsence
from xmatters.utils.connection import ApiBridge
from xmatters.import_jobs import Import
import urllib.parse


class xMattersSession(ApiBridge):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}',
                  'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}',
                  'get_oncall': '/on-call?groups={group_ids}',
                  'get_oncall_summary': '/on-call-summary?groups={group_ids}',
                  'get_people': '/people',
                  'get_person_by_id': '/people/{person_id}',
                  'get_conference_bridges': '/conference-bridges',
                  'get_conference_bridge_by_id': '/conference-bridges/{bridge_id}',
                  'get_events': '/events',
                  'get_event_by_id': '/events/{event_id}',
                  'get_temporary_absences': '/temporary-absences',
                  'get_audit': '/audits?{event_id}',
                  'get_device_names': '/device-names',
                  'get_device_types': '/device-types',
                  'get_dynamic_teams': '/dynamic-teams',
                  'get_dynamic_team_by_id': '/dynamic-teams/{dynamic_team_id}',
                  'get_forms': '/forms',
                  'get_import_jobs': '/imports',
                  'get_plans': '/plans',
                  'get_incidents': '/incidents',
                  'get_plan_by_id': '/plans/{plan_id}'}

    def __init__(self, base_url, auth, timeout=3, max_retries=3):
        p_url = urllib.parse.urlparse(base_url)
        instance_url = 'https://{}'.format(p_url.netloc)
        base_url = '{}/api/xm/1'.format(instance_url)
        self.con = auth
        self.con.init_session(base_url, timeout, max_retries)
        super(xMattersSession, self).__init__(self)

    def get_audit(self, params=None):
        url = self.build_url(self._endpoints.get('get_audit'))
        data = self.con.get(url, params)
        return Pagination(self, data, Audit) if data.get('data') else []

    def get_devices(self, params=None):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url, params)
        return Pagination(self, data, xmatters.utils.factories.device_factory) if data.get('data') else []

    def get_device_by_id(self, device_id, params=None):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url, params)
        return xmatters.utils.factories.device_factory(self, data) if data else None

    def get_device_names(self, params=None):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.get(url, params)
        return Pagination(self, data, DeviceName) if data.get('data') else []

    def get_device_types(self, params=None):
        url = self.build_url(self._endpoints.get('get_device_types'))
        data = self.con.get(url, params)
        return DeviceTypes(data) if data else None

    def get_dynamic_teams(self, params=None):
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.get(url, params)
        return Pagination(self, data, DynamicTeam) if data.get('data') else []

    def get_dynamic_team_by_id(self, dynamic_team_id, params=None):
        url = self.build_url(self._endpoints.get('get_dynamic_team_by_id').format(dynamic_team_id=dynamic_team_id))
        data = self.con.get(url, params)
        return DynamicTeam(self, data) if data else None

    def get_events(self, params=None):
        url = self.build_url(self._endpoints.get('get_events'))
        data = self.con.get(url, params)
        return Pagination(self, data, Event) if data.get('data') else []

    def get_event_by_id(self, event_id, params=None):
        url = self.build_url(self._endpoints.get('get_event_by_id').format(event_id=event_id))
        data = self.con.get(url, params)
        return Event(self, data) if data else None

    def get_conference_bridges(self, params=None):
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.get(url, params)
        return Pagination(self, data, ConferenceBridge) if data.get('data') else []

    def get_conference_bridge_by_id(self, bridge_id, params=None):
        url = self.build_url(self._endpoints.get('get_conference_bridge_by_id').format(bridge_id=bridge_id))
        data = self.con.get(url, params)
        return ConferenceBridge(self, data) if data else None

    def get_forms(self, params=None):
        url = self.build_url(self._endpoints.get('get_forms'))
        data = self.con.get(url, params)
        return Pagination(self, data, Form) if data.get('data') else []

    def get_groups(self, params=None):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.get(url, params)
        return Pagination(self, data, Group) if data.get('data') else []

    def get_group_by_id(self, group_id, params=None):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url, params)
        return Group(self, data) if data else None

    def get_import_jobs(self, params=None):
        url = self.build_url(self._endpoints.get('get_import_jobs'))
        data = self.con.get(url, params).get('data')
        return [Import(self, job) for job in data] if data else []

    def get_incidents(self, params=None):
        url = self.build_url(self._endpoints.get('get_incidents'))
        data = self.con.get(url, params)
        return Pagination(self, data, Incident) if data.get('data') else []

    def get_oncall(self, group_ids, params=None):
        group_ids = ','.join(group_ids) if isinstance(group_ids, list) else group_ids
        url = self.build_url(self._endpoints.get('get_oncall').format(group_ids=group_ids))
        data = self.con.get(url, params)
        return Pagination(self, data, OnCall) if data.get('data') else []

    def get_oncall_summary(self, group_ids, params=None):
        group_ids = ','.join(group_ids) if isinstance(group_ids, list) else group_ids
        url = self.build_url(self._endpoints.get('get_oncall_summary').format(group_ids=group_ids))
        data = self.con.get(url, params)
        return [OnCallSummary(self, summary) for summary in data] if data else None

    def get_people(self, params=None):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params)
        return Pagination(self, data, Person) if data.get('data') else []

    def get_person_by_id(self, person_id, params=None):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url, params)
        return Person(self, data) if data else None

    def get_plans(self, params=None):
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.get(url, params)
        return Pagination(self, data, Plan) if data.get('data') else []

    def get_plan_by_id(self, plan_id):
        url = self.build_url(self._endpoints.get('get_plan_by_id').format(person_id=plan_id))
        data = self.con.get(url)
        return Plan(self, data) if data else None

    # TODO
    def get_roles(self, params=None):
        pass

    # TODO
    def get_scenarios(self, params=None):
        pass

    # TODO
    def get_services(self, params=None):
        pass

    # TODO
    def get_sites(self, params=None):
        pass

    # TODO
    def get_site_by_id(self, site_id):
        pass

    # TODO
    def get_subscription_forms(self, params=None):
        pass

    # TODO
    def get_subscription_form_by_id(self, sub_form_id):
        pass

    # TODO
    def get_subscriptions(self, params=None):
        pass

    # TODO
    def get_subscription_by_id(self, sub_id):
        pass

    def get_temporary_absences(self, params=None):
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.get(url, params)
        return Pagination(self, data, TemporaryAbsence) if data.get('data') else []

    @property
    def base_url(self):
        return self.con.base_url

    @property
    def instance_url(self):
        return self.con.instance_url

    @property
    def timeout(self):
        return self.con.timeout

    @property
    def max_retries(self):
        return self.con.max_retries

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

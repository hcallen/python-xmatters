from xmatters import utils as util, factories as factory
from xmatters.connection import ApiBridge
from xmatters.xm_objects.common import Pagination
from xmatters.xm_objects.conference_bridges import ConferenceBridge
from xmatters.xm_objects.device_types import DeviceTypes
from xmatters.xm_objects.dynamic_teams import DynamicTeam
from xmatters.xm_objects.event_supressions import EventSuppression
from xmatters.xm_objects.events import Event
from xmatters.xm_objects.forms import Form
from xmatters.xm_objects.groups import Group
from xmatters.xm_objects.import_jobs import Import
from xmatters.xm_objects.incidents import Incident
from xmatters.xm_objects.oncall import OnCall
from xmatters.xm_objects.oncall_summary import OnCallSummary
from xmatters.xm_objects.people import Person
from xmatters.xm_objects.plans import Plan
from xmatters.xm_objects.roles import Role
from xmatters.xm_objects.scenarios import Scenario
from xmatters.xm_objects.services import Service
from xmatters.xm_objects.sites import Site
from xmatters.xm_objects.subscription_forms import SubscriptionForm
from xmatters.xm_objects.subscriptions import Subscription
from xmatters.xm_objects.temporary_absences import TemporaryAbsence


class AuditsEndpoint(ApiBridge):
    def __init__(self, parent):
        super(AuditsEndpoint, self).__init__(parent)

        self._endpoints = {'get_audit': '/audits'}

    def get_audit(self, event_id, audit_type=util.AUDIT_TYPES, sort_order='ASCENDING', params=None):

        # process parameters
        params = params if params else {}
        if 'eventId' not in params.keys():
            params['eventId'] = event_id
        if audit_type and 'auditType' not in params.keys():
            params['auditType'] = ','.join(audit_type).upper() if isinstance(audit_type, list) else audit_type.upper()
        if sort_order and 'sortOrder' not in params.keys():
            params['sortOrder'] = sort_order.upper()

        url = self.build_url(self._endpoints.get('get_audit'))
        data = self.con.get(url, params)
        return Pagination(self, data, factory.audit) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesEndpoint(ApiBridge):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}'}

    def __init__(self, parent):
        super(DevicesEndpoint, self).__init__(parent)

    def get_devices(self, device_status=None, device_type=None, device_names=None, phone_number_format='E164',
                    params=None):

        # process parameters
        params = params if params else {}
        if device_status and 'deviceStatus' not in params.keys():
            params['deviceStatus'] = device_status.upper()
        if device_type and 'deviceType' not in params.keys():
            params['deviceType'] = device_type.upper()
        if device_names and 'deviceNames' not in params.keys():
            params['deviceNames'] = ','.join(device_names).upper() if isinstance(device_names,
                                                                                 list) else device_names.upper()
        if phone_number_format and 'phoneNumberFormat' not in params.keys():
            params['phoneNumberFormat'] = phone_number_format.upper()

        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url, params)
        return Pagination(self, data, factory.device) if data.get('data') else []

    def get_device_by_id(self, device_id, params=None):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url, params)
        return factory.device(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNamesEndpoint(ApiBridge):
    _endpoints = {'get_device_names': '/device-names'}

    def __init__(self, parent):
        super(DeviceNamesEndpoint, self).__init__(parent)

    def get_device_names(self, params=None):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.get(url, params)
        return Pagination(self, data, factory.device_name) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceTypesEndpoint(ApiBridge):
    _endpoints = {'get_device_types': '/device-types'}

    def __init__(self, parent):
        super(DeviceTypesEndpoint, self).__init__(parent)

    def get_device_types(self, params=None):
        url = self.build_url(self._endpoints.get('get_device_types'))
        data = self.con.get(url, params)
        return DeviceTypes(data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DynamicTeamsEndpoint(ApiBridge):
    _endpoints = {'get_dynamic_teams': '/dynamic-teams',
                  'get_dynamic_team_by_id': '/dynamic-teams/{dynamic_team_id}'}

    def get_dynamic_teams(self, params=None):
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.get(url, params)
        return Pagination(self, data, DynamicTeam) if data.get('data') else []

    def get_dynamic_team_by_id(self, dynamic_team_id, params=None):
        url = self.build_url(self._endpoints.get('get_dynamic_team_by_id').format(dynamic_team_id=dynamic_team_id))
        data = self.con.get(url, params)
        return DynamicTeam(self, data) if data else None

    def __init__(self, parent):
        super(DynamicTeamsEndpoint, self).__init__(parent)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventsEndpoint(ApiBridge):
    _endpoints = {'get_events': '/events',
                  'get_event_by_id': '/events/{event_id}'}

    def __init__(self, parent):
        super(EventsEndpoint, self).__init__(parent)

    def get_events(self, params=None):
        url = self.build_url(self._endpoints.get('get_events'))
        data = self.con.get(url, params)
        return Pagination(self, data, Event) if data.get('data') else []

    def get_event_by_id(self, event_id, params=None):
        url = self.build_url(self._endpoints.get('get_event_by_id').format(event_id=event_id))
        data = self.con.get(url, params)
        return Event(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventSuppressionsEndpoint(ApiBridge):
    _endpoints = {'get_event_suppressions_by_event_id': '/event-suppressions?event={event_id}'}

    def __init__(self, parent):
        super(EventSuppressionsEndpoint, self).__init__(parent)

    def get_event_suppressions_by_event_id(self, event_id, params=None):
        url = self.build_url(self._endpoints.get('get_event_suppressions_by_event_id').format(event_id))
        data = self.con.get(url, params)
        return Pagination(self, data, EventSuppression) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferenceBridgesEndpoint(ApiBridge):
    _endpoints = {'get_conference_bridges': '/conference-bridges',
                  'get_conference_bridge_by_id': '/conference-bridges/{bridge_id}'}

    def __init__(self, parent):
        super(ConferenceBridgesEndpoint, self).__init__(parent)

    def get_conference_bridges(self, params=None):
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.get(url, params)
        return Pagination(self, data, ConferenceBridge) if data.get('data') else []

    def get_conference_bridge_by_id(self, bridge_id, params=None):
        url = self.build_url(self._endpoints.get('get_conference_bridge_by_id').format(bridge_id=bridge_id))
        data = self.con.get(url, params)
        return ConferenceBridge(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormsEndpoint(ApiBridge):
    _endpoints = {'get_forms': '/forms'}

    def __init__(self, parent):
        super(FormsEndpoint, self).__init__(parent)

    def get_forms(self, params=None):
        url = self.build_url(self._endpoints.get('get_forms'))
        data = self.con.get(url, params)
        return Pagination(self, data, Form) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class GroupsEndpoint(ApiBridge):
    _endpoints = {'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}'}

    def __init__(self, parent):
        super(GroupsEndpoint, self).__init__(parent)

    def get_groups(self, params=None):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.get(url, params)
        return Pagination(self, data, Group) if data.get('data') else []

    def get_group_by_id(self, group_id, params=None):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url, params)
        return Group(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ImportJobsEndpoint(ApiBridge):
    _endpoints = {'get_import_jobs': '/imports'}

    def __init__(self, parent):
        super(ImportJobsEndpoint, self).__init__(parent)

    def get_import_jobs(self, params=None):
        url = self.build_url(self._endpoints.get('get_import_jobs'))
        data = self.con.get(url, params).get('data')
        return [Import(self, job) for job in data] if data else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentsEndpoint(ApiBridge):
    _endpoints = {'get_incidents': '/incidents'}

    def __init__(self, parent):
        super(IncidentsEndpoint, self).__init__(parent)

    def get_incidents(self, params=None):
        url = self.build_url(self._endpoints.get('get_incidents'))
        data = self.con.get(url, params)
        return Pagination(self, data, Incident) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallEndpoint(ApiBridge):
    _endpoints = {'get_oncall': '/on-call?groups={group_ids}'}

    def __init__(self, parent):
        super(OnCallEndpoint, self).__init__(parent)

    def get_oncall(self, group_ids, params=None):
        group_ids = ','.join(group_ids) if isinstance(group_ids, list) else group_ids
        url = self.build_url(self._endpoints.get('get_oncall').format(group_ids=group_ids))
        data = self.con.get(url, params)
        return Pagination(self, data, OnCall) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallSummaryEndpoint(ApiBridge):
    _endpoints = {'get_oncall_summary': '/on-call-summary?groups={group_ids}'}

    def __init__(self, parent):
        super(OnCallSummaryEndpoint, self).__init__(parent)

    def get_oncall_summary(self, group_ids, params=None):
        group_ids = ','.join(group_ids) if isinstance(group_ids, list) else group_ids
        url = self.build_url(self._endpoints.get('get_oncall_summary').format(group_ids=group_ids))
        data = self.con.get(url, params)
        return [OnCallSummary(self, summary) for summary in data] if data else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PeopleEndpoint(ApiBridge):
    _endpoints = {'get_people': '/people',
                  'get_person_by_id': '/people/{person_id}'}

    def __init__(self, parent):
        super(PeopleEndpoint, self).__init__(parent)

    def get_people(self, params=None):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params)
        return Pagination(self, data, Person) if data.get('data') else []

    def get_person_by_id(self, person_id, params=None):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url, params)
        return Person(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PlansEndpoint(ApiBridge):
    _endpoints = {'get_plans': '/plans',
                  'get_plan_by_id': '/plans/{plan_id}'}

    def __init__(self, parent):
        super(PlansEndpoint, self).__init__(parent)

    def get_plans(self, params=None):
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.get(url, params)
        return Pagination(self, data, Plan) if data.get('data') else []

    def get_plan_by_id(self, plan_id, params=None):
        url = self.build_url(self._endpoints.get('get_plan_by_id').format(person_id=plan_id))
        data = self.con.get(url, params)
        return Plan(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RolesEndpoint(ApiBridge):
    _endpoints = {'get_roles': '/roles'}

    def __init__(self, parent):
        super(RolesEndpoint, self).__init__(parent)

    def get_roles(self, params=None):
        url = self.build_url(self._endpoints.get('get_roles'))
        data = self.con.get(url, params)
        return Pagination(self, data, Role) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenariosEndpoint(ApiBridge):
    _endpoints = {'get_scenarios': '/scenarios',
                  'get_scenario_by_id': '/scenarios/{scenario_id}'}

    def __init__(self, parent):
        super(ScenariosEndpoint, self).__init__(parent)

    def get_scenarios(self, params=None):
        url = self.build_url(self._endpoints.get('get_scenarios'))
        data = self.con.get(url, params)
        return Pagination(self, data, Scenario) if data.get('data') else []

    def get_scenario_by_id(self, scenario_id, params=None):
        url = self.build_url(self._endpoints.get('get_scenario_by_id').format(scenario_id=scenario_id))
        data = self.con.get(url, params)
        return Scenario(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ServicesEndpoint(ApiBridge):
    _endpoints = {'get_services': '/services',
                  'get_service_by_id': '/scenarios/{service_id}'}

    def __init__(self, parent):
        super(ServicesEndpoint, self).__init__(parent)

    def get_services(self, params=None):
        url = self.build_url(self._endpoints.get('get_services'))
        data = self.con.get(url, params)
        return Pagination(self, data, Service) if data.get('data') else []

    def get_service_by_id(self, service_id, params=None):
        url = self.build_url(self._endpoints.get('get_service_by_id').format(service_id=service_id))
        data = self.con.get(url, params)
        return Service(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SitesEndpoint(ApiBridge):
    _endpoints = {'get_sites': '/sites',
                  'get_site_by_id': '/sites/{site_id}'}

    def __init__(self, parent):
        super(SitesEndpoint, self).__init__(parent)

    def get_sites(self, params=None):
        url = self.build_url(self._endpoints.get('get_sites'))
        data = self.con.get(url, params)
        return Pagination(self, data, Site) if data.get('data') else []

    def get_site_by_id(self, site_id, params=None):
        url = self.build_url(self._endpoints.get('get_site_by_id').format(site_id=site_id))
        data = self.con.get(url, params)
        return Site(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionsEndpoint(ApiBridge):
    _endpoints = {'get_subscriptions': '/subscriptions',
                  'get_subscription_by_id': '/subscription-forms/{sub_id}'}

    def __init__(self, parent):
        super(SubscriptionsEndpoint, self).__init__(parent)

    def get_subscriptions(self, params=None):
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.get(url, params)
        return Pagination(self, data, Subscription) if data else []

    def get_subscription_by_id(self, sub_id, params=None):
        url = self.build_url(self._endpoints.get('get_subscription_by_id').format(sub_id=sub_id))
        data = self.con.get(url, params)
        return SubscriptionForm(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormsEndpoint(ApiBridge):
    _endpoints = {'get_subscription_forms': '/subscription-forms',
                  'get_subscription_form_id': '/subscription-forms/{sub_form_id}'}

    def __init__(self, parent):
        super(SubscriptionFormsEndpoint, self).__init__(parent)

    def get_subscription_forms(self, params=None):
        url = self.build_url(self._endpoints.get('get_subscription_forms'))
        data = self.con.get(url, params)
        return Pagination(self, data, SubscriptionForm) if data.get('data') else []

    def get_subscription_form_by_id(self, sub_form_id, params=None):
        url = self.build_url(self._endpoints.get('get_subscription_form_by_id').format(sub_form_id=sub_form_id))
        data = self.con.get(url, params)
        return SubscriptionForm(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class TemporaryAbsencesEndpoint(ApiBridge):
    _endpoints = {'get_temporary_absences': '/temporary-absences'}

    def __init__(self, parent):
        super(TemporaryAbsencesEndpoint, self).__init__(parent)

    def get_temporary_absences(self, params=None):
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.get(url, params)
        return Pagination(self, data, TemporaryAbsence) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

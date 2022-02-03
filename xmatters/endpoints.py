from datetime import datetime
import xmatters.factories as factory
import xmatters.xm_objects.forms
from xmatters.connection import ApiBridge
from xmatters.xm_objects.common import Pagination, RequestReference
from xmatters.xm_objects.conference_bridges import ConferenceBridge
from xmatters.xm_objects.device_types import DeviceTypes
from xmatters.xm_objects.dynamic_teams import DynamicTeam
from xmatters.xm_objects.event_supressions import EventSuppression
from xmatters.xm_objects.events import Event
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
import xmatters.utils as util


class AuditsEndpoint(ApiBridge):
    """ Used to interact with '/audit' endpoint """

    def __init__(self, parent):
        """
        :param parent: XMSession instance
        :type parent: :class:`xmatters.session.XMSession`
        """
        super(AuditsEndpoint, self).__init__(parent)

        self._endpoints = {'get_audit': '/audits'}

    def get_audit(self, event_id, audit_type=None, sort_order=None, params=None):
        """
        Perform an audit on a specified event id.
        :param event_id: xMatters event id
        :type event_id: str
        :param audit_type: Comma-separated list of audit types
        :type audit_type: str or list, optional
        :param sort_order: Sort order of the results
        :type sort_order: str, optional
        :param params: Parameters to apply to the request
        :type params: dict, optional
        :return: Pagination of audit objects
        :rtype: :class:`xmatters.xm_objects.common.Pagination`
        """

        audit_type = ','.join(audit_type) if isinstance(audit_type, list) else audit_type
        arg_params = {'eventId': event_id, 'auditType': audit_type, 'sortOrder': sort_order}
        url = self.build_url(self._endpoints.get('get_audit'))
        data = self.con.get(url=url, params=self.build_params(arg_params, params))
        return Pagination(self, data, factory.audit) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesEndpoint(ApiBridge):
    """ Used to interact with '/devices' endpoint """
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}'}

    def __init__(self, parent):
        """
        :param parent: XMSession instance
        :type parent: :class:`xmatters.session.XMSession`
        """
        super(DevicesEndpoint, self).__init__(parent)

    def get_devices(self, device_status=None, device_type=None, device_names=None, phone_number_format=None,
                    params=None):
        device_names = ','.join(device_names) if isinstance(device_names, list) else device_names
        arg_params = {'deviceStatus': device_status, 'deviceType': device_type,
                      'phoneNumberFormat': phone_number_format, 'deviceNames': device_names}
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url=url, params=self.build_params(arg_params, params))
        return Pagination(self, data, factory.device) if data.get('data') else []

    def get_device_by_id(self, device_id, params=None):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url=url, params=params)
        return factory.device(self, data) if data else None

    def create_device(self, data):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.post(url, data=data)
        return factory.device(self, data) if data else None

    def update_device(self, data):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.post(url=url, data=data)
        return factory.device(self, data) if data else None

    def delete_device(self, device_id):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.delete(url=url)
        return factory.device(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNamesEndpoint(ApiBridge):
    _endpoints = {'get_device_names': '/device-names',
                  'delete_device_name': '/device-names/{device_name_id}'}

    def __init__(self, parent):
        super(DeviceNamesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_device_names(self, device_types=None, search=None, sort_by=None, sort_order=None, params=None):
        device_types = ','.join(device_types) if isinstance(device_types, list) else device_types
        arg_params = {'search': search, 'sortBy': sort_by, 'sortOrder': sort_order, 'deviceTypes': device_types}
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.get(url=url, params=self.build_params(arg_params, params))
        return Pagination(self, data, factory.device_name) if data.get('data') else []

    def create_device_name(self, data):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.post(url, data=data)
        return factory.device_name(data) if data else None

    def update_device_name(self, data):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.post(url, data=data)
        return factory.device_name(data) if data else None

    def delete_device_name(self, device_name_id):
        url = self.build_url(self._endpoints.get('delete_device_name').format(device_name_id=device_name_id))
        data = self.con.delete(url)
        return factory.device_name(data) if data else None

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

    # TODO: Test
    def create_dynamic_team(self, data):
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    # TODO: Test
    def update_dynamic_team(self, data):
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    # TODO: Test
    def delete_dynamic_team(self, dynamic_team_id):
        url = self.build_url(self._endpoints.get('get_dynamic_team_by_id').format(dynamic_team_id=dynamic_team_id))
        data = self.con.delete(url=url)
        return DynamicTeam(self, data) if data else None

    def __init__(self, parent):
        super(DynamicTeamsEndpoint, self).__init__(parent)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventsEndpoint(ApiBridge):
    _endpoints = {'get_events': '/events',
                  'get_event_by_id': '/events/{event_id}',
                  'trigger_event': '{instance_url}/api/integration/1/functions/{func_id}/triggers'}

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

    # TODO
    # def trigger_event(self, function_id, data, params=None):
    #     url = self._endpoints.get('trigger_event').format(instance_url=self.con.instance_url, func_id=function_id)
    #     data = self.con.post(url, data=data, params=params)
    #     return RequestReference(data) if data else None

    # TODO: Test
    def change_event_status(self, data):
        url = self.build_url(self._endpoints.get('get_events'))
        data = self.con.post(url, data=data)
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

    # TODO: Test
    def create_conference_bridge(self, data):
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    # TODO: Test
    def update_conference_bridge(self, data):
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    # TODO: Test
    def delete_conference_bridge(self, bridge_id):
        url = self.build_url(self._endpoints.get('get_conference_bridge_by_id').format(bridge_id=bridge_id))
        data = self.con.delete(url=url)
        return DynamicTeam(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormsEndpoint(ApiBridge):
    _endpoints = {'get_forms': '/forms',
                  'get_form_by_id': '/forms/{form_id}'}

    def __init__(self, parent):
        super(FormsEndpoint, self).__init__(parent)

    def get_forms(self, params=None):
        url = self.build_url(self._endpoints.get('get_forms'))
        data = self.con.get(url, params)
        return Pagination(self, data, xmatters.xm_objects.forms.Form) if data.get('data') else []

    # TODO: Test
    def get_form_by_id(self, form_id):
        url = self.build_url(self._endpoints.get('get_form_by_id').format(form_id=form_id))
        data = self.con.get(url)
        return xmatters.xm_objects.forms.Form(self, data) if data else None

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

    # TODO: Test
    def create_group(self, data):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    # TODO: Test
    def update_group(self, data):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    # TODO: Test
    def delete_group(self, group_id):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.delete(url)
        return Group(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ImportJobsEndpoint(ApiBridge):
    _endpoints = {'get_import_jobs': '/imports',
                  'get_import_job_by_id': '/imports/{import_id}'}

    def __init__(self, parent):
        super(ImportJobsEndpoint, self).__init__(parent)

    def get_import_jobs(self, params=None):
        url = self.build_url(self._endpoints.get('get_import_jobs'))
        data = self.con.get(url, params).get('data')
        return [Import(self, job) for job in data] if data else []

    # TODO: Test
    def get_import_job_by_id(self, import_id):
        url = self.build_url(self._endpoints.get('get_import_job_by_id').format(import_id=import_id))
        data = self.con.get(url)
        return Import(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentsEndpoint(ApiBridge):
    _endpoints = {'get_incidents': '/incidents',
                  'update_incident': '/incidents/{incident_id}'}

    def __init__(self, parent):
        super(IncidentsEndpoint, self).__init__(parent)

    def get_incidents(self, params=None):
        url = self.build_url(self._endpoints.get('get_incidents'))
        data = self.con.get(url, params)
        return Pagination(self, data, Incident) if data.get('data') else []

    # TODO
    # def trigger_incident(self, data, params=None):
    #     url = self._endpoints.get('trigger_incident').format(instance_url=self.con.instance_url)
    #     data = self.con.post(url, data=data, params=params)
    #     return RequestReference(data) if data else None

    # TODO: Test
    def update_incident(self, incident_id, data):
        url = self.build_url(self._endpoints.get('update_incident').format(incident_id=incident_id))
        data = self.con.post(url, data=data)
        return Incident(self, data) if data else None

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

    # TODO: Test params
    def get_people(self, search=None, operand=None, fields=None, property_names=None, property_values=None,
                   devices_exist=None, devices_test_status=None, site=None, status=None, supervisors_exists=None,
                   groups=None, groups_exist=None, roles=None, supervisors=None, created_from=None, created_to=None,
                   created_before=None, created_after=None, sort_by=None, sort_order=None, at=None, params=None):

        # process list params
        search = '+'.join(search) if isinstance(search, list) else search
        for param in (fields, property_names, property_values, groups, roles, supervisors):
            param = ','.join(param) if isinstance(param, list) else param
        # process time params
        for param in (created_from, created_to, created_before, created_after):
            param = param if isinstance(at, datetime) else util.TimeAttribute(param)
        arg_params = {'search': search, 'operand': operand, 'fields': fields, 'propertyNames': property_names,
                      'propertyValues': property_values, 'devices.exists': devices_exist,
                      'devices.testStatus': devices_test_status, 'site': site, 'status': status,
                      'supervisors.exists': supervisors_exists, 'groups': groups, 'groups.exists': groups_exist,
                      'roles': roles, 'supervisors': supervisors, 'createdFrom': created_from,
                      'createdTo': created_to, 'createdBefore': created_before, 'createdAfter': created_after,
                      'sortBy': sort_by, 'sortOrder': sort_order, 'at': at}
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, self.build_params(arg_params, params))
        return Pagination(self, data, Person) if data.get('data') else []

    def get_person_by_id(self, person_id, params=None):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url, params)
        return Person(self, data) if data else None

    def get_people_by_query(self, first_name=None, last_name=None, target_name=None, web_login=None, phone_number=None,
                            email_address=None):
        if all(p is None for p in (first_name, last_name, target_name, web_login, phone_number, email_address)):
            raise ValueError('must assign a parameter to query by')
        arg_params = {'firstName': first_name,
                      'lastName': last_name,
                      'targetName': target_name,
                      'webLogin': web_login,
                      'phoneNumber': phone_number,
                      'emailAddress': email_address}
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params=self.build_params(arg_params=arg_params))
        return Pagination(self, data, Person) if data.get('data') else []

    # TODO: Test
    def create_person(self, data):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    # TODO: Test
    def update_person(self, data):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    # TODO: Test
    def delete_person(self, person_id):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.delete(url)
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

    # TODO: Test
    def create_plan(self, data):
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    # TODO: Test
    def update_plan(self, data):
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    # TODO: Test
    def delete_plan(self, plan_id):
        url = self.build_url(self._endpoints.get('get_plan_by_id').format(plan_id=plan_id))
        data = self.con.delete(url)
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

    # TODO: Test
    def create_service(self, data):
        url = self.build_url(self._endpoints.get('get_services'))
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    # TODO: Test
    def update_service(self, data):
        url = self.build_url(self._endpoints.get('get_services'))
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    # TODO: Test
    def delete_service(self, service_id):
        url = self.build_url(self._endpoints.get('get_service_by_id').format(service_id=service_id))
        data = self.con.delete(url)
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

    # TODO: Test
    def create_site(self, data):
        url = self.build_url(self._endpoints.get('get_sites'))
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    # TODO: Test
    def update_site(self, data):
        url = self.build_url(self._endpoints.get('get_sites'))
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    # TODO: Test
    def delete_site(self, site_id):
        url = self.build_url(self._endpoints.get('get_site_by_id').format(site_id=site_id))
        data = self.con.delete(url)
        return Site(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionsEndpoint(ApiBridge):
    _endpoints = {'get_subscriptions': '/subscriptions',
                  'get_subscription_by_id': '/subscription-forms/{sub_id}',
                  'get_subscribers': '/subscribers',
                  'unsubscribe_person': '/subscribers/{person_id}'}

    def __init__(self, parent):
        super(SubscriptionsEndpoint, self).__init__(parent)

    def get_subscriptions(self, params=None):
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.get(url, params)
        return Pagination(self, data, Subscription) if data else []

    def get_subscription_by_id(self, subscription_id, params=None):
        url = self.build_url(self._endpoints.get('get_subscription_by_id').format(sub_id=subscription_id))
        data = self.con.get(url, params)
        return SubscriptionForm(self, data) if data else None

    # TODO: Test
    def get_subscribers(self, params=None):
        url = self.build_url(self._endpoints.get('get_subscribers'))
        subscribers = self.con.get(url, params)
        return Pagination(self, subscribers, Person) if subscribers.get('data') else []

    # TODO: Test
    def unsubscribe_person(self, person_id):
        url = self.build_url(self._endpoints.get('unsubscribe_person').format(person_id=person_id))
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    # TODO: Test
    def create_subscription(self, data):
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    # TODO: Test
    def update_subscription(self, data):
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    # TODO: Test
    def delete_subscription(self, subscription_id):
        url = self.build_url(self._endpoints.get('get_subscription_by_id').format(sub_id=subscription_id))
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

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
    _endpoints = {'get_temporary_absences': '/temporary-absences',
                  'delete_temporary_absence': '/temporary-absences/{temp_abs_id}'}

    def __init__(self, parent):
        super(TemporaryAbsencesEndpoint, self).__init__(parent)

    def get_temporary_absences(self, params=None):
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.get(url, params)
        return Pagination(self, data, TemporaryAbsence) if data.get('data') else []

    # TODO: Test
    def create_temporary_absence(self, data):
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.post(url, data=data)
        return TemporaryAbsence(self, data) if data else None

    # TODO: Test
    def delete_temporary_absence(self, temporary_absence_id):
        url = self.build_url(self._endpoints.get('delete_temporary_absence').format(temp_abs_id=temporary_absence_id))
        data = self.con.delete(url)
        return TemporaryAbsence(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


# TODO
class UploadUsersEndpoint(ApiBridge):
    _endpoints = {'upload_user_upload_file': '/uploads/users-v1',
                  'upload_epic_zipsync_file': '/uploads/epic-v1'}

    def __init__(self, parent):
        super(UploadUsersEndpoint, self).__init__(parent)

    def upload_user_upload_file(self, file_path):
        pass

    def upload_epic_zipsync_file(self, file_path):
        pass

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

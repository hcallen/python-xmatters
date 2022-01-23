import xmatters.constructors
from xmatters.audit import Audit
from xmatters.common import Pagination
from xmatters.devices import DeviceTypes
from xmatters.events import Event, DeviceName
from xmatters.groups import Group
from xmatters.oncall import OnCall, OnCallSummary
from xmatters.people import Person
from xmatters.utils.utils import ApiComponent
from xmatters.temporary_absences import TemporaryAbsence


class xMattersSession(ApiComponent):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}',
                  'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}',
                  'get_oncall': '/on-call?groups={group_ids}',
                  'get_oncall_summary': '/on-call-summary?groups={group_ids}',
                  'get_person_by_id': '/people/{person_id}',
                  'get_people': '/people',
                  'get_events': '/events',
                  'get_event_by_id': '/events/{event_id}',
                  'get_temporary_absences': '/temporary-absences',
                  'get_audit': '/audits?{event_id}',
                  'get_device_names': '/device-names',
                  'get_device_types': '/device-types'}

    def __init__(self, auth, timeout=3, retries=3):
        self.con = auth
        self.con.timeout = timeout
        self.con.retries = retries
        super(xMattersSession, self).__init__(self)

    def get_devices(self, params=None):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url, params)
        return Pagination(self, data, xmatters.constructors.device_factory) if data.get('data') else []

    def get_device_by_id(self, device_id, params=None):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url, params)
        return xmatters.constructors.device_factory(self, data) if data else None

    def get_groups(self, params=None):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.get(url, params)
        return Pagination(self, data, Group) if data.get('data') else []

    def get_group_by_id(self, group_id, params=None):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url, params)
        return Group(self, data) if data else None

    def get_person_by_id(self, person_id, params=None):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url, params)
        return Person(self, data) if data else None

    def get_people(self, params=None):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params)
        return Pagination(self, data, Person) if data.get('data') else []

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

    def get_events(self, params=None):
        url = self.build_url(self._endpoints.get('get_events'))
        data = self.con.get(url, params)
        return Pagination(self, data, Event) if data.get('data') else []

    def get_event_by_id(self, event_id, params=None):
        url = self.build_url(self._endpoints.get('get_event_by_id').format(event_id=event_id))
        data = self.con.get(url, params)
        return Event(self, data) if data else None

    def get_temporary_absences(self, params=None):
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.get(url, params)
        return Pagination(self, data, TemporaryAbsence) if data.get('data') else []

    def get_audit(self, params):
        url = self.build_url(self._endpoints.get('get_audit'))
        data = self.con.get(url, params)
        return Pagination(self, data, Audit) if data.get('data') else []

    def get_device_names(self, params=None):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.get(url, params)
        return Pagination(self, data, DeviceName) if data.get('data') else []

    def get_device_types(self, params=None):
        url = self.build_url(self._endpoints.get('get_device_types'))
        data = self.con.get(url, params)
        return DeviceTypes(data) if data else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.con.base_url)

    def __str__(self):
        return self.__repr__()

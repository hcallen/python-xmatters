import xmatters.constructors
from xmatters.common import Pagination
from xmatters.groups import Group
from xmatters.oncall import OnCall
from xmatters.people import Person
from xmatters.utils import ApiComponent



class xMattersSession(ApiComponent):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}',
                  'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}',
                  'get_oncall': '/on-call?groups={group_ids}',
                  'get_person_by_id': '/people/{person_id}',
                  'get_people': '/people'}

    def __init__(self, auth, timeout=3, retries=3):
        self.con = auth
        self.con.timeout = timeout
        self.con.retries = retries
        super(xMattersSession, self).__init__(self)

    def get_devices(self, params=None):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url, params)
        return Pagination(self, data, xmatters.constructors.device_factory)

    def get_device_by_id(self, device_id, params=None):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url, params)
        return xmatters.constructors.device_factory(self, data)

    def get_groups(self, params=None):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.get(url, params)
        return Pagination(self, data, Group)

    def get_group_by_id(self, group_id, params=None):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url, params)
        return Group(self, data)

    def get_person_by_id(self, person_id, params=None):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url, params)
        return Person(self, data)

    def get_people(self, params=None):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params)
        return Pagination(self, data, Person)

    def get_oncall(self, group_ids, params=None):
        if isinstance(group_ids, list):
            group_ids = ','.join(group_ids)
        url = self.build_url(self._endpoints.get('get_oncall').format(group_ids=group_ids))
        data = self.con.get(url, params)
        return Pagination(self, data, OnCall)

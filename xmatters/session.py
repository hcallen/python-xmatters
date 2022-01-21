from .devices import device_constructor
from .groups import Group
from .oncall import OnCall
from .people import Person
from .utils import ApiComponent


class xMattersSession(ApiComponent):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}',
                  'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}',
                  'get_oncall': '/on-call?groups={group_ids}',
                  'get_person_by_id': '/people/{person_id}',
                  'get_people': '/people'}

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.con = auth
        super(xMattersSession, self).__init__(self)

    def get_devices(self):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url).get('data')
        return [device_constructor(device)(self, device) for device in data]

    def get_device_by_id(self, device_id):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url)
        return device_constructor(data)(self, data)

    def get_groups(self):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.get(url).get('data')
        return [Group(self, group) for group in data]

    def get_group_by_id(self, group_id):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url)
        return Group(self, data)

    def get_person_by_id(self, person_id):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url)
        return Person(self, data)

    def get_people(self):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url).get('data')
        return [Person(self, person) for person in data]

    def get_oncall(self, group_ids):
        url = self.build_url(self._endpoints.get('get_oncall').format(group_ids=group_ids))
        data = self.con.get(url).get('data')
        return [OnCall(self, oncall) for oncall in data]

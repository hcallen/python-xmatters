from xmatters.device import Device
from xmatters.group import Group
from xmatters.person import Person
from xmatters.utils import ApiComponent


class xMattersSession(ApiComponent):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}',
                  'get_groups': '/groups',
                  'get_group_by_ip': '/groups/{group_id}',
                  'get_person_by_id': '/people/{person_id}',
                  'get_people': '/people'}

    person_constructor = Person
    device_constructor = Device
    group_constructor = Group

    def __init__(self, parent):
        super(xMattersSession, self).__init__(parent)

    def get_devices(self):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.s.get(url).json()
        return [self.device_constructor(self, device) for device in data.get('data')]

    def get_device_by_id(self, device_id):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.s.get(url).json()
        return self.person_constructor(self, data)

    def get_groups(self):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.s.get(url).json()
        print(data)
        return [self.group_constructor(self, group) for group in data.get('data')]

    def get_group_by_id(self, group_id):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.s.get(url).json()
        return self.group_constructor(self, data)

    def get_person_by_id(self, person_id):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.s.get(url).json()
        return self.person_constructor(self, data)

    def get_people(self):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.s.get(url).json()
        return [self.person_constructor(self, person) for person in data.get('data')]

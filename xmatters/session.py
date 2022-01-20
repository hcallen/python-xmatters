from .devices import device_constructor
from .groups import Group
from .oncall import OnCall
from .people import Person
from .utils import ApiComponent
from .auth import BasicAuth, OAuth


class Session(ApiComponent):
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}',
                  'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}',
                  'get_oncall_by_id': '/on-call?groups={group_id}',
                  'get_person_by_id': '/people/{person_id}',
                  'get_people': '/people'}

    def __init__(self, base_url):
        if base_url.endswith('/'):
            self.base_url = base_url[:-1]
        else:
            self.base_url = base_url
        self.con = None
        super(Session, self).__init__(self)

    def authenticate(self, credentials=None, client_id=None, refresh_token=None, token_path=None):
        if client_id and credentials:
            pass
        elif credentials:
            self.con = BasicAuth(credentials)

    def get_devices(self):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url).json().get('data')
        return [device_constructor(device)(self, device) for device in data]

    def get_device_by_id(self, device_id):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url).json()
        return device_constructor(data)(self, data)

    def get_groups(self):
        url = self.build_url(self._endpoints.get('get_groups'))
        r = self.con.get(url)
        data = self.con.get(url).json().get('data')
        return [Group(self, group) for group in data]

    def get_group_by_id(self, group_id):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url).json()
        return Group(self, data)

    def get_person_by_id(self, person_id):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url).json()
        return Person(self, data)

    def get_people(self):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url).json().get('data')
        return [Person(self, person) for person in data]

    def get_oncall_by_id(self, group_id):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url).json().get('data')
        return [OnCall(self, oncall) for oncall in data]

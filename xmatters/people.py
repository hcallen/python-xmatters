from .devices import device_constructor
from .common import Recipient, Role


class Person(Recipient):
    _endpoints = {'get_devices': '/devices',
                  'roles': '?embed=roles'}

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.license_type = data.get('licenseType')
        self.language = data.get('language')
        self.timezone = data.get('timezone')
        self.web_login = data.get('webLogin')
        self.last_login = data.get('lastLogin')
        self.when_created = data.get('whenCreated')
        self.when_updated = data.get('whenUpdated')
        self.phone_login = data.get('phoneLogin')
        self.phone_pin = data.get('phonePin')
        self.properties = data.get('properties')

    @property
    def roles(self):
        url = self.build_url(self._endpoints.get('roles'))
        data = self.con.get(url).get('roles', {}).get('data', [])
        return [Role(role) for role in data]

    @property
    def devices(self):
        return self.get_devices()

    def get_devices(self):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url).get('data')
        return [device_constructor(device)(self, device) for device in data]

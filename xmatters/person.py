from xmatters.device import device_constructors
from xmatters.common import Recipient, Role


class Person(Recipient):
    _endpoints = {'get_devices': '/devices',
                  'roles': '?embed=roles'}
    device_constructor = device_constructors

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
        data = self.s.get(url).json()
        return [Role(role) for role in data.get('roles').get('data')]

    @property
    def devices(self):
        return self.get_devices()

    def get_devices(self):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.s.get(url).json()
        return [self.device_constructor[device.get('deviceType')](self, device) for device in data.get('data')]

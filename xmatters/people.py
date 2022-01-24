import xmatters.utils.constructors
from xmatters.common import Recipient, SelfLink
from xmatters.roles import Role
from xmatters.utils.connection import ApiBridge


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

    def get_devices(self, params=None):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url, params).get('data')
        return [xmatters.utils.constructors.device_factory(self, device) for device in data]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class PersonReference(ApiBridge):
    def __init__(self, parent, data):
        super(PersonReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()

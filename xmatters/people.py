import xmatters.utils.factories
import xmatters.utils.utils
from xmatters.common import Recipient, SelfLink, Pagination
from xmatters.roles import Role
from xmatters.utils.connection import ApiBridge


class Person(Recipient):
    _endpoints = {'get_devices': '/devices',
                  'roles': '?embed=roles',
                  'get_supervisors': '/supervisors',
                  'supervisors': '?embed=supervisors'}

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.license_type = data.get('licenseType')
        self.language = data.get('language')
        self.timezone = data.get('timezone')
        self.web_login = data.get('webLogin')
        self.phone_login = data.get('phoneLogin')
        self.phone_pin = data.get('phonePin')
        self.properties = data.get('properties', {})
        last_login = data.get('lastLogin')
        when_created = data.get('whenCreated')
        when_updated = data.get('whenUpdated')
        self.last_login = xmatters.utils.utils.TimeAttribute(last_login) if last_login else None
        self.when_created = xmatters.utils.utils.TimeAttribute(when_created) if when_created else None
        self.when_updated = xmatters.utils.utils.TimeAttribute(when_updated) if when_updated else None

    @property
    def roles(self):
        url = self.build_url(self._endpoints.get('roles'))
        data = self.con.get(url).get('roles', {})
        return Pagination(self, data, Role) if data.get('data') else []

    @property
    def devices(self):
        return self.get_devices()

    @property
    def supervisors(self):
        url = self.build_url(self._endpoints.get('supervisors'))
        data = self.con.get(url).get('supervisors', {})
        return Pagination(self, data, Person) if data.get('data') else []

    def get_supervisors(self):
        return self.supervisors

    # Does the '/supervisors' endpoint work?
    # def get_supervisors(self, params=None):
    #     url = self.build_url(self._endpoints.get('get_supervisors'))
    #     s = self.con.get(url, params)
    #     return Pagination(self, s, Person) if s.get('data') else []

    def get_devices(self, params=None):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url, params).get('data')
        return [xmatters.utils.factories.device_factory(self, device) for device in data]

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

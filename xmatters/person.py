from xmatters.device import Device
from xmatters.utils import ApiComponent


class Person(ApiComponent):
    _endpoints = {'get_devices': '/devices'}
    device_constructor = Device

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)

        self.object_id = data.get('id')
        self.target_name = data.get('targetName')
        self.externally_owned = data.get('externallyOwned')
        self.recipient_type = data.get('recipientType')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.license_type = data.get('licenseType')
        self.language = data.get('language')
        self.timezone = data.get('timezone')
        self.web_login = data.get('webLogin')
        self.last_login = data.get('lastLogin')
        self.when_created = data.get('whenCreated')
        self.when_updated = data.get('whenUpdated')
        self.status = data.get('status')
        self.phone_login = data.get('phoneLogin')
        self.phone_pin = data.get('phonePin')
        self.properties = data.get('properties')

    def get_devices(self):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.s.get(url).json()
        return [self.device_constructor(self, device) for device in data.get('data')]


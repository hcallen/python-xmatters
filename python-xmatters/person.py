from utils import ApiComponent


class Person(ApiComponent):
    _endpoints = {'get_devices': '/people'}

    def __init__(self, parent, person_data):
        super(Person, self).__init__(parent)

        self.object_id = person_data.get('id')
        self.target_name = person_data.get('targetName')
        self.externally_owned = person_data.get('externallyOwned')
        self.recipient_type = person_data.get('recipientType')
        self.first_name = person_data.get('firstName')
        self.last_name = person_data.get('lastName')
        self.license_type = person_data.get('licenseType')
        self.language = person_data.get('language')
        self.timezone = person_data.get('timezone')
        self.web_login = person_data.get('webLogin')
        self.last_login = person_data.get('lastLogin')
        self.when_created = person_data.get('whenCreated')
        self.when_updated = person_data.get('whenUpdated')
        self.status = person_data.get('status')

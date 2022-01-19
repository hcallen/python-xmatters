from xmatters.person import Person
from xmatters.utils import ApiComponent


class Group(ApiComponent):
    _endpoints = {'get_supervisors': '/supervisors'}
    supervisor_constructor = Person

    def __init__(self, parent, data):
        super(Group, self).__init__(parent, data)
        self.object_id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.status = data.get('status')
        self.externally_owned = data.get('externallyOwned')
        self.allow_duplicates = data.get('allowDuplicates')
        self.use_default_devices = data.get('useDefaultDevices')
        self.observed_by_all = data.get('observedByAll')
        self.description = data.get('description')
        self.created = data.get('created')
        self.group_type = data.get('groupType')

    def get_supervisors(self):
        url = self.build_url(self._endpoints.get('get_supervisors'))
        data = self.s.get(url).json()
        print(data)
        return [self.supervisor_constructor(self, person) for person in data.get('data')]

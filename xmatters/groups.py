from xmatters.person import Person
from xmatters.utils import ApiComponent
from xmatters.common import Recipient, Role, SelfLink


class GroupReference(ApiComponent):
    def __init__(self, parent, data):
        super(GroupReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.links = SelfLink(data.get('links'))


class Group(Recipient):
    _endpoints = {'get_supervisors': '/supervisors',
                  'observers': '?embed=observers',
                  'get_oncall': '?groups={group_id}'}
    supervisor_constructor = Person

    def __init__(self, parent, data):
        super(Group, self).__init__(parent, data)
        self.allow_duplicates = data.get('allowDuplicates')
        self.description = data.get('description')
        self.observed_by_all = data.get('observedByAll')
        self.response_count = data.get('responseCount')
        self.response_count_threshold = data.get('responseCount')
        self.use_default_devices = data.get('responseCountThreshold')
        self.created = data.get('created')
        self.group_type = data.get('groupType')

    @property
    def observers(self):
        url = self.build_url(self._endpoints.get('observers'))
        data = self.s.get(url).json()
        return [Role(role) for role in data.get('observers').get('data')]

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_supervisors(self):
        url = self.build_url(self._endpoints.get('get_supervisors'))
        data = self.s.get(url).json()
        return [self.supervisor_constructor(self, person) for person in data.get('data')]

    def get_oncall(self):
        url = self.build_url(self._endpoints.get('get_oncall'))
        data = self.s.get(url).json()

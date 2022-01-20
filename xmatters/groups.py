from .oncall import OnCall
from .people import Person
from .common import Recipient, Role
from .shifts import Shift


class Group(Recipient):
    _endpoints = {'get_supervisors': '/supervisors',
                  'get_oncall': '{base_url}/on-call?groups={group_id}',
                  'observers': '?embed=observers',
                  'get_shifts': '/shifts'}

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
        data = self.con.get(url).json()
        return [Role(role) for role in data.get('observers').get('data')]

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_supervisors(self):
        url = self.build_url(self._endpoints.get('get_supervisors'))
        data = self.con.get(url).json().get('data')
        return [Person(self, person) for person in data]

    def get_oncall(self):
        url = self._endpoints.get('get_oncall').format(base_url=self.base_url, group_id=self.id)
        data = self.con.get(url).json().get('data')
        return [OnCall(self, oncall) for oncall in data]

    def get_shifts(self):
        url = self.build_url(self._endpoints.get('get_shifts'))
        data = self.con.get(url).json().get('data')
        return [Shift(self, shift) for shift in data]

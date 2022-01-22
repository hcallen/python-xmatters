from xmatters.common import Recipient
from xmatters.oncall import OnCall
from xmatters.people import Person
from xmatters.roles import Role
from xmatters.shifts import Shift
from xmatters.common import Pagination

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
        data = self.con.get(url).get('observers').get('data')
        return [Role(role) for role in data]

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_supervisors(self, params=None):
        url = self.build_url(self._endpoints.get('get_supervisors'))
        data = self.con.get(url, params=params).get('data')
        return [Person(self, person) for person in data]

    def get_oncall(self, params=None):
        url = self._endpoints.get('get_oncall').format(base_url=self.base_url, group_id=self.id)
        data = self.con.get(url, params=params).get('data')
        return [OnCall(self, oncall) for oncall in data]

    def get_shifts(self, params=None):
        url = self.build_url(self._endpoints.get('get_shifts'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Shift)

    def __repr__(self):
        return '<Group {}>'.format(self.target_name)

    def __str__(self):
        return self.__repr__()




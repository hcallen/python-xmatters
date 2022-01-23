from xmatters.common import Recipient, Pagination
from xmatters.people import Person
from xmatters.roles import Role


class DynamicTeam(Recipient):
    _endpoints = {'supervisors': '?embed=supervisors',
                  'observers': '?embed=observers'}

    def __init__(self, parent, data):
        super(DynamicTeam, self).__init__(parent, data)
        self.response_count = data.get('responseCount')
        self.response_count_threshold = data.get('responseCountThreshold')
        self.use_emergency_device = data.get('useEmergencyDevice')
        self.description = data.get('description')
        criteria = data.get('criteria')  # TODO

    @property
    def observers(self):
        url = self.build_url(self._endpoints.get('observers'))
        observers = self.con.get(url).get('observers', {}).get('data')
        return [Role(role) for role in observers] if observers else []

    @property
    def supervisors(self, params=None):
        url = self.build_url(self._endpoints.get('supervisors'))
        data = self.con.get(url, params)
        return Pagination(self, data, Person) if data.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()

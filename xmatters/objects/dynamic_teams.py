from xmatters.objects.common import Recipient, SelfLink
from xmatters.utils import Pagination
from xmatters.objects.people import Person
from xmatters.objects.roles import Role


class DynamicTeamsCriterion(object):
    def __init__(self, data):
        self.criterion_type = data.get('criterionType')  #: :vartype: str
        self.field = data.get('field')  #: :vartype: str
        self.operand = data.get('operand')  #: :vartype: str
        self.category = data.get('category')  #: :vartype: str
        self.value = data.get('value')  #: :vartype: str


class DynamicTeamsReference(object):
    def __init__(self, data):
        self.id = data.get('criterionType')  #: :vartype: str
        self.target_name = data.get('targetName')  #: :vartype: str
        self.recipient_type = data.get('recipientType')  #: :vartype: str


class DynamicTeam(Recipient):

    def __init__(self, parent, data):
        super(DynamicTeam, self).__init__(parent, data)
        self.response_count = data.get('responseCount')  #: :vartype: int
        self.response_count_threshold = data.get('responseCountThreshold')  #: :vartype: str
        self.use_emergency_device = data.get('useEmergencyDevice')  #: :vartype: bool
        self.description = data.get('description')  #: :vartype: str
        criteria = data.get('criteria')
        self.criteria = DynamicTeamsCriterion(
            criteria) if criteria else None  #: :vartype: :class:`~xmatters.objects.dynamic_teams.DynamicTeamsCriterion`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def observers(self):
        """ Alias of :meth:`get_observers` """
        return self.get_observers()

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_members(self):
        url = self._get_url('/members')
        data = self.con.get(url)
        return Pagination(self, data, Person) if data.get('data') else None

    def get_observers(self):
        url = self._get_url('?embed=observers')
        observers = self.con.get(url).get('observers', {}).get('data')
        return [Role(role) for role in observers] if observers else []

    def get_supervisors(self):
        url = self._get_url('?embed=supervisors')
        supervisors = self.con.get(url).get('supervisors', {})
        return Pagination(self, supervisors, Person) if supervisors.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()

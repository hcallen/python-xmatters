import xmatters.utils
from xmatters.endpoints.common import Recipient, ReferenceByIdAndSelfLink, RecipientReference
from xmatters.endpoints.oncall import OnCall, SelfLink
from xmatters.endpoints.people import Person
from xmatters.endpoints.roles import Role
from xmatters.endpoints.shifts import Shift, GroupReference
from xmatters.endpoints.common import Pagination
from xmatters.connection import ApiBridge


class GroupMembershipShiftReference(ApiBridge):
    """ Custom object for shift information embedded in a group membership response """

    def __int__(self, parent, data):
        super(GroupMembershipShiftReference, self).__init__(parent, data)
        self.id = data.get('id')
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None
        self.name = data.get('name')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class GroupMembership(ApiBridge):
    _endpoints = {'shifts': '/groups/{group_id}/members?embed=shifts'}

    def __init__(self, parent, data):
        super(GroupMembership, self).__init__(parent, data)
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None
        member = data.get('member')
        self.member = RecipientReference(self, member) if member else None
        shifts = data.get('shifts')
        self.shifts = Pagination(self, shifts, GroupMembershipShiftReference) if shifts.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Group(Recipient):
    _endpoints = {'get_supervisors': '/supervisors',
                  'get_oncall': '{base_url}/on-call?groups={group_id}',
                  'observers': '?embed=observers',
                  'get_shifts': '/shifts',
                  'get_members': '/members?embed=shifts',
                  'get_shift_by_id': '/shifts/{shift_id}'}

    def __init__(self, parent, data):
        super(Group, self).__init__(parent, data)
        self.allow_duplicates = data.get('allowDuplicates')
        self.description = data.get('description')
        self.observed_by_all = data.get('observedByAll')
        self.response_count = data.get('responseCount')
        self.response_count_threshold = data.get('responseCount')
        self.use_default_devices = data.get('responseCountThreshold')
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None
        self.group_type = data.get('groupType')
        site = data.get('site')
        self.site = ReferenceByIdAndSelfLink(self, site) if site else None
        self.services = data.get('services', [])

    @property
    def observers(self):
        url = self.build_url(self._endpoints.get('observers'))
        observers = self.con.get(url).get('observers', {}).get('data')
        return [Role(role) for role in observers] if observers else []

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_supervisors(self, params=None):
        url = self.build_url(self._endpoints.get('get_supervisors'))
        data = self.con.get(url, params)
        return Pagination(self, data, Person) if data.get('data') else []

    def get_oncall(self, params=None):
        url = self._endpoints.get('get_oncall').format(base_url=self.con.base_url, group_id=self.id)
        data = self.con.get(url, params=params)
        return Pagination(self, data, OnCall) if data.get('data') else []

    def get_shifts(self, params=None):
        url = self.build_url(self._endpoints.get('get_shifts'))
        data = self.con.get(url, params)
        return Pagination(self, data, Shift) if data.get('data') else []

    def get_shift_by_id(self, shift_id):
        url = self.build_url(self._endpoints.get('get_shift_by_id').format(shift_id=shift_id))
        data = self.con.get(url)
        return Shift(self, data) if data else None

    def get_members(self, params=None):
        url = self.build_url(self._endpoints.get('get_members'))
        data = self.con.get(url, params)
        return Pagination(self, data, GroupMembership) if data.get('data') else []

    def get_observers(self):
        return self.observers

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()

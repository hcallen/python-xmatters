import xmatters.factories

import xmatters.objects.sites
import xmatters.objects.common
import xmatters.objects.utils
import xmatters.utils
from xmatters.objects.roles import Role
from xmatters.utils import ApiBase
import xmatters.objects.groups


class UserQuota(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(UserQuota, self).__init__(parent, data)
        self.stakeholder_users_enabled = data.get('stakeholderUsersEnabled')  #: :vartype: bool
        stakeholder_users = data.get('stakeholderUsers')
        self.stakeholder_users = xmatters.objects.common.QuotaItem(self, stakeholder_users) if stakeholder_users else None  #: :vartype: :class:`~xmatters.objects.common.QuotaItem`
        full_users = data.get('fullUsers')
        self.full_users = xmatters.objects.common.QuotaItem(self, full_users) if full_users else None  #: :vartype: :class:`~xmatters.objects.common.QuotaItem`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Person(xmatters.objects.common.Recipient):

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)
        self.first_name = data.get('firstName')  #: :vartype: str
        self.last_name = data.get('lastName')  #: :vartype: str
        self.license_type = data.get('licenseType')  #: :vartype: str
        self.language = data.get('language')  #: :vartype: str
        self.timezone = data.get('timezone')  #: :vartype: str
        self.web_login = data.get('webLogin')  #: :vartype: str
        self.phone_login = data.get('phoneLogin')  #: :vartype: str
        self.phone_pin = data.get('phonePin')  #: :vartype: str
        self.properties = data.get('properties', {})  #: :vartype: dict
        last_login = data.get('lastLogin')
        self.last_login = xmatters.objects.utils.TimeAttribute(last_login) if last_login else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        when_created = data.get('whenCreated')
        self.when_created = xmatters.objects.utils.TimeAttribute(when_created) if when_created else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        when_updated = data.get('whenUpdated')
        self.when_updated = xmatters.objects.utils.TimeAttribute(when_updated) if when_updated else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, data) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        site = data.get('site')
        self.site = xmatters.objects.sites.SiteReference(self, site) if site else None  #: :vartype: :class:`~xmatters.objects.sites.SiteReference`

    @property
    def full_name(self):
        """

        :rtype: str
        """
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def roles(self):
        """ Alias for :meth:`get_roles` """
        return self.get_roles()

    @property
    def devices(self):
        """ Alias for :meth:`get_devices` """
        return self.get_devices()

    @property
    def supervisors(self):
        """ Alias for :meth:`get_supervisors` """
        return self.get_supervisors()

    def get_roles(self):
        """

        :rtype: :class:`~xmatters.objects.utils.Pagination` of :class:`~xmatters.objects.roles.Role`
        """
        url = self._get_url('?embed=roles')
        data = self._con.get(url)
        roles = data.get('roles', {})
        return xmatters.objects.utils.Pagination(self, roles, Role) if roles.get('data') else []

    def get_supervisors(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.utils.Pagination` of :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url('/supervisors')
        s = self._con.get(url, params=params, **kwargs)
        return xmatters.objects.utils.Pagination(self, s, Person) if s.get('data') else []

    def get_devices(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.utils.Pagination` of :class:`~xmatters.factories.DeviceFactory`
        """
        url = self._get_url('/devices')
        devices = self._con.get(url, params=params, **kwargs)
        return xmatters.objects.utils.Pagination(self, devices, xmatters.factories.DeviceFactory) if devices.get('data') else []

    def get_groups(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.utils.Pagination` of :class:`~xmatters.objects.groups.GroupMembership`
        """
        url = self._get_url('/group-memberships')
        groups = self._con.get(url, params=params, **kwargs)
        return xmatters.objects.utils.Pagination(self, groups, xmatters.objects.groups.GroupMembership) if groups.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()



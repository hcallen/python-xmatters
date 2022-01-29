import xmatters.endpoints.events as events
import xmatters.endpoints.forms as forms
import xmatters.factories as factory
import xmatters.utils
from xmatters.connection import ApiBridge
from xmatters.endpoints.common import Pagination, SelfLink
from xmatters.endpoints.people import PersonReference
from xmatters.endpoints.plans import PlanReference
from xmatters.endpoints.roles import Role


class ScenarioPermission(ApiBridge):
    def __init__(self, parent, data):
        super(ScenarioPermission, self).__init__(parent, data)
        self.permissible_type = data.get('permissibleType')
        self.editor = data.get('editor')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermissionPerson(ScenarioPermission):
    def __init__(self, parent, data):
        super(ScenarioPermissionPerson, self).__init__(parent, data)
        person = data.get('person')
        self.person = PersonReference(self, person) if person else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermissionRole(ScenarioPermission):
    def __init__(self, parent, data):
        super(ScenarioPermissionRole, self).__init__(parent, data)
        role = data.get('role')
        self.role = Role(role) if role else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Scenario(ApiBridge):
    _endpoints = {'properties': '?embed=properties'}

    def __init__(self, parent, data):
        super(Scenario, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        plan = data.get('plan')
        self.plan = PlanReference(plan) if plan else None
        form = data.get('form')
        self.form = xmatters.endpoints.forms.FormReference(form) if form else None
        self.priority = data.get('priority')
        self.position = data.get('position')
        self.bypass_phone_intro = data.get('bypassPhoneIntro')
        self.escalation_override = data.get('escalationOverride')
        self.expiration_in_minutes = data.get('expirationInMinutes')
        self.override_device_restrictions = data.get('overrideDeviceRestrictions')
        self.require_phone_password = data.get('requirePhonePassword')
        sender_overrides = data.get('senderOverrides')
        self.sender_overrides = forms.SenderOverrides(sender_overrides) if sender_overrides else None
        vm_opts = data.get('voicemailOptions')
        self.voicemail_options = events.VoicemailOptions(vm_opts) if vm_opts else None
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, factory.device_name) if tdns.get('data') else []
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None
        perm = data.get('permitted', {}).get('data')
        self.permitted = [factory.scenario_permission(self, p) for p in perm] if perm else []
        rs = data.get('recipients')
        self.recipients = Pagination(self, factory.recipient(self, data), rs) if rs.get('data') else None
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def properties(self):
        url = self.build_url(self._endpoints.get('properties'))
        data = self.con.get(url)
        return data.get('properties', {})

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

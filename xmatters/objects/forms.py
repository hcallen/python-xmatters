import xmatters.connection
import xmatters.factories
import xmatters.objects.common
import xmatters.objects.events
import xmatters.objects.plans
import xmatters.objects.scenarios
import xmatters.utils
from xmatters.objects.device_names import TargetDeviceNameSelector
from xmatters.objects.utils import Pagination


class Form(xmatters.utils.ApiBase):
    _endpoints = {'response_options': '?embed=responseOptions',
                  'get_response_options': '/response-options',
                  'get_sections': '{base_url}/forms/{form_id}/sections',
                  'recipients': '?embed=recipients',
                  'get_scenarios': '/scenarios'}

    def __init__(self, parent, data):
        super(Form, self).__init__(parent, data)
        self.id = data.get('id')     #: :vartype: str
        self.form_id = data.get('formId')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        self.description = data.get('description')   #: :vartype: str
        self.mobile_enabled = data.get('mobileEnabled')   #: :vartype: str
        self.ui_enabled = data.get('uiEnabled')    #: :vartype: bool
        self.api_enabled = data.get('apiEnabled')     #: :vartype: bool
        sender_overrides = data.get('senderOverrides')
        self.sender_overrides = SenderOverrides(self, sender_overrides) if sender_overrides else None    #: :vartype: :class:`~xmatters.objects.forms.SenderOverrides`
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, data) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.trigger_type = data.get('triggerType')  #: :vartype: str

    @property
    def response_options(self):
        """ Alias of :meth:`get_response_options` """
        return self.get_response_options()

    @property
    def recipients(self):
        """ Alias of :meth:`get_recipients` """
        return self.get_recipients()

    def get_recipients(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('recipients'))
        recipients = self._con.get(url, params=params, **kwargs).get('recipients', {})
        return Pagination(self, recipients, xmatters.factories.RecipientFactory) if recipients.get('data') else []

    def get_response_options(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_response_options'))
        options = self._con.get(url, params=params, **kwargs)
        return Pagination(self, options, xmatters.objects.events.ResponseOption) if options.get(
            'data') else []

    def create_response_options(self, data):
        url = self._get_url(self._endpoints.get('get_response_options'))
        options = self._con.post(url, data=data)
        return Pagination(self, options, xmatters.objects.events.ResponseOption) if options.get(
            'data') else []

    def get_sections(self, params=None, **kwargs):
        url = self._endpoints.get('get_sections').format(base_url=self._con.api_base_url, form_id=self.id)
        s = self._con.get(url, params=params, **kwargs)
        return Pagination(self, s, xmatters.factories.SectionFactory) if s.get('data') else []

    def get_scenarios(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_scenarios'))
        s = self._con.get(url, params=params, **kwargs)
        return Pagination(self, s, xmatters.objects.scenarios.Scenario) if s.get('data') else []

    def create_scenario(self, data):
        url = self._get_url(self._endpoints.get('get_scenarios'))
        data = self._con.post(url, data=data)
        return xmatters.objects.scenarios.Scenario(self, data) if data else None

    def update_scenario(self, data):
        url = self._get_url(self._endpoints.get('get_scenarios'))
        data = self._con.post(url, data=data)
        return xmatters.objects.scenarios.Scenario(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormReference(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(FormReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__)

    def __str__(self):
        return self.__repr__()


class SectionValue(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(SectionValue, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.value = data.get('value')   #: :vartype: str
        self.visible = data.get('visible')   #: :vartype: bool


class FormSection(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(FormSection, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        form = data.get('form')
        self.form = FormReference(self, form) if form else None    #: :vartype: :class:`~xmatters.objects.forms.FormReference`
        self.title = data.get('title')   #: :vartype: str
        self.type = data.get('type')   #: :vartype: str
        self.visible = data.get('visible')   #: :vartype: bool
        self.collapsed = data.get('collapsed')   #: :vartype: bool
        self.order_num = data.get('orderNum')    #: :vartype: int


class SenderOverrides(FormSection):
    def __init__(self, parent, data):
        super(SenderOverrides, self).__init__(parent, data)
        caller_id = data.get('callerId')
        self.caller_id = SectionValue(self, caller_id) if caller_id else None  #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        display_name = data.get('displayName')
        self.display_name = SectionValue(self, display_name) if display_name else None  #: :vartype: :class:`~xmatters.objects.forms.SectionValue`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()


class IncidentSectionItem(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(IncidentSectionItem, self).__init__(parent, data)
        self.value = data.get('value')   #: :vartype: str
        self.order_num = data.get('orderNum')    #: :vartype: int
        self.visible = data.get('visible')   #: :vartype: bool
        self.required = data.get('required')    #: :vartype: bool

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentSection(FormSection):
    def __init__(self, parent, data):
        super(IncidentSection, self).__init__(parent, data)
        summary = data.get('summary')
        self.summary = IncidentSectionItem(self, summary) if summary else None    #: :vartype: :class:`~xmatters.objects.forms.IncidentSectionItem`
        description = data.get('description')
        self.description = IncidentSectionItem(self, description) if description else None    #: :vartype: :class:`~xmatters.objects.forms.IncidentSectionItem`
        severity = data.get('severity')
        self.severity = IncidentSectionItem(self, severity) if severity else None    #: :vartype: :class:`~xmatters.objects.forms.IncidentSectionItem`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferenceBridgeSection(FormSection):
    def __init__(self, parent, data):
        super(ConferenceBridgeSection, self).__init__(parent, data)
        self.bridge_type = data.get('bridgeType')   #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.bridge_type)

    def __str__(self):
        return self.__repr__()


class CustomSectionItems(FormSection):

    def __init__(self, parent, data):
        super(CustomSectionItems, self).__init__(parent, data)
        items = data.get('items')
        self.items = [CustomSection(self, i) for i in items] if items else []    #: :vartype: [:class:`~xmatters.objects.forms.CustomSection`]

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class CustomSection(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(CustomSection, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        form_section = data.get('formSection')
        self.form_section = FormReference(self, form_section) if form_section else None    #: :vartype: :class:`~xmatters.objects.forms.FormReference`
        self.order_num = data.get('orderNum')   #: :vartype: int
        self.required = data.get('required')    #: :vartype: bool
        self.multiline_text = data.get('multiLineText')     #: :vartype: bool
        self.visible = data.get('visible')    #: :vartype: bool
        self.include_in_callback = data.get('includeInCallback')   #: :vartype: bool
        property_definition = data.get('propertyDefinition')
        self.property_definition = xmatters.objects.common.PropertyDefinition(self, property_definition) if property_definition else None    #: :vartype: :class:`~xmatters.objects.common.PropertyDefinition`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesSection(FormSection):
    def __init__(self, parent, data):
        super(DevicesSection, self).__init__(parent, data)
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, TargetDeviceNameSelector) if tdns.get('data') else []    #: :vartype: :class:`~xmatters.objects.utils.Pagination` of :class:`~xmatters.objects.device_names.TargetDeviceNameSelector`
        self.target_device_names_id = data.get('targetDeviceNamesId')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class HandlingSection(FormSection):
    def __init__(self, parent, data):
        super(HandlingSection, self).__init__(parent, data)
        threshold = data.get('otherResponseCountThreshold')
        self.other_response_count_threshold = SectionValue(self, threshold) if threshold else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        priority = data.get('priority')
        self.priority = SectionValue(self, priority) if priority else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        expiration_in_minutes = data.get('expirationInMinutes')
        self.expiration_in_minutes = SectionValue(self, expiration_in_minutes) if expiration_in_minutes else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        override = data.get('overrideDeviceRestrictions')
        self.override_device_restrictions = SectionValue(self, override) if override else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        escalation_override = data.get('escalationOverride')
        self.escalation_override = SectionValue(self, escalation_override) if escalation_override else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        bypass_phone_intro = data.get('bypassPhoneIntro')
        self.bypass_phone_intro = SectionValue(self, bypass_phone_intro) if bypass_phone_intro else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        require_phone_password = data.get('requirePhonePassword')
        self.require_phone_password = SectionValue(self, require_phone_password) if require_phone_password else None    #: :vartype: :class:`~xmatters.objects.forms.SectionValue`
        voicemail_options = data.get('voicemailOptions')
        self.voicemail_options = xmatters.objects.events.VoicemailOptions(self, data) if voicemail_options else None    #: :vartype: :class:`~xmatters.objects.events.VoicemailOptions`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientsSection(FormSection):
    def __init__(self, parent, data):
        super(RecipientsSection, self).__init__(parent, data)
        recipients = data.get('recipients', {})
        self.recipients = Pagination(self, recipients, xmatters.objects.common.Recipient) if recipients.get('data') else []    #: :vartype: :class:`~xmatters.objects.utils.Pagination` of :class:`~xmatters.objects.common.Recipient`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SenderOverridesSection(FormSection):
    def __init__(self, parent, data):
        super(SenderOverridesSection, self).__init__(parent, data)
        caller_id = data.get('callerId')    #: :vartype: :class:`~xmatters.objects.forms.SenderOverrides`
        self.caller_id = SectionValue(self, caller_id) if caller_id else None
        display_name = data.get('displayName')
        self.display_name = SectionValue(self, display_name) if display_name else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()



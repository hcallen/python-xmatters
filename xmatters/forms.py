import xmatters.constructors
from xmatters.common import SelfLink, Pagination, Recipient
from xmatters.device_names import TargetDeviceNameSelector
from xmatters.events import VoicemailOptions, ResponseOption
from xmatters.plans import PlanReference
from xmatters.utils.utils import ApiBridge


class PropertyDefinition(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.help_text = data.get('helpText')
        self.default = data.get('default')
        self.max_length = data.get('maxLength')
        self.min_length = data.get('minLength')
        self.pattern = data.get('pattern')
        self.validate = data.get('validate')


class FormReference(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')

    def __repr__(self):
        return '<{}>'.format(self.__class__)

    def __str__(self):
        return self.__repr__()


class SectionValue(object):
    """ Custom """

    def __init__(self, data):
        self.id = data.get('id')
        self.value = data.get('value')
        self.visible = data.get('visible')


class SenderOverrides(object):
    def __init__(self, data):
        caller_id = data.get('callerId')
        self.caller_id = SectionValue(caller_id) if caller_id else None
        display_name = data.get('displayName')
        self.display_name = SectionValue(display_name) if display_name else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormSection(ApiBridge):
    def __init__(self, parent, data):
        super(FormSection, self).__init__(parent, data)
        self.id = data.get('id')
        form = data.get('form')
        self.form = FormReference(form) if form else None
        self.title = data.get('title')
        self.type = data.get('type')
        self.visible = data.get('visible')
        self.collapsed = data.get('collapsed')
        self.order_num = data.get('orderNum')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()


class ConferenceBridgeSection(FormSection):
    def __init__(self, parent, data):
        super(ConferenceBridgeSection, self).__init__(parent, data)
        self.bridge_type = data.get('bridgeType')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.bridge_type)

    def __str__(self):
        return self.__repr__()


class CustomSectionItems(FormSection):
    """ custom """

    def __init__(self, parent, data):
        super(CustomSectionItems, self).__init__(parent, data)
        items = data.get('items')
        self.items = [CustomSection(i) for i in items] if items else []


class CustomSection(object):
    def __init__(self, data):
        self.id = data.get('id')
        form_section = data.get('formSection')
        self.form_section = FormReference(form_section) if form_section else None
        self.order_num = data.get('orderNum')
        self.required = data.get('required')
        self.multiline_text = data.get('multiLineText')
        self.visible = data.get('visible')
        self.include_in_callback = data.get('includeInCallback')
        property_definition = data.get('propertyDefinition')
        self.property_definition = PropertyDefinition(property_definition) if property_definition else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesSection(FormSection):
    def __init__(self, parent, data):
        super(DevicesSection, self).__init__(parent, data)
        devices = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, devices, TargetDeviceNameSelector) if devices.get('data') else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class HandlingSection(FormSection):
    def __init__(self, parent, data):
        super(HandlingSection, self).__init__(parent, data)
        threshold = data.get('otherResponseCountThreshold')
        self.other_response_count_threshold = SectionValue(threshold) if threshold else None
        priority = data.get('priority')
        self.priority = SectionValue(priority) if priority else None
        expiration_in_minutes = data.get('expirationInMinutes')
        self.expiration_in_minutes = SectionValue(expiration_in_minutes) if expiration_in_minutes else None
        override = data.get('overrideDeviceRestrictions')
        self.override_device_restrictions = SectionValue(override) if override else None
        escalation_override = data.get('escalationOverride')
        self.escalation_override = SectionValue(escalation_override) if escalation_override else None
        bypass_phone_intro = data.get('bypassPhoneIntro')
        self.bypass_phone_intro = SectionValue(bypass_phone_intro) if bypass_phone_intro else None
        require_phone_password = data.get('requirePhonePassword')
        self.require_phone_password = SectionValue(require_phone_password) if require_phone_password else None
        voicemail_options = data.get('voicemailOptions')
        self.voicemail_options = VoicemailOptions(data) if voicemail_options else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientsSection(FormSection):
    def __init__(self, parent, data):
        super(RecipientsSection, self).__init__(parent, data)
        recipients = data.get('recipients', {})
        self.recipients = Pagination(self, recipients, Recipient) if recipients.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SenderOverridesSection(FormSection):
    def __init__(self, parent, data):
        super(SenderOverridesSection, self).__init__(parent, data)
        self.sender_overrides = SenderOverrides(data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Form(ApiBridge):
    _endpoints = {'response_options': '?embed=responseOptions',
                  'get_response_options': '/response-options',
                  'get_sections': '{base_url}/forms/{form_id}/sections',
                  'recipients': '?embed=recipients'}

    def __init__(self, parent, data):
        super(Form, self).__init__(parent, data)
        self.id = data.get('id')
        self.form_id = data.get('formId')
        self.name = data.get('name')
        self.description = data.get('description')
        self.mobile_enabled = data.get('mobileEnabled')
        self.ui_enabled = data.get('uiEnabled')
        self.api_enabled = data.get('apiEnabled')
        sender_overrides = data.get('senderOverrides')
        self.sender_overrides = SenderOverrides(sender_overrides) if sender_overrides else None
        plan = data.get('plan')
        self.plan = PlanReference(plan) if plan else None
        links = data.get('links')
        self.links = SelfLink(self, data) if links else None

    @property
    def response_options(self):
        return self.get_response_options()

    @property
    def recipients(self):
        url = self.build_url(self._endpoints.get('recipients'))
        recipients = self.con.get(url).get('recipients',{}).get('data')
        return [Recipient(self, r) for r in recipients] if recipients else []

    def get_response_options(self):
        url = self.build_url(self._endpoints.get('get_response_options'))
        response_options = self.con.get(url)
        return Pagination(self, response_options, ResponseOption) if response_options.get('data') else []

    def get_sections(self):
        url = self._endpoints.get('get_sections').format(base_url=self.con.base_url, form_id=self.id)
        s = self.con.get(url)
        return Pagination(self, s, xmatters.constructors.sections_factory, 'type') if s.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

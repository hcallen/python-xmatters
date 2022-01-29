import xmatters.endpoints.devices
import xmatters.endpoints.groups
import xmatters.endpoints.audit
import xmatters.endpoints.people
import xmatters.endpoints.forms
import xmatters.endpoints.dynamic_teams
import xmatters.endpoints.scenarios
import xmatters.endpoints.device_names
from xmatters.endpoints.plan_endpoints import BasicAuthentication, OAuth2Authentication
from xmatters.endpoints.plan_properties import Boolean, Hierarchy, MultLinkSelectList, SingleSelectList, Number, \
    Password, Text

_devices = {'EMAIL': xmatters.endpoints.devices.EmailDevice,
            'VOICE': xmatters.endpoints.devices.VoiceDevice,
            'TEXT_PHONE': xmatters.endpoints.devices.SMSDevice,
            'TEXT_PAGER': xmatters.endpoints.devices.TextPagerDevice,
            'APPLE_PUSH': xmatters.endpoints.devices.ApplePushDevice,
            'ANDROID_PUSH': xmatters.endpoints.devices.AndroidPushDevice,
            'FAX': xmatters.endpoints.devices.FaxDevice,
            'VOICE_IVR': xmatters.endpoints.devices.PublicAddressDevice,
            'GENERIC': xmatters.endpoints.devices.GenericDevice}


def device_factory(parent, data):
    device_type = data.get('deviceType')
    o = _devices.get(device_type)
    return o(parent, data) if o else None


_recipients = {'GROUP': xmatters.endpoints.groups.Group,
               'PERSON': xmatters.endpoints.people.Person,
               'DEVICE': xmatters.endpoints.devices.Device,
               'DYNAMIC_TEAM': xmatters.endpoints.dynamic_teams.DynamicTeam}


def recipient_factory(parent, data, recipient_type=None):
    recipient_type = data.get('recipientType') if recipient_type is None else recipient_type
    o = _recipients.get(recipient_type)
    return o(parent, data) if o else None


_audit_types = {'EVENT_ANNOTATED': xmatters.endpoints.audit.AuditAnnotation,
                'EVENT_CREATED': xmatters.endpoints.audit.Audit,
                'EVENT_SUSPENDED': xmatters.endpoints.audit.Audit,
                'EVENT_RESUMED': xmatters.endpoints.audit.Audit,
                'EVENT_COMPLETED': xmatters.endpoints.audit.Audit,
                'EVENT_TERMINATED': xmatters.endpoints.audit.Audit,
                'RESPONSE_RECEIVED': xmatters.endpoints.audit.Response}


def audit_factory(parent, data):
    """ For use with audit types """
    audit_type = data.get('type')
    o = _audit_types.get(audit_type)
    return o(parent, data) if o else None


_form_sections = {'CONFERENCE_BRIDGE': xmatters.endpoints.forms.ConferenceBridgeSection,
                  'CUSTOM_SECTION': xmatters.endpoints.forms.CustomSectionItems,
                  'DEVICE_FILTER': xmatters.endpoints.forms.DevicesSection,
                  'HANDLING_OPTIONS': xmatters.endpoints.forms.HandlingSection,
                  'ATTACHMENTS': xmatters.endpoints.forms.FormSection,
                  'SENDER_OVERRIDES': xmatters.endpoints.forms.SenderOverridesSection,
                  'RECIPIENTS': xmatters.endpoints.forms.RecipientsSection,
                  'RESPONSE_CHOICES': xmatters.endpoints.forms.FormSection}


def sections_factory(parent, data, section_type):
    """ For use with form sections """
    o = _form_sections.get(section_type)
    return o(parent, data) if o else None


_auth_types = {'NO_AUTH': None,
               'BASIC': BasicAuthentication,
               'OAUTH2': OAuth2Authentication,
               'OAUTH2_FORCE': OAuth2Authentication,
               'OAUTH_SLACK': OAuth2Authentication}


def auth_factory(data, auth_type):
    """ For use with plan endpoints """
    o = _auth_types.get(auth_type)
    return o(data) if o else None


_properties = {'BOOLEAN': Boolean,
               'HIERARCHY': Hierarchy,
               'LIST_TEXT_MULTI_SELECT': MultLinkSelectList,
               'LIST_TEXT_SINGLE_SELECT': SingleSelectList,
               'NUMBER': Number,
               'PASSWORD': Password,
               'TEXT': Text}


def prop_factory(data):
    """ For use with plan properties """
    prop_type = data.get('propertyType')
    o = _properties.get(prop_type)
    return o(data) if o else None


_scenario_permissions = {'PERSON': xmatters.endpoints.scenarios.ScenarioPermissionPerson,
                         'ROLE': xmatters.endpoints.scenarios.ScenarioPermissionRole}


def scenario_permissions_factory(parent, data):
    """ For use with scenario endpoints """
    perm_type = data.get('permissibleType')
    o = _scenario_permissions.get(perm_type)
    return o(parent, data) if o else None


_device_names = {'EMAIL': xmatters.endpoints.device_names.DeviceNameEmail}


def device_name_factory(data):
    device_type = data.get('deviceType')
    o = _device_names.get(device_type, xmatters.endpoints.device_names.DeviceName)
    return o(data) if o else None

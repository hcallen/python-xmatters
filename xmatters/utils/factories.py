import xmatters.devices
import xmatters.groups
import xmatters.people
import xmatters.dynamic_teams
import xmatters.audit
import xmatters.forms
from xmatters.plan_endpoints import BasicAuthentication, OAuth2Authentication
from xmatters.plan_properties import Boolean, Hierarchy, MultLinkSelectList, SingleSelectList, Number, Password, Text

_devices = {'EMAIL': xmatters.devices.EmailDevice,
            'VOICE': xmatters.devices.VoiceDevice,
            'TEXT_PHONE': xmatters.devices.SMSDevice,
            'TEXT_PAGER': xmatters.devices.TextPagerDevice,
            'APPLE_PUSH': xmatters.devices.ApplePushDevice,
            'ANDROID_PUSH': xmatters.devices.AndroidPushDevice,
            'FAX': xmatters.devices.FaxDevice,
            'VOICE_IVR': xmatters.devices.PublicAddressDevice,
            'GENERIC': xmatters.devices.GenericDevice}


def device_factory(parent, data):
    device_type = data.get('deviceType')
    o = _devices.get(device_type)
    return o(parent, data) if o else None


_recipients = {'GROUP': xmatters.groups.Group,
               'PERSON': xmatters.people.Person,
               'DEVICE': xmatters.devices.Device,
               'DYNAMIC_TEAM': xmatters.dynamic_teams.DynamicTeam}


def recipient_factory(parent, data, recipient_type):
    o = _recipients.get(recipient_type)
    return o(parent, data) if o else None


_audit_types = {'EVENT_ANNOTATED': xmatters.audit.AuditAnnotation,
                'EVENT_CREATED': xmatters.audit.Audit,
                'EVENT_SUSPENDED': xmatters.audit.Audit,
                'EVENT_RESUMED': xmatters.audit.Audit,
                'EVENT_COMPLETED': xmatters.audit.Audit,
                'EVENT_TERMINATED': xmatters.audit.Audit,
                'RESPONSE_RECEIVED': xmatters.audit.Response}


def audit_factory(parent, data):
    """ For use with audit types """
    audit_type = data.get('type')
    o = _audit_types.get(audit_type)
    return o(parent, data) if o else None


_oncall_recipients = {'PERSON': xmatters.people.PersonReference,
                      'GROUP': xmatters.groups.GroupReference,
                      'DYNAMIC_TEAM': xmatters.dynamic_teams.DynamicTeam,
                      'DEVICE': xmatters.devices.Device}


def oncall_recipients_factory(parent, data):
    """ For use with on-call summaries"""
    recipient_type = data.get('recipientType')
    o = _oncall_recipients.get(recipient_type)
    return o(parent, data) if o else None


_form_sections = {'CONFERENCE_BRIDGE': xmatters.forms.ConferenceBridgeSection,
                  'CUSTOM_SECTION': xmatters.forms.CustomSectionItems,
                  'DEVICE_FILTER': xmatters.forms.DevicesSection,
                  'HANDLING_OPTIONS': xmatters.forms.HandlingSection,
                  'ATTACHMENTS': xmatters.forms.FormSection,
                  'SENDER_OVERRIDES': xmatters.forms.SenderOverridesSection,
                  'RECIPIENTS': xmatters.forms.RecipientsSection,
                  'RESPONSE_CHOICES': xmatters.forms.FormSection}


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

import xmatters.xm_objects.devices
import xmatters.xm_objects.groups
import xmatters.xm_objects.audits as audits
import xmatters.xm_objects.people
import xmatters.xm_objects.forms
import xmatters.xm_objects.dynamic_teams
import xmatters.xm_objects.scenarios
import xmatters.xm_objects.device_names
import xmatters.xm_objects.plan_endpoints
import xmatters.xm_objects.plan_properties

_devices = {'EMAIL': xmatters.xm_objects.devices.EmailDevice,
            'VOICE': xmatters.xm_objects.devices.VoiceDevice,
            'TEXT_PHONE': xmatters.xm_objects.devices.SMSDevice,
            'TEXT_PAGER': xmatters.xm_objects.devices.TextPagerDevice,
            'APPLE_PUSH': xmatters.xm_objects.devices.ApplePushDevice,
            'ANDROID_PUSH': xmatters.xm_objects.devices.AndroidPushDevice,
            'FAX': xmatters.xm_objects.devices.FaxDevice,
            'VOICE_IVR': xmatters.xm_objects.devices.PublicAddressDevice,
            'GENERIC': xmatters.xm_objects.devices.GenericDevice}


def device(parent, data):
    device_type = data.get('deviceType')
    o = _devices.get(device_type)
    return o(parent, data) if o else None


_recipients = {'GROUP': xmatters.xm_objects.groups.Group,
               'PERSON': xmatters.xm_objects.people.Person,
               'DEVICE': xmatters.xm_objects.devices.Device,
               'DYNAMIC_TEAM': xmatters.xm_objects.dynamic_teams.DynamicTeam}


def recipient(parent, data, recipient_type=None):
    recipient_type = data.get('recipientType') if recipient_type is None else recipient_type
    o = _recipients.get(recipient_type)
    return o(parent, data) if o else None


_audit_types = {'EVENT_ANNOTATED': audits.AuditAnnotation,
                'EVENT_CREATED': audits.Audit,
                'EVENT_SUSPENDED': audits.Audit,
                'EVENT_RESUMED': audits.Audit,
                'EVENT_COMPLETED': audits.Audit,
                'EVENT_TERMINATED': audits.Audit,
                'RESPONSE_RECEIVED': audits.AuditResponse,
                'NOTIFICATION_DELIVERED': audits.AuditNotification}


def audit(parent, data):
    """ For use with audit types """
    audit_type = data.get('type')
    o = _audit_types.get(audit_type)
    return o(parent, data) if o else None


_form_sections = {'CONFERENCE_BRIDGE': xmatters.xm_objects.forms.ConferenceBridgeSection,
                  'CUSTOM_SECTION': xmatters.xm_objects.forms.CustomSectionItems,
                  'DEVICE_FILTER': xmatters.xm_objects.forms.DevicesSection,
                  'HANDLING_OPTIONS': xmatters.xm_objects.forms.HandlingSection,
                  'ATTACHMENTS': xmatters.xm_objects.forms.FormSection,
                  'SENDER_OVERRIDES': xmatters.xm_objects.forms.SenderOverridesSection,
                  'RECIPIENTS': xmatters.xm_objects.forms.RecipientsSection,
                  'RESPONSE_CHOICES': xmatters.xm_objects.forms.FormSection}


def section(parent, data, section_type):
    """ For use with form sections """
    o = _form_sections.get(section_type)
    return o(parent, data) if o else None


_auth_types = {'NO_AUTH': None,
               'BASIC': xmatters.xm_objects.plan_endpoints.BasicAuthentication,
               'OAUTH2': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
               'OAUTH2_FORCE': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
               'OAUTH_SLACK': xmatters.xm_objects.plan_endpoints.OAuth2Authentication}


def auth(data, auth_type):
    """ For use with plan endpoints """
    o = _auth_types.get(auth_type)
    return o(data) if o else None


_properties = {'BOOLEAN': xmatters.xm_objects.plan_properties .Boolean,
               'HIERARCHY': xmatters.xm_objects.plan_properties .Hierarchy,
               'LIST_TEXT_MULTI_SELECT': xmatters.xm_objects.plan_properties .MultLinkSelectList,
               'LIST_TEXT_SINGLE_SELECT': xmatters.xm_objects.plan_properties .SingleSelectList,
               'NUMBER': xmatters.xm_objects.plan_properties .Number,
               'PASSWORD': xmatters.xm_objects.plan_properties .Password,
               'TEXT': xmatters.xm_objects.plan_properties .Text}


def plan_property(data):
    """ For use with plan properties """
    prop_type = data.get('propertyType')
    o = _properties.get(prop_type)
    return o(data) if o else None


_scenario_permissions = {'PERSON': xmatters.xm_objects.scenarios.ScenarioPermissionPerson,
                         'ROLE': xmatters.xm_objects.scenarios.ScenarioPermissionRole}


def scenario_permission(parent, data):
    """ For use with scenario endpoints """
    perm_type = data.get('permissibleType')
    o = _scenario_permissions.get(perm_type)
    return o(parent, data) if o else None


_device_names = {'EMAIL': xmatters.xm_objects.device_names.DeviceNameEmail}


def device_name(data):
    device_type = data.get('deviceType')
    o = _device_names.get(device_type, xmatters.xm_objects.device_names.DeviceName)
    return o(data) if o else None

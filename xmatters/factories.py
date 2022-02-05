import xmatters.xm_objects.devices
import xmatters.xm_objects.groups
import xmatters.xm_objects.audits
import xmatters.xm_objects.people
import xmatters.xm_objects.dynamic_teams
import xmatters.xm_objects.scenarios
import xmatters.xm_objects.device_names
import xmatters.xm_objects.plan_endpoints
import xmatters.xm_objects.plan_properties
import xmatters.xm_objects.forms

device_types_o = {'EMAIL': xmatters.xm_objects.devices.EmailDevice,
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
    o = device_types_o.get(device_type)
    return o(parent, data) if o else None


recipient_types_o = {'GROUP': xmatters.xm_objects.groups.Group,
                     'PERSON': xmatters.xm_objects.people.Person,
                     'DEVICE': xmatters.xm_objects.devices.Device,
                     'DYNAMIC_TEAM': xmatters.xm_objects.dynamic_teams.DynamicTeam}


def recipient(parent, data, recipient_type=None):
    recipient_type = data.get('recipientType') if recipient_type is None else recipient_type
    o = recipient_types_o.get(recipient_type)
    return o(parent, data) if o else None


audit_types_o = {'EVENT_ANNOTATED': xmatters.xm_objects.audits.AuditAnnotation,
                 'EVENT_CREATED': xmatters.xm_objects.audits.Audit,
                 'EVENT_SUSPENDED': xmatters.xm_objects.audits.Audit,
                 'EVENT_RESUMED': xmatters.xm_objects.audits.Audit,
                 'EVENT_COMPLETED': xmatters.xm_objects.audits.Audit,
                 'EVENT_TERMINATED': xmatters.xm_objects.audits.Audit,
                 'RESPONSE_RECEIVED': xmatters.xm_objects.audits.AuditResponse,
                 'NOTIFICATION_DELIVERED': xmatters.xm_objects.audits.AuditNotification,
                 'NOTIFICATION_FAILED': xmatters.xm_objects.audits.AuditNotification}


def audit(parent, data):
    """ For use with audit types """
    audit_type = data.get('type')
    o = audit_types_o.get(audit_type)
    return o(parent, data) if o else None


form_section_types_o = {'CONFERENCE_BRIDGE': xmatters.xm_objects.forms.ConferenceBridgeSection,
                        'CUSTOM_SECTION': xmatters.xm_objects.forms.CustomSectionItems,
                        'DEVICE_FILTER': xmatters.xm_objects.forms.DevicesSection,
                        'HANDLING_OPTIONS': xmatters.xm_objects.forms.HandlingSection,
                        'ATTACHMENTS': xmatters.xm_objects.forms.FormSection,
                        'SENDER_OVERRIDES': xmatters.xm_objects.forms.SenderOverridesSection,
                        'RECIPIENTS': xmatters.xm_objects.forms.RecipientsSection,
                        'RESPONSE_CHOICES': xmatters.xm_objects.forms.FormSection}


def section(parent, data, section_type):
    """ For use with form sections """
    o = form_section_types_o.get(section_type)
    return o(parent, data) if o else None


auth_types_o = {'NO_AUTH': None,
                'BASIC': xmatters.xm_objects.plan_endpoints.BasicAuthentication,
                'OAUTH2': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
                'OAUTH2_FORCE': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
                'OAUTH_SLACK': xmatters.xm_objects.plan_endpoints.OAuth2Authentication}


def auth(data, auth_type):
    """ For use with plan endpoints """
    o = auth_types_o.get(auth_type)
    return o(data) if o else None


properties_o = {'BOOLEAN': xmatters.xm_objects.plan_properties.Boolean,
                'HIERARCHY': xmatters.xm_objects.plan_properties.Hierarchy,
                'LIST_TEXT_MULTI_SELECT': xmatters.xm_objects.plan_properties.MultLinkSelectList,
                'LIST_TEXT_SINGLE_SELECT': xmatters.xm_objects.plan_properties.SingleSelectList,
                'NUMBER': xmatters.xm_objects.plan_properties.Number,
                'PASSWORD': xmatters.xm_objects.plan_properties.Password,
                'TEXT': xmatters.xm_objects.plan_properties.Text}


def plan_property(data):
    """ For use with plan properties """
    prop_type = data.get('propertyType')
    o = properties_o.get(prop_type)
    return o(data) if o else None


scenario_permissions_o = {'PERSON': xmatters.xm_objects.scenarios.ScenarioPermissionPerson,
                          'ROLE': xmatters.xm_objects.scenarios.ScenarioPermissionRole}


def scenario_permission(parent, data):
    """ For use with scenario endpoints """
    perm_type = data.get('permissibleType')
    o = scenario_permissions_o.get(perm_type)
    return o(parent, data) if o else None


device_names_o = {
    'ANDROID_PUSH': xmatters.xm_objects.device_names.DeviceName,
    'APPLE_PUSH': xmatters.xm_objects.device_names.DeviceName,
    'EMAIL': xmatters.xm_objects.device_names.DeviceNameEmail,
    'FAX': xmatters.xm_objects.device_names.DeviceName,
    'GENERIC': xmatters.xm_objects.device_names.DeviceName,
    'TEXT_PAGER': xmatters.xm_objects.device_names.DeviceName,
    'TEXT_PHONE': xmatters.xm_objects.device_names.DeviceName,
    'VOICE': xmatters.xm_objects.device_names.DeviceName,
    'VOICE_IVR': xmatters.xm_objects.device_names.DeviceName}


def device_name(data):
    device_type = data.get('deviceType')
    o = device_names_o.get(device_type)
    return o(data) if o else None

import xmatters.devices
import xmatters.groups
import xmatters.people
import xmatters.dynamic_teams
import xmatters.audit

_device_objects = {'EMAIL': xmatters.devices.EmailDevice,
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
    o = _device_objects.get(device_type)
    return o(parent, data) if o else None


_recipient_object = {'GROUP': xmatters.groups.Group,
                     'PERSON': xmatters.people.Person,
                     'DEVICE': xmatters.devices.Device,
                     'DYNAMIC_TEAM': xmatters.dynamic_teams.DynamicTeam}


def recipient_factory(parent, recipient_type, data):
    o = _recipient_object.get(recipient_type)
    return o(parent, data) if o else None


_audit_objects = {'EVENT_ANNOTATED': xmatters.audit.AuditAnnotation,
                  'EVENT_CREATED': xmatters.audit.Audit,
                  'EVENT_SUSPENDED': xmatters.audit.Audit,
                  'EVENT_RESUMED': xmatters.audit.Audit,
                  'EVENT_COMPLETED': xmatters.audit.Audit,
                  'EVENT_TERMINATED': xmatters.audit.Audit,
                  'RESPONSE_RECEIVED': xmatters.audit.Response}


def audit_factory(parent, data):
    audit_type = data.get('type')
    o = _audit_objects.get(audit_type)
    return o(parent, data) if o else None

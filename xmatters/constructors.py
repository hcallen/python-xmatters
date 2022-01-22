import xmatters.devices
import xmatters.groups
import xmatters.people
import xmatters.dynamic_teams

_device_objects = {'EMAIL': xmatters.devices.EmailDevice,
                   'VOICE': xmatters.devices.VoiceDevice,
                   'TEXT_PHONE': xmatters.devices.SMSDevice,
                   'TEXT_PAGER': xmatters.devices.TextPagerDevice,
                   'APPLE_PUSH': xmatters.devices.ApplePushDevice,
                   'ANDROID_PUSH': xmatters.devices.AndroidPushDevice,
                   'FAX': xmatters.devices.FaxDevice,
                   'VOICE_IVR': xmatters.devices.PublicAddressDevice,
                   'GENERIC': xmatters.devices.GenericDevice}


def device_constructor(parent, data):
    return _device_objects[data.get('deviceType')](parent, data)


_recipient_objects = {'GROUP': xmatters.groups.Group,
                      'PERSON': xmatters.people.Person,
                      'DEVICE': device_constructor,
                      'DYNAMIC_TEAM': xmatters.dynamic_teams.DynamicTeam}
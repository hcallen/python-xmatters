from .common import PersonReference, ReferenceById, Recipient


class DeviceTimeframe(object):
    def __init__(self, data):
        self.days = data.get('days')
        self.duration_in_minutes = data.get('durationInMinutes')
        self.exclude_holidays = data.get('excludeHolidays')
        self.name = data.get('name')
        self.start_time = data.get('startTime')
        self.timezone = data.get('timezone')


class Device(Recipient):
    _endpoints = {'timeframes': '?embed=timeframes'}

    def __init__(self, parent, data):
        super(Device, self).__init__(parent, data)
        self.default_device = data.get('defaultDevice')
        self.delay = data.get('delay')
        self.description = data.get('description')
        self.device_type = data.get('deviceType')
        self.name = data.get('name')
        self.owner = PersonReference(self, data.get('owner'))
        self.priority_threshold = data.get('priorityThreshold')
        self.provider = ReferenceById(data.get('provider'))
        self.sequence = data.get('sequence')
        self.test_status = data.get('testStatus')

    @property
    def timeframes(self):
        url = self.build_url(self._endpoints.get('timeframes'))
        data = self.con.get(url).get('timeframes', {}).get('data', [])
        return [DeviceTimeframe(timeframe) for timeframe in data]


class EmailDevice(Device):
    def __init__(self, parent, data):
        super(EmailDevice, self).__init__(parent, data)
        self.email_address = data.get('emailAddress')


class VoiceDevice(Device):
    def __init__(self, parent, data):
        super(VoiceDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')


class SMSDevice(Device):
    def __init__(self, parent, data):
        super(SMSDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')


class TextPagerDevice(Device):
    def __init__(self, parent, data):
        super(TextPagerDevice, self).__init__(parent, data)
        self.pin = data.get('pin')
        self.two_way_device = data.get('twoWayDevice')


class ApplePushDevice(Device):
    def __init__(self, parent, data):
        super(ApplePushDevice, self).__init__(parent, data)
        self.account_id = data.get('accountId')
        self.apn_token = data.get('apnToken')
        self.alert_sound = data.get('alertSound')
        self.sound_status = data.get('soundStatus')
        self.sounds_threshold = data.get('soundThreshold')


class AndroidPushDevice(Device):
    def __init__(self, parent, data):
        super(AndroidPushDevice, self).__init__(parent, data)
        self.account_id = data.get('accountId')
        self.registration_id = data.get('registrationId')


class FaxDevice(Device):
    def __init__(self, parent, data):
        super(FaxDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')
        self.country = data.get('country')


class PublicAddressDevice(Device):
    def __init__(self, parent, data):
        super(PublicAddressDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')


class GenericDevice(Device):
    def __init__(self, parent, data):
        super(GenericDevice, self).__init__(parent, data)
        self.phone_number = data.get('pin')


_device_classes = {'EMAIL': EmailDevice,
                   'VOICE': VoiceDevice,
                   'TEXT_PHONE': SMSDevice,
                   'TEXT_PAGER': TextPagerDevice,
                   'APPLE_PUSH': ApplePushDevice,
                   'ANDROID_PUSH': AndroidPushDevice,
                   'FAX': FaxDevice,
                   'VOICE_IVR': PublicAddressDevice,
                   'GENERIC': GenericDevice}


def device_constructor(data):
    return _device_classes[data.get('deviceType')]

from xmatters.utils import ApiComponent


class Device(ApiComponent):
    def __init__(self, parent, data):
        super(Device, self).__init__(parent, data)
        self.object_id = data.get('id')
        self.name = data.get('name')
        self.target_name = data.get('targetName')
        self.device_type = data.get('deviceType')
        self.description = data.get('description')
        self.test_status = data.get('testStatus')
        self.externally_owned = data.get('externallyOwned')
        self.default_device = data.get('defaultDevice')
        self.priority_threshold = data.get('priorityThreshold')
        self.sequence = data.get('sequence')
        self.delay = data.get('delay')
        self.privileged = data.get('privileged')
        self.recipient_type = data.get('recipientType')
        self.status = data.get('status')
        self.provider_id = data.get('provider').get('id')

        if self.device_type == 'TEXT_PAGER':
            self.pin = data.get('pin')
            self.two_way_device = data.get('twoWayDevice')
        elif self.device_type == 'APPLE_PUSH':
            self.apn_token = data.get('apnToken')
            self.sound_status = data.get('soundStatus')
        elif self.device_type in ('TEXT_PHONE', 'VOICE'):
            self.phone_number = data.get('phoneNumber')
            self.country = data.get('country')
        elif self.device_type == 'ANDROID_PUSH':
            self.phone_number = data.get('accountId')
            self.country = data.get('registrationId')

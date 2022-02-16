
class TargetDeviceNameSelector(object):
    def __init__(self, data):
        self.name = data.get('name')    #: :vartype: str
        self.selected = data.get('selected')    #: :vartype: bool
        self.visible = data.get('visible')    #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class DeviceName(object):
    def __init__(self, data):
        self.id = data.get('id')    #: :vartype: str
        self.device_type = data.get('deviceType')    #: :vartype: str
        self.name = data.get('name')    #: :vartype: str
        self.description = data.get('description')    #: :vartype: str
        self.privileged = data.get('privileged')    #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class DeviceNameEmail(DeviceName):
    def __init__(self, data):
        super(DeviceNameEmail, self).__init__(data)
        self.domains = data.get('domains', [])    #: :vartype: list

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()

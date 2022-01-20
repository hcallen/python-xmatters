from xmatters.utils import ApiComponent
from xmatters.common import SelfLink, Recipient
from xmatters.groups import GroupReference


class ShiftOccurrenceMember(ApiComponent):
    def __init__(self, parent, data):
        super(ShiftOccurrenceMember, self).__init__(parent, data)
        self.member = Recipient(self, data.get('member'))
        self.position = data.get('position')
        self.delay = data.get('delay')
        self.escalation_type = data.get('escalationType')
        self.replacements = None


class ShiftReference(ApiComponent):
    def __init__(self, parent, data):
        super(ShiftReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.links = SelfLink(data.get('links'))
        self.name = data.get('name')


class OnCall(ApiComponent):
    def __init__(self, parent, data):
        super(OnCall, self).__init__(parent)
        self.group = GroupReference(parent, data.get('group'))
        self.shift = ShiftReference(parent, data.get('shift'))
        self.start = data.get('start')
        self.end = data.get('end')

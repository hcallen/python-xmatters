from xmatters.common import Recipient, SelfLink
from xmatters.utils import ApiComponent
from xmatters.shifts import GroupReference


class Replacer(ApiComponent):
    def __init__(self, parent, data):
        super(Replacer, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.links = SelfLink(data.get('links'))
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.status = data.get('status')


class ShiftOccurrenceMember(ApiComponent):
    def __init__(self, parent, data):
        super(ShiftOccurrenceMember, self).__init__(parent, data)
        self.member = Recipient(self, data.get('member'))
        self.position = data.get('position')
        self.delay = data.get('delay')
        self.escalation_type = data.get('escalationType')
        self.replacements = [TemporaryReplacement(self, r) for r in data.get('replacements', {}).get('data', [])]


class ShiftReference(ApiComponent):
    def __init__(self, parent, data):
        super(ShiftReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.links = SelfLink(data.get('links', {}))
        self.name = data.get('name')


class TemporaryReplacement(ApiComponent):
    def __init__(self, parent, data):
        super(TemporaryReplacement, self).__init__(parent, data)
        self.start = data.get('start')
        self.end = data.get('end')
        self.replacement = TemporaryReplacement(self, data.get('replacement'))


class OnCall(ApiComponent):
    def __init__(self, parent, data):
        super(OnCall, self).__init__(parent)
        self.group = GroupReference(parent, data.get('group'))
        self.shift = ShiftReference(parent, data.get('shift', {}))
        self.start = data.get('start')
        self.end = data.get('end')
        self.members = [ShiftOccurrenceMember(self, m) for m in data.get('members', {}).get('data', [])]

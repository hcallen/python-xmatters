import xmatters.utils.constructors
import xmatters.people
from xmatters.common import Recipient, SelfLink
from xmatters.people import PersonReference
from xmatters.utils.connection import ApiBridge
from xmatters.shifts import GroupReference


class Replacer(ApiBridge):
    def __init__(self, parent, data):
        super(Replacer, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.status = data.get('status')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftOccurrenceMember(ApiBridge):
    def __init__(self, parent, data):
        super(ShiftOccurrenceMember, self).__init__(parent, data)
        self.member = Recipient(self, data.get('member'))
        self.position = data.get('position')
        self.delay = data.get('delay')
        self.escalation_type = data.get('escalationType')
        self.replacements = [TemporaryReplacement(self, r) for r in data.get('replacements', {}).get('data', [])]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.member.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftReference(ApiBridge):
    def __init__(self, parent, data):
        super(ShiftReference, self).__init__(parent, data)
        self.id = data.get('id')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None
        self.name = data.get('name')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class TemporaryReplacement(ApiBridge):
    def __init__(self, parent, data):
        super(TemporaryReplacement, self).__init__(parent, data)
        self.start = data.get('start')
        self.end = data.get('end')
        self.replacement = TemporaryReplacement(self, data.get('replacement'))


class OnCall(ApiBridge):
    def __init__(self, parent, data):
        super(OnCall, self).__init__(parent)
        self.group = GroupReference(parent, data.get('group'))
        self.shift = ShiftReference(parent, data.get('shift', {}))
        self.start = data.get('start')
        self.end = data.get('end')
        self.members = [ShiftOccurrenceMember(self, m) for m in data.get('members', {}).get('data', [])]

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallSummary(ApiBridge):
    def __init__(self, parent, data):
        super(OnCallSummary, self).__init__(parent, data)
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None
        shift = data.get('shift')
        self.shift = ShiftReference(self, shift) if shift else None
        recipient = data.get('recipient')
        self.recipient = xmatters.utils.constructors.oncall_recipients_factory(self, recipient) if recipient else None
        absence = data.get('absence')
        self.absence = PersonReference(self, absence) if absence else None
        self.delay = data.get('delay')
        self.escalation_level = data.get('escalationLevel')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

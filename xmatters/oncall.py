import xmatters.constructors
import xmatters.people
from xmatters.common import Recipient, SelfLink, ReferenceByIdAndTargetName, ReferenceByIdAndName
from xmatters.people import PersonReference
from xmatters.utils.utils import ApiComponent
from xmatters.shifts import GroupReference, Shift


class Replacer(ApiComponent):
    def __init__(self, parent, data):
        super(Replacer, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(links) if links else None
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.status = data.get('status')

    def get_self(self):
        data = self.con.get(self.base_resource)
        return xmatters.people.Person(self, data) if data else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftOccurrenceMember(ApiComponent):
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


class ShiftReference(ApiComponent):
    def __init__(self, parent, data):
        super(ShiftReference, self).__init__(parent, data)
        self.id = data.get('id')
        links = data.get('links')
        self.links = SelfLink(links) if links else None
        self.name = data.get('name')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


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

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallSummary(ApiComponent):
    def __init__(self, parent, data):
        super(OnCallSummary, self).__init__(parent, data)
        group = data.get('group')
        self.group = ReferenceByIdAndName(self, group) if group else None
        shift = data.get('shift')
        self.shift = ReferenceByIdAndName(self, shift) if shift else None
        recipient = data.get('recipient')
        self.recipient = ReferenceByIdAndTargetName(self, recipient) if recipient else None
        absence = data.get('absence')
        self.absence = ReferenceByIdAndTargetName(self, absence) if absence else None
        self.delay = data.get('delay')
        self.escalation_level = data.get('escalationLevel')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

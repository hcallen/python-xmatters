import xmatters.utils as util
from xmatters.xm_objects.common import Recipient, SelfLink, Pagination
from xmatters.connection import ApiBridge
from xmatters.xm_objects.shifts import GroupReference


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
        # TODO: update to recipient factory
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
        group = data.get('group')
        self.group = GroupReference(parent, group) if group else None
        shift = data.get('shift')
        self.shift = ShiftReference(parent, shift) if shift else None
        start = data.get('start')
        self.start = util.TimeAttribute(start) if start else None
        end = data.get('end')
        self.end = util.TimeAttribute(end) if end else None
        members = data.get('members', {})
        self.members = list(Pagination(self, members, ShiftOccurrenceMember)) if members.get('data') else []

    # TODO: update to include full shift instead of reference
    # @property
    # def shift(self):
    #     pass

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()



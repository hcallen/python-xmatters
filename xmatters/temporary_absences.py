from xmatters.people import PersonReference
from xmatters.shifts import GroupReference
from xmatters.utils.utils import ApiBridge


class TemporaryAbsence(ApiBridge):
    def __init__(self, parent, data):
        super(TemporaryAbsence, self).__init__(parent, data)
        self.id = data.get('id')
        self.absence_type = data.get('absenceType')
        member = data.get('member')
        self.member = PersonReference(self, member) if member else None
        self.start = data.get('start')
        self.end = data.get('end')
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None
        replacement = data.get('replacement')
        self.replacement = PersonReference(self, replacement) if replacement else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.member.target_name)

    def __str__(self):
        return self.__repr__()

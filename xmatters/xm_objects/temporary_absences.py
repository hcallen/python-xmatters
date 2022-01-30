import xmatters.utils as util
from xmatters.xm_objects.people import PersonReference
from xmatters.xm_objects.shifts import GroupReference
from xmatters.connection import ApiBridge


class TemporaryAbsence(ApiBridge):
    def __init__(self, parent, data):
        super(TemporaryAbsence, self).__init__(parent, data)
        self.id = data.get('id')
        self.absence_type = data.get('absenceType')
        member = data.get('member')
        self.member = PersonReference(self, member) if member else None
        start = data.get('start')
        self.start = util.TimeAttribute(start) if start else None
        end = data.get('end')
        self.end = util.TimeAttribute(end) if end else None
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None
        replacement = data.get('replacement')
        self.replacement = PersonReference(self, replacement) if replacement else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.member.target_name)

    def __str__(self):
        return self.__repr__()


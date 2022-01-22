import xmatters.groups
from xmatters.common import ReferenceByIdAndSelfLink, SelfLink, Recipient

from xmatters.utils import ApiComponent


class GroupReference(ApiComponent):
    def __init__(self, parent, data):
        super(GroupReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.links = SelfLink(data.get('links'))

    def get_self(self):
        data = self.con.get(self.base_resource)
        return xmatters.groups.Group(self, data)

    def __repr__(self):
        return '<GroupReference {}>'.format(self.target_name)

    def __str__(self):
        return self.__repr__()


class End(object):
    def __init__(self, data):
        self.end_by = data.get('endBy')
        self.date = data.get('date')
        self.repetitions = data.get('repetitions')


class Rotation(object):
    def __init__(self, data):
        self.type = data.get('type')
        self.direction = data.get('direction')
        self.interval = data.get('interval')
        self.interval_unit = data.get('intervalUnit')
        self.next_rotation_time = data.get('nextRotationTime')


class ShiftRecurrence(object):
    def __init__(self, data):
        self.frequency = data.get('frequency')
        self.repeat_every = data.get('repeatEvery')
        self.on_days = data.get('onDays')
        self.on = data.get('on')
        self.months = data.get('months')
        self.data_on_month = data.get('dateOfMonth')
        self.day_of_week_classifier = data.get('dayOfWeekClassifier')
        self.day_of_week = data.get('dayOfWeek')
        self.end = End(data.get('end'))


class ShiftMember(ApiComponent):
    def __init__(self, parent, data):
        super(ShiftMember, self).__init__(parent, data)
        self.position = data.get('position')
        self.delay = data.get('delay')
        self.escalation_type = data.get('escalationType')
        self.in_rotation = data.get('inRotation')
        self.recipient = Recipient(self, data.get('recipient'))
        self.shift = ReferenceByIdAndSelfLink(self, data.get('shift'))

    def __repr__(self):
        return '<ShiftMember {}>'.format(self.recipient.target_name)

    def __str__(self):
        return self.__repr__()


class Shift(ApiComponent):
    _endpoints = {'get_members': '/members'}

    def __init__(self, parent, data):
        super(Shift, self).__init__(parent, data)
        self.id = data.get('id')
        self.group = GroupReference(self, data.get('group'))
        self.links = SelfLink(data.get('links'))
        self.name = data.get('name')
        self.start = data.get('start')
        self.end = data.get('end')
        self.timezone = data.get('timezone')
        self.recurrence = ShiftRecurrence(data.get('recurrence'))

    @property
    def members(self):
        return self.get_members()

    def get_members(self):
        url = self.build_url(self._endpoints.get('get_members'))
        data = self.con.get(url).get('data')
        return [ShiftMember(self, m) for m in data]

    def __repr__(self):
        return '<Shift {}>'.format(self.name)

    def __str__(self):
        return self.__repr__()

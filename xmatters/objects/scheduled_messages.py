import xmatters.utils
import xmatters.objects.common
import xmatters.objects.events
import xmatters.objects.utils


class ScheduledMessage(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(ScheduledMessage, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str
        owner = data.get('owner')
        self.owner = xmatters.objects.common.PersonReference(self,
                                                             owner) if owner else None  #: :vartype: :class:`~xmatters.objects.common.PersonReference`
        event = data.get('event')
        self.event = xmatters.objects.events.Event(self, event) if event else None  #: :vartype: :class:`~xmatters.objects.events.Event`
        recurrence = data.get('recurrance')
        self.recurrence = MessageRecurrence(self,
                                            recurrence) if recurrence else None  #: :vartype: :class:`~xmatters.objects.scheduled_messages.MessageRecurrence`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class MessageRecurrence(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(MessageRecurrence, self).__init__(parent, data)
        self.frequency = data.get('frequency')  #: :vartype: str
        self.repeat_every = data.get('repeatEvery')  #: :vartype: str
        self.on_days = data.get('onDays')  #: :vartype: list[str]
        self.on = data.get('on')  #: :vartype: str
        self.months = data.get('months')  #: :vartype: list[str]
        self.date_of_month = data.get('dateOfMonth')  #: :vartype: str
        self.day_of_week_classifier = data.get('dayOfWeekClassifier')  #: :vartype: str
        self.day_of_week = data.get('dayOfWeek')  #: :vartype: str
        end = data.get('end')
        self.end = MessageEnd(self, data) if end else None  #: :vartype: :class:`~xmatters.objects.scheduled_messages.MessageEnd`
        start_time = data.get('startTime')
        self.start_time = xmatters.objects.utils.TimeAttribute(
            start_time) if start_time else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class MessageEnd(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(MessageEnd, self).__init__(parent, data)
        self.end_by = data.get('endBy')  #: :vartype: str
        date = data.get('date')
        self.date = xmatters.objects.utils.TimeAttribute(date) if date else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        self.repetitions = data.get('repetitions')  #: :vartype: int

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

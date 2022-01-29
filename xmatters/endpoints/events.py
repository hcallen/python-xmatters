import xmatters.factories as factory
import xmatters.utils as util
from xmatters.endpoints.common import Recipient, Pagination, SelfLink
from xmatters.endpoints.event_supressions import EventSuppression
from xmatters.endpoints.forms import FormReference
from xmatters.endpoints.people import PersonReference
from xmatters.endpoints.plans import PlanReference
from xmatters.connection import ApiBridge


class Message(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.message_type = data.get('messageType')
        self.subject = data.get('subject')
        self.body = data.get('body')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.subject)

    def __str__(self):
        return self.__repr__()


class UserDeliveryResponse(object):
    def __init__(self, data):
        self.text = data.get('text')
        self.notification = data.get('notification')
        received = data.get('received')
        self.received = util.TimeAttribute(received) if received else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Conference(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.bridge_id = data.get('bridgeId')
        self.bridge_number = data.get('bridgeNumber')
        self.type = data.get('type')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class VoicemailOptions(object):
    def __init__(self, data):
        self.retry = data.get('retry')
        self.every = data.get('every')
        self.leave = data.get('leave')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Translation(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.language = data.get('language')
        self.text = data.get('text')
        self.prompt = data.get('prompt')
        self.description = data.get('description')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ResponseOption(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.number = data.get('number')
        self.text = data.get('text')
        self.description = data.get('description')
        self.prompt = data.get('prompt')
        self.action = data.get('action')
        self.contribution = data.get('contribution')
        self.join_conference = data.get('joinConference')
        self.allow_comments = data.get('allowComments')
        self.redirect_rul = data.get('redirectUrl')
        translations = data.get('translations', {}).get('data', [])
        self.translations = [Translation(t) for t in translations]

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferencePointer(object):
    def __init__(self, data):
        self.bridge_id = data.get('bridgeId')
        self.type = data.get('type')
        self.bridge_number = data.get('bridgeNumber')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventReference(ApiBridge):
    def __init__(self, parent, data):
        super(EventReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.event_id = data.get('eventId')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Notification(ApiBridge):
    def __init__(self, parent, data):
        super(Notification, self).__init__(parent, data)
        self.id = data.get('id')
        self.recipient = Recipient(self, data.get('recipient'))
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None
        delivered = data.get('delivered')
        self.delivered = util.TimeAttribute(delivered) if delivered else None
        responded = data.get('responded')
        self.responded = util.TimeAttribute(responded) if responded else None
        self.delivery_status = data.get('deliveryStatus')
        self.responses = data.get('responses', [])

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.recipient.target_name)

    def __str__(self):
        return self.__repr__()


class UserDeliveryData(ApiBridge):
    def __init__(self, parent, data):
        super(UserDeliveryData, self).__init__(parent, data)
        event = data.get('event')
        self.event = EventReference(self, event) if event else None
        person = data.get('person')
        self.person = PersonReference(self, person) if person else None
        self.delivery_status = data.get('deliveryStatus')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.person.target_name)

    def __str__(self):
        return self.__repr__()


class Annotation(ApiBridge):
    def __init__(self, parent, data):
        super(Annotation, self).__init__(parent, data)
        self.id = data.get('id')
        event = data.get('event')
        self.event = EventReference(self, event)
        author = data.get('author')
        self.author = PersonReference(self, author)
        self.comment = data.get('comment')
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Event(ApiBridge):
    _endpoints = {'messages': '?embed=messages',
                  'annotations': '?embed=annotations',
                  'properties': '?embed=properties',
                  'recipients': '?embed=recipients',
                  'response_options': '?embed=responseOptions',
                  'get_user_deliveries': '/events/{event_id}/user-deliveries',
                  'get_audit': '{base_url}/audits'}

    def __init__(self, parent, data):
        super(Event, self).__init__(parent, data)
        self.bypass_phone_intro = data.get('bypassPhoneIntro')
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None
        self.conference = Conference(data.get('conference')) if data.get('conference') else None
        self.escalation_override = data.get('escalationOverride')
        self.event_id = data.get('eventId')
        self.event_type = data.get('eventType')
        self.expiration_in_minutes = data.get('expirationInMinutes')
        self.flood_control = data.get('floodControl')
        self.plan = PlanReference(data.get('plan')) if data.get('plan') else None
        self.form = FormReference(data.get('form')) if data.get('form') else None
        self.id = data.get('id')
        self.incident = data.get('incident')
        self.override_device_restrictions = data.get('overrideDeviceRestrictions')
        self.other_response_count = data.get('otherResponseCount')
        self.other_response_count_threshold = data.get('otherResponseCountThreshold')
        self.priority = data.get('priority')
        self.require_phone_password = data.get('requirePhonePassword')
        self.response_count_enabled = data.get('responseCountsEnabled')
        submitter = data.get('submitter')
        self.submitter = PersonReference(self, submitter) if submitter else None
        self.status = data.get('status')
        suppressions = data.get('suppressions', {}).get('data', [])
        self.suppressions = [EventSuppression(self, s) for s in suppressions]
        terminated = data.get('terminated')
        self.terminated = util.TimeAttribute(terminated) if terminated else None
        voicemail_options = data.get('voicemailOptions')
        self.voicemail_options = VoicemailOptions(voicemail_options) if voicemail_options else None

    def get_audit(self, audit_types=util.AUDIT_TYPES, params=None):
        params = params if params else {}
        params['eventId'] = self.event_id
        if audit_types and 'auditType' not in params.keys():
            if isinstance(audit_types, str):
                params['auditType'] = audit_types.upper()
            elif isinstance(audit_types, list):
                params['auditType'] = ','.join(audit_types).upper()
        url = self._endpoints.get('get_audit').format(base_url=self.con.base_url)
        data = self.con.get(url, params)
        return Pagination(self, data, factory.audit) if data.get('data') else []

    @property
    def annotations(self):
        url = self.build_url(self._endpoints.get('annotations'))
        data = self.con.get(url)
        annotations = data.get('annotations')
        return Pagination(self, annotations, Annotation) if annotations.get('data') else []

    @property
    def messages(self):
        url = self.build_url(self._endpoints.get('messages'))
        data = self.con.get(url)
        messages = data.get('messages')
        return Pagination(self, messages, Message) if messages.get('data') else []

    @property
    def properties(self):
        url = self.build_url(self._endpoints.get('properties'))
        data = self.con.get(url)
        return data.get('properties', {})

    @property
    def recipients(self):
        url = self.build_url(self._endpoints.get('recipients'))
        data = self.con.get(url)
        recipients = data.get('recipients')
        return Pagination(self, recipients, Message) if recipients.get('data') else []

    @property
    def response_options(self):
        url = self.build_url(self._endpoints.get('response_options'))
        data = self.con.get(url)
        response_options = data.get('responseOptions', {}).get('data')
        return [ResponseOption(r) for r in response_options] if response_options else []

    def __repr__(self):
        return '<{} Created: {} Type: {}>'.format(self.__class__.__name__, self.created, self.event_type)

    def __str__(self):
        return self.__repr__()

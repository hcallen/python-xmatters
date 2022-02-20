import xmatters.objects.utils
from xmatters.objects.common import SelfLink, ReferenceById, PersonReference
from xmatters.utils import ApiBase
from xmatters.objects.services import Service


class IncidentProperty(ApiBase):

    def __init__(self, parent, data):
        super(IncidentProperty, self).__init__(parent, data)
        self.name = data.get('name')  #: :vartype: str
        self.level = data.get('level')  #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class Incident(ApiBase):
    _endpoints = {'add_timeline_note': '/timeline-entries'}

    def __init__(self, parent, data):
        super(Incident, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.incident_identifier = data.get('incidentIdentifier')  #: :vartype: str
        self.summary = data.get('summary')  #: :vartype: str
        self.description = data.get('description')  #: :vartype: str
        severity = data.get('severity')
        self.severity = IncidentProperty(self, severity) if severity else None  #: :vartype: :class:`~xmatters.objects.incidents.IncidentProperty`
        status = data.get('status')
        self.status = IncidentProperty(self, status) if status else None  #: :vartype: :class:`~xmatters.objects.incidents.IncidentProperty`
        initiated_by = data.get('initiatedBy')
        self.initiated_by = PersonReference(self, initiated_by) if initiated_by else None  #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        commander = data.get('commander')
        self.commander = PersonReference(self, commander) if commander else None  #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.request_id = data.get('requestId')  #: :vartype: str
        impacted_services = data.get('impactedServices', [])
        self.impacted_services = [Service(self, s) for s in impacted_services]  #: :vartype: list of :class:`~xmatters.objects.services.Service`
        reporter = data.get('reporter')
        self.reporter = PersonReference(self, reporter) if reporter else None  #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        created_at = data.get('createdAt')
        self.created_at = xmatters.objects.utils.TimeAttribute(created_at) if created_at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        updated_at = data.get('updated_at')
        self.updated_at = xmatters.objects.utils.TimeAttribute(updated_at) if updated_at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        acknowledged_at = data.get('acknowledgeAt')
        self.acknowledged_at = xmatters.objects.utils.TimeAttribute(acknowledged_at) if acknowledged_at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        owner = data.get('owner')
        self.owner = PersonReference(self, owner) if owner else None  #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        owner_resolver = data.get('ownerResolver')
        self.owner_resolver = ReferenceById(self, owner_resolver) if owner_resolver else None  #: :vartype: :class:`~xmatters.objects.common.ReferenceById`
        resolved_at = data.get('resolvedAt')
        self.resolved_at = xmatters.objects.utils.TimeAttribute(resolved_at) if resolved_at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        impact_start_at = data.get('impactStartAt')
        self.impact_start_at = xmatters.objects.utils.TimeAttribute(impact_start_at) if impact_start_at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        mitigated_at = data.get('mitigatedAt')
        self.mitigated_at = xmatters.objects.utils.TimeAttribute(mitigated_at) if mitigated_at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`

    def add_timeline_note(self, data):
        url = self._get_url(self._endpoints.get('add_timeline_note'))
        data = self._con.post(url, data=data)
        return IncidentNote(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentNote(ApiBase):
    def __init__(self, parent, data):
        super(IncidentNote, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        at = data.get('at')
        self.at = xmatters.objects.utils.TimeAttribute(at) if at else None  #: :vartype: :class:`~xmatters.objects.utils.TimeAttribute`
        self.entry_type = data.get('entryType')  #: :vartype: str
        self.text = data.get('text')  #: :vartype: str
        added_by = data.get('addedBy')
        self.added_dy = PersonReference(self, added_by) if added_by else None  #: :vartype: :class:`~xmatters.objects.people.PersonReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentDetails(ApiBase):
    def __init__(self, parent, data):
        super(IncidentDetails, self).__init__(parent, data)
        self.summary = data.get('summary')  #: :vartype: str
        self.description = data.get('description')  #: :vartype: str
        self.severity = data.get('severity')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

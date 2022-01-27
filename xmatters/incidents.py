from xmatters.people import PersonReference
from xmatters.utils.connection import ApiBridge


class Incident(ApiBridge):
    def __init__(self, parent, data):
        super(Incident, self).__init__(parent, data)
        self.id = data.get('id')
        self.incident_identifier = data.get('incidentIdentifier')
        self.summary = data.get('summary')
        self.description = data.get('description')
        self.severity = data.get('severity')
        self.status = data.get('status')
        initiated_by = data.get('initiatedBy')
        self.initiated_by = PersonReference(self, initiated_by) if initiated_by else None
        commander = data.get('commander')
        self.commander = PersonReference(self, commander) if commander else None
        self.request_id = data.get('requestId')
        self.impacted_services = data.get('impactedServices')

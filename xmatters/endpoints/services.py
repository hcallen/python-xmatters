from xmatters.connection import ApiBridge
from xmatters.endpoints.shifts import GroupReference


class Service(ApiBridge):
    def __init__(self, parent, data):
        super(Service, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipients_type = data.get('recipientType')
        self.description = data.get('description')
        owned_by = data.get('ownedBy')
        self.owned_by = GroupReference(self, owned_by) if owned_by else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
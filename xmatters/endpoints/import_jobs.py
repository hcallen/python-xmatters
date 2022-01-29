import xmatters.utils as util
from xmatters.connection import ApiBridge
from xmatters.endpoints.people import PersonReference
from xmatters.endpoints.common import SelfLink


class ImportMessage(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.message_level = data.get('messageLevel')
        self.message_type = data.get('messageType')
        self.description = data.get('description')
        self.line = data.get('line')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.message_type)

    def __str__(self):
        return self.__repr__()


class Import(ApiBridge):
    _endpoints = {'get_messages': '/import-messages'}

    def __init__(self, parent, data):
        super(Import, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.transform = data.get('transform')
        self.status = data.get('status')
        started = data.get('started')
        self.started = util.TimeAttribute(started) if started else None
        self.last_updated_at = data.get('lastUpdatedAt')
        by = data.get('by')
        self.by = PersonReference(parent, by) if by else None
        self.total_count = data.get('totalCount')
        self.processed_count = data.get('processedCount')
        finished_at = data.get('finishedAt')
        self.finished_at = util.TimeAttribute(finished_at) if finished_at else None
        links = data.get('links')
        self.links = SelfLink(parent, links)

    def get_messages(self, params=None):
        url = self.build_url(self._endpoints.get('get_messages'))
        messages = self.con.get(url, params).get('data', None)
        return [ImportMessage(m) for m in messages] if messages else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()

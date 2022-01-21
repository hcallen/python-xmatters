from .utils import ApiComponent



class GroupReference(ApiComponent):
    def __init__(self, parent, data):
        super(GroupReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.links = SelfLink(data.get('links'))


class PersonReference(ApiComponent):
    def __init__(self, parent, data):
        super(PersonReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.recipient_type = data.get('recipientType')
        self.links = SelfLink(data.get('links'))


class Recipient(ApiComponent):
    def __init__(self, parent, data):
        super(Recipient, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        self.external_key = data.get('externalKey')
        self.externally_owned = data.get('externallyOwned')
        self.locked = data.get('locked')
        self.status = data.get('status')
        self.links = SelfLink(data.get('links'))


class ReferenceById(object):
    def __init__(self, data):
        self.id = data.get('id')


class ReferenceByIdAndSelfLink(ApiComponent):
    def __init__(self, parent, data):
        super(ReferenceByIdAndSelfLink, self).__init__(parent, data)
        self.id = data.get('id')
        self.links = SelfLink(data.get('links', {}))


class SelfLink(object):
    def __init__(self, data):
        self.self = data.get('self')


class Role(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')

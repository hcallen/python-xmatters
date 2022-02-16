class Attachments(object):
    def __init__(self, data):
        self.name = data.get('name')  #: :vartype: str
        self.path = data.get('path')  #: :vartype: str
        self.size = data.get('size')  #: :vartype: str


class AttachmentsReference(object):
    def __init__(self, data):
        self.path = data.get('path')  #: :vartype: str

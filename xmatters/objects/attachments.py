import xmatters.utils


class Attachments(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(Attachments, self).__init__(parent, data)
        self.name = data.get('name')  #: :vartype: str
        self.path = data.get('path')  #: :vartype: str
        self.size = data.get('size')  #: :vartype: str


class AttachmentsReference(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(AttachmentsReference, self).__init__(parent, data)
        self.path = data.get('path')  #: :vartype: str

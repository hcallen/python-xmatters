import xmatters.connection
import xmatters.objects.common
import xmatters.utils


class DeviceTypes(xmatters.utils.ApiBase):
    def __init__(self, parent, data):
        super(DeviceTypes, self).__init__(parent, data)
        self.count = data.get('count')  #: :vartype: int
        self.total = data.get('total')  #: :vartype: int
        self.data = data.get('data', [])  #: :vartype: list
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None #: :vartype: `~xmatters.objects.common.SelfLinks`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

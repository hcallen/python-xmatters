from xmatters.connection import ApiBridge
from xmatters.endpoints.common import SelfLink


class Site(ApiBridge):
    def __init__(self, parent, data):
        super(Site, self).__init__(parent, data)
        self.id = data.get('id')
        self.address1 = data.get('address1')
        self.address2 = data.get('address2')
        self.city = data.get('city')
        self.country = data.get('country')
        self.external_key = data.get('externalKey')
        self.externally_owned = data.get('externallyOwned')
        self.language = data.get('language')
        self.latitude = data.get('latitude')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None
        self.longitude = data.get('longitude')
        self.name = data.get('name')
        self.postal_code = data.get('postalCode')
        self.state = data.get('state')
        self.status = data.get('status')
        self.timezone = data.get('timezone')
